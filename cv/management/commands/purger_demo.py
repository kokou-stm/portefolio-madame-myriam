"""Supprime les publications de démonstration.

Les trois articles chargés à la mise en place du site sont des textes fictifs,
rédigés uniquement pour valider la mise en page. Ils ne reflètent aucune prise
de position réelle et doivent être supprimés avant toute mise en ligne.
"""

from django.core.management.base import BaseCommand

from cv.models import Article

TITRES_DEMO = [
    "Vers une couverture santé universelle : ce que nous avons appris à l'INAM",
    "Réunion des Présidents des Parlements des États africains atlantiques",
    "Jeunesse et emploi : sortir de la logique de l'assistance",
]


class Command(BaseCommand):
    help = "Supprime les publications de démonstration."

    def add_arguments(self, parser):
        parser.add_argument(
            "--rubriques",
            action="store_true",
            help="Supprime également les rubriques de démonstration devenues vides.",
        )

    def handle(self, *args, **options):
        nombre, _ = Article.objects.filter(titre__in=TITRES_DEMO).delete()

        if options["rubriques"]:
            from cv.models import Rubrique

            vides = Rubrique.objects.filter(articles__isnull=True)
            noms = list(vides.values_list("nom", flat=True))
            vides.delete()
            if noms:
                self.stdout.write(f"Rubriques vides supprimées : {', '.join(noms)}.")

        if nombre:
            self.stdout.write(
                self.style.SUCCESS("Publications de démonstration supprimées.")
            )
        else:
            self.stdout.write("Aucune publication de démonstration trouvée.")
