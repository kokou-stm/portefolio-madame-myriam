"""Service des médias téléversés, avec prise en charge des requêtes partielles.

Safari et iOS n'affichent une vidéo que si le serveur répond « 206 Partial
Content » aux requêtes `Range`. La vue django.views.static.serve n'envoie que
le fichier entier : sur iPhone, le lecteur resterait vide.
"""

import mimetypes
import os
import re

from django.conf import settings
from django.core.exceptions import SuspiciousFileOperation
from django.http import Http404, HttpResponse, StreamingHttpResponse
from django.utils._os import safe_join
from django.views.static import serve

PLAGE = re.compile(r"bytes=(\d*)-(\d*)$")
TAILLE_BLOC = 64 * 1024


def _lire(chemin, debut, longueur):
    with open(chemin, "rb") as f:
        f.seek(debut)
        reste = longueur
        while reste > 0:
            bloc = f.read(min(TAILLE_BLOC, reste))
            if not bloc:
                break
            reste -= len(bloc)
            yield bloc


def servir_media(request, path):
    plage = PLAGE.match(request.headers.get("Range", "").strip())
    if not plage or plage.groups() == ("", ""):
        reponse = serve(request, path, document_root=settings.MEDIA_ROOT)
        # Annonce au navigateur qu'il peut demander des morceaux du fichier.
        reponse["Accept-Ranges"] = "bytes"
        return reponse

    try:
        chemin = safe_join(settings.MEDIA_ROOT, path)
    except SuspiciousFileOperation:
        raise Http404
    if not os.path.isfile(chemin):
        raise Http404

    taille = os.path.getsize(chemin)
    debut_txt, fin_txt = plage.groups()
    if debut_txt == "":
        # « bytes=-N » : les N derniers octets.
        debut, fin = max(taille - int(fin_txt), 0), taille - 1
    else:
        debut = int(debut_txt)
        fin = min(int(fin_txt), taille - 1) if fin_txt else taille - 1

    if debut >= taille or debut > fin:
        reponse = HttpResponse(status=416)
        reponse["Content-Range"] = f"bytes */{taille}"
        return reponse

    longueur = fin - debut + 1
    type_mime = mimetypes.guess_type(chemin)[0] or "application/octet-stream"
    reponse = StreamingHttpResponse(
        _lire(chemin, debut, longueur), status=206, content_type=type_mime
    )
    reponse["Content-Length"] = str(longueur)
    reponse["Content-Range"] = f"bytes {debut}-{fin}/{taille}"
    reponse["Accept-Ranges"] = "bytes"
    return reponse
