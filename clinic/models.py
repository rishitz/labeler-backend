from clinic.choices import DesignationChoices, DicomTypeChoices, MediaExtensionChoices
from labeler.django.db import models


class Dicom(models.Model):

    study = models.ForeignKey(
        "Study",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name="dicoms",
    )
    file = models.FileField(
        upload_to="upload_to",
        blank=True,
        null=True,
    )
    index = models.IntegerField(blank=True, null=True)

    # Meta data fields
    manufacturer = models.CharField(
        max_length=50,
        blank=True,
        null=True,
    )
    manufacturer_model_name = models.CharField(
        max_length=50,
        blank=True,
        null=True,
    )
    physical_units_x_direction = models.CharField(
        max_length=20,
        blank=True,
        null=True,
    )
    physical_units_y_direction = models.CharField(
        max_length=20,
        blank=True,
        null=True,
    )
    physical_delta_x = models.FloatField(
        blank=True,
        null=True,
    )
    physical_delta_y = models.FloatField(
        blank=True,
        null=True,
    )
    type = models.CharField(
        max_length=20,
        blank=True,
        null=True,
        choices=DicomTypeChoices.choices,
    )
    number_of_frames = models.IntegerField(
        blank=True,
        null=True,
    )
    pixel_height = models.IntegerField(
        blank=True,
        null=True,
    )
    pixel_width = models.IntegerField(
        blank=True,
        null=True,
    )
    frames_per_second = models.FloatField(
        blank=True,
        null=True,
    )
    designation = models.CharField(
        max_length=16,
        choices=DesignationChoices.choices,
        blank=True,
        null=True,
    )

    def upload_to(self, instance):
        return f"Dicoms/{self.uuid}.dcm"

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["study", "index"],
                name="unique_study_index",
            ),
        ]
        indexes = [
            models.Index(fields=["designation"]),
            models.Index(fields=["type"]),
        ]


class Study(models.Model):
    number_of_dicoms = models.IntegerField(
        blank=True,
        null=True,
    )
    number_of_usable_dicoms = models.IntegerField(
        blank=True,
        null=True,
    )
    designation = models.CharField(
        max_length=16,
        choices=DesignationChoices.choices,
        blank=True,
        null=True,
    )

    class Meta:
        verbose_name_plural = "Studies"
        indexes = [
            models.Index(fields=["designation"]),
        ]


class Frame(models.Model):
    media = models.ForeignKey(
        "Media",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="frames",
    )
    index = models.IntegerField(
        blank=True,
        null=True,
    )
    file = models.FileField(
        upload_to="upload_to",
        blank=True,
        null=True,
    )
    extension = models.CharField(
        max_length=3,
        blank=True,
        null=True,
    )

    def upload_to(self, instance):
        return f"Frames/{self.uuid}.{self.extension}"


class Media(models.Model):

    dicom = models.OneToOneField(
        "Dicom",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="media",
    )
    file = models.FileField(
        upload_to="upload_to",
        blank=True,
        null=True,
    )
    extension = models.CharField(
        max_length=3,
        blank=True,
        null=True,
        choices=MediaExtensionChoices.choices,
    )

    def upload_to(self, instance):
        return f"Media/{self.uuid}.{self.extension}"
