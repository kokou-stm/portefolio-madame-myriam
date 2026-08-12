import re

import markdown
from django.db import models
from django.templatetags.static import static
from django.urls import reverse
from django.utils import timezone
from django.utils.safestring import mark_safe
from django.utils.text import slugify


class Profil(models.Model):
    """Informations d'en-tête du site. Une seule instance est utilisée."""

    nom = models.CharField("Nom complet", max_length=120)
    titre = models.CharField("Titre principal", max_length=200)
    sous_titre = models.CharField("Fonction actuelle", max_length=200, blank=True)
    accroche = models.TextField("Phrase d'accroche", blank=True)
    biographie = models.TextField("Biographie", blank=True)
    photo = models.ImageField("Portrait", upload_to="portraits/", blank=True)
    photo_credit = models.CharField("Crédit photo", max_length=250, blank=True)
    image_fond = models.ImageField(
        "Image d'arrière-plan",
        upload_to="fonds/",
        blank=True,
        help_text=(
            "Vue de l'Assemblée nationale affichée derrière le titre d'accueil. "
            "Format paysage large, 1920 px minimum. Elle est fortement assombrie : "
            "seule la silhouette du bâtiment se devine."
        ),
    )

    ville = models.CharField("Ville", max_length=100, blank=True)
    pays = models.CharField("Pays", max_length=100, blank=True)
    email = models.EmailField("Adresse e-mail", blank=True)
    telephone = models.CharField("Téléphone", max_length=60, blank=True)
    linkedin = models.URLField("LinkedIn", max_length=500, blank=True)
    twitter = models.URLField("X / Twitter", max_length=500, blank=True)
    facebook = models.URLField("Facebook", max_length=500, blank=True)
    instagram = models.URLField("Instagram", max_length=500, blank=True)
    tiktok = models.URLField("TikTok", max_length=500, blank=True)

    class Meta:
        verbose_name = "Profil"
        verbose_name_plural = "Profil"

    def __str__(self):
        return self.nom

    @property
    def localisation(self):
        return ", ".join(p for p in (self.ville, self.pays) if p)


class Chiffre(models.Model):
    """Indicateur mis en avant sur la page d'accueil (ex. « 500 000 assurés »)."""

    valeur = models.CharField("Valeur", max_length=40)
    libelle = models.CharField("Libellé", max_length=120)
    ordre = models.PositiveSmallIntegerField("Ordre", default=0)

    class Meta:
        verbose_name = "Chiffre clé"
        verbose_name_plural = "Chiffres clés"
        ordering = ["ordre"]

    def __str__(self):
        return f"{self.valeur} — {self.libelle}"


class Experience(models.Model):
    poste = models.CharField("Poste", max_length=200)
    organisation = models.CharField("Organisation", max_length=200)
    lieu = models.CharField("Lieu", max_length=120, blank=True)
    periode = models.CharField("Période", max_length=80)
    photo = models.ImageField(
        "Photo",
        upload_to="experiences/",
        blank=True,
        help_text=(
            "Facultatif : une photo prise pendant cette fonction — cérémonie, "
            "mission de terrain, signature d'accord. Format paysage de "
            "préférence. La fiche s'affiche très bien sans photo."
        ),
    )
    photo_legende = models.CharField(
        "Légende de la photo",
        max_length=250,
        blank=True,
        help_text="Décrire la scène : lieu, événement, date.",
    )
    description = models.TextField(
        "Missions",
        blank=True,
        help_text="Une mission par ligne. Chaque ligne devient une puce.",
    )
    en_cours = models.BooleanField("Poste actuel", default=False)
    ordre = models.PositiveSmallIntegerField(
        "Ordre", default=0, help_text="Du plus récent (0) au plus ancien."
    )

    class Meta:
        verbose_name = "Expérience professionnelle"
        verbose_name_plural = "Expériences professionnelles"
        ordering = ["ordre"]

    def __str__(self):
        return f"{self.poste} — {self.organisation}"

    @property
    def missions(self):
        return [ligne.strip() for ligne in self.description.splitlines() if ligne.strip()]

    @property
    def annee_debut(self):
        """Année de début, lue dans la période libre, pour la pastille du parcours.

        « Octobre 2020 — Août 2024 » donne 2020, « Depuis juin 2024 » donne 2024.
        Le premier millésime rencontré est toujours celui du début.
        """
        annees = re.findall(r"\b(1[89]\d{2}|20\d{2})\b", self.periode)
        return annees[0] if annees else ""


