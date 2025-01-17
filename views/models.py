from authorization.models import User
from labeler.django.db import models
from views.choices import ViewClassMediaTypeChoices, ViewClassTypeChoices


class ViewClass(models.LabelCategoryMixin):

    window = models.CharField(
        max_length=40,
        blank=True,
        null=True,
    )
    view = models.CharField(
        max_length=40,
        blank=True,
        null=True,
    )
    type = models.CharField(
        max_length=20,
        blank=True,
        null=True,
        choices=ViewClassTypeChoices.choices,
    )
    media_type = models.CharField(
        max_length=20,
        blank=True,
        null=True,
        default=ViewClassMediaTypeChoices.VIDEO,
        choices=ViewClassMediaTypeChoices.choices,
    )

    def __str__(self):
        return f"{self.media_type} - {self.type} - {self.window} {self.view}"

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["window", "view", "type", "media_type"],
                name="unique_view_class",
            )
        ]
        verbose_name = "View Class"
        verbose_name_plural = "View Classes"


class ViewLabel(models.Model):

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name="view_labels",
    )
    dicom = models.ForeignKey(
        "clinic.Dicom",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name="view_labels",
    )
    view_class = models.ForeignKey(
        "views.ViewClass",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="view_labels",
    )

    class Meta:
        verbose_name = "View Label"
        verbose_name_plural = "View Labels"
        constraints = [
            models.UniqueConstraint(
                fields=["user", "dicom"],
                name="unique_view_per_user_dicom",
            )
        ]
