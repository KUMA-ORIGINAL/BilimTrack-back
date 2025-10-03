# academics/migrations/0039_fix_split.py
from django.db import migrations


def re_split_old_grade(apps, schema_editor):
    Grade = apps.get_model('academics', 'Grade')

    mapping = {
        10: ('A', 5),
        9:  ('A', 4),
        8:  ('A', 4),
        7:  ('A', 3),
        6:  ('A', 3),
        5:  ('A', 0),
        4:  ('B', 0),
        3:  ('C', 0),
        2:  ('N', 0),
        1:  ('N', 0),
        0:  ('N', 0),
    }

    for row in Grade.objects.all():
        total = row.grade or 0
        att, act = mapping.get(total, (None, None))
        row.attendance = att
        row.grade = act
        row.save(update_fields=["attendance", "grade"])


class Migration(migrations.Migration):
    dependencies = [
        ("academics", "0037_grade_attendance_alter_grade_grade"),
    ]
    operations = [
        migrations.RunPython(re_split_old_grade),
    ]
