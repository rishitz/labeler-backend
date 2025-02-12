# Generated by Django 5.1.3 on 2024-12-31 19:15

import django.db.models.deletion
import uuid
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('clinic', '0001_initial'),
        ('phases', '0001_initial'),
        ('views', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='KeypointCollectionClass',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('icid', models.CharField(blank=True, editable=False, max_length=50, null=True, unique=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('is_deleted', models.BooleanField(default=False)),
                ('value', models.CharField(max_length=100, null=True, unique=True)),
                ('phase_classes', models.ManyToManyField(blank=True, related_name='key_point_collection_classes', to='phases.phaseclass')),
                ('view_classes', models.ManyToManyField(blank=True, related_name='key_point_collection_classes', to='views.viewclass')),
            ],
            options={
                'verbose_name_plural': 'Key Point Collection Classes',
            },
        ),
        migrations.CreateModel(
            name='KeypointClass',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('icid', models.CharField(blank=True, editable=False, max_length=50, null=True, unique=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('is_deleted', models.BooleanField(default=False)),
                ('value', models.CharField(blank=True, max_length=128, null=True)),
                ('order', models.IntegerField(default=0)),
                ('key_point_pair', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='keypoints.keypointclass')),
                ('key_point_collection_class', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='key_point_classes', to='keypoints.keypointcollectionclass')),
            ],
            options={
                'verbose_name_plural': 'Key Point Classes',
                'ordering': ['key_point_collection_class', 'order'],
                'unique_together': {('key_point_collection_class', 'order'), ('value', 'key_point_collection_class')},
            },
        ),
        migrations.CreateModel(
            name='KeypointCollectionLabel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('icid', models.CharField(blank=True, editable=False, max_length=50, null=True, unique=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('is_deleted', models.BooleanField(default=False)),
                ('accepted', models.BooleanField(blank=True, null=True)),
                ('deny_reason', models.CharField(blank=True, choices=[('BAD_DICOM', 'Bad DICOM'), ('BAD_LABEL', 'Bad Label')], default=None, max_length=16, null=True)),
                ('cardiac_cycle_phase', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='key_point_collections', to='phases.phaseclass')),
                ('frame', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='key_point_collections', to='clinic.frame')),
                ('key_point_collection_class', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='key_point_collections', to='keypoints.keypointcollectionclass')),
                ('review_user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='keypointcollection_reviews', to=settings.AUTH_USER_MODEL)),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='key_point_collections', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'Key Point Collection Labels',
            },
        ),
        migrations.CreateModel(
            name='KeypointLabel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('icid', models.CharField(blank=True, editable=False, max_length=50, null=True, unique=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('is_deleted', models.BooleanField(default=False)),
                ('x', models.IntegerField(blank=True, default=0, null=True)),
                ('y', models.IntegerField(blank=True, default=0, null=True)),
                ('key_point_class', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='key_points', to='keypoints.keypointclass')),
                ('key_point_collection', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='key_points', to='keypoints.keypointcollectionlabel')),
            ],
            options={
                'verbose_name_plural': 'Key Points',
            },
        ),
    ]