class Formation(models.Model):
    intitule = models.CharField("Intitulé", max_length=250)
    etablissement = models.CharField("Établissement", max_length=200, blank=True)
    annee = models.CharField("Année", max_length=40)
    mention = models.CharField("Mention", max_length=120, blank=True)
    ordre = models.PositiveSmallIntegerField("Ordre", default=0)

    class Meta:
        verbose_name = "Formation"
        verbose_name_plural = "Formations et diplômes"
        ordering = ["ordre"]

    def __str__(self):
        return f"{self.annee} — {self.intitule}"


class Competence(models.Model):
    # Les pictogrammes sont des SVG intégrés au site : pas de dépendance
    # externe, donc rien à charger et rien qui puisse disparaître.
    ICONES = [
        ("courbe", "Courbe — management, pilotage"),
        ("bouclier", "Bouclier — assurance, risques"),
        ("personnes", "Personnes — social, communauté"),
        ("ecran", "Écran — informatique, projets"),
        ("balance", "Balance — gouvernance, politiques publiques"),
        ("coeur", "Cœur — santé, prévention"),
        ("globe", "Globe — international, partenariats"),
        ("document", "Document — expertise, études"),
    ]

    intitule = models.CharField("Compétence", max_length=150)
    description = models.CharField("Précision", max_length=250, blank=True)
    icone = models.CharField(
        "Pictogramme", max_length=20, choices=ICONES, default="courbe"
    )
    ordre = models.PositiveSmallIntegerField("Ordre", default=0)

    class Meta:
        verbose_name = "Domaine d'expertise"
        verbose_name_plural = "Domaines d'expertise"
        ordering = ["ordre"]

    def __str__(self):
        return self.intitule


class Distinction(models.Model):
    intitule = models.CharField("Intitulé", max_length=250)
    detail = models.CharField("Détail", max_length=250, blank=True)
    annee = models.CharField("Année", max_length=40, blank=True)

    photo = models.ImageField("Photo (téléversée)", upload_to="distinctions/", blank=True)
    photo_fichier = models.CharField(
        "Photo livrée (fichier)",
        max_length=200,
        blank=True,
        help_text="Réservé aux images fournies avec le site. Laisser vide pour un téléversement.",
    )
    photo_legende = models.CharField("Légende de la photo", max_length=250, blank=True)
    photo_credit = models.CharField(
        "Crédit de la photo",
        max_length=200,
        blank=True,
        help_text="Auteur ou source du cliché.",
    )
    ordre = models.PositiveSmallIntegerField("Ordre", default=0)

    class Meta:
        verbose_name = "Distinction & engagement"
        verbose_name_plural = "Distinctions & engagements"
        ordering = ["ordre"]

    def __str__(self):
        return self.intitule

    @property
    def photo_src(self):
        if self.photo:
            return self.photo.url
        if self.photo_fichier:
            return static(self.photo_fichier)
        return ""


