from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.utils.text import slugify
from django.contrib.auth.models import User


class Genres(models.Model):
    genre_title = models.CharField(max_length=200, verbose_name="نام ژانر")
    slug = models.SlugField(verbose_name="اسلاگ", db_index=True, unique=True)

    def __str__(self):
        return self.genre_title

    def save(self, *args, **kwargs):
        self.slug = slugify(self.genre_title)
        super().save(*args, **kwargs)


class Platform(models.Model):
    title = models.CharField(max_length=200, verbose_name="نام پلتفرم")
    slug = models.SlugField(verbose_name="اسلاگ", db_index=True, unique=True)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.slug = slugify(self.genre_title)
        super().save(*args, **kwargs)


class Directors(models.Model):
    full_name = models.CharField(max_length=200, verbose_name="نام")
    slug = models.SlugField(verbose_name="اسلاگ", db_index=True, unique=True)
    prizes = models.TextField(verbose_name="جایزه ها")
    age = models.IntegerField(verbose_name="سن")
    born_place = models.CharField(max_length=200, verbose_name="مکان تولد")
    nationality = models.CharField(max_length=200, verbose_name="ملیت")
    bio = models.TextField(verbose_name="بیوگرافی")
    picture = models.ImageField(verbose_name="عکس", upload_to="images/directors")

    def __str__(self):
        return self.full_name

    def save(self, *args, **kwargs):
        self.slug = slugify(self.full_name)
        super().save(*args, **kwargs)


class Actors(models.Model):
    full_name = models.CharField(max_length=200, verbose_name="نام")
    slug = models.SlugField(verbose_name="اسلاگ", db_index=True, unique=True)
    prizes = models.TextField(verbose_name="جایزه ها")
    age = models.IntegerField(verbose_name="سن")
    born_place = models.CharField(max_length=200, verbose_name="مکان تولد")
    nationality = models.CharField(max_length=200, verbose_name="ملیت")
    bio = models.TextField(verbose_name="بیوگرافی")
    picture = models.ImageField(verbose_name="عکس", upload_to="images/actors")

    def __str__(self):
        return self.full_name

    def save(self, *args, **kwargs):
        self.slug = slugify(self.full_name)
        super().save(*args, **kwargs)


class Comments(models.Model):
    parent = models.ForeignKey(
        to="Comments",
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        verbose_name="نظری که به آن پاسخ داده شده است",
    )
    name = models.CharField(max_length=150, verbose_name="نام")
    created_date = models.DateTimeField(auto_now_add=True, verbose_name="تاریخ ثبت")
    edited_date = models.DateTimeField(auto_now_add=True, verbose_name="تاریخ ویرایش")
    is_reply = models.BooleanField(default=False, verbose_name="پاسخ است")
    is_been_replied = models.BooleanField(
        default=False, verbose_name="پاسخ داده شده است"
    )
    is_edited = models.BooleanField(default=False, verbose_name="ویرایش شده است")
    rating_number = models.IntegerField(
        verbose_name="نمره سایت",
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        default=0,
    )
    text = models.TextField(verbose_name="متن نظر")

    def __str__(self):
        return f"{str(self.user)}, {self.created_date}"

    def fill_previous_text(self, id):
        comment = Comments.objects.get(id=id)
        comment.previous_text += f"edited date: {self.edited_date}\r {self.text}\r"
        comment.save()


class Countries(models.Model):
    country_name = models.CharField(max_length=200, verbose_name="نام کشور")
    slug = models.SlugField(verbose_name="اسلاگ", db_index=True, unique=True)

    def __str__(self):
        return self.country_name

    def save(self, *args, **kwargs):
        self.slug = slugify(self.country_name)
        super().save(*args, **kwargs)


class AgeLimits(models.Model):
    title = models.CharField(max_length=200, verbose_name="عنوان")
    min_age = models.IntegerField(verbose_name="حداقل سن")

    def __str__(self):
        return self.title


class MoviesInfo(models.Model):
    name = models.CharField(max_length=200, verbose_name="نام فیلم")
    slug = models.SlugField(verbose_name="اسلاگ", db_index=True, unique=True)
    genre = models.ManyToManyField(to=Genres, verbose_name="ژانر")
    directors = models.ManyToManyField(
        to=Directors, verbose_name="کارگردان"
    )
    actors = models.ManyToManyField(to=Actors, verbose_name="بازیگران")
    created_date = models.CharField(
        max_length=4,
        verbose_name="سال ساخت",
        validators=[MinValueValidator(4), MaxValueValidator(4)],
    )
    country = models.ManyToManyField(to=Countries, verbose_name="کشور")
    age_limit = models.ForeignKey(
        to=AgeLimits, verbose_name="محدویدت سنی", on_delete=models.CASCADE
    )
    platform = models.ForeignKey(
        Platform,
        on_delete=models.CASCADE,
        verbose_name="پلتفرم پخش",
        related_name="movie_platform",
    )
    summery = models.TextField(verbose_name="خلاصه")

    def __str__(self):
        return f"{self.type} {self.name} {self.created_date}"

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class SeriesInfo(models.Model):
    STATUS = (
        ("np", "درحال پخش"),
        ("fi", "تمام شده"),
        ("ca", "لغو شده"),
    )

    name = models.CharField(max_length=200, verbose_name="نام سریال")
    slug = models.SlugField(verbose_name="اسلاگ", unique=True)
    genre = models.ManyToManyField(to=Genres, verbose_name="ژانر")
    status = models.CharField(
        verbose_name="وضیعت پخش", choices=STATUS, max_length=200
    )
    directors = models.ManyToManyField(
        to=Directors, verbose_name="کارگردان", blank=True
    )
    platform = models.CharField(max_length=200, verbose_name="کانال پخش کننده")
    actors = models.ManyToManyField(to=Actors, verbose_name="بازیگران")
    created_date = models.CharField(
        max_length=4,
        verbose_name="سال ساخت",
        validators=[MinValueValidator(4), MaxValueValidator(4)],
    )
    country = models.ManyToManyField(to=Countries, verbose_name="کشور")
    age_limit = models.ForeignKey(
        to=AgeLimits, verbose_name="محدویدت سنی", on_delete=models.CASCADE
    )
    summery = models.TextField(verbose_name="خلاصه")
    platform = models.ForeignKey(
        Platform,
        on_delete=models.CASCADE,
        verbose_name="پلتفرم پخش",
        related_name="series_platform",
    )

    def __str__(self):
        return f"{self.type} {self.name} {self.created_date}"

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super().save(*args, **kwargs)

