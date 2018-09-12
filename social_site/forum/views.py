from django.contrib.auth.decorators import login_required
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.http import HttpResponseRedirect, HttpResponseBadRequest
from django.shortcuts import render, get_object_or_404
from django.views.generic.edit import CreateView, DeleteView
from django.urls import reverse

from .forms import DiscussioneModelForm, PostModelForm
from .models import Discussione, Post, Sezione
from .mixins import StaffMixin
# Create your views here.

class CreaSezione(StaffMixin, CreateView):
    model = Sezione
    fields = "__all__"
    template_name = "forum/crea_sezione.html"
    success_url = "/"

def visualizzaSezione(request, pk):
    sezione = get_object_or_404(Sezione, pk=pk)
    discussioni_sezione = Discussione.objects.filter(sezione_di_appartenenza=sezione).order_by("-data_creazione")
    context = { "sezione": sezione , "discussioni": discussioni_sezione}
    return render(request, "forum/singola_sezione.html", context)

@login_required
def creaDiscussione(request, pk):
    sezione = get_object_or_404(Sezione, pk=pk)
    if request.method == "POST":
        form = DiscussioneModelForm(request.POST)
        if form.is_valid:
            discussione = form.save(commit=False)
            discussione.sezione_di_appartenenza = sezione
            discussione.autore_discussione = request.user
            discussione.save()
            primo_post = Post.objects.create(
                discussione = discussione,
                autore_post = request.user,
                contenuto = form.cleaned_data["contenuto"]
            )
            return HttpResponseRedirect(discussione.get_absolute_url())
    else:
        form = DiscussioneModelForm()
    context = {"form": form, "sezione": sezione}
    return render(request, "forum/crea_discussione.html", context)

def visualizzaDiscussione(request, pk):
    discussione = get_object_or_404(Discussione, pk=pk)
    posts_discussione = Post.objects.filter(discussione=discussione)
    # aggiungiamo la gestione di paginazione dei risultati
    paginator = Paginator(posts_discussione, 5)

    page = request.GET.get("pagina")
    posts_page = paginator.get_page(page)

    form_risposta = PostModelForm
    context = {"discussione": discussione,
               "lista_posts": posts_page,
               "form_risposta": form_risposta }
    return render(request, "forum/singola_discussione.html", context)

@login_required
def aggiungiRisposta(request, pk):
    discussione = get_object_or_404(Discussione, pk=pk)
    if request.method == "POST":
        form = PostModelForm(request.POST)
        if form.is_valid:
            form.save(commit=False)
            form.instance.discussione = discussione
            form.instance.autore_post = request.user
            form.save()
            url_discussione = reverse("discussione_view", kwargs={"pk": pk})
            # appena inserito un messaggio di risposta si viene mandati all'ultima pagina
            # dei messaggi per poter vedere il proprio messaggio
            pagine_in_discussione = discussione.get_n_pages()
            if pagine_in_discussione > 1 :
                return HttpResponseRedirect(url_discussione + "?pagina=" + str(pagine_in_discussione))
            else :
                return HttpResponseRedirect(url_discussione)
    else:
        return HttpResponseBadRequest()

class CancellaPost(DeleteView):
    """ utilizza in automatico il template : post_confirm_delete.html """
    model = Post
    success_url = "/"

    # Filtra il quesryset in modo che contenga solo post dell'autore_post
    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(autore_post_id=self.request.user.id)
