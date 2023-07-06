from django.db import models
from django.urls import reverse
from django.contrib.auth.models import AbstractUser

# Utility for adding created/updated timestamps


class TrackingModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
        ordering = ('-created_at',)


class User(AbstractUser):
    email = models.EmailField(
        unique=True,
    )


class Letter(TrackingModel):

    DRAFT = 'draft'
    SENT = 'sent'
    DELIVERED = 'delivered'
    READ = 'read'

    STATUS_CHOICES = [
        (DRAFT, 'Draft'),
        (SENT, 'Sent'),
        (DELIVERED, 'Delivered'),
        (READ, 'Read'),
    ]

    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default=DRAFT,
    )

    title = models.CharField(
        max_length=100,
    )

    # 'date' is just another text field. actual dates handled by TrackingModel
    date = models.CharField(
        max_length=2500,
        blank=True,
    )

    opener = models.CharField(
        max_length=2500,
        blank=True,
        help_text='Dear [name],'
    )

    body = models.CharField(
        max_length=2500,
    )

    closer = models.CharField(
        max_length=2500,
        blank=True,
        help_text='Regards,',
        verbose_name='Complimentary close'
    )

    signature = models.CharField(
        max_length=2500,
        blank=True,
    )

    postscript = models.CharField(
        max_length=2500,
        blank=True,
        help_text='P.S. [message]'
    )

    author = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name='authored',
    )

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('letter_detail', kwargs={'pk': self.pk})

    def get_status(self):
        return self.status


class Recipient(models.Model):

    letter = models.ForeignKey(
        Letter,
        on_delete=models.CASCADE,
    )

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='received',
    )
