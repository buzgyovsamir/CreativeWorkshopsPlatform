from django.db import migrations


def seed_groups(apps, schema_editor):
    Group = apps.get_model('auth', 'Group')
    Permission = apps.get_model('auth', 'Permission')

    organizers, _ = Group.objects.get_or_create(name='Organizers')
    participants, _ = Group.objects.get_or_create(name='Participants')

    organizer_permissions = Permission.objects.filter(
        content_type__app_label='workshops',
        codename__in=[
            'add_workshop',
            'change_workshop',
            'delete_workshop',
            'view_workshop',
            'view_category',
            'view_tag',
        ],
    )

    participant_permissions = Permission.objects.filter(
        content_type__app_label__in=['bookings', 'reviews', 'workshops'],
        codename__in=[
            'add_booking',
            'change_booking',
            'view_booking',
            'add_review',
            'change_review',
            'delete_review',
            'view_review',
            'view_workshop',
        ],
    )

    organizers.permissions.set(organizer_permissions)
    participants.permissions.set(participant_permissions)


def unseed_groups(apps, schema_editor):
    Group = apps.get_model('auth', 'Group')
    Group.objects.filter(name__in=['Organizers', 'Participants']).delete()


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
        ('bookings', '0001_initial'),
        ('reviews', '0001_initial'),
        ('workshops', '0002_seed_categories_and_tags'),
    ]

    operations = [
        migrations.RunPython(seed_groups, unseed_groups),
    ]
