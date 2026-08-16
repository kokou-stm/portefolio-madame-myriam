"""Charge des articles et tribunes documentés pour garnir la section Actualités."""

from datetime import datetime, timezone as dt_timezone
from django.core.management.base import BaseCommand
from django.utils import timezone
from django.utils.text import slugify

from cv.models import Article, Rubrique

ARTICLES = [
    {
        "titre": "Journée de l'Arbre 2026 : Reboisement citoyen et engagement pour le développement durable",
        "rubrique_nom": "Événements",
        "a_la_une": True,
        "publie_le": datetime(2026, 6, 1, 10, 0, tzinfo=dt_timezone.utc),
        "image_path": "img/evenements/journee-arbre-arrosage.jpeg",
        "image_legende": "Action de reboisement et d'arrosage des plants lors de la Journée de l'Arbre 2026",
        "chapo": (
            "À l’occasion de la Journée de l’Arbre (1er juin 2026), Myriam Dossou d'Almeida s'est jointe "
            "aux collectivités locales, aux jeunes volontaires et aux populations pour une grande campagne "
            "de reboisement citoyen et de sensibilisation écologique."
        ),
        "contenu": (
            "Le 1er juin marque chaque année au Togo la **Journée de l'Arbre**, une tradition citoyenne "
            "majeure dédiée à la préservation de notre environnement et à la lutte contre les effets du "
            "changement climatique.\n\n"
            "### Un geste vertueux pour les générations futures\n\n"
            "Entourée d'élus locaux, de jeunes volontaires de l'ANVT et de représentants d'associations "
            "environnementales, Myriam Dossou d'Almeida a participé à la mise en terre et à l'arrosage "
            "de plusieurs centaines de jeunes plants d'espèces locales et ombragées.\n\n"
            "« Planter un arbre, c’est poser un acte d'amour envers l’avenir. C’est protéger nos sols, "
            "préserver la biodiversité de nos collectivités et offrir un cadre de vie sain à nos enfants. »\n\n"
            "### Mobiliser la jeunesse autour des enjeux écologiques\n\n"
            "Au-delà de la mise en terre des plants, cette journée a été l'occasion d'échanger avec la jeunesse "
            "sur l'importance cruciale du suivi et de l'entretien des espaces reboisés.\n\n"
            "En cohérence avec les politiques de développement à la base et la vision nationale, cette initiative "
            "s'inscrit dans l'ambition collective de renforcer la couverture forestière et la résilience écologique "
            "de nos communes."
        ),
    },
    {
        "titre": "Diaspora, capital et développement africain : de Solidar’ Santé à un partenariat durable",
        "rubrique_nom": "Tribunes",
        "a_la_une": False,
        "publie_le": datetime(2026, 2, 10, 10, 0, tzinfo=dt_timezone.utc),
        "image_path": "img/evenements/diaspora-developpement.png",
        "image_legende": "Myriam Dossou-D'Almeida — Tribune sur la diaspora, le capital et le développement africain",
        "chapo": (
            "Au-delà des transferts financiers de solidarité, Myriam Dossou d'Almeida plaide pour une "
            "véritable stratégie publique de mobilisation des compétences de la diaspora, de l'épargne "
            "productive et du transfert d'innovation vers le continent."
        ),
        "contenu": (
            "Au cours de ma carrière, dans la conduite de politiques publiques, la gestion d’une institution "
            "de protection sociale ou l’accompagnement d’initiatives de développement, j’ai eu à expérimenter, "
            "à plusieurs reprises, la volonté sincère de nos frères et sœurs de la diaspora de contribuer "
            "au progrès de leur pays d’origine.\n\n"
            "Certains proposent leurs services. D’autres souhaitent partager une expertise acquise dans des "
            "environnements professionnels exigeants. D’autres encore mobilisent leurs réseaux, offrent du matériel, "
            "accompagnent des équipes, conseillent des entrepreneurs ou tentent d’introduire des solutions "
            "technologiques nouvelles.\n\n"
            "Il y a, derrière ces démarches, une forme de générosité qui ne dit pas toujours son nom. Une volonté "
            "de transmettre, de rendre utile une expérience acquise ailleurs et de maintenir un lien concret avec le continent.\n\n"
            "Cette énergie est précieuse. Pourtant, elle ne produit pas toujours les résultats espérés. "
            "Non pas parce que la bonne volonté ferait défaut, mais parce qu’elle se heurte souvent à une "
            "appréciation imparfaite des réalités locales, à des différences de vécu, de parcours, d’objectifs ou de méthodes.\n\n"
            "### La diaspora apporte bien plus que des transferts financiers\n\n"
            "Le rôle économique de la diaspora africaine est souvent mesuré à travers les transferts de fonds envoyés "
            "aux familles. Ces ressources financent l’alimentation, les soins, l’éducation, le logement, les cérémonies "
            "familiales et de nombreuses activités génératrices de revenus. Elles constituent un puissant mécanisme "
            "de solidarité et, dans plusieurs pays, un véritable amortisseur social.\n\n"
            "Selon la Banque mondiale, les transferts officiellement enregistrés vers l’Afrique subsaharienne étaient "
            "estimés à environ **56 milliards de dollars en 2024**. À l’échelle des pays à revenu faible ou intermédiaire, "
            "ces flux ont dépassé les investissements directs étrangers et l’aide publique au développement réunis.\n\n"
            "Mais réduire la diaspora à ces seuls transferts serait une erreur. Son capital est aussi humain, intellectuel, "
            "technologique, professionnel et relationnel.\n\n"
            "> « L’innovation pertinente n’est pas celle qui reproduit mécaniquement un modèle extérieur. C’est celle qui associe l’expérience internationale à l’intelligence du terrain. »\n\n"
            "À titre d’illustration, on peut citer plusieurs initiatives récentes portées par la diaspora africaine "
            "et togolaise. La rencontre récente de médecins de la diaspora togolaise, par exemple, a permis de renforcer "
            "les échanges avec les praticiens locaux autour de la formation continue, de la télémédecine et de l’amélioration "
            "de la prise en charge de certaines pathologies. De même, le projet d’assurance maladie [« Solidar’ Santé »](http://news.alome.com/h/70829.html) initié par la diaspora togolaise en Belgique témoigne d’une volonté concrète de contribuer à la protection sociale au pays, en s’appuyant sur des mécanismes solidaires et des partenariats structurés.\n\n"
            "### Le retour se prépare comme un projet de vie\n\n"
            "Le retour au pays est souvent envisagé comme la conséquence naturelle de l’attachement aux origines. "
            "Or il constitue une transition personnelle, familiale, professionnelle et économique majeure. Il doit être préparé.\n\n"
            "Il serait donc utile que les États développent de véritables parcours d’accompagnement : information avant le retour, "
            "guichet unique, orientation professionnelle, reconnaissance des qualifications, assistance à la création d’entreprise, "
            "facilitation administrative et mise en relation avec les institutions.\n\n"
            "Le retour définitif ne doit toutefois pas constituer la seule forme d’engagement. Les mobilités circulaires, "
            "les missions temporaires, l’enseignement à distance, le mentorat, le conseil stratégique et les collaborations "
            "hybrides permettent également de mettre les compétences de la diaspora au service du continent.\n\n"
            "### De la solidarité au capital productif\n\n"
            "À côté des flux de solidarité familiale, une partie de l’épargne volontaire de la diaspora pourrait être "
            "orientée vers des investissements productifs : entreprises, agriculture, logement, santé, énergie, infrastructures, "
            "économie numérique, industrie et adaptation climatique.\n\n"
            "Pour y parvenir, il ne suffit pas d’invoquer le patriotisme. Un investissement n’est pas un don. La diaspora "
            "doit pouvoir connaître le porteur du projet, l’utilisation prévue des fonds, les risques, les garanties, la "
            "gouvernance, les perspectives de rentabilité et les conditions de sortie.\n\n"
            "> « La confiance ne se décrète pas. Elle se construit par la transparence, la compétence et le respect des engagements. »\n\n"
            "### Construire une politique publique de mobilisation des compétences\n\n"
            "Nous avons besoin d’une architecture qui permette d’identifier les compétences de la diaspora et de les "
            "mettre en relation avec les besoins réels de nos pays. Cette politique pourrait notamment prévoir :\n\n"
            "- Un **registre volontaire** des compétences et expertises ;\n"
            "- Un **portefeuille public de projets** structurés et évalués ;\n"
            "- Des **missions d’expertise** de courte, moyenne ou longue durée ;\n"
            "- Des **binômes associant systématiquement** experts de la diaspora et professionnels locaux ;\n"
            "- Des **mécanismes de transfert de compétences** et de formation des équipes ;\n"
            "- Un **accompagnement des projets de retour** et d’entrepreneuriat ;\n"
            "- Des **outils financiers sécurisés** et transparents ;\n"
            "- Une **évaluation indépendante** des projets réalisés.\n\n"
            "### Organiser la rencontre des deux Afrique\n\n"
            "La diaspora n’est pas extérieure à l’Afrique. Elle en est une extension humaine, économique, intellectuelle "
            "et culturelle. Notre défi n’est pas seulement de mobiliser davantage la diaspora. Il est de mieux organiser sa contribution.\n\n"
            "« L’Afrique ne manque pas de talents. Une partie de ces talents vit sur le continent ; une autre vit ailleurs. "
            "Le développement exige que ces deux expériences cessent de s’observer à distance et apprennent à construire ensemble. "
            "Lorsque l’expertise internationale rencontre l’intelligence du terrain, lorsque la générosité s’appuie sur une méthode "
            "et lorsque la confiance est protégée par des institutions solides, la diaspora cesse d’être seulement une ressource "
            "extérieure. Elle devient pleinement coproductrice de la transformation africaine. »"
        ),
    },
    {
        "titre": "Forum Régional sur l'Inclusion Financière et la Protection Sociale à Lomé",
        "rubrique_nom": "Événements",
        "a_la_une": False,
        "publie_le": datetime(2026, 5, 15, 9, 30, tzinfo=dt_timezone.utc),
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
        "titre": "Retour sur la distinction Africa Political Outlook 2025 à Bruxelles",
        "rubrique_nom": "Presse",
        "a_la_une": False,
        "publie_le": datetime(2025, 2, 12, 16, 0, tzinfo=dt_timezone.utc),
        "image_path": "img/evenements/honoris-causa.jpg",
        "image_legende": "Reconnaissance internationale décernée au sommet Africa Political Outlook 2025 à Bruxelles",
        "chapo": (
            "En février 2025 à Bruxelles, Myriam Dossou-D'Almeida a été honorée du Prix Leadership, Governance "
            "& Impact au sommet Africa Political Outlook pour son engagement constant en faveur de l'inclusion "
            "et du développement à la base."
        ),
        "contenu": (
            "Réunis à Bruxelles lors de l'édition 2025 du sommet Africa Political Outlook, les dirigeants et "
            "décideurs internationaux ont salué le parcours de Myriam Dossou-D'Almeida, ancienne Ministre et "
            "6ᵉ Vice-Présidente de l'Assemblée nationale du Togo.\n\n"
            "Cette distinction — le Prix Leadership, Governance & Impact 2025 — a récompensé son action continue "
            "en faveur du développement local, de la structuration des régimes de protection sociale et de la "
            "lutte contre la vulnérabilité dans les territoires."
        ),
    },
    {
        "titre": "Intervention à l'Assemblée nationale : Le cap de la cohésion sociale et du développement local",
        "rubrique_nom": "Discours",
        "a_la_une": False,
        "publie_le": datetime(2024, 6, 14, 11, 0, tzinfo=dt_timezone.utc),
        "image_path": "img/assemblee-nationale.jpg",
        "image_legende": "Palais de l'Assemblée nationale du Togo, Lomé",
        "chapo": (
            "Déclaration officielle prononcée le 14 juin 2024 lors de la séance inaugurale de la "
            "nouvelle législature de l'Assemblée nationale du Togo, réaffirmant l'engagement "
            "parlementaire au service des collectivités et de la jeunesse."
        ),
        "contenu": (
            "Le 14 juin 2024, lors de la séance inaugurale marquant le début de la nouvelle législature, "
            "Myriam Dossou-D'Almeida, élue 6ᵉ Vice-Présidente de l'Assemblée nationale du Togo, "
            "s'est adressée à la représentation nationale pour poser les jalons de l'action parlementaire.\n\n"
            "### Renforcer l'action de proximité et le rôle des collectivités\n\n"
            "S'appuyant sur son expérience au ministère du Développement à la Base et à la municipalité "
            "du Golfe 4, elle a insisted sur l'accompagnement des communes, le financement de "
            "l'entrepreneuriat des jeunes et la consolidation de la cohésion sociale comme axes "
            "stratégiques majeurs."
        ),
    },
    {
        "titre": "Accompagnement de l'entrepreneuriat : Bilan des financements accordés aux jeunes",
        "rubrique_nom": "Actualités",
        "a_la_une": False,
        "publie_le": datetime(2024, 1, 28, 10, 0, tzinfo=dt_timezone.utc),
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
        "titre": "L'assurance maladie universelle : Un modèle d'extension progressive en Afrique de l'Ouest",
        "rubrique_nom": "Tribunes",
        "a_la_une": False,
        "publie_le": datetime(2023, 11, 20, 14, 0, tzinfo=dt_timezone.utc),
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
]


class Command(BaseCommand):
    help = "Charge des articles et tribunes dans la section Actualités."

    def handle(self, *args, **options):
        Article.objects.all().delete()
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
                    "publie_le": donnees.get("publie_le", timezone.now()),
                },
            )
            compteur += 1

        self.stdout.write(
            self.style.SUCCESS(f"{compteur} articles chargés avec succès avec leurs dates historiques.")
        )
