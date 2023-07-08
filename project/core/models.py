from django.db import models
from django.utils import timezone
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
        return self.username


class LetterQuerySet(models.QuerySet):
    def drafts(self):
        return self.filter(status='draft')

    def deliveries(self):
        return self.filter(status='delivered')

    def reads(self):
        return self.filter(status='read')




class Letter(TrackingModel):

    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('sent', 'Sent'),
        ('delivered', 'Delivered'),
        ('read', 'Read'),
    ]

    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default='draft',
    )

    sent_date = models.DateTimeField(
        null=True,
        blank=True,
    )

    delivery_date = models.DateTimeField(
        # Calculated after letter is sent
        null=True,
        blank=True,
    )

    title = models.CharField(
        max_length=100,
    )

    body = models.TextField(
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

    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=True,
        related_name='owned_letters',
        default=author,
    )


    def send(self):
        self.status = 'sent'
        self.sent_date = timezone.now()
        # TODO: update with ZipCodeAPI value
        self.delivery_date = self.sent_date + timezone.timedelta(days=1)
        self.save()

    def deliver(self):
        self.status = 'delivered'
        self.owner = self.recipient
        self.save()

    def mark_as_read(self):
        self.status = 'read'
        self.save()

    def is_owned_by(self, user):
        return self.owner == user


    letters = LetterQuerySet.as_manager()

    def __str__(self):
        return self.title
