"""Charge des articles et tribunes documentés pour garnir la section Actualités."""

from django.core.management.base import BaseCommand
from django.utils import timezone
from django.utils.text import slugify

from cv.models import Article, Rubrique

ARTICLES = [
    {
        "titre": "Forum Régional sur l'Inclusion Financière et la Protection Sociale à Lomé",
        "rubrique_nom": "Événements",
        "a_la_une": True,
        "image_path": "img/evenements/conference-ministere.jpg",
        "image_legende": "Ouverture officielle du Forum Régional à Lomé",
        "chapo": (
            "À l'occasion de l'ouverture du Forum sur l'inclusion financière et la protection "
            "sociale en Afrique de l'Ouest, Myriam Dossou d'Almeida est intervenue pour "
            "rappeler l'urgence d'allier innovation assurantielle et solidarité nationale."
        ),
        "contenu": (
            "Lomé a abrité cette semaine les travaux du Forum Régional sur l'Inclusion "
            "Financière et la Protection Sociale.\n\n"
            "Intervenant en ouverture des panels ministériels, Myriam Dossou d'Almeida a "
            "rappelé les avancées majeures du Togo en matière de couverture maladie universelle "
            "et d'accès aux services financiers de base pour les populations vulnérables.\n\n"
            "### Allier solidarité nationale et viabilité technique\n\n"
            "S'appuyant sur douze années d'expérience à la direction générale de l'Institut "
            "National d'Assurance Maladie (INAM), elle a souligné que l'extension de la protection "
            "sociale repose sur deux piliers indissociables : une gouvernance technique "
            "rigoureuse et une volonté politique de solidarité nationale.\n\n"
            "« L'assurance maladie ne doit plus être perçue comme un luxe réservé aux salariés "
            "du secteur formel, mais comme un droit fondamental et un levier majeur de productivité "
            "économique pour nos pays », a-t-elle affirmé devant les délégations sous-régionales."
        ),
    },
    {
        "titre": "Discours à l'Assemblée nationale : Le cap de la solidarité et du développement local",
        "rubrique_nom": "Discours",
        "a_la_une": False,
        "image_path": "img/assemblee-nationale.jpg",
        "image_legende": "Palais de l'Assemblée nationale du Togo",
        "chapo": (
            "Prise de parole lors de l'ouverture de la session ordinaire de l'Assemblée nationale, "
            "réaffirmant l'engagement parlementaire au service des collectivités territoriales."
        ),
        "contenu": (
            "À l'ouverture de la session parlementaire, Myriam Dossou d'Almeida, Vice-Présidente "
            "de l'Assemblée nationale, s'est adressée à la représentation nationale pour rappeler "
            "l'importance d'adopter des lois en prise directe avec les réalités quotidiennes des citoyens.\n\n"
            "### Renforcer l'action de proximité et le rôle des collectivités\n\n"
            "Revenant sur son expérience au ministère du Développement à la Base et à la municipalité "
            "du Golfe 4, elle a insisté sur l'accompagnement des communes et le financement de "
            "l'entrepreneuriat des jeunes comme axes stratégiques de cohésion sociale."
        ),
    },
    {
        "titre": "L'assurance maladie universelle : Un modèle d'extension progressive en Afrique de l'Ouest",
        "rubrique_nom": "Tribunes",
        "a_la_une": False,
        "image_path": "img/evenements/inam-signature.jpg",
        "image_legende": "Signature de partenariat institutionnel pour l'AMU",
        "chapo": (
            "Analyse sur les défis de la généralisation de la couverture maladie et l'expérience "
            "togolaise d'intégration des secteurs formel et informel."
        ),
        "contenu": (
            "La généralisation de l'assurance maladie en Afrique subsaharienne est l'un des "
            "défis majeurs de notre décennie. Au Togo, le passage du régime obligatoire des agents "
            "publics (INAM) vers l'Assurance Maladie Universelle (AMU) offre des enseignements précieux.\n\n"
            "### Les enseignements de douze ans de gestion\n\n"
            "Pendant douze ans à la tête de l'INAM, nous avons démontré qu'il est possible de gérer "
            "un régime d'assurance maladie sans déficit technique ni financier, tout en élargissant "
            "progressivement les prestations et en préparant le terrain pour l'accueil de "
            "l'ensemble de la population."
        ),
    },
    {
        "titre": "Accompagnement de l'entrepreneuriat : Bilan des financements accordés aux jeunes",
        "rubrique_nom": "Actualités",
        "a_la_une": False,
        "image_path": "img/evenements/jeunesse-parole.jpg",
        "image_legende": "Cérémonie de remise d'attestations et d'équipements aux jeunes promoteurs",
        "chapo": (
            "Le Fonds d'Appui aux Initiatives Économiques des Jeunes (FAIEJ) a permis de financer "
            "1 852 nouveaux projets d'entreprise pour un montant de 2,68 milliards FCFA."
        ),
        "contenu": (
            "Le bilan d'étape des mécanismes d'appui à la jeunesse confirme la dynamique de "
            "création d'entreprises locales. Sous la tutelle du ministère du Développement à la Base "
            "et de la Jeunesse, le FAIEJ a franchi le cap des 1 852 projets financés en une année.\n\n"
            "Ces investissements ciblent prioritairement la transformation agricole, les services "
            "numériques et l'artisanat, permettant d'insérer durablement les jeunes bacheliers et "
            "diplômés dans le tissu économique national."
        ),
    },
    {
        "titre": "Distinction internationale à Bruxelles pour le développement local et la lutte contre la vulnérabilité",
        "rubrique_nom": "Presse",
        "a_la_une": False,
        "image_path": "img/evenements/honoris-causa.jpg",
        "image_legende": "Reconnaissance internationale décernée à Bruxelles",
        "chapo": (
            "Myriam Dossou d'Almeida a été honorée au sommet Africa Political Outlook pour "
            "son engagement constant en faveur de l'inclusion et du développement à la base."
        ),
        "contenu": (
            "Réunis à Bruxelles lors du sommet Africa Political Outlook, les dirigeants et décisionnaires "
            "africains ont salué le parcours de Myriam Dossou d'Almeida, ancienne Ministre et 6ᵉ "
            "Vice-Présidente de l'Assemblée nationale.\n\n"
            "Cette distinction récompense plus de quinze années d'actions de terrain, depuis la "
            "structuration des régimes de protection sociale jusqu'à la mise en œuvre de micro-projets "
            "communautaires dans toutes les préfectures du Togo."
        ),
    },
]


class Command(BaseCommand):
    help = "Charge des articles et tribunes dans la section Actualités."

    def handle(self, *args, **options):
        compteur = 0
        for i, donnees in enumerate(ARTICLES):
            rubrique, _ = Rubrique.objects.get_or_create(nom=donnees["rubrique_nom"])
            slug = slugify(donnees["titre"])

            article, created = Article.objects.update_or_create(
                slug=slug,
                defaults={
                    "titre": donnees["titre"],
                    "rubrique": rubrique,
                    "chapo": donnees["chapo"],
                    "contenu": donnees["contenu"],
                    "image": "",
                    "image_fichier": donnees["image_path"],
                    "image_legende": donnees["image_legende"],
                    "a_la_une": donnees["a_la_une"],
                    "statut": Article.PUBLIE,
                    "publie_le": timezone.now(),
                },
            )
            compteur += 1

        self.stdout.write(
            self.style.SUCCESS(f"{compteur} articles chargés avec succès.")
        )
