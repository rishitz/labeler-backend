from authorization.models import User
from labeler.django.db import models
from segmentations.choices import DenyChoices


class KeypointCollectionClass(models.LabelCategoryMixin):

    value = models.CharField(
        null=True,
        unique=True,
        max_length=100,
    )

    view_classes = models.ManyToManyField(
        "views.ViewClass",
        blank=True,
        related_name="keypoint_collection_classes",
    )
    phase_classes = models.ManyToManyField(
        "phases.PhaseClass",
        blank=True,
        related_name="keypoint_collection_classes",
    )

    class Meta:
        verbose_name = "Keypoint Collection Class"
        verbose_name_plural = "Keypoint Collection Classes"


class KeypointCollectionLabel(models.Model):

    user = models.ForeignKey(
        User,
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name="keypoint_collections",
    )
    frame = models.ForeignKey(
        "clinic.Frame",
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name="keypoint_collections",
    )
    cardiac_cycle_phase = models.ForeignKey(
        "phases.PhaseClass",
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name="keypoint_collections",
    )
    keypoint_collection_class = models.ForeignKey(
        "KeypointCollectionClass",
        on_delete=models.CASCADE,
        related_name="keypoint_collections",
        blank=True,
        null=True,
    )

    class Meta:
        verbose_name = "Keypoint Collection Label"
        verbose_name_plural = "Keypoint Collection Labels"


class KeypointClass(models.LabelCategoryMixin):

    value = models.CharField(
        max_length=128,
        null=True,
        blank=True,
    )
    keypoint_pair = models.OneToOneField(
        "self",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )
    keypoint_collection_class = models.ForeignKey(
        "KeypointCollectionClass",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name="keypoint_classes",
    )
    order = models.IntegerField(
        default=0,
    )

    class Meta:
        verbose_name = "Keypoint Class"
        verbose_name_plural = "Keypoint Classes"
        constraints = [
            models.UniqueConstraint(
                fields=["value", "keypoint_collection_class"],
                name="unique_keypoint_class",
            ),
            models.UniqueConstraint(
                fields=["order", "keypoint_collection_class"],
                name="unique_order",
            ),
        ]


class KeypointLabel(models.Model):

    keypoint_class = models.ForeignKey(
        "KeypointClass",
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name="keypoints",
    )
    keypoint_collection = models.ForeignKey(
        "KeypointCollectionLabel",
        on_delete=models.CASCADE,
        related_name="keypoints",
        blank=True,
        null=True,
    )
    x = models.IntegerField(
        default=0,
        null=True,
        blank=True,
    )
    y = models.IntegerField(
        default=0,
        null=True,
        blank=True,
    )

    class Meta:
        verbose_name = "Keypoint Label"
        verbose_name_plural = "Keypoint Labels"
