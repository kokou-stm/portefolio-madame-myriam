"""Charge les photos de galerie librement réutilisables.

Ces trois images proviennent de Wikimedia Commons sous licence Creative
Commons : elles sont donc republiables ici, à condition de citer l'auteur et la
licence — ce que fait chaque champ `credit` / `licence`.

C'est l'ensemble des photos de Mme Dossou d'Almeida disponibles en ligne sous
une licence libre. Les photos de presse et du ministère, elles, restent
protégées et ne peuvent pas être ajoutées ici sans autorisation ; elles doivent
venir des archives du cabinet, via l'administration.
"""

from django.core.management.base import BaseCommand

from cv.models import Photo

PHOTOS = [
    {
        "fichier_statique": "img/galerie/evenement-entrepreneurs.jpg",
        "legende": "Journée du Jeune et de la Femme Entrepreneurs, à Lomé",
        "date": "",
        "credit": "Baname Laré",
        "licence": "CC BY 4.0",
        "source_url": "https://commons.wikimedia.org/wiki/File:Mariam_Dossou_et_M%C3%A9dissa_Sama.jpg",
    },
    {
        "fichier_statique": "img/galerie/portrait-gouvernement.jpg",
        "legende": "Portrait officiel, membre du Gouvernement du Togo",
        "date": "",
        "credit": "Fdimpact",
        "licence": "CC BY-SA 4.0",
        "source_url": "https://commons.wikimedia.org/wiki/File:Myriam_Dossou-d%27Almeida,_Ministre_du_d%C3%A9veloppement_%C3%A0_la_base,_de_la_jeunesse_et_de_l%E2%80%99emploi_des_jeunes_au_sein_du_nouveau_Gouvernement_du_Togo.png",
    },
    {
        "fichier_statique": "img/galerie/portrait-ministere.jpg",
        "legende": "Ministre du Développement à la Base, de la Jeunesse et de l'Emploi des Jeunes",
        "date": "",
        "credit": "Fdimpact",
        "licence": "CC BY-SA 4.0",
        "source_url": "https://commons.wikimedia.org/wiki/File:Myriam_Dossou-D%27Almeida,_Ministre_du_D%C3%A9veloppement_%C3%A0_la_Base,_de_la_Jeunesse_et_de_l%27Emploi_des_Jeunes_du_Togo.png",
    },
]


class Command(BaseCommand):
    help = "Charge les photos de galerie sous licence libre (Wikimedia Commons)."

    def handle(self, *args, **options):
        # Repérage par fichier livré : idempotent, ne touche pas aux photos
        # ajoutées depuis l'administration.
        for i, donnees in enumerate(PHOTOS):
            Photo.objects.update_or_create(
                fichier_statique=donnees["fichier_statique"],
                defaults={**donnees, "ordre": i},
            )

        self.stdout.write(
            self.style.SUCCESS(
                f"{Photo.objects.filter(fichier_statique__gt='').count()} photos "
                "libres chargées, toutes créditées. Les autres clichés (cabinet) "
                "se téléversent depuis l'administration."
            )
        )
