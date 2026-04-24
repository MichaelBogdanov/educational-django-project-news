from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin


# Create your models here.
class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('Поле электронной почты обязательно')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(email, password, **extra_fields)  

class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField('Почта', unique=True)
    
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    
    objects = CustomUserManager()
    
    USERNAME_FIELD = 'email'
    
    def __str__(self):
        return self.email

    class Meta:
        verbose_name = 'пользователя'
        verbose_name_plural = 'Пользователи'

class Category(models.Model):
    name = models.CharField('Название категории', max_length=100)
    description = models.TextField('Описание категории')
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = 'категорию'
        verbose_name_plural = 'Категории'

class News(models.Model):
    title = models.CharField('Заголовок', max_length=100)
    description = models.TextField('Описание')
    photo = models.ImageField('Изображение', upload_to='news/', blank=True, null=True)
    created_at = models.DateTimeField('Дата создания', auto_now_add=True)
    is_published = models.BooleanField('Статус публикации')
    
    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name = 'новость'
        verbose_name_plural = 'Новости'
        ordering = ['-created_at']

class NewsCategory(models.Model):
    news = models.ForeignKey(News, on_delete=models.PROTECT)
    category = models.ForeignKey(Category, on_delete=models.PROTECT)
    
    def __str__(self):
        return f'{self.category} - {self.news}'
    
    class Meta:
        verbose_name = 'категорию к новости'
        verbose_name_plural = 'Категории новостей'

class Comment(models.Model):
    news = models.ForeignKey(News, on_delete=models.PROTECT)
    user = models.ForeignKey(CustomUser, on_delete=models.PROTECT)
    message = models.CharField('Текст', max_length=256)
    created_at = models.DateTimeField('Дата и время создания', auto_now_add=True)
    
    def __str__(self) -> str:
        return f"[{ self.created_at }] { self.message }"
    
    class Meta:
        verbose_name = 'комментарий'
        verbose_name_plural = 'Комментарии'
        ordering = ['-created_at']