from uuid import uuid4

# from django.core.files.storage import get_storage_class
from django.db.models import *  # noqa: F403, F401
from django.db.utils import IntegrityError

from labeler.django.db import models


def generate_icid(uuid, char):
    """
    Generate a custom iCardio ID string based on the provided character prefix.
    """

    full_uuid = str(uuid).upper().replace("-", "")

    return f"{char}-{full_uuid[0:4]}-{full_uuid[4:8]}-{full_uuid[8:12]}"


def generate_link(instance):
    """Generates a temporary access URL for the document in the S3 bucket."""

    # if instance.file:

    #     report_storage = get_storage_class()()

    #     url = report_storage.url(instance.file.name)

    #     return url

    return None


class Model(models.Model):
    """Abstract base model to add common fields for all models."""

    uuid = models.UUIDField(
        default=uuid4,
        editable=False,
        unique=True,
    )
    icid = models.CharField(
        unique=True, max_length=50, blank=True, null=True, editable=False
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        editable=False,
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        editable=False,
    )

    is_deleted = models.BooleanField(default=False)

    @property
    def link(self):
        return generate_link(self)

    def save(self, *args, **kwargs):

        # Set uuid if not already set
        if not self.uuid:
            self.uuid = uuid4()

        # Set icid if not already set
        if not self.icid:

            char = type(self).__name__[0:2].lower()

            try:
                self.icid = generate_icid(self.uuid, char)

            except IntegrityError:
                self.icid = None  # Reset icid to avoid recursion issues
                self.save(*args, **kwargs)  # Retry saving with a new ICID

        super().save(*args, **kwargs)

    def __str__(self):
        return str(getattr(self, "icid", self.uuid))

    class Meta:
        abstract = True


class LabelCategoryMixin(models.Model):
    @classmethod
    def options(cls):
        options = []
        for instance in cls.objects.all():
            options.append(
                {
                    "name": "value",
                    "value": instance.value,
                    "id": instance.id,
                    "uuid": instance.uuid,
                }
            )
        return options

    def __str__(self):
        return self.value

    class Meta:
        abstract = True
