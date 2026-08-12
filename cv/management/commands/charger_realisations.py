"""Charge les réalisations documentées publiquement.

Chaque entrée provient d'une publication de presse ou d'une page
institutionnelle, citée dans `source_url`. Rien n'est extrapolé : lorsqu'une
source ne donne pas de chiffre, aucun chiffre n'est affiché.

Photos : les clichés d'événements rattachés ici (`photo_fichier`) proviennent
des archives du cabinet, fournies par la responsable du site et publiées sous
sa responsabilité ; ils sont crédités « Cabinet / Ministère ». Les autres
clichés se téléversent depuis l'administration.
"""

from django.core.management.base import BaseCommand

from cv.models import Realisation

REALISATIONS = [
    {
        "titre": "Extension de l'assurance maladie à toute la population",
        "domaine": Realisation.PROTECTION,
        "annee": "2022-2024",
        "chiffre": "",
        "chiffre_libelle": "",
        "description": (
            "En juillet 2022, les attributions de l'Institut National d'Assurance "
            "Maladie sont élargies à la gestion de l'Assurance Maladie Universelle. "
            "L'institut, qu'elle dirige, devient l'organisme chargé de mettre en "
            "œuvre le passage d'un régime réservé aux agents publics à une "
            "couverture ouverte à l'ensemble des Togolais."
        ),
        "source_url": "https://www.togofirst.com/fr/sante/0707-10287-togo-les-attributions-de-l-inam-elargies-a-la-gestion-de-l-assurance-maladie-universelle",
        "source_nom": "Togo First",
    },
    {
        "titre": "Douze années à la direction de l'assurance maladie",
        "domaine": Realisation.PROTECTION,
        "annee": "2012-2024",
        "chiffre": "12 ans",
        "chiffre_libelle": "à la tête de l'INAM, de sa montée en charge à l'AMU",
        "description": (
            "Elle dirige l'Institut National d'Assurance Maladie jusqu'en octobre "
            "2024, date à laquelle elle passe la main pour rejoindre l'Assemblée "
            "nationale. À son départ, elle retient une transformation : permettre "
            "aux familles de se soigner sans se ruiner."
        ),
        "photo_fichier": "img/evenements/inam-signature.jpg",
        "photo_legende": "À l'INAM, cap vers l'Assurance Maladie Universelle",
        "photo_credit": "INAM / Cabinet",
        "source_url": "https://togobreakingnews.info/inam-myriam-dossou-reconnaissante/",
        "source_nom": "Togo Breaking News",
    },
    {
        "titre": "Lancement du projet « Jeunes Bacheliers Engagés »",
        "domaine": Realisation.JEUNESSE,
        "annee": "2022",
        "chiffre": "",
        "chiffre_libelle": "",
        "description": (
            "Le 9 septembre 2022, elle lance à Lomé le projet Jeunes Bacheliers "
            "Engagés, porté par l'Agence Nationale du Volontariat au Togo. Le "
            "dispositif propose aux nouveaux bacheliers une formation courte et un "
            "accompagnement, pour éviter la rupture entre le lycée et la suite."
        ),
        "photo_fichier": "img/evenements/jeunesse-parole.jpg",
        "photo_legende": "Prise de parole devant la jeunesse, à Lomé",
        "photo_credit": "Ministère du Développement à la base",
        "source_url": "https://togoanvt.org/lanvt-lance-officiellement-le-projet-jeunes-bacheliers-engages-jbe/",
        "source_nom": "Agence Nationale du Volontariat au Togo",
    },
    {
        "titre": "Financement des initiatives économiques des jeunes",
        "domaine": Realisation.JEUNESSE,
        "annee": "2023",
        "chiffre": "1 852 projets",
        "chiffre_libelle": "financés pour 2,68 milliards FCFA en 2023",
        "description": (
            "Sous sa tutelle ministérielle, le Fonds d'Appui aux Initiatives "
            "Économiques des Jeunes finance 1 852 nouveaux projets portés par des "
            "jeunes en 2023, pour un montant de 2,68 milliards de francs CFA."
        ),
        "photo_fichier": "img/evenements/conference-ministere.jpg",
        "photo_legende": "Conférence ministérielle sur l'appui aux jeunes",
        "photo_credit": "Ministère du Développement à la base",
        "source_url": "https://www.agenceecofin.com/entreprendre/2801-115634-togo-en-2023-le-faiej-a-permis-de-financer-1-852-nouveaux-projets-a-hauteur-de-2-68-milliards-fcfa",
        "source_nom": "Agence Ecofin",
    },
    {
        "titre": "Suivi de terrain des projets de développement local",
        "domaine": Realisation.TERRITOIRES,
        "annee": "2020-2024",
        "chiffre": "",
        "chiffre_libelle": "",
        "description": (
            "Elle se rend dans les préfectures pour constater l'avancement des "
            "micro-projets financés par le Fonds d'Appui aux Collectivités "
            "Territoriales — infrastructures marchandes, bâtiments scolaires — et "
            "échanger directement avec les populations bénéficiaires."
        ),
        "photo_fichier": "img/evenements/terrain.jpg",
        "photo_legende": "Supervision des réalisations sur le terrain",
        "photo_credit": "Ministère du Développement à la base",
        "source_url": "https://devbase.gouv.tg/myriam-dossou-dalmeida-visite-les-realisations-de-lanadeb-dans-la-prefecture-de-yoto/",
        "source_nom": "Ministère du Développement à la Base",
    },
    {
        "titre": "Marraine de la Jeune Chambre Internationale",
        "domaine": Realisation.JEUNESSE,
        "annee": "2022",
        "chiffre": "",
        "chiffre_libelle": "",
        "description": (
            "Elle accepte le parrainage de la Jeune Chambre Internationale du Togo "
            "pour le mandat 2022, en appui à l'engagement citoyen et au leadership "
            "des jeunes actifs."
        ),
        "source_url": "https://devbase.gouv.tg/myriam-dossou-dalmeida-marraine-de-la-jci-pour-le-mandat-2022/",
        "source_nom": "Ministère du Développement à la Base",
    },
    {
        "titre": "Élection à la Vice-Présidence de l'Assemblée nationale",
        "domaine": Realisation.PARLEMENT,
        "annee": "Depuis juin 2024",
        "chiffre": "",
        "chiffre_libelle": "",
        "description": (
            "Le 14 juin 2024, elle est élue 6ᵉ Vice-Présidente de l'Assemblée "
            "nationale du Togo, au sein du bureau présidé par Kodjo Adedze, à "
            "l'ouverture de la nouvelle législature."
        ),
        "photo_fichier": "img/assemblee-nationale.jpg",
        "photo_legende": "Assemblée nationale du Togo, Lomé",
        "source_url": "https://assemblee-nationale.tg/les-instances/bureau/",
        "source_nom": "Assemblée nationale togolaise",
    },
    {
        "titre": "Docteur Honoris Causa",
        "domaine": Realisation.RECONNAISSANCE,
        "annee": "2024",
        "chiffre": "",
        "chiffre_libelle": "",
        "description": (
            "Le 13 novembre 2024 à Abidjan, elle est élevée au rang de Docteur "
            "Honoris Causa par le Centre de Valorisation Professionnelle de Tunis "
            "et l'Institut Africain de Recherche Pluridisciplinaire Appliquée, "
            "pour sa contribution au développement du Togo."
        ),
        "photo_fichier": "img/evenements/honoris-causa.jpg",
        "photo_legende": "Cérémonie de Docteur Honoris Causa, Abidjan, novembre 2024",
        "photo_credit": "Cabinet",
        "source_url": "https://gapola.tg/abidjan-myriam-dossou-dalmeida-elevee-au-rang-de-dr-honoris-causas/",
        "source_nom": "GAPOLA",
    },
    {
        "titre": "Distinction pour le leadership africain",
        "domaine": Realisation.RECONNAISSANCE,
        "annee": "2025",
        "chiffre": "",
        "chiffre_libelle": "",
        "description": (
            "Elle est distinguée à Bruxelles pour son action en matière de "
            "développement local et de lutte contre la vulnérabilité."
        ),
        "source_url": "https://togobreakingnews.info/myriam-dossou-dalmeida-distinguee-bruxelles/",
        "source_nom": "Togo Breaking News",
    },
]


class Command(BaseCommand):
    help = "Charge les réalisations documentées, avec leurs sources."

    def handle(self, *args, **options):
        # Repérage par titre : relancer la commande met à jour sans dupliquer,
        # et ne touche pas aux entrées ajoutées depuis l'administration.
        for i, donnees in enumerate(REALISATIONS):
            Realisation.objects.update_or_create(
                titre=donnees["titre"], defaults={**donnees, "ordre": i}
            )

        self.stdout.write(
            self.style.SUCCESS(
                f"{Realisation.objects.count()} réalisations en base, "
                f"toutes sourcées, photos du cabinet rattachées."
            )
        )
