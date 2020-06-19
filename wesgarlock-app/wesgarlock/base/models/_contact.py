from django.contrib.auth import get_user_model
from django.db import models
from modelcluster.models import ClusterableModel, ParentalKey
from wagtail.admin.edit_handlers import FieldPanel, InlinePanel


class MessageThread(ClusterableModel):
    email = models.EmailField()
    owner = models.ForeignKey(
        "wesgarlockbase.User",
        blank=True,
        null=True,
        on_delete=models.CASCADE
    )

    def save(self, *args, **kwawrgs):
        if self.owner is None:
            self.owner = get_user_model().objects.filter(email=self.email).first()
        super().save()

    panels = [
        FieldPanel("email"),
        FieldPanel("owner"),
        InlinePanel("thread_messages", label="Messages")
    ]

    def __str__(self):
        return f"{(self.owner or self.email )} messages"


class Message(models.Model):
    thread = ParentalKey(
        MessageThread,
        on_delete=models.CASCADE,
        related_name="thread_messages"
    )

    email = models.EmailField(max_length=255)

    author = models.ForeignKey(
        "wesgarlockbase.User",
        on_delete=models.CASCADE,
        blank=True,
        null=True
    )

    created_time = models.DateTimeField(
        auto_now_add=True
    )

    edited_time = models.DateTimeField(
        auto_now=True
    )

    reply_to = models.ForeignKey(
        "self",
        on_delete=models.CASCADE,
        blank=True,
        null=True

    )

    body = models.TextField()
