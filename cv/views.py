from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth import authenticate, login, logout
from django.core.paginator import Paginator
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse

from .forms import ArticleForm, ConnexionForm, MessageForm, PhotoForm, VideoForm
from .models import (
    Article,
    Chiffre,
    Competence,
    Distinction,
    Experience,
    Formation,
    Message,
    Photo,
    Profil,
    Realisation,
    Rubrique,
    Video,
)


def _profil():
    return Profil.objects.first()


def accueil(request):
    return render(
        request,
        "cv/accueil.html",
        {
            "profil": _profil(),
            "chiffres": Chiffre.objects.all(),
            "competences": Competence.objects.all(),
            "experiences": Experience.objects.all()[:3],
            "articles": Article.publies.select_related("rubrique")[:3],
        },
    )


def biographie(request):
    return render(
        request,
        "cv/biographie.html",
        {
            "profil": _profil(),
            "chiffres": Chiffre.objects.all(),
        },
    )


def parcours(request):
    return render(
        request,
        "cv/parcours.html",
        {
            "profil": _profil(),
            "experiences": Experience.objects.all(),
            "formations": Formation.objects.all(),
            "distinctions": Distinction.objects.all(),
            "competences": Competence.objects.all(),
        },
    )


def realisations(request):
    toutes = Realisation.objects.all()

    domaine = request.GET.get("domaine")
    domaines_valides = dict(Realisation.DOMAINES)
    if domaine not in domaines_valides:
        domaine = None

    return render(
        request,
        "cv/realisations.html",
        {
            "profil": _profil(),
            "realisations": toutes.filter(domaine=domaine) if domaine else toutes,
            # Seuls les domaines effectivement renseignés apparaissent en filtre.
            "domaines": [
                (cle, libelle)
                for cle, libelle in Realisation.DOMAINES
                if toutes.filter(domaine=cle).exists()
            ],
            "domaine_actif": domaine,
        },
    )


def engagements(request):
    return render(
        request,
        "cv/engagements.html",
        {
            "profil": _profil(),
            "distinctions": Distinction.objects.all(),
        },
    )


def galerie(request):
    thematique_slug = request.GET.get("thematique")
    videos = Video.objects.all()
    if thematique_slug:
        videos = videos.filter(thematique=thematique_slug)

    shorts = [v for v in videos if v.est_short]
    videos_longues = [v for v in videos if not v.est_short]

    return render(
        request,
        "cv/galerie.html",
        {
            "profil": _profil(),
            "photos": Photo.objects.all(),
            "videos": videos,
            "shorts": shorts,
            "videos_longues": videos_longues,
            "thematiques": Video.THEMATIQUES,
            "thematique_active": thematique_slug,
        },
    )


def publications(request):
    articles = Article.publies.select_related("rubrique")

    rubrique = None
    slug = request.GET.get("rubrique")
    if slug:
        rubrique = get_object_or_404(Rubrique, slug=slug)
        articles = articles.filter(rubrique=rubrique)

    une = None
    if not rubrique:
        une = articles.filter(a_la_une=True).first()
        if une:
            articles = articles.exclude(pk=une.pk)

    page = Paginator(articles, 9).get_page(request.GET.get("page"))

    return render(
        request,
        "cv/publications.html",
        {
            "profil": _profil(),
            "une": une,
            "page": page,
            "rubriques": Rubrique.objects.filter(articles__in=Article.publies.all())
            .distinct(),
            "rubrique_active": rubrique,
        },
    )


def article(request, slug):
    article = get_object_or_404(
        Article.objects.select_related("rubrique"), slug=slug
    )
    # Un brouillon reste consultable par son autrice, pour se relire avant parution.
    if not article.est_visible and not request.user.is_staff:
        raise Http404

    autres = Article.publies.exclude(pk=article.pk)
    if article.rubrique:
        meme_rubrique = autres.filter(rubrique=article.rubrique)
        autres = meme_rubrique if meme_rubrique.exists() else autres

    return render(
        request,
        "cv/article.html",
        {"profil": _profil(), "article": article, "autres": autres[:3]},
    )


def contact(request):
    if request.method == "POST":
        form = MessageForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(
                request,
                "Votre message a bien été transmis. Une réponse vous sera adressée "
                "dans les meilleurs délais.",
            )
            return redirect(reverse("contact"))
    else:
        form = MessageForm()

    return render(request, "cv/contact.html", {"profil": _profil(), "form": form})


def connexion_admin(request):
    if request.user.is_authenticated and request.user.is_staff:
        return redirect("admin_dashboard")

    if request.method == "POST":
        form = ConnexionForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            user = authenticate(request, username=username, password=password)
            if user is not None and user.is_staff:
                login(request, user)
                messages.success(request, f"Bienvenue {user.first_name or user.username} dans votre espace d'administration.")
                return redirect("admin_dashboard")
            else:
                messages.error(request, "Identifiants incorrects ou accès non autorisé.")
    else:
        form = ConnexionForm()

    return render(request, "cv/connexion.html", {"profil": _profil(), "form": form})


def deconnexion_admin(request):
    logout(request)
    messages.info(request, "Vous avez été déconnectée avec succès.")
    return redirect("accueil")


@staff_member_required(login_url="connexion_admin")
def admin_dashboard(request):
    articles = Article.objects.select_related("rubrique").all()
    messages_recus = Message.objects.all().order_by("-envoye_le")[:10]
    videos = Video.objects.all()
    photos = Photo.objects.all()

    nb_total = articles.count()
    nb_publies = articles.filter(statut=Article.PUBLIE).count()
    nb_brouillons = articles.filter(statut=Article.BROUILLON).count()
    nb_messages = Message.objects.count()

    return render(
        request,
        "cv/admin_dashboard.html",
        {
            "profil": _profil(),
            "articles": articles,
            "messages_recus": messages_recus,
            "videos": videos,
            "photos": photos,
            "nb_total": nb_total,
            "nb_publies": nb_publies,
            "nb_brouillons": nb_brouillons,
            "nb_messages": nb_messages,
        },
    )


