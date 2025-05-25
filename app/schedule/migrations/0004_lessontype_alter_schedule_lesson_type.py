# schedule/migrations/0004_lesson_type_foreignkey.py

from django.db import migrations, models
import django.db.models.deletion


def create_lesson_types_and_migrate_data(apps, schema_editor):
    LessonType = apps.get_model('schedule', 'LessonType')
    Schedule = apps.get_model('schedule', 'Schedule')

    # 1. Создаём типы занятий
    lesson_type_map = {
        'lecture': 'Лекция',
        'practice': 'Практика',
        'lab': 'Лабораторная',
        'seminar': 'Семинар',
    }

    type_objs = {}
    for code, name in lesson_type_map.items():
        obj = LessonType.objects.create(name=name)
        type_objs[code] = obj

    # 2. Обновляем расписание
    for schedule in Schedule.objects.all():
        # если старое значение — это строка, например 'lecture'
        lesson_code = schedule.lesson_type  # строка: 'lecture', 'practice', и т.д.
        lesson_obj = type_objs.get(lesson_code)
        if lesson_obj:
            schedule.lesson_type = lesson_obj
            schedule.save()


class Migration(migrations.Migration):

    dependencies = [
        ('schedule', '0003_alter_schedule_teacher_delete_teacher'),
    ]

    operations = [
        # 1. Создаём модель LessonType
        migrations.CreateModel(
            name='LessonType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='Название типа')),
            ],
            options={
                'verbose_name': 'Тип занятия',
                'verbose_name_plural': 'Типы занятий',
            },
        ),

        # 2. Временно переименовываем старое поле, чтобы сохранить данные
        migrations.RenameField(
            model_name='schedule',
            old_name='lesson_type',
            new_name='lesson_type_old',
        ),

        # 3. Добавляем новое поле ForeignKey
        migrations.AddField(
            model_name='schedule',
            name='lesson_type',
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to='schedule.lessontype',
                verbose_name='Тип занятия'
            ),
        ),

        # 4. Переносим данные
        migrations.RunPython(create_lesson_types_and_migrate_data),

        # 5. Удаляем старое поле
        migrations.RemoveField(
            model_name='schedule',
            name='lesson_type_old',
        ),
    ]
