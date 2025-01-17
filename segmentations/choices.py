from labeler.django.db import models


class DenyChoices(models.TextChoices):
    BAD_DICOM = ("BAD_DICOM", "Bad DICOM")
    BAD_LABEL = ("BAD_LABEL", "Bad Label")
