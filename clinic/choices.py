from labeler.django.db import models


class DesignationChoices(models.TextChoices):
    TRAIN = ("TRAIN", "Train")
    TEST = ("TEST", "Test")
    VAL = ("VAL", "Validation")


class DicomTypeChoices(models.TextChoices):
    COLOR = ("Color", "Color")
    STANDARD = ("Standard", "Standard")
    SINGLE_FRAME = ("Single Frame", "Single Frame")


class MediaExtensionChoices(models.TextChoices):
    MP4 = ("mp4", "mp4")
    PNG = ("png", "png")
