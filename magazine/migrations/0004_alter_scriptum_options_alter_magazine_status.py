# Generated by Django 4.0.4 on 2022-06-01 02:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('magazine', '0003_alter_magazine_issue_alter_magazine_publication_date_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='scriptum',
            options={'ordering': ['title'], 'verbose_name_plural': 'scripta'},
        ),
        migrations.AlterField(
            model_name='magazine',
            name='status',
            field=models.CharField(choices=[('d', 'Draft'), ('p', 'Published'), ('w', 'Withdrawn')], default='d', editable=False, max_length=1),
        ),
    ]
