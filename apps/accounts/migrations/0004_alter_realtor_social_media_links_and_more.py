# Generated by Django 4.2.17 on 2025-04-14 07:49

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_alter_realtor_bio_alter_realtor_company_address_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='realtor',
            name='social_media_links',
            field=models.JSONField(blank=True, default=dict, null=True),
        ),
        migrations.CreateModel(
            name='UserNotificationPreference',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email_notifications_enabled', models.BooleanField(default=True, help_text='Receive email notifications for important updates')),
                ('new_leads_email', models.BooleanField(default=True, help_text='Get email notifications when new leads are generated')),
                ('account_updates_email', models.BooleanField(default=True, help_text='Get email notifications about important account changes')),
                ('marketing_emails', models.BooleanField(default=True, help_text='Receive promotional emails and special offers')),
                ('in_app_notifications', models.BooleanField(default=True, help_text='Receive notifications within the HabitatHunt dashboard')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='notification_preferences', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'User Notification Preference',
                'verbose_name_plural': 'User Notification Preferences',
            },
        ),
    ]
