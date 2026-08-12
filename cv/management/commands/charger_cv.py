"""Charge le contenu initial du site à partir du CV.

Idempotent : relancer la commande met le contenu à jour sans créer de doublons.
Les coordonnées privées (adresse du domicile, téléphones personnels) sont
volontairement laissées vides — à renseigner depuis l'administration si besoin.
"""

from django.core.management.base import BaseCommand

from cv.models import Chiffre, Competence, Distinction, Experience, Formation, Profil, Rubrique

PROFIL = {
    "nom": "Myriam Dossou d'Almeida",
    "titre": "Experte en assurances et protection sociale",
    "sous_titre": "Vice-Présidente de l'Assemblée nationale du Togo",
    "accroche": (
        "Trente années d'expertise en assurance et en réassurance, mises au service "
        "de la protection sociale et de la réduction des vulnérabilités."
    ),
    "biographie": (
        "Forte d'une expérience diversifiée et solide en assurance, enrichie par des "
        "formations continues tout au long de sa carrière, Myriam Dossou d'Almeida a "
        "choisi de mettre son expertise technique au service du social.\n\n"
        "Son parcours l'a conduite de la souscription en assurance IARD au sein du "
        "Groupement Togolais d'Assurances jusqu'à la direction de la réassurance du "
        "groupe NSIA pour dix-huit filiales réparties dans onze pays d'Afrique "
        "occidentale et centrale, en passant par Paris, chez AXA puis Marsh.\n\n"
        "De 2012 à 2024, elle dirige l'Institut National d'Assurance Maladie du Togo, "
        "où elle met en place et pilote un régime obligatoire couvrant plus de "
        "500 000 assurés, sans déficit technique ni financier. Elle y développe des "
        "dispositifs d'extension progressive vers l'assurance maladie universelle : "
        "gratuité de la prise en charge des femmes enceintes, universités du "
        "troisième âge, hôpitaux mère-enfant, projet pilote pour les personnes "
        "vulnérables de Timbou.\n\n"
        "La passion du service public et la volonté de contribuer aux stratégies de "
        "développement économique durable se traduisent par un engagement politique "
        "actif : conseillère municipale du Golfe 4, puis Ministre du Développement à "
        "la Base, de la Jeunesse et de l'Emploi des Jeunes de 2020 à 2024, et depuis "
        "juin 2024 Vice-Présidente de l'Assemblée nationale du Togo."
    ),
    "photo_credit": (
        "Portrait : Fdimpact, via Wikimedia Commons, licence CC BY-SA 4.0."
    ),
    "ville": "Lomé",
    "pays": "Togo",
    "email": "",
    "telephone": "",
    "twitter": "https://x.com/DossouMyriam",
    "facebook": "https://www.facebook.com/myriamdossoudalmeida",
    "instagram": "https://www.instagram.com/myriamdossoudalmeida/",
    "tiktok": "https://www.tiktok.com/@myriamdossou",
}

CHIFFRES = [
    ("500 000+", "Assurés bénéficiaires du régime obligatoire d'assurance maladie"),
    ("12 ans", "À la direction générale de l'Institut National d'Assurance Maladie"),
    ("18", "Filiales de réassurance coordonnées dans 11 pays africains"),
    ("30 ans", "D'expérience en assurance, réassurance et protection sociale"),
]

COMPETENCES = [
    ("Assurance et réassurance", "Souscription, traités, placement facultatif, équilibre technique des régimes.", "bouclier"),
    ("Protection sociale", "Conception et pilotage de régimes d'assurance maladie à couverture nationale.", "coeur"),
    ("Management stratégique", "Direction générale, gouvernance et développement du leadership des équipes.", "courbe"),
    ("Politiques publiques", "Conduite de politiques de développement à la base et d'emploi des jeunes.", "balance"),
    ("Développement communautaire", "Filets sociaux, volontariat, réduction des vulnérabilités.", "personnes"),
    ("Financements alternatifs de la santé", "Mobilisation de partenaires techniques et financiers internationaux.", "globe"),
    ("Pilotage de projets informatiques", "Conduite de systèmes d'information d'envergure institutionnelle.", "ecran"),
]

