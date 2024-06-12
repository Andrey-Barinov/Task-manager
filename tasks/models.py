from django.db import models
from django.contrib.auth import get_user_model
from statuses.models import Status


class Task(models.Model):
    name = models.CharField(max_length=150, unique=True, null=False)

    description = models.TextField(blank=True)

    status = models.ForeignKey(Status, on_delete=models.PROTECT, null=False)

    executor = models.ForeignKey(
        get_user_model(), on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name="executor"
    )

    author = models.ForeignKey(
        get_user_model(),
        on_delete=models.PROTECT,
        null=False,
        related_name="author"
    )

    created_at = models.DateTimeField(auto_now_add=True)
