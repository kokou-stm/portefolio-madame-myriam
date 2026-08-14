"""Routage principal du site."""

from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from django.views.static import serve

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("cv.urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
else:
    # WhiteNoise indexe les fichiers au démarrage : il ne verrait pas un
    # portrait téléversé depuis l'admin avant le redémarrage suivant. Les
    # médias passent donc par Django. Acceptable ici — quelques images, un
    # trafic de portfolio — mais à basculer vers un stockage objet si le site
    # venait à servir beaucoup de fichiers.
    urlpatterns += [
        path(
            "media/<path:path>",
            serve,
            {"document_root": settings.MEDIA_ROOT},
            name="media",
        ),
    ]

handler404 = "cv.views.page_not_found"
handler500 = "cv.views.server_error"
