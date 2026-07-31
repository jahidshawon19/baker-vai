from django.db import models
from django.contrib.auth import get_user_model
from ckeditor.fields import RichTextField

User = get_user_model()


class Category(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='categories/', blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = 'Categories'
        ordering = ['name']

    def __str__(self):
        return self.name


class Essay(models.Model):
    class Status(models.TextChoices):
        DRAFT = 'draft', 'Draft'
        PUBLISHED = 'published', 'Published'
        ARCHIVED = 'archived', 'Archived'

    class Language(models.TextChoices):
        ENGLISH = 'en', 'English'
        BENGALI = 'bn', 'Bengali'

    title = models.CharField(max_length=300)
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL, null=True, blank=True, related_name='essays'
    )
    content = RichTextField()
    language = models.CharField(max_length=10, choices=Language.choices, default=Language.ENGLISH)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.DRAFT)
    featured = models.BooleanField(default=False)
    created_by = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True, related_name='essays'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    published_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        verbose_name_plural = 'Essays'
        ordering = ['-created_at']

    def __str__(self):
        return self.title


class EssayQuote(models.Model):
    essay = models.ForeignKey(Essay, on_delete=models.CASCADE, related_name='quotes')
    quote = models.TextField()

    def __str__(self):
        return f'Quote from "{self.essay.title}"'
