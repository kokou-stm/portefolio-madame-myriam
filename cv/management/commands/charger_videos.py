"""Charge la visiothèque des 10 vidéos YouTube classées par thématique."""

from django.core.management.base import BaseCommand
from cv.models import Video

VIDEOS = [
    # 🏛️ Travail parlementaire
    {
        "titre": "Travaux et prise de fonction à l'Assemblée nationale du Togo",
        "youtube_url": "https://youtu.be/WYNlAAVOexc",
        "youtube_id": "WYNlAAVOexc",
        "est_short": False,
        "thematique": Video.PARLEMENT,
        "date": "2024",
        "legende": "Déclarations et représentation au sein du bureau de l'Assemblée nationale",
    },
    {
        "titre": "Intervention officielle lors de la session parlementaire",
        "youtube_url": "https://youtu.be/s7OsqThumNg",
        "youtube_id": "s7OsqThumNg",
        "est_short": False,
        "thematique": Video.PARLEMENT,
        "date": "2024",
        "legende": "Prise de parole devant la représentation nationale à Lomé",
    },
    {
        "titre": "Temps fort à la Présidence de l'Assemblée nationale",
        "youtube_url": "https://youtube.com/shorts/lVYEO5asqDE",
        "youtube_id": "lVYEO5asqDE",
        "est_short": True,
        "thematique": Video.PARLEMENT,
        "date": "2024",
        "legende": "Extrait d'intervention parlementaire",
    },

    # 🏥 Protection sociale & AMU
    {
        "titre": "Bilan de l'INAM et déploiement de l'Assurance Maladie Universelle (AMU)",
        "youtube_url": "https://youtu.be/qoXl_UFPm1c",
        "youtube_id": "qoXl_UFPm1c",
        "est_short": False,
        "thematique": Video.PROTECTION,
        "date": "2023",
        "legende": "Bilan de la couverture santé et stratégie d'extension de l'AMU au Togo",
    },
    {
        "titre": "Politique de protection sociale et d'inclusion assurantielle",
        "youtube_url": "https://youtube.com/watch?v=bCAMExkebSg",
        "youtube_id": "bCAMExkebSg",
        "est_short": False,
        "thematique": Video.PROTECTION,
        "date": "2023",
        "legende": "Présentation des dispositifs d'appui aux populations vulnérables",
    },
    {
        "titre": "Focus sur la prise en charge et le régime obligatoire INAM",
        "youtube_url": "https://youtube.com/shorts/vd6Xu8k0dWw",
        "youtube_id": "vd6Xu8k0dWw",
        "est_short": True,
        "thematique": Video.PROTECTION,
        "date": "2023",
        "legende": "Explication sur la couverture maladie universelle",
    },

    # 🌱 Jeunesse & Développement
    {
        "titre": "Accompagnement des jeunes entrepreneurs et projets FAIEJ",
        "youtube_url": "https://youtu.be/rouA7JqWPgk",
        "youtube_id": "rouA7JqWPgk",
        "est_short": False,
        "thematique": Video.JEUNESSE,
        "date": "2023",
        "legende": "Remise de financements et équipements aux jeunes initiateurs de projets",
    },
    {
        "titre": "Missions de développement à la base et projets communautaires",
        "youtube_url": "https://youtu.be/OSJZQdn4s9E",
        "youtube_id": "OSJZQdn4s9E",
        "est_short": False,
        "thematique": Video.JEUNESSE,
        "date": "2023",
        "legende": "Suivi des réalisations du FACT dans les préfectures du Togo",
    },
    {
        "titre": "Lancement du projet « Jeunes Bacheliers Engagés » (ANVT)",
        "youtube_url": "https://youtube.com/shorts/Ml2nLMBrIVE",
        "youtube_id": "Ml2nLMBrIVE",
        "est_short": True,
        "thematique": Video.JEUNESSE,
        "date": "2022",
        "legende": "Mobilisation citoyenne et volontariat des jeunes bacheliers",
    },

    # 🎙️ Discours & Événements
    {
        "titre": "Allocution officielle et cérémonies publiques",
        "youtube_url": "https://youtube.com/shorts/W1bhSdrZ2jo",
        "youtube_id": "W1bhSdrZ2jo",
        "est_short": True,
        "thematique": Video.DISCOURS,
        "date": "2024",
        "legende": "Extrait de prise de parole lors d'un événement officiel",
    },
]


class Command(BaseCommand):
    help = "Charge les 10 vidéos YouTube classées par thématique."

    def handle(self, *args, **options):
        Video.objects.all().delete()
        for i, donnees in enumerate(VIDEOS):
            Video.objects.create(**donnees, ordre=i)

        self.stdout.write(
            self.style.SUCCESS(f"{Video.objects.count()} vidéos chargées avec succès.")
        )
