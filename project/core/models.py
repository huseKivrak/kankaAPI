from django.db import models
from django.urls import reverse
from django.contrib.auth.models import BaseUserManager, AbstractUser, PermissionsMixin
from django.core.validators import RegexValidator

# Utility for adding created/updated timestamps


class TrackingModel(models.Model):
    '''Adds created_at and updated_at fields'''
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    class Meta:
        abstract = True
        ordering = ('-created_at',)

class UserProfileManager(BaseUserManager):
    """Manager for user profiles"""

    def create_user(self, email, username, password=None):
        if not email:
            raise ValueError('Users must have an email')

        email = self.normalize_email(email)
        user = self.model(email=email, username=username)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, username, password):
        user = self.create_user(email, username, password)
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)



class User(AbstractUser, PermissionsMixin):
    email = models.EmailField(
        unique=True,
    )

    username = models.CharField(
        max_length=50,
        unique=True,
    )

    is_active = models.BooleanField(
        default=True,
    )

    zip_code = models.CharField(
        max_length=10,
        validators=[RegexValidator(
            regex='^[0-9]{5}(?:-[0-9]{4})?$|^$',
            message='Zip code must be in the format XXXXX or XXXXX-XXXX',
            code='invalid_zip_code'
        )]
    )

    objects = UserProfileManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email', 'zip_code']

    def __str__(self):
        return self.email



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

    delivery_date = models.DateTimeField(
        null=True,
        blank=True,
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

    body = models.TextField(
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
        related_name='authored_letters',
    )

    recipient = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='received_letters',
    )

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('letter_detail', kwargs={'pk': self.pk})

    def get_status(self):
        return self.status