class Realisation(models.Model):
    """Action publique menée, adossée à une source vérifiable.

    Le champ `source_url` est obligatoire à dessein : sur le site d'une élue,
    une réalisation qu'on ne peut pas rattacher à une publication devient une
    affirmation invérifiable.
    """

    PROTECTION = "protection"
    JEUNESSE = "jeunesse"
    TERRITOIRES = "territoires"
    PARLEMENT = "parlement"
    RECONNAISSANCE = "reconnaissance"
    DOMAINES = [
        (PROTECTION, "Protection sociale et santé"),
        (JEUNESSE, "Jeunesse et emploi"),
        (TERRITOIRES, "Développement des territoires"),
        (PARLEMENT, "Travail parlementaire"),
        (RECONNAISSANCE, "Reconnaissances"),
    ]

    titre = models.CharField("Titre", max_length=220)
    domaine = models.CharField(
        "Domaine", max_length=20, choices=DOMAINES, default=PROTECTION
    )
    annee = models.CharField(
        "Année ou période", max_length=40, help_text="Par exemple « 2022 » ou « 2020-2024 »."
    )
    description = models.TextField("Description", help_text="Deux à quatre phrases.")
    chiffre = models.CharField(
        "Chiffre à mettre en avant",
        max_length=60,
        blank=True,
        help_text="Facultatif : « 1 852 projets », « 500 000 assurés »…",
    )
    chiffre_libelle = models.CharField(
        "Précision du chiffre", max_length=120, blank=True
    )

    photo = models.ImageField("Photo (téléversée)", upload_to="realisations/", blank=True)
    photo_fichier = models.CharField(
        "Photo livrée (fichier)",
        max_length=200,
        blank=True,
        help_text="Réservé aux images fournies avec le site. Laisser vide pour un téléversement.",
    )
    photo_legende = models.CharField("Légende de la photo", max_length=250, blank=True)
    photo_credit = models.CharField(
        "Crédit de la photo",
        max_length=200,
        blank=True,
        help_text="Auteur ou source du cliché (ex. « Cabinet / Ministère »).",
    )

    source_url = models.URLField(
        "Lien de la source",
        max_length=500,
        help_text="Article de presse ou page officielle attestant de cette réalisation.",
    )
    source_nom = models.CharField(
        "Nom de la source",
        max_length=120,
        help_text="Par exemple « République Togolaise » ou « Agence Ecofin ».",
    )

    ordre = models.PositiveSmallIntegerField("Ordre", default=0)

    class Meta:
        verbose_name = "Réalisation"
        verbose_name_plural = "Réalisations et engagements"
        ordering = ["ordre"]

    def __str__(self):
        return f"{self.annee} — {self.titre}"

    @property
    def photo_src(self):
        """URL de la photo : téléversement admin prioritaire, sinon fichier livré."""
        if self.photo:
            return self.photo.url
        if self.photo_fichier:
            from django.templatetags.static import static

            return static(self.photo_fichier)
        return ""


class Rubrique(models.Model):
    """Catégorie de publication (Tribune, Actualité, Discours…)."""

    nom = models.CharField("Nom", max_length=80, unique=True)
    slug = models.SlugField("Adresse", max_length=80, unique=True, blank=True)
    ordre = models.PositiveSmallIntegerField("Ordre", default=0)

    class Meta:
        verbose_name = "Rubrique"
        verbose_name_plural = "Rubriques"
        ordering = ["ordre", "nom"]

    def __str__(self):
        return self.nom

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.nom)
        super().save(*args, **kwargs)


class ArticlePublieManager(models.Manager):
    def get_queryset(self):
        return (
            super()
            .get_queryset()
            .filter(statut=Article.PUBLIE, publie_le__lte=timezone.now())
        )


class Article(models.Model):
    BROUILLON = "brouillon"
    PUBLIE = "publie"
    STATUTS = [
        (BROUILLON, "Brouillon — visible de vous seule"),
        (PUBLIE, "Publié — visible par tous"),
    ]

    titre = models.CharField("Titre", max_length=200)
    slug = models.SlugField(
        "Adresse de la page",
        max_length=220,
        unique=True,
        blank=True,
        help_text="Laisser vide : l'adresse est créée automatiquement à partir du titre.",
    )
    rubrique = models.ForeignKey(
        Rubrique,
        verbose_name="Rubrique",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="articles",
    )
    chapo = models.TextField(
        "Résumé",
        blank=True,
        help_text="Résumé de deux ou trois lignes, affiché en tête d'article et dans la liste.",
    )
    contenu = models.TextField(
        "Texte",
        help_text=(
            "Écrivez normalement, en séparant les paragraphes par une ligne vide. "
            "Mise en forme facultative : **gras**, *italique*, ## Intertitre, "
            "[texte du lien](https://adresse)."
        ),
    )
    image = models.ImageField("Image d'illustration", upload_to="articles/", blank=True)
    image_fichier = models.CharField(
        "Image livrée (fichier)",
        max_length=200,
        blank=True,
        help_text="Réservé aux images fournies avec le site. Laisser vide pour un téléversement.",
    )
    image_legende = models.CharField("Légende de l'image", max_length=250, blank=True)

    statut = models.CharField(
        "Statut", max_length=12, choices=STATUTS, default=BROUILLON
    )
    publie_le = models.DateTimeField(
        "Date de publication",
        default=timezone.now,
        help_text="Une date future programme la parution.",
    )
    a_la_une = models.BooleanField(
        "Mettre à la une",
        default=False,
        help_text="Affiche l'article en tête de la page Publications.",
    )
    modifie_le = models.DateTimeField("Dernière modification", auto_now=True)

    objects = models.Manager()
    publies = ArticlePublieManager()

    class Meta:
        verbose_name = "Publication"
        verbose_name_plural = "Publications"
        ordering = ["-publie_le"]

    def __str__(self):
        return self.titre

    def save(self, *args, **kwargs):
        if not self.slug:
            base = slugify(self.titre)[:200] or "publication"
            slug, n = base, 2
            while Article.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f"{base}-{n}"
                n += 1
            self.slug = slug
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("article", args=[self.slug])

    @property
    def image_src(self):
        if self.image_fichier:
            return static(self.image_fichier)
        if self.image:
            return self.image.url
        return ""

    @property
    def est_visible(self):
        return self.statut == self.PUBLIE and self.publie_le <= timezone.now()

    @property
    def contenu_html(self):
        # Les articles ne sont rédigés que depuis l'administration, par une
        # autrice de confiance : le HTML produit n'est donc pas assaini.
        return mark_safe(
            markdown.markdown(self.contenu, extensions=["extra", "nl2br", "smarty"])
        )

    @property
    def temps_lecture(self):
        return max(1, round(len(self.contenu.split()) / 200))