EXPERIENCES = [
    {
        "poste": "Vice-Présidente de l'Assemblée nationale",
        "organisation": "Assemblée nationale du Togo",
        "lieu": "Lomé",
        "periode": "Depuis juin 2024",
        "en_cours": True,
        "description": (
            "Participation à la direction des travaux parlementaires\n"
            "Représentation de l'institution dans les instances interparlementaires africaines"
        ),
    },
    {
        "poste": "Ministre du Développement à la Base, de la Jeunesse et de l'Emploi des Jeunes",
        "organisation": "Gouvernement de la République togolaise",
        "lieu": "Lomé",
        "periode": "Octobre 2020 — Août 2024",
        "description": (
            "Mise en œuvre de programmes de filets sociaux et de développement communautaire\n"
            "Coordination de projets de développement et d'emploi des jeunes\n"
            "Implémentation d'un programme de transformation intégré des jeunes\n"
            "Projet conjoint de déploiement de jeunes volontaires agents de santé communautaire\n"
            "Stratégie de lutte contre la consommation de produits psychotropes chez les jeunes"
        ),
    },
    {
        "poste": "Directrice Générale",
        "organisation": "Institut National d'Assurance Maladie (INAM)",
        "lieu": "Lomé",
        "periode": "Février 2012 — Octobre 2024",
        "description": (
            "Mise en place et gestion d'un régime obligatoire d'assurance maladie de plus de 500 000 assurés\n"
            "Pilotage de l'équilibre technique du régime, sans déficit technique ni financier\n"
            "Développement des systèmes de management et de leadership\n"
            "Initiatives d'appui à la santé des bénéficiaires et approche participative de prévention\n"
            "Stratégies d'extension progressive vers l'assurance maladie universelle : gratuité de la prise "
            "en charge des femmes enceintes, universités du 3ᵉ âge, hôpitaux mère-enfant, projet pilote "
            "pour les personnes vulnérables de Timbou\n"
            "Plaidoyer pour la mise en place d'un paquet de soins essentiels\n"
            "Mobilisation de partenaires : Socieux-UE, PNUD"
        ),
    },
    {
        "poste": "Directrice de la Réassurance Groupe",
        "organisation": "NSIA-Participations Holding S.A.",
        "lieu": "Abidjan",
        "periode": "Août 2006 — Avril 2012",
        "description": (
            "Coordination des opérations de réassurance du groupe en Afrique occidentale et centrale\n"
            "Création du Département Réassurance et du Pool de Réassurance\n"
            "Optimisation et négociation des traités de réassurance de 18 filiales dans 11 pays\n"
            "Placement des réassurances facultatives"
        ),
    },
    {
        "poste": "Gestionnaire technique",
        "organisation": "Marsh",
        "lieu": "France",
        "periode": "Mai — Septembre 2006",
        "description": "Mise en place de polices locales DIC-DIL pour des clients internationaux",
    },
    {
        "poste": "Gestionnaire de compte — Cessions",
        "organisation": "AXA",
        "lieu": "France",
        "periode": "Septembre — Décembre 2005",
        "description": "Élaboration de plans de réassurance et renouvellement des traités",
    },
    {
        "poste": "Responsable Commerciale",
        "organisation": "Groupement Togolais d'Assurances — Compagnie Africaine d'Assurance",
        "lieu": "Lomé",
        "periode": "Août 2004 — Septembre 2005",
        "description": (
            "Développement d'un réseau de commerciaux indépendants\n"
            "Mise en place d'une dynamique de croissance du portefeuille"
        ),
    },
    {
        "poste": "Adjointe au Directeur d'agence",
        "organisation": "GTA — C2A",
        "lieu": "Lomé",
        "periode": "Mai 2002 — Novembre 2003",
        "description": (
            "Appui à la coordination des activités et des équipes front office de l'agence principale\n"
            "Supervision de la souscription et suivi de portefeuille"
        ),
    },
    {
        "poste": "Souscripteur polyvalent — gestionnaire technico-commerciale",
        "organisation": "Groupement Togolais d'Assurances (GTA) IARD",
        "lieu": "Lomé",
        "periode": "Avril 1990 — Avril 2002",
        "description": "Souscription et gestion technico-commerciale de portefeuille IARD",
    },
]

FORMATIONS = [
    ("2023", "Programme de leadership ministériel", "Harvard University", ""),
    ("2012", "Programme de formation en protection sociale", "Organisation Internationale du Travail — Turin", ""),
    ("2005", "MBA — Management de l'Entreprise d'Assurances", "ENASS, École Nationale d'Assurance — Paris", ""),
    ("2005", "Diplôme du Cycle International", "ENASS — Paris", ""),
    ("2004", "Diplôme de l'Institut Africain d'Assurances", "Tunis", "Mention Très bien"),
    ("1995-1996", "DT-A, Diplôme de Technicien d'Assurances", "Institut International d'Assurances — Lomé", ""),
    ("1988-1990", "École Supérieure des Techniques de Gestion (ESTEG)", "Lomé, Togo", ""),
    ("1985-1988", "Faculté de pharmacie", "Reims, Champagne-Ardenne", ""),
    ("1985", "Baccalauréat série C", "", ""),
]

