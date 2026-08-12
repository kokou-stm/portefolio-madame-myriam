from django.urls import path

from . import views

urlpatterns = [
    path("", views.accueil, name="accueil"),
    path("biographie/", views.biographie, name="biographie"),
    path("parcours/", views.parcours, name="parcours"),
    path("realisations/", views.realisations, name="realisations"),
    path("engagements/", views.engagements, name="engagements"),
    path("actualites/", views.publications, name="publications"),
    path("actualites/<slug:slug>/", views.article, name="article"),
    path("galerie/", views.galerie, name="galerie"),
    path("contact/", views.contact, name="contact"),
    # Espace administration sur-mesure
    path("connexion/", views.connexion_admin, name="connexion_admin"),
    path("deconnexion/", views.deconnexion_admin, name="deconnexion_admin"),
    path("espace-admin/", views.admin_dashboard, name="admin_dashboard"),
    path("espace-admin/publier/", views.admin_article_creer, name="admin_article_creer"),
    path("espace-admin/modifier/<int:pk>/", views.admin_article_modifier, name="admin_article_modifier"),
    path("espace-admin/supprimer/<int:pk>/", views.admin_article_supprimer, name="admin_article_supprimer"),
]

