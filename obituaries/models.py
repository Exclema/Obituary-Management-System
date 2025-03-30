from django.db import models
from django.utils.text import slugify
from django.utils import timezone

class Obituary(models.Model):
    name = models.CharField(max_length=100)
    date_of_birth = models.DateField()
    date_of_death = models.DateField()
    content = models.TextField()
    author = models.CharField(max_length=100)
    submission_date = models.DateTimeField(default=timezone.now)
    slug = models.SlugField(max_length=255, unique=True, blank=True)
    
    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(f"{self.name}-{self.date_of_birth}-{self.date_of_death}")
            self.slug = base_slug
            counter = 1
            while Obituary.objects.filter(slug=self.slug).exists():
                self.slug = f"{base_slug}-{counter}"
                counter += 1
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.name} ({self.date_of_birth} - {self.date_of_death})"
