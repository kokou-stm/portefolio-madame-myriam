from .models import Profil


def profil(request):
    """Fournit le profil au contexte de tous les templates."""
    return {"profil": Profil.objects.first()}
