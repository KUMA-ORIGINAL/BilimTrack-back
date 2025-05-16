import random
import logging
from unidecode import unidecode

from django.utils.text import slugify
from import_export import resources, fields
from .models import User

logger = logging.getLogger(__name__)


class UserResource(resources.ModelResource):

    class Meta:
        model = User
        exclude = ('id',)
        import_id_fields = ()
        fields = ('first_name', 'last_name', 'role', 'group', 'username', 'plain_password')

    def before_import_row(self, row, **kwargs):
        first_name = row.get('first_name', '').strip()
        last_name = row.get('last_name', '').strip()
        group_id = row.get('group')

        logger.info(f"📥 Импортируем: {first_name} {last_name}, группа: {group_id}")

        if User.objects.filter(first_name=first_name, last_name=last_name, group_id=group_id).exists():
            logger.warning(f"⚠️ Пропущен: {first_name} {last_name} уже существует в группе {group_id}")
            raise Exception(f"Пользователь {first_name} {last_name} уже существует в группе {group_id}")

        try:
            transliterated = unidecode(f"{last_name}{first_name[0]}")  # ИвановИ → IvanovI
            base_username = slugify(transliterated).lower()
        except Exception as e:
            logger.error(f"❌ Ошибка при генерации username: {e}")
            raise

        if not base_username:
            logger.error("❌ slugify вернул пустую строку — проверь имя/фамилию")
            raise Exception(f"Невозможно сгенерировать username из: {last_name} {first_name}")

        username = base_username

        pin = str(random.randint(0, 9999)).zfill(4)

        logger.info(f"✅ Сгенерирован логин: {username}, PIN: {pin}")

        row['username'] = username
        row['plain_password'] = pin
        row['_raw_password'] = pin  # временно для set_password

    def before_save_instance(self, instance, row, **kwargs):
        raw_password = row.get('_raw_password')
        if raw_password:
            instance.set_password(raw_password)
            instance.plain_password = raw_password

    def dehydrate_group(self, instance):
        return instance.group.name if instance.group else ''