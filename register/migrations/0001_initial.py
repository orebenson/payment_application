from django.contrib.auth.hashers import make_password
from django.db import migrations


def create_admin(apps, schema_editor):
    User = apps.get_registered_model('auth', 'User')
    admin = User(
        username='admin1',
        email='admin1@admin.com',
        password=make_password('admin1'),
        is_superuser=True,
        is_staff=True
    )
    admin.save()


class Migration(migrations.Migration):
    dependencies = [
        ('auth', '0001_initial')
    ]

    operations = [
        migrations.RunPython(create_admin),
    ]