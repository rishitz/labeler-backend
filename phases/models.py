from authorization.models import User
from labeler.django.db import models


class PhaseClass(models.Model):

    value = models.CharField(
        unique=True,
        max_length=100,
        blank=True,
        null=True,
    )
    view_classes = models.ManyToManyField(
        "views.ViewClass",
        related_name="phase_classes",
        blank=True,
        through="phases.PhaseView",
    )

    class Meta:
        verbose_name = "Phase Class"
        verbose_name_plural = "Phase Classes"


class PhaseLabel(models.Model):

    frame = models.ForeignKey(
        "clinic.Frame",
        on_delete=models.SET_NULL,
        related_name="phase_labels",
        null=True,
        blank=True,
    )
    user = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        related_name="phase_labels",
        null=True,
        blank=True,
    )
    phase_class = models.ForeignKey(
        "phases.PhaseClass",
        on_delete=models.SET_NULL,
        related_name="phase_labels",
        null=True,
        blank=True,
    )

    class Meta:
        verbose_name = "Phase Label"
        verbose_name_plural = "Phase Labels"


class PhaseView(models.Model):
    """Intermediate model to represent a many-to-many relationship between PhaseClass and ViewClass"""

    phase_class = models.ForeignKey(
        "phases.PhaseClass",
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name="phase_views",
    )
    view_class = models.ForeignKey(
        "views.ViewClass",
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name="phase_views",
    )

    class Meta:
        verbose_name = "Phase Class to View Class"
        verbose_name_plural = "Phase Classes to View Classes"
        constraints = [
            models.UniqueConstraint(
                fields=["phase_class", "view_class"],
                name="unique_phase_view",
            )
        ]
