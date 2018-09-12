from django.contrib import admin
from .models import Discussione, Post, Sezione

# Personalizzazione dell'applicazione admin
class DiscussioneModelAdmin(admin.ModelAdmin):
    model = Discussione
    list_display = ['titolo', 'sezione_di_appartenenza', 'autore_discussione']
    search_fields =  ['titolo', 'autore_discussione']
    list_filter =['sezione_di_appartenenza', 'data_creazione']

class PostModelAdmin(admin.ModelAdmin):
    model = Post
    list_display = ['autore_post', 'discussione']
    search_fields = ['contenuto']
    list_filter = ['data_creazione', 'autore_post']

class SezioneModelAdmin(admin.ModelAdmin):
    model = Sezione
    list_display = ['nome_sezione', 'descrizione']


# Register your models here.
admin.site.register(Discussione, DiscussioneModelAdmin)
admin.site.register(Post, PostModelAdmin)
admin.site.register(Sezione, SezioneModelAdmin)
