from PIL import Image
from datetime import datetime, timedelta
from django.contrib.auth.models import User
from django.db import models
from django.utils.text import slugify

# Create your models here.


class Category(models.Model):
    category = models.CharField(max_length=50)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.category

    def save(self, *args, **kwargs):
        self.slug = slugify(self.category)
        super(Category, self).save(*args, **kwargs)

    class Meta:
        verbose_name_plural = "Categories"


class Book(models.Model):
    title = models.CharField(max_length=300)
    slug = models.SlugField(unique=True)
    description = models.TextField(max_length=1000, default="About book")
    image = models.ImageField(
        default='default_book.png', upload_to='books_pics')
    author = models.CharField(max_length=100)
    book_amount = models.IntegerField()
    publish_date = models.DateField()
    number_of_pages = models.IntegerField()
    category = models.ForeignKey(Category, on_delete=models.PROTECT)
    last_rating = models.IntegerField(default=0)

    def __str__(self):
        return self.title

    @property
    def actual_rating(self):
        list_of_stars = []
        for star in range(self.last_rating):
            list_of_stars.append(star)
        return list_of_stars

    @property
    def calc_rating(self):
        ratings = BookReview.objects.filter(book=self)
        if ratings:
            result = 0
            for rating in ratings:
                result += rating.rating
            result = int(result / len(ratings))
            return result
        else:
            return 0

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(Book, self).save(*args, **kwargs)
        img = Image.open(self.image.path)

        if img.height > 200 or img.width > 200:
            output_size = (150, 300)
            img.thumbnail(output_size)
            img.save(self.image.path)


class BookRentHistory(models.Model):
    book = models.ForeignKey(
        Book, on_delete=models.PROTECT, editable=False)
    user = models.ForeignKey(
        User, on_delete=models.PROTECT, editable=False, related_name='books')
    rent_date = models.DateField(auto_now_add=True, editable=False)
    back_date = models.DateField(
        default=datetime.now()+timedelta(days=30))

    @property
    def how_many_days(self):
        return str(self.back_date - datetime.now().date())[:2]


class BookReview(models.Model):
    book = models.ForeignKey(
        Book, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    rating = models.IntegerField()


class BookComment(models.Model):
    book = models.ForeignKey(
        Book, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    text = models.CharField(max_length=300)


class InBoxMessages(models.Model):
    name = models.CharField(max_length=20)
    email = models.EmailField()
    message = models.TextField(max_length=500)

    def __str__(self):
        return f'Message from {self.name}'
