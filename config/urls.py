"""Routage principal du site."""

from django.contrib import admin
from django.urls import include, path

from cv.medias import servir_media

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("cv.urls")),
    # WhiteNoise indexe les fichiers au démarrage : il ne verrait pas un
    # portrait téléversé depuis l'admin avant le redémarrage suivant. Les
    # médias passent donc par Django, avec lecture partielle pour que les
    # vidéos se lisent aussi sur iPhone et Safari (voir cv/medias.py).
    path("media/<path:path>", servir_media, name="media"),
]

handler404 = "cv.views.page_not_found"
handler500 = "cv.views.server_error"
