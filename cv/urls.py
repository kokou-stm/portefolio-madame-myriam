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
    # Gestion des vidéos YouTube
    path("espace-admin/video/ajouter/", views.admin_video_creer, name="admin_video_creer"),
    path("espace-admin/video/modifier/<int:pk>/", views.admin_video_modifier, name="admin_video_modifier"),
    path("espace-admin/video/supprimer/<int:pk>/", views.admin_video_supprimer, name="admin_video_supprimer"),
    # Gestion des photos de la galerie
    path("espace-admin/photo/ajouter/", views.admin_photo_creer, name="admin_photo_creer"),
    path("espace-admin/photo/modifier/<int:pk>/", views.admin_photo_modifier, name="admin_photo_modifier"),
    path("espace-admin/photo/supprimer/<int:pk>/", views.admin_photo_supprimer, name="admin_photo_supprimer"),
]

