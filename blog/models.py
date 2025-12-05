from django.db import models

class Post(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField(help_text='Armazene HTML aqui')
    posted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title