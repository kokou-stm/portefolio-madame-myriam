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

        # Amorçage de la Whitelist 2FA et des comptes autorisés
        from cv.models import EmailAutorise
        emails_defaut = [
            ("myriam.dossou@yahoo.fr", "Myriam DOSSOU-D’ALMEIDA"),
            ("sekpona30@gmail.com", "Sekpona KOKOU"),
            ("fabricesassou@gmail.com", "Fabrice SASSOU"),
            ("contact@myriamdossou.com", "Cabinet Officiel"),
        ]
        for em_str, nom in emails_defaut:
            EmailAutorise.objects.get_or_create(email=em_str, defaults={"nom_utilisateur": nom})
            u = Utilisateur.objects.filter(email__iexact=em_str).first()
            if not u:
                u = Utilisateur.objects.filter(username__iexact=em_str).first()
            if not u:
                Utilisateur.objects.create_user(
                    username=em_str,
                    email=em_str,
                    password="Myd#urHt%H^PAtEuzF!G",
                    is_staff=True,
                    first_name=nom.split()[0],
                    last_name=" ".join(nom.split()[1:]) if len(nom.split()) > 1 else "",
                )
            else:
                u.is_staff = True
                u.save()

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