DISTINCTIONS = [
    {
        "intitule": "Marraine de la Jeune Chambre Internationale du Togo",
        "detail": (
            "Accompagnement et parrainage officiel du mandat 2022 de la JCI Togo, "
            "en appui à l'engagement citoyen, à l'entrepreneuriat et au leadership des jeunes actifs."
        ),
        "annee": "2022",
        "photo_fichier": "img/evenements/jeunesse-parole.jpg",
        "photo_legende": "Parrainage officiel et intervention devant la Jeune Chambre Internationale du Togo",
        "photo_credit": "Cabinet / Ministère",
    },
    {
        "intitule": "Docteur Honoris Causa",
        "detail": (
            "Décerné en novembre 2024 à Abidjan par le Centre de Valorisation Professionnelle de Tunis "
            "et l'Institut Africain de Recherche Pluridisciplinaire Appliquée (IARPA) pour sa contribution au développement."
        ),
        "annee": "2024",
        "photo_fichier": "img/evenements/honoris-causa.jpg",
        "photo_legende": "Cérémonie de remise du grade de Docteur Honoris Causa, Abidjan 2024",
        "photo_credit": "Cabinet",
    },
    {
        "intitule": "Distinction pour le leadership africain & développement local",
        "detail": (
            "Prix du développement local et de la lutte contre la vulnérabilité décerné lors du sommet "
            "Africa Political Outlook à Bruxelles en reconnaissance de son action publique."
        ),
        "annee": "2025",
        "photo_fichier": "img/evenements/leadership-africain.png",
        "photo_legende": "Distinction pour le leadership africain et le développement local à Bruxelles",
        "photo_credit": "Ministère / Cabinet",
    },
    {
        "intitule": "Conseillère municipale de la commune du Golfe 4",
        "detail": (
            "Élue locale engagée au conseil municipal de la commune du Golfe 4 à Lomé, "
            "pour le renforcement de l'action de proximité et le développement territorial."
        ),
        "annee": "2019-2025",
        "photo_fichier": "img/evenements/terrain.jpg",
        "photo_legende": "Engagement citoyen et action municipale de proximité à Lomé",
        "photo_credit": "Cabinet",
    },
    {
        "intitule": "Enseignante vacataire CNAM / ENASS",
        "detail": (
            "Intervenante de 2008 à 2015 au Conservatoire National des Arts et Métiers (France) "
            "et à l'École Nationale d'Assurance (ENASS - Paris) au sein du MBA Management de l'Entreprise d'Assurances."
        ),
        "annee": "2008-2015",
        "photo_fichier": "img/galerie/portrait-gouvernement.jpg",
        "photo_legende": "Transmission et enseignement supérieur en assurance internationale",
        "photo_credit": "Fdimpact",
    },
    {
        "intitule": "Thèse professionnelle sur la réassurance CIMA",
        "detail": (
            "Travail de recherche et mémoire professionnel intitulé « La réassurance dans la zone CIMA : "
            "approche de groupe », présenté à l'ENASS (Paris)."
        ),
        "annee": "2005",
        "photo_fichier": "img/evenements/these-professionnelle.png",
        "photo_legende": "Thèse professionnelle en réassurance CIMA — ENASS Paris",
        "photo_credit": "Archives personnelles / Cabinet",
    },
]


class Command(BaseCommand):
    help = "Charge le contenu initial du site à partir du CV."

    def handle(self, *args, **options):
        profil, _ = Profil.objects.update_or_create(
            pk=Profil.objects.values_list("pk", flat=True).first() or 1,
            defaults=PROFIL,
        )

        Chiffre.objects.all().delete()
        Chiffre.objects.bulk_create(
            Chiffre(valeur=v, libelle=l, ordre=i)
            for i, (v, l) in enumerate(CHIFFRES)
        )

        Competence.objects.all().delete()
        Competence.objects.bulk_create(
            Competence(intitule=t, description=d, icone=ic, ordre=i)
            for i, (t, d, ic) in enumerate(COMPETENCES)
        )

        Experience.objects.all().delete()
        Experience.objects.bulk_create(
            Experience(ordre=i, **donnees) for i, donnees in enumerate(EXPERIENCES)
        )

        Formation.objects.all().delete()
        Formation.objects.bulk_create(
            Formation(annee=a, intitule=i_, etablissement=e, mention=m, ordre=idx)
            for idx, (a, i_, e, m) in enumerate(FORMATIONS)
        )

        Distinction.objects.all().delete()
        Distinction.objects.bulk_create(
            Distinction(ordre=i, **d) for i, d in enumerate(DISTINCTIONS)
        )

        for r_nom in ["Événements", "Actualités", "Tribunes", "Discours", "Presse"]:
            Rubrique.objects.get_or_create(nom=r_nom)

        self.stdout.write(
            self.style.SUCCESS(
                f"Contenu chargé : {profil.nom}, "
                f"{Experience.objects.count()} expériences, "
                f"{Formation.objects.count()} formations, "
                f"{Distinction.objects.count()} distinctions."
            )
        )
