import random
import logging
from unidecode import unidecode

from django.utils.text import slugify
from import_export import resources

from .models import User

logger = logging.getLogger(__name__)


class StudentResource(resources.ModelResource):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Загружаем все данные студентов с отчеством и организацией
        users = User.objects.values_list(
            "first_name", "last_name", "patronymic", "group_id", "username", "organization_id"
        )

        # Ключ учитывает ФИО + group_id + org_id
        self.existing_students = {
            (fn.strip().lower(), ln.strip().lower(), (pn or "").strip().lower(), gid, org)
            for fn, ln, pn, gid, u, org in users
        }

        self.existing_usernames = {u for _, _, _, _, u, _ in users}

    class Meta:
        model = User
        exclude = ("id",)
        import_id_fields = ()
        use_bulk = True
        fields = (
            "first_name",
            "last_name",
            "patronymic",   # 🔑 добавлено
            "group",
            "username",
            "plain_password",
        )

    def before_import_row(self, row, **kwargs):
        first_name = row.get("first_name", "").strip()
        last_name = row.get("last_name", "").strip()
        patronymic = (row.get("patronymic") or "").strip()
        group_id = row.get("group")

        # Берем organization из request
        request = kwargs.get("request")
        organization_id = None
        if request and hasattr(request, "user") and request.user.is_authenticated:
            if hasattr(request.user, "organization_id"):
                organization_id = request.user.organization_id

        logger.info(
            f"📥 Импортируем студента: {last_name} {first_name} {patronymic}, "
            f"group={group_id}, org={organization_id}"
        )

        # --- Проверка дублей с учетом отчества и organization
        key = (
            first_name.lower(),
            last_name.lower(),
            patronymic.lower(),
            int(group_id) if group_id else None,
            int(organization_id) if organization_id else None,
        )
        if key in self.existing_students:
            logger.warning(
                f"⚠️ Пропущен: {first_name} {patronymic} {last_name} уже существует "
                f"в группе {group_id}, org={organization_id}"
            )
            raise Exception(
                f"Студент {first_name} {patronymic} {last_name} уже существует "
                f"в группе {group_id}, org={organization_id}"
            )

        # --- Генерация username (только Фамилия + первая буква Имени, отчество можно не брать)
        try:
            transliterated = unidecode(f"{last_name}{first_name[0]}")  # ИвановИ → ivanovi
            base_username = slugify(transliterated).lower()
        except Exception as e:
            logger.error(f"❌ Ошибка при генерации username: {e}")
            raise

        if not base_username:
            raise Exception(
                f"Невозможно сгенерировать username из: {last_name} {first_name}"
            )

        username = base_username
        counter = 1
        while username in self.existing_usernames:
            username = f"{base_username}{counter}"
            counter += 1

        # --- Генерация PIN
        pin = str(random.randint(0, 9999)).zfill(4)
        logger.info(f"✅ Сгенерирован логин={username}, PIN={pin}")

        # Записываем данные в row
        row["username"] = username
        row["plain_password"] = pin
        row["_raw_password"] = pin
        row["role"] = "student"
        row["organization"] = organization_id

        # Пополняем кэши
        self.existing_students.add(key)
        self.existing_usernames.add(username)

    def before_save_instance(self, instance, row, **kwargs):
        raw_password = row.get("_raw_password")
        if raw_password:
            instance.set_password(raw_password)
            instance.plain_password = raw_password

        # Присваиваем организацию из request
        request = kwargs.get("request")
        if request and hasattr(request, "user") and request.user.is_authenticated:
            if hasattr(request.user, "organization"):
                instance.organization = request.user.organization

    def dehydrate_group(self, instance):
        return instance.group.name if instance.group else ""


class MentorResource(resources.ModelResource):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Загружаем все данные один раз, чтобы избежать N+1 запросов
        users = User.objects.values_list(
            "first_name", "last_name", "patronymic", "organization_id", "username"
        )

        self.existing_users = {
            (fn.strip().lower(), ln.strip().lower(), (pn or "").strip().lower(), org)
            for fn, ln, pn, org, _ in users
        }
        self.existing_usernames = {u for _, _, _, _, u in users}

    class Meta:
        model = User
        verbose_name = 'Преподаватели'
        exclude = ('id',)
        import_id_fields = ()
        fields = (
            'first_name',
            'last_name',
            'patronymic',
            'email',
            'google_meet_link',
            'organization',
            'role',
            'username',
            'plain_password',   # ⚠️ опасно, но оставляю под твой кейс
        )

    def before_import_row(self, row, **kwargs):
        first_name = row.get('first_name', '').strip()
        last_name = row.get('last_name', '').strip()
        patronymic = (row.get("patronymic") or "").strip()
        organization_id = row.get('organization')

        logger.info(
            f"📥 Импортируем МЕНТОРА: {last_name} {first_name} {patronymic}, org={organization_id},"
        )

        # --- Защита от дубликатов
        key = (first_name.lower(), last_name.lower(), patronymic.lower(), int(organization_id) if organization_id else None)
        if key in self.existing_users:
            logger.warning(f"⚠️ Пропущен: {last_name} {first_name} {patronymic} уже есть в org={organization_id}")
            raise Exception(f"Ментор {first_name} {last_name} уже существует в организации {organization_id}")

        # --- Генерация username
        try:
            transliterated = unidecode(f"{last_name}{first_name[0]}")  # ИвановИ → IvanovI
            base_username = slugify(transliterated).lower()
        except Exception as e:
            logger.error(f"❌ Ошибка при генерации username: {e}")
            raise

        if not base_username:
            raise Exception(f"Невозможно сгенерировать username из: {last_name} {first_name}")

        username = base_username
        counter = 1
        while username in self.existing_usernames:
            username = f"{base_username}{counter}"
            counter += 1

        # --- Генерация PIN
        pin = str(random.randint(0, 9999)).zfill(4)

        logger.info(f"✅ Сгенерирован логин={username}, PIN={pin}")

        row['username'] = username
        row['plain_password'] = pin  # ⚠️ можно убрать, но оставляю совместимость
        row['_raw_password'] = pin
        row['role'] = 'mentor'

        # Добавляем в кеш "существующих"
        self.existing_users.add(key)
        self.existing_usernames.add(username)

    def before_save_instance(self, instance, row, **kwargs):
        raw_password = row.get('_raw_password')
        if raw_password:
            instance.set_password(raw_password)
            # Опционально, если прям нужно хранить:
            instance.plain_password = raw_password

    def dehydrate_organization(self, instance):
        return instance.organization.name if instance.organization else ''
