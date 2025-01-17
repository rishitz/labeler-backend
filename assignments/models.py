from authorization.models import User
from labeler.django.db import models


class FullStudyAnnotationSet(models.Model):

    name = models.CharField(
        max_length=256,
        null=True,
        blank=True,
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="full_study_annotation_sets",
    )

    class Meta:
        verbose_name = "Full Study Annotation Set"
        verbose_name_plural = "Full Study Annotation Sets"


class StudyLabelingJob(models.Model):

    study = models.ForeignKey(
        "clinic.Study",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="study_labeling_jobs",
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="study_labeling_jobs",
    )
    annotation_set = models.ForeignKey(
        FullStudyAnnotationSet,
        on_delete=models.CASCADE,
        related_name="study_labeling_jobs",
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["study", "user", "annotation_set"],
                name="unique_study_labeling_job",
            )
        ]
        verbose_name = "Study Labeling Job"
        verbose_name_plural = "Study Labeling Jobs"


class DicomLabelingJob(models.Model):
    dicom = models.ForeignKey(
        "clinic.Dicom",
        on_delete=models.CASCADE,
        related_name="dicom_labeling_jobs",
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="dicom_labeling_jobs",
    )
    study_labeling_job = models.ForeignKey(
        StudyLabelingJob,
        on_delete=models.CASCADE,
        related_name="dicom_labeling_jobs",
    )
    annotation_set = models.ForeignKey(
        FullStudyAnnotationSet,
        on_delete=models.CASCADE,
        related_name="dicom_labeling_jobs",
    )

    class Meta:
        verbose_name = "Dicom Labeling Job"
        verbose_name_plural = "Dicom Labeling Jobs"
