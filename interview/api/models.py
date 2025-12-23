from django.db import models
from django.contrib.auth.models import User


class BaseModel(models.Model):
    """
    Abstract base model with common fields for all models
    """
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    created_by = models.ForeignKey(
        User, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name='%(class)s_created',
        help_text="User who created this record"
    )
    updated_by = models.ForeignKey(
        User, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name='%(class)s_updated',
        help_text="User who last updated this record"
    )

    class Meta:
        abstract = True  # This makes it an abstract base class


class Topic(BaseModel):
    """
    Topic/Category for interview questions
    """
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    slug = models.SlugField(max_length=100, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']


class Question(BaseModel):
    """
    Interview question model
    """
    DIFFICULTY_CHOICES = [
        ('easy', 'Easy'),
        ('medium', 'Medium'),
        ('hard', 'Hard'),
    ]
    
    text = models.TextField(help_text="The interview question")
    topic = models.ForeignKey(
        Topic, 
        on_delete=models.CASCADE, 
        related_name='questions',
        help_text="Topic/Category of the question"
    )
    difficulty = models.CharField(
        max_length=10, 
        choices=DIFFICULTY_CHOICES, 
        default='medium'
    )
    expected_answer = models.TextField(blank=True, help_text="Expected or sample answer")
    tags = models.CharField(max_length=200, blank=True, help_text="Comma-separated tags")

    def __str__(self):
        return f"{self.topic.name} - {self.text[:50]}"

    class Meta:
        ordering = ['-created_at']
