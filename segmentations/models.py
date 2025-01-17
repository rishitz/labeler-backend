import base64
import os

from django.core.files import File

from authorization.models import User
from labeler.django.db import models


class SegmentationClass(models.Model):
    value = models.CharField(
        max_length=32,
        unique=True,
    )
    view_classes = models.ManyToManyField(
        "views.ViewClass",
        blank=True,
        related_name="segmentation_classes",
    )

    def __str__(self):
        return self.value

    class Meta:
        verbose_name = "Segmentation Class"
        verbose_name_plural = "Segmentation Classes"


class SegmentationLabel(models.Model):

    def upload_to(self, instance):
        return f"Labels/Segmentations/{self.uuid}.{self.extension}"

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name="segmentation_labels",
    )
    frame = models.ForeignKey(
        "clinic.Frame",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name="segmentation_labels",
    )
    segmentation_class = models.ForeignKey(
        "segmentations.SegmentationClass",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="segmentation_labels",
    )
    cardiac_cycle_phase = models.ForeignKey(
        "phases.PhaseClass",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name="segmentation_labels",
    )

    file = models.FileField(
        upload_to=upload_to,
        blank=True,
        null=True,
    )
    paths = models.JSONField(
        blank=True,
        null=True,
    )
    is_fully_visible = models.BooleanField(
        default=True,
    )

    def save_bytes(self, byte_string):
        """Save a byte string as an image file."""
        byte_string = byte_string.replace("data:image/png;base64", "")
        byte_string = base64.b64decode(byte_string)

        temp_file = f"{self.uuid}.{self.extension}"

        with open(temp_file, "wb") as file:
            file.write(byte_string)

        self.file = File(open(temp_file, "rb"))
        self.save()

        os.remove(temp_file)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["user", "frame", "segmentation_class"],
                name="unique_user_frame_segmentation_class",
            )
        ]
        verbose_name = "Segmentation Label"
        verbose_name_plural = "Segmentation Labels"
