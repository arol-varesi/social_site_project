from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
import math

# Create your models here.

class Sezione(models.Model):
    """
    le sezioni dividono il sito per categorie di discussione
    ciascuna sezione contiene svariate  Discussioni
    create dagli amministratori del sito
    """
    nome_sezione = models.CharField(max_length = 80)
    descrizione = models.CharField(max_length = 150, blank=True, null=True)
    logo_sezione = models.ImageField(blank=True, null=True)

    def __str__(self):
        return self.nome_sezione

    def get_absolute_url(self):
        return reverse("sezione_view", kwargs={"pk": self.pk})

    def get_last_discussions(self):
        return Discussione.objects.filter(sezione_di_appartenenza=self).order_by("-data_creazione")[:2]

    def get_number_of_posts_in_section(self):
        return Post.objects.filter(discussione__sezione_di_appartenenza=self).count()

    class Meta:
        verbose_name = "sezione"
        verbose_name_plural = "sezioni"


class Discussione(models.Model):
    titolo = models.CharField(max_length=120)
    data_creazione = models.DateTimeField(auto_now_add=True)
    autore_discussione = models.ForeignKey(User, on_delete=models.CASCADE, related_name="discussioni")
    sezione_di_appartenenza = models.ForeignKey(Sezione, on_delete=models.CASCADE)

    def __str__(self):
        return self.titolo

    def get_absolute_url(self):
        return reverse("discussione_view", kwargs={"pk": self.pk})

    def get_n_pages(self):
        return math.ceil(self.post_set.count() / 5) 

    class Meta:
        verbose_name = "discussione"
        verbose_name_plural = "discussioni"

class Post(models.Model):
    autore_post = models.ForeignKey(User, on_delete=models.CASCADE, related_name="posts")
    contenuto = models.TextField()
    data_creazione = models.DateTimeField(auto_now_add=True)
    discussione = models.ForeignKey(Discussione, on_delete=models.CASCADE)

    def __str__(self):
        return self.autore_post.username

    class Meta:
        verbose_name = "post"
        verbose_name_plural = "posts"