class Photo(models.Model):
    """Cliché de la galerie : événement, cérémonie, mission de terrain.

    L'image vient soit d'un téléversement admin (`image`), soit d'un fichier
    livré avec le site (`fichier_statique`, pour les clichés issus de Wikimedia).
    Le téléversement prime. `credit`/`licence` sont obligatoires dès qu'une image
    n'appartient pas à Mme Dossou d'Almeida — une photo Creative Commons doit
    toujours être attribuée.
    """

    image = models.ImageField("Photo (téléversée)", upload_to="galerie/", blank=True)
    fichier_statique = models.CharField(
        "Fichier livré",
        max_length=200,
        blank=True,
        help_text="Réservé aux images fournies avec le site. Laisser vide pour un téléversement.",
    )
    legende = models.CharField(
        "Légende",
        max_length=250,
        blank=True,
        help_text="Décrire la scène : lieu, événement, date.",
    )
    date = models.CharField(
        "Date ou période",
        max_length=60,
        blank=True,
        help_text="Facultatif, par exemple « Juin 2024 ».",
    )
    credit = models.CharField(
        "Crédit / auteur",
        max_length=200,
        blank=True,
        help_text="Auteur de la photo. Obligatoire pour une image sous licence Creative Commons.",
    )
    licence = models.CharField(
        "Licence",
        max_length=60,
        blank=True,
        help_text="Par exemple « CC BY 4.0 ». À laisser vide pour les photos de votre cabinet.",
    )
    source_url = models.URLField("Lien de la source", max_length=500, blank=True)
    ordre = models.PositiveSmallIntegerField("Ordre", default=0)

    class Meta:
        verbose_name = "Photo de la galerie"
        verbose_name_plural = "Galerie"
        ordering = ["ordre"]

    def __str__(self):
        return self.legende or f"Photo {self.pk}"

    @property
    def src(self):
        if self.image:
            return self.image.url
        if self.fichier_statique:
            from django.templatetags.static import static

            return static(self.fichier_statique)
        return ""

    @property
    def credit_complet(self):
        """Ligne de crédit compacte : « © Auteur — CC BY 4.0 »."""
        morceaux = [m for m in (self.credit, self.licence) if m]
        return " — ".join(morceaux)


class Message(models.Model):
    nom = models.CharField("Nom", max_length=120)
    email = models.EmailField("Adresse e-mail")
    organisation = models.CharField("Organisation", max_length=150, blank=True)
    objet = models.CharField("Objet", max_length=200)
    contenu = models.TextField("Message")
    envoye_le = models.DateTimeField("Reçu le", auto_now_add=True)
    lu = models.BooleanField("Lu", default=False)

    class Meta:
        verbose_name = "Message reçu"
        verbose_name_plural = "Messages reçus"
        ordering = ["-envoye_le"]

    def __str__(self):
        return f"{self.nom} — {self.objet}"
