from labeler.django.db import models


class ViewClassMediaTypeChoices(models.TextChoices):
    VIDEO = ("Video", "Video")
    SINGLE_FRAME = ("Single Frame", "Single Frame")


class ViewClassTypeChoices(models.TextChoices):
    STANDARD = ("Standard", "Standard")
    COLOR = ("Color", "Color")
