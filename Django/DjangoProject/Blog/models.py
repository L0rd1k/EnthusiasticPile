from django.db import models
from datetime import date, datetime, timedelta

import jwt

from django.urls import reverse
from django.core import validators
from django.conf import settings

from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.models import BaseUserManager

class Category(models.Model):
    name = models.CharField("Категория", max_length=150)
    description = models.TextField("Описание")
    url = models.SlugField(max_length=160, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"

class Actor(models.Model):
    name = models.CharField("Имя", max_length=100)
    age = models.PositiveSmallIntegerField("Возраст", default=0)
    description = models.TextField("Описание")
    image = models.ImageField("Изображение", upload_to="actors/")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('actor_detail', kwargs={"slug": self.name})

    class Meta:
        verbose_name = "Актеры и режиссеры"
        verbose_name_plural = "Актеры и режиссеры"

class Genre(models.Model):
    name = models.CharField("Имя", max_length=100)
    description = models.TextField("Описание")
    url = models.SlugField(max_length=160, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Жанр"
        verbose_name_plural = "Жанры"

class Movie(models.Model):
    title = models.CharField("Название", max_length=100)
    tagline = models.CharField("Слоган", max_length=100, default='')
    description = models.TextField("Описание")
    poster = models.ImageField("Постер", upload_to="movies/")
    year = models.PositiveSmallIntegerField("Дата выхода", default=2019)
    country = models.CharField("Страна", max_length=30)
    directors = models.ManyToManyField(Actor, verbose_name="режиссер", related_name="film_director")
    actors = models.ManyToManyField(Actor, verbose_name="актеры", related_name="film_actor")
    genres = models.ManyToManyField(Genre, verbose_name="жанры")
    world_premiere = models.DateField("Примьера в мире", default=date.today)
    budget = models.PositiveIntegerField("Бюджет", default=0, help_text="указывать сумму в долларах")

    fees_in_usa = models.PositiveIntegerField("Сборы в США", default=0, help_text="указывать сумму в долларах")
    fess_in_world = models.PositiveIntegerField("Сборы в мире", default=0, help_text="указывать сумму в долларах")
    category = models.ForeignKey(Category, verbose_name="Категория", on_delete=models.SET_NULL, null=True)
    url = models.SlugField(max_length=130, unique=True)
    draft = models.BooleanField("Черновик", default=False)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("movie_detail", kwargs={"slug": self.url})

    def get_review(self):
        return self.reviews_set.filter(parent__isnull=True)

    class Meta:
        verbose_name = "Фильм"
        verbose_name_plural = "Фильмы"

class MovieShots(models.Model):
    """Кадры из фильма"""
    title = models.CharField("Заголовок", max_length=100)
    description = models.TextField("Описание")
    image = models.ImageField("Изображение", upload_to="movie_shots/")
    movie = models.ForeignKey(Movie, verbose_name="Фильм", on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Кадр из фильма"
        verbose_name_plural = "Кадры из фильма"

class RatingStar(models.Model):
    """Звезда рейтинга"""
    value = models.SmallIntegerField("Значение", default=0)

    def __str__(self):
        return f'{self.value}'

    class Meta:
        verbose_name = "Звезда рейтинга"
        verbose_name_plural = "Звезды рейтинга"
        ordering = ["-value"]

class Rating(models.Model):
    """Рейтинг"""
    ip = models.CharField("IP адрес", max_length=15)
    star = models.ForeignKey(RatingStar, on_delete=models.CASCADE, verbose_name="звезда")
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, verbose_name="фильм")

    def __str__(self):
        return f"{self.star} - {self.movie}"

    class Meta:
        verbose_name = "Рейтинг"
        verbose_name_plural = "Рейтинги"

class Review(models.Model):
    """Отзывы"""
    email = models.EmailField()
    name = models.CharField("Имя", max_length=100)
    text = models.TextField("Сообщение", max_length=5000)
    parent = models.ForeignKey(
        'self', verbose_name="Родитель", on_delete=models.SET_NULL, blank=True, null=True
    )
    movie = models.ForeignKey(Movie, verbose_name="фильм", on_delete=models.CASCADE, related_name="reviews")

    def __str__(self):
        return f"{self.name} - {self.movie}"

    class Meta:
        verbose_name = "Отзыв"
        verbose_name_plural = "Отзывы"

class UserManager(BaseUserManager):
    # Django требует, чтобы пользовательские User определяли свой собственный класс Manager.
    # Унаследовав от BaseUserManager, мы получаем много кода, используемого Django для создания User.

    # Все, что нам нужно сделать, это переопределить функцию create_user, которую мы будем использовать для создания объектов User.
    def _create_user(self, username, email, password=None, **extra_fields):
        if not username:
            raise ValueError('Укзанное имя пользователя должно быть установлено')
        if not email:
            raise ValueError('Данный адрес электоронной почты должен быть установлен')
        email = self.normalize_email(email)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user
    
    # Создает и возвращает 'User' с адресом электронной почты, именем пользователя и паролем.
    def create_user(self, username, email, password=None, **extra_fields):
        extra_fields.setdefault('is_stuff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(username, email, password, **extra_fields)

    # Создает и возвращает пользователя с правами суперпользователя (администратора).
    def create_superuser(self, username, email, password, **extra_fields):
        extra_fields.setdefault('is_stuff', True)
        extra_fields.setdefault('is_superuser', True)
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Суперпользователь должен иметь is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Суперпользователь должен иметь is_superuser=True.')
        return self._create_user(username, email, password, **extra_fields)



class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(db_index = True, max_length=255, unique=True)
    email = models.EmailField(validators=[validators.validate_email], unique=True,blank=False)
    is_stuff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    USERNAME_FIELD = 'email' # свойство использует поле email для входа
    REQUIRED_FIELDS = ('username',)

    objects = UserManager() # класс UserManager, должен управлять объектами этого типа.

    def __str__(self):
        return self.username # возвращает строковое прдставление класса 'User'

    @property
    def token(self): 
        #Позволяет нам получить токен пользователя, вызвав user.token вместо user.generate_jwt_token().
        #Декоратор `@property` выше делает это возможным 'token' называется «динамическим свойством ».
        return self._generate_jwt_token()

    def _generate_jwt_token(self):
        # Создает веб-токен JSON, в котором хранится идентификатор этого пользователя и срок его действия составляет 60 дней в будущем.
        dt = datetime.now() + timedelta(days=60)
        token = jwt.encode({
            'id': self.pk,
            'exp': int(dt.strftime('%s'))
            }, settings.SECRET_KEY, algorithm='HS256')
        return token.decode('utf-8')
    
    def get_full_name(self):
        return self.username
    
    def get_short_name(self):
        return self.username

