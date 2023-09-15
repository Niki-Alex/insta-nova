import os
import uuid

from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django.utils.text import slugify
from django.utils.translation import gettext as _
from phonenumber_field.modelfields import PhoneNumberField
from rest_framework.exceptions import ValidationError


def user_image_file_path(instance, filename):
    _, extension = os.path.splitext(filename)
    filename = f"{slugify(instance)}-{uuid.uuid4()}{extension}"

    return os.path.join("uploads", "users", filename)


class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError("The given email must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self._create_user(email, password, **extra_fields)


class User(AbstractUser):
    email = models.EmailField(
        _("email address"),
        unique=True,
        error_messages={"unique": _("An user with that email already exists.")},
    )
    username = models.CharField(max_length=64, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    biography = models.TextField(null=True, blank=True)
    phone_number = PhoneNumberField(null=True, blank=True)
    avatar = models.ImageField(null=True, blank=True, upload_to=user_image_file_path)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = UserManager()


class UserFollowing(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name="following")
    following_user_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name="followers")
    created = models.DateTimeField(auto_now_add=True, db_index=True)

    @staticmethod
    def validate_user_following(
            user: User,
            following_user: User,
            error_to_raise
    ):
        if user.following.filter(following_user_id=following_user).exists():
            raise error_to_raise(f"You already follow to {following_user}")

    def clean(self) -> None:
        UserFollowing.validate_user_following(
            self.user_id,
            self.following_user_id,
            ValidationError
        )

    def save(
        self, force_insert=False, force_update=False, using=None, update_fields=None
    ):
        self.full_clean()
        return super(UserFollowing, self).save(
            force_insert, force_update, using, update_fields
        )

    class Meta:
        unique_together = ("user_id", "following_user_id")
        index_together = ("user_id", "following_user_id")
        ordering = ["-created"]

    def __str__(self):
        return f"{self.user_id} follows {self.following_user_id}"
