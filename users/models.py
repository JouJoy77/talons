from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db.models.signals import post_save
from django.urls import reverse

# from django.utils.translation import ugettext_lazy as _

Hostel = (
    ('Push_9', 'Pushkina, 32'),
    ('Push_8', 'Pushkina, 32a'),
)

class Tickets(models.Model):

    title = models.CharField(
        max_length=255,
        verbose_name='Наименование'
    )
    description = models.TextField(verbose_name='Описание')
    price = models.DecimalField('Цена', decimal_places=2, max_digits=5)
    slug = models.SlugField(unique=True)

    class Meta:
        verbose_name = 'Талончик'
        verbose_name_plural = 'Талончики'

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse(
            'ticket_detail',
            kwargs={
                'ticket_slug': self.slug,
            }
        )


class UserManager(BaseUserManager):

    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError('Отсутствует адрес электронной почты')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser должен иметь поле is_staff==True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser должен иметь поле is_superuser==True.')

        return self._create_user(email, password, **extra_fields)


class User(AbstractUser):

    username = models.CharField(max_length=20,unique=True)
    email = models.EmailField(('email address'), unique=True)
    hostel = models.CharField(max_length=100, choices=Hostel)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return f'{self.username}, {self.hostel}'


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.user.username} Profile'

def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

post_save.connect(create_user_profile, sender=User)