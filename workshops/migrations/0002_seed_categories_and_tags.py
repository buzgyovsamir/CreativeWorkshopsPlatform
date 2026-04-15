from django.db import migrations


def seed_data(apps, schema_editor):
    Category = apps.get_model('workshops', 'Category')
    Tag = apps.get_model('workshops', 'Tag')

    categories = [
        ('Painting', 'painting', 'Painting workshops'),
        ('Photography', 'photography', 'Photography workshops'),
        ('Pottery', 'pottery', 'Pottery workshops'),
        ('Music', 'music', 'Music workshops'),
        ('Crafts', 'crafts', 'Craft workshops'),
    ]

    tags = [
        ('Beginner', 'beginner'),
        ('Advanced', 'advanced'),
        ('Weekend', 'weekend'),
        ('Kids Friendly', 'kids-friendly'),
        ('Outdoor', 'outdoor'),
    ]

    for name, slug, description in categories:
        Category.objects.get_or_create(
            slug=slug,
            defaults={
                'name': name,
                'description': description,
            }
        )

    for name, slug in tags:
        Tag.objects.get_or_create(
            slug=slug,
            defaults={
                'name': name,
            }
        )


def unseed_data(apps, schema_editor):
    Category = apps.get_model('workshops', 'Category')
    Tag = apps.get_model('workshops', 'Tag')

    Category.objects.filter(slug__in=[
        'painting',
        'photography',
        'pottery',
        'music',
        'crafts',
    ]).delete()

    Tag.objects.filter(slug__in=[
        'beginner',
        'advanced',
        'weekend',
        'kids-friendly',
        'outdoor',
    ]).delete()


class Migration(migrations.Migration):

    dependencies = [
        ('workshops', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(seed_data, unseed_data),
    ]