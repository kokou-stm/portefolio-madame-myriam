"""Charge les réalisations concrètes et résultats mesurables."""

from django.core.management.base import BaseCommand
from cv.models import Realisation

REALISATIONS = [
    {
        "titre": "Extension de l'assurance maladie à toute la population",
        "domaine": Realisation.PROTECTION,
        "annee": "2022-2024",
        "chiffre": "AMU",
        "chiffre_libelle": "Élargissement des attributions de l'INAM à l'Assurance Maladie Universelle",
        "description": (
            "En juillet 2022, les attributions de l'Institut National d'Assurance "
            "Maladie (INAM) sont officiellement élargies à la gestion de l'Assurance Maladie Universelle. "
            "L'institut devient l'organisme moteur pour la couverture maladie de l'ensemble de la population togolaise."
        ),
        "photo_fichier": "img/evenements/extension-amu.png",
        "photo_legende": "Déploiement et extension de l'Assurance Maladie Universelle (AMU)",
        "photo_credit": "INAM / Cabinet",
        "source_url": "https://www.togofirst.com/fr/sante/0707-10287-togo-les-attributions-de-l-inam-elargies-a-la-gestion-de-l-assurance-maladie-universelle",
        "source_nom": "Togo First",
    },
    {
        "titre": "12 années à la direction de l'INAM",
        "domaine": Realisation.PROTECTION,
        "annee": "2012-2024",
        "chiffre": "12 ans",
        "chiffre_libelle": "à la direction générale de l'INAM sans déficit technique ni financier",
        "description": (
            "Direction opérationnelle et stratégique de l'INAM pendant 12 ans. "
            "Sous sa conduite, l'organisme a assuré la prise en charge de plus de 500 000 assurés "
            "du secteur public tout en maintenant un équilibre financier rigoureux et sans aucun déficit."
        ),
        "photo_fichier": "img/evenements/inam-signature.jpg",
        "photo_legende": "À la direction générale de l'INAM",
        "photo_credit": "INAM / Cabinet",
        "source_url": "https://togobreakingnews.info/inam-myriam-dossou-reconnaissante/",
        "source_nom": "Togo Breaking News",
    },
    {
        "titre": "Lancement du projet « Jeunes Bacheliers Engagés »",
        "domaine": Realisation.JEUNESSE,
        "annee": "2022",
        "chiffre": "ANVT",
        "chiffre_libelle": "Projet national de volontariat et d'accompagnement civique",
        "description": (
            "Lancement officiel du projet « Jeunes Bacheliers Engagés », porté par l'Agence "
            "Nationale du Volontariat au Togo (ANVT). Le dispositif offre aux nouveaux bacheliers "
            "une formation d'immersion citoyenne et un accompagnement vers l'enseignement supérieur."
        ),
        "photo_fichier": "img/evenements/jeunesse-parole.jpg",
        "photo_legende": "Prise de parole devant la jeunesse lors du lancement",
        "photo_credit": "Ministère du Développement à la base",
        "source_url": "https://togoanvt.org/lanvt-lance-officiellement-le-projet-jeunes-bacheliers-engages-jbe/",
        "source_nom": "Agence Nationale du Volontariat au Togo",
    },
    {
        "titre": "Financement de 1 852 projets de jeunes pour 2,68 milliards FCFA",
        "domaine": Realisation.JEUNESSE,
        "annee": "2023",
        "chiffre": "1 852 projets",
        "chiffre_libelle": "financés pour un montant de 2,68 milliards FCFA via le FAIEJ",
        "description": (
            "Sous sa tutelle ministérielle, le Fonds d'Appui aux Initiatives Économiques "
            "des Jeunes (FAIEJ) a permis de financer 1 852 nouveaux projets d'entreprises "
            "portés par des jeunes promoteurs sur l'ensemble du territoire national."
        ),
        "photo_fichier": "img/evenements/conference-ministere.jpg",
        "photo_legende": "Remise officielle d'attestations et financement aux jeunes entrepreneurs",
        "photo_credit": "Ministère du Développement à la base",
        "source_url": "https://www.agenceecofin.com/entreprendre/2801-115634-togo-en-2023-le-faiej-a-permis-de-financer-1-852-nouveaux-projets-a-hauteur-de-2-68-milliards-fcfa",
        "source_nom": "Agence Ecofin",
    },
    {
        "titre": "Suivi de terrain des projets de développement local (FACT)",
        "domaine": Realisation.TERRITOIRES,
        "annee": "2020-2024",
        "chiffre": "FACT",
        "chiffre_libelle": "Supervision des micro-projets dans les collectivités territoriales",
        "description": (
            "Missions de suivi de proximité dans les préfectures pour évaluer l'avancement des "
            "projets financés par le Fonds d'Appui aux Collectivités Territoriales : "
            "infrastructures marchandes, centres communautaires et bâtiments scolaires."
        ),
        "photo_fichier": "img/evenements/terrain.jpg",
        "photo_legende": "Inspection de terrain et échanges avec les acteurs locaux",
        "photo_credit": "Ministère du Développement à la base",
        "source_url": "https://devbase.gouv.tg/myriam-dossou-dalmeida-visite-les-realisations-de-lanadeb-dans-la-prefecture-de-yoto/",
        "source_nom": "Ministère du Développement à la Base",
    },
    {
        "titre": "Élection à la 6ᵉ Vice-Présidence de l'Assemblée nationale",
        "domaine": Realisation.PARLEMENT,
        "annee": "Depuis juin 2024",
        "chiffre": "6ᵉ VP",
        "chiffre_libelle": "Membre du Bureau de la représentation nationale du Togo",
        "description": (
            "Élection le 14 juin 2024 comme 6ᵉ Vice-Présidente de l'Assemblée nationale du Togo "
            "pour participer à la direction des travaux parlementaires et au rayonnement institutionnel."
        ),
        "photo_fichier": "img/assemblee-nationale.jpg",
        "photo_legende": "Palais de l'Assemblée nationale du Togo",
        "photo_credit": "Assemblée nationale",
        "source_url": "https://assemblee-nationale.tg/les-instances/bureau/",
        "source_nom": "Assemblée nationale togolaise",
    },
]


class Command(BaseCommand):
    help = "Charge les 6 réalisations concrètes du parcours."

    def handle(self, *args, **options):
        Realisation.objects.all().delete()
        for i, donnees in enumerate(REALISATIONS):
            Realisation.objects.create(**donnees, ordre=i)

        self.stdout.write(
            self.style.SUCCESS(
                f"{Realisation.objects.count()} réalisations chargées avec succès."
            )
        )