@staff_member_required(login_url="connexion_admin")
def admin_article_creer(request):
    if request.method == "POST":
        form = ArticleForm(request.POST, request.FILES)
        if form.is_valid():
            article = form.save()
            messages.success(
                request,
                f"La publication « {article.titre} » a été enregistrée "
                f"({'Publiée' if article.statut == Article.PUBLIE else 'Brouillon'}).",
            )
            return redirect("admin_dashboard")
    else:
        form = ArticleForm()

    return render(
        request,
        "cv/admin_article_form.html",
        {
            "profil": _profil(),
            "form": form,
            "titre_page": "Nouvel événement / publication",
            "bouton_action": "Publier / Enregistrer",
        },
    )


@staff_member_required(login_url="connexion_admin")
def admin_article_modifier(request, pk):
    article = get_object_or_404(Article, pk=pk)
    if request.method == "POST":
        form = ArticleForm(request.POST, request.FILES, instance=article)
        if form.is_valid():
            article = form.save()
            messages.success(request, f"La publication « {article.titre} » a bien été mise à jour.")
            return redirect("admin_dashboard")
    else:
        form = ArticleForm(instance=article)

    return render(
        request,
        "cv/admin_article_form.html",
        {
            "profil": _profil(),
            "form": form,
            "article": article,
            "titre_page": f"Modifier : {article.titre}",
            "bouton_action": "Enregistrer les modifications",
        },
    )


@staff_member_required(login_url="connexion_admin")
def admin_article_supprimer(request, pk):
    article = get_object_or_404(Article, pk=pk)
    if request.method == "POST":
        titre = article.titre
        article.delete()
        messages.success(request, f"La publication « {titre} » a été supprimée.")
    return redirect("admin_dashboard")


# --- Gestion des Vidéos YouTube (Espace Admin) ---

@staff_member_required(login_url="connexion_admin")
def admin_video_creer(request):
    if request.method == "POST":
        form = VideoForm(request.POST)
        if form.is_valid():
            video = form.save()
            messages.success(request, f"La vidéo YouTube « {video.titre} » a été ajoutée à la galerie.")
            return redirect("admin_dashboard")
    else:
        form = VideoForm()

    return render(
        request,
        "cv/admin_video_form.html",
        {
            "profil": _profil(),
            "form": form,
            "titre_page": "Ajouter une vidéo YouTube à la galerie",
            "bouton_action": "Ajouter la vidéo",
        },
    )


@staff_member_required(login_url="connexion_admin")
def admin_video_modifier(request, pk):
    video = get_object_or_404(Video, pk=pk)
    if request.method == "POST":
        form = VideoForm(request.POST, instance=video)
        if form.is_valid():
            video = form.save()
            messages.success(request, f"La vidéo « {video.titre} » a bien été mise à jour.")
            return redirect("admin_dashboard")
    else:
        form = VideoForm(instance=video)

    return render(
        request,
        "cv/admin_video_form.html",
        {
            "profil": _profil(),
            "form": form,
            "video": video,
            "titre_page": f"Modifier la vidéo : {video.titre}",
            "bouton_action": "Enregistrer les modifications",
        },
    )


@staff_member_required(login_url="connexion_admin")
def admin_video_supprimer(request, pk):
    video = get_object_or_404(Video, pk=pk)
    if request.method == "POST":
        titre = video.titre
        video.delete()
        messages.success(request, f"La vidéo « {titre} » a été retirée de la galerie.")
    return redirect("admin_dashboard")


# --- Gestion des Photos de Galerie (Espace Admin) ---

@staff_member_required(login_url="connexion_admin")
def admin_photo_creer(request):
    if request.method == "POST":
        form = PhotoForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "La photo a été ajoutée à la galerie.")
            return redirect("admin_dashboard")
    else:
        form = PhotoForm()

    return render(
        request,
        "cv/admin_photo_form.html",
        {
            "profil": _profil(),
            "form": form,
            "titre_page": "Téléverser / Ajouter une photo",
            "bouton_action": "Ajouter la photo",
        },
    )


@staff_member_required(login_url="connexion_admin")
def admin_photo_modifier(request, pk):
    photo = get_object_or_404(Photo, pk=pk)
    if request.method == "POST":
        form = PhotoForm(request.POST, request.FILES, instance=photo)
        if form.is_valid():
            form.save()
            messages.success(request, "La photo a bien été mise à jour.")
            return redirect("admin_dashboard")
    else:
        form = PhotoForm(instance=photo)

    return render(
        request,
        "cv/admin_photo_form.html",
        {
            "profil": _profil(),
            "form": form,
            "photo": photo,
            "titre_page": "Modifier la photo de galerie",
            "bouton_action": "Enregistrer les modifications",
        },
    )


@staff_member_required(login_url="connexion_admin")
def admin_photo_supprimer(request, pk):
    photo = get_object_or_404(Photo, pk=pk)
    if request.method == "POST":
        photo.delete()
        messages.success(request, "La photo a été retirée de la galerie.")
    return redirect("admin_dashboard")


def page_not_found(request, exception=None):
    """Page d'erreur 404 personnalisée."""
    return render(request, "404.html", {"profil": _profil()}, status=404)


def server_error(request):
    """Page d'erreur 500 personnalisée."""
    return render(request, "500.html", {"profil": _profil()}, status=500)


