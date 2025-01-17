from labeler.django.db import models


class QualityClassChoices(models.TextChoices):
    GOOD = ("good", "Good")
    BAD = ("bad", "Bad")
