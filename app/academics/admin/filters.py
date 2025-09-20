from django.contrib.admin import SimpleListFilter
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from unfold.contrib.filters.admin import RelatedDropdownFilter

from account.models import ROLE_ADMIN
from schedule.models import LessonTime
from ..models import EducationLevel, Course, Group, Subject, Session

User = get_user_model()


class EducationLevelFilter(SimpleListFilter):
    title = _('Уровень образования')
    parameter_name = 'education_level'

    def lookups(self, request, model_admin):
        """
        Какие варианты уровней показываем в админке.
        """
        qs = EducationLevel.objects.all()

        if request.user.is_superuser:
            levels = qs
        elif request.user.role == ROLE_ADMIN:
            # админ видит только уровни для своей организации
            levels = qs.filter(organization_id=request.user.organization_id)
        else:
            levels = qs.none()

        return [(level.id, level.name) for level in levels]

    def queryset(self, request, queryset):
        """
        Фактическая фильтрация запроса по выбранному уровню образования.
        """
        if self.value():
            return queryset.filter(education_level_id=self.value())
        return queryset


class CourseFilter(SimpleListFilter):
    title = _('Курс')
    parameter_name = 'course'

    def lookups(self, request, model_admin):
        """
        Список доступных курсов, которые видит пользователь.
        """
        qs = Course.objects.all()

        if request.user.is_superuser:
            courses = qs
        elif request.user.role == ROLE_ADMIN:
            courses = qs.filter(organization_id=request.user.organization_id)
        else:
            courses = qs.none()

        return [(course.id, str(course)) for course in courses]

    def queryset(self, request, queryset):
        """
        Фильтрация queryset'а модели по выбранному курсу.
        """
        if self.value():
            return queryset.filter(course_id=self.value())
        return queryset



class GroupDropdownFilter(RelatedDropdownFilter):
    title = _('Группа')
    parameter_name = 'group'

    def field_choices(self, field, request, model_admin):
        """
        Здесь ограничиваем список групп в зависимости от роли пользователя.
        """

        qs = Group.objects.all()

        if request.user.is_superuser:
            groups = qs
        elif request.user.role == ROLE_ADMIN:
            groups = qs.filter(course__organization_id=request.user.organization_id)
        else:
            groups = qs.none()

        return [(g.pk, str(g)) for g in groups]


class SubjectDropdownFilter(RelatedDropdownFilter):
    title = _('Предмет')
    parameter_name = 'subject'

    def field_choices(self, field, request, model_admin):
        """
        Список предметов в зависимости от роли пользователя.
        """
        qs = Subject.objects.all()

        if request.user.is_superuser:
            subjects = qs
        elif request.user.role == ROLE_ADMIN:
            # только предметы своей организации
            subjects = qs.filter(organization_id=request.user.organization_id)
        else:
            subjects = qs.none()

        return [(s.pk, str(s)) for s in subjects]


class MentorDropdownFilter(RelatedDropdownFilter):
    title = _('Преподаватель')
    parameter_name = 'mentor'

    def field_choices(self, field, request, model_admin):
        """
        Список менторов (пользователей с ролью mentor),
        отфильтрованный по роли администратора.
        """
        qs = User.objects.filter(role='mentor')  # если у тебя именно так хранится

        if request.user.is_superuser:
            mentors = qs
        elif request.user.role == ROLE_ADMIN:
            mentors = qs.filter(organization_id=request.user.organization_id)
        else:
            mentors = qs.none()

        return [(m.pk, str(m)) for m in mentors]


class StudentDropdownFilter(RelatedDropdownFilter):
    title = _('Студент')
    parameter_name = 'student'

    def field_choices(self, field, request, model_admin):
        """
        Список менторов (пользователей с ролью mentor),
        отфильтрованный по роли администратора.
        """
        qs = User.objects.filter(role='student')  # если у тебя именно так хранится

        if request.user.is_superuser:
            mentors = qs
        elif request.user.role == ROLE_ADMIN:
            mentors = qs.filter(organization_id=request.user.organization_id)
        else:
            mentors = qs.none()

        return [(m.pk, str(m)) for m in mentors]


class SessionDropdownFilter(RelatedDropdownFilter):
    title = _('Сессия')
    parameter_name = 'session'

    def field_choices(self, field, request, model_admin):
        """
        Список сессий в зависимости от роли пользователя
        """
        qs = Session.objects.all()

        if request.user.is_superuser:
            sessions = qs
        elif request.user.role == ROLE_ADMIN:
            sessions = qs.filter(subject__organization_id=request.user.organization_id)
        else:
            sessions = qs.none()

        return [(s.pk, str(s)) for s in sessions]


class LessonTimeDropdownFilter(RelatedDropdownFilter):
    title = _('Время занятия')
    parameter_name = 'lesson_time'

    def field_choices(self, field, request, model_admin):
        """
        Список LessonTime в зависимости от роли пользователя
        """
        qs = LessonTime.objects.all()

        if request.user.is_superuser:
            lesson_times = qs
        elif request.user.role == ROLE_ADMIN:
            lesson_times = qs.filter(organization_id=request.user.organization_id)
        else:
            lesson_times = qs.none()

        return [(lt.pk, str(lt)) for lt in lesson_times]


class CourseDropdownFilter(RelatedDropdownFilter):
    title = _('Курс')
    parameter_name = 'course'

    def field_choices(self, field, request, model_admin):
        qs = Course.objects.all()

        if request.user.is_superuser:
            courses = qs
        elif request.user.role == ROLE_ADMIN:
            courses = qs.filter(organization_id=request.user.organization_id)
        else:
            courses = qs.none()

        return [(course.id, str(course)) for course in courses]
