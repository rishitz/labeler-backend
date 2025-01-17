from authorization.models import User
from clinic.models import Dicom
from labeler.django.db import models
from quality.choices import QualityClassChoices


class QualityLabel(models.LabelCategoryMixin):
    """Model for quality labels assigned to dicoms."""

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="quality_labels",
        null=True,
        blank=True,
    )
    dicom = models.ForeignKey(
        Dicom,
        on_delete=models.CASCADE,
        related_name="quality_labels",
        null=True,
        blank=True,
    )
    quality_class = models.CharField(
        max_length=10,
        choices=QualityClassChoices.choices,
        null=True,
        blank=True,
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["user", "dicom"],
                name="unique_quality_per_user_dicom",
            )
        ]
        verbose_name = "Quality Label"
        verbose_name_plural = "Quality Labels"
