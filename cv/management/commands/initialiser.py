"""Amorçage du site au premier démarrage sur le serveur.

Exécutée à chaque déploiement, cette commande ne doit jamais écraser le travail
saisi depuis l'administration : elle ne charge le contenu du CV que si la base
est encore vide, et ne touche jamais à un compte existant.
"""

import os

from django.contrib.auth import get_user_model
from django.core.management import call_command
from django.core.management.base import BaseCommand

from cv.models import Profil


class Command(BaseCommand):
    help = "Prépare la base au premier démarrage (contenu initial, compte d'accès)."

    def handle(self, *args, **options):
        if Profil.objects.exists():
            self.stdout.write("Contenu déjà présent : chargement ignoré.")
        else:
            call_command("charger_cv")

        # Réalisations et galerie : commandes idempotentes (update_or_create),
        # rejouées à chaque déploiement pour propager les mises à jour de contenu
        # sans écraser les entrées créées depuis l'administration.
        call_command("charger_realisations")
        call_command("charger_galerie")
        call_command("charger_articles")
        call_command("charger_videos")

        identifiant = os.environ.get("DJANGO_ADMIN_USER")
        motdepasse = os.environ.get("DJANGO_ADMIN_PASSWORD")

        if not identifiant or not motdepasse:
            self.stdout.write("Aucun compte à créer (variables absentes).")
            return

        Utilisateur = get_user_model()
        if Utilisateur.objects.filter(username=identifiant).exists():
            # Le mot de passe a pu être changé depuis l'admin : on n'y touche pas.
            self.stdout.write(f"Le compte « {identifiant} » existe déjà.")
            return

        Utilisateur.objects.create_superuser(
            username=identifiant,
            email=os.environ.get("DJANGO_ADMIN_EMAIL", ""),
            password=motdepasse,
        )
        self.stdout.write(self.style.SUCCESS(f"Compte « {identifiant} » créé."))
