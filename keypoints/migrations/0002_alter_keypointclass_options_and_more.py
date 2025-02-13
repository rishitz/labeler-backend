# Generated by Django 5.1.3 on 2024-12-31 19:24

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clinic', '0002_alter_media_options'),
        ('keypoints', '0001_initial'),
        ('phases', '0001_initial'),
        ('views', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='keypointclass',
            options={'verbose_name': 'Keypoint Class', 'verbose_name_plural': 'Keypoint Classes'},
        ),
        migrations.AlterModelOptions(
            name='keypointcollectionclass',
            options={'verbose_name': 'Keypoint Collection Class', 'verbose_name_plural': 'Keypoint Collection Classes'},
        ),
        migrations.AlterModelOptions(
            name='keypointcollectionlabel',
            options={'verbose_name': 'Keypoint Collection Label', 'verbose_name_plural': 'Keypoint Collection Labels'},
        ),
        migrations.AlterModelOptions(
            name='keypointlabel',
            options={'verbose_name': 'Keypoint Label', 'verbose_name_plural': 'Keypoint Labels'},
        ),
        migrations.RenameField(
            model_name='keypointclass',
            old_name='key_point_pair',
            new_name='keypoint_pair',
        ),
        migrations.AlterUniqueTogether(
            name='keypointclass',
            unique_together=set(),
        ),
        migrations.RemoveField(
            model_name='keypointcollectionlabel',
            name='accepted',
        ),
        migrations.RemoveField(
            model_name='keypointcollectionlabel',
            name='deny_reason',
        ),
        migrations.RemoveField(
            model_name='keypointcollectionlabel',
            name='key_point_collection_class',
        ),
        migrations.RemoveField(
            model_name='keypointcollectionlabel',
            name='review_user',
        ),
        migrations.RemoveField(
            model_name='keypointlabel',
            name='key_point_class',
        ),
        migrations.RemoveField(
            model_name='keypointlabel',
            name='key_point_collection',
        ),
        migrations.AddField(
            model_name='keypointclass',
            name='keypoint_collection_class',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='keypoint_classes', to='keypoints.keypointcollectionclass'),
        ),
        migrations.AddField(
            model_name='keypointcollectionlabel',
            name='keypoint_collection_class',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='keypoint_collections', to='keypoints.keypointcollectionclass'),
        ),
        migrations.AddField(
            model_name='keypointlabel',
            name='keypoint_class',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='keypoints', to='keypoints.keypointclass'),
        ),
        migrations.AddField(
            model_name='keypointlabel',
            name='keypoint_collection',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='keypoints', to='keypoints.keypointcollectionlabel'),
        ),
        migrations.AlterField(
            model_name='keypointcollectionclass',
            name='phase_classes',
            field=models.ManyToManyField(blank=True, related_name='keypoint_collection_classes', to='phases.phaseclass'),
        ),
        migrations.AlterField(
            model_name='keypointcollectionclass',
            name='view_classes',
            field=models.ManyToManyField(blank=True, related_name='keypoint_collection_classes', to='views.viewclass'),
        ),
        migrations.AlterField(
            model_name='keypointcollectionlabel',
            name='cardiac_cycle_phase',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='keypoint_collections', to='phases.phaseclass'),
        ),
        migrations.AlterField(
            model_name='keypointcollectionlabel',
            name='frame',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='keypoint_collections', to='clinic.frame'),
        ),
        migrations.AlterField(
            model_name='keypointcollectionlabel',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='keypoint_collections', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddConstraint(
            model_name='keypointclass',
            constraint=models.UniqueConstraint(fields=('value', 'keypoint_collection_class'), name='unique_keypoint_class'),
        ),
        migrations.AddConstraint(
            model_name='keypointclass',
            constraint=models.UniqueConstraint(fields=('order', 'keypoint_collection_class'), name='unique_order'),
        ),
        migrations.RemoveField(
            model_name='keypointclass',
            name='key_point_collection_class',
        ),
    ]
