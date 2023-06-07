from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
import uuid
from cloudinary.models import CloudinaryField
# Create your models here.


class UserManager(BaseUserManager):
    def create_user(self, email, username, password=None):
        if not email:
            raise ValueError("enter a valid email")
        if not username:
            raise ValueError("enter a username")

        user = self.model(
            email=self.normalize_email(email),
            username=username,

        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password=None):
        user = self.create_user(
            email=self.normalize_email(email),
            username=username,
            password=password
        )

        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.is_active = True
        user.save(using=self._db)
        return user


class UserCategory(models.Model):
    name = models.CharField(max_length=200, verbose_name='category')

    def __str__(self) -> str:
        return self.name


class User(AbstractBaseUser):
    uid = models.UUIDField(primary_key=True, default=uuid.uuid4,
                           editable=False)
    username = models.CharField(max_length=255, unique=True)
    email = models.EmailField(max_length=100, unique=True)
    address = models.TextField(max_length=500, null=True, blank=True)
    phone = models.IntegerField(null=True, blank=True)
    profileImage = CloudinaryField('image')
    user_category = models.ForeignKey(
        UserCategory, on_delete=models.CASCADE, blank=True, null=True)
    registered_on = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
    objects = UserManager()

    def __str__(self) -> str:
        return self.username

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True


class ProductCategory(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self) -> str:
        return self.name


class Product(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    product_id = models.UUIDField(default=uuid.uuid4, unique=True,
                                  editable=False, primary_key=True)
    product_name = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)
    product_price = models.DecimalField(
        decimal_places=2, max_digits=15, default=00.00)
    product_category = models.ForeignKey(
        ProductCategory, on_delete=models.CASCADE, related_name='category')
    product_image = CloudinaryField('product_image')
    date_created = models.DateTimeField(auto_now_add=True)
    condition = models.CharField(max_length=200)

    def __str__(self) -> str:
        return self.product_name
