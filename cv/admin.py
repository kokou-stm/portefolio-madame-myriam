from django.contrib import admin

from .models import (
    Article,
    Chiffre,
    Competence,
    Distinction,
    Experience,
    Formation,
    Message,
    Photo,
    Profil,
    Realisation,
    Rubrique,
    Video,
)

admin.site.site_header = "Administration du site"
admin.site.site_title = "Myriam Dossou d'Almeida"
admin.site.index_title = "Contenu du site"


@admin.register(Profil)
class ProfilAdmin(admin.ModelAdmin):
    fieldsets = (
        ("Identité", {"fields": ("nom", "titre", "sous_titre", "accroche")}),
        (
            "Présentation",
            {"fields": ("biographie", "photo", "image_fond", "photo_credit")},
        ),
        ("Contact", {"fields": ("ville", "pays", "email", "telephone")}),
        ("Réseaux", {"fields": ("linkedin", "twitter", "facebook", "instagram", "tiktok")}),
    )

    def has_add_permission(self, request):
        # Un profil unique : on édite celui qui existe déjà.
        return not Profil.objects.exists()


@admin.register(Experience)
class ExperienceAdmin(admin.ModelAdmin):
    list_display = ("poste", "organisation", "periode", "a_une_photo", "en_cours", "ordre")
    list_editable = ("ordre",)
    list_filter = ("en_cours",)
    search_fields = ("poste", "organisation", "description")
    fieldsets = (
        (None, {"fields": ("poste", "organisation", "lieu", "periode", "description")}),
        (
            "Photo",
            {
                "fields": ("photo", "photo_legende"),
                "description": (
                    "Facultatif. Une photo prise pendant cette fonction rend la "
                    "fiche beaucoup plus vivante, mais la mise en page reste "
                    "soignée sans."
                ),
            },
        ),
        ("Affichage", {"fields": ("en_cours", "ordre")}),
    )

    @admin.display(description="Photo", boolean=True)
    def a_une_photo(self, obj):
        return bool(obj.photo)


@admin.register(Formation)
class FormationAdmin(admin.ModelAdmin):
    list_display = ("annee", "intitule", "etablissement", "ordre")
    list_editable = ("ordre",)
    search_fields = ("intitule", "etablissement")


@admin.register(Competence)
class CompetenceAdmin(admin.ModelAdmin):
    list_display = ("intitule", "icone", "description", "ordre")
    list_editable = ("icone", "ordre")


@admin.register(Chiffre)
class ChiffreAdmin(admin.ModelAdmin):
    list_display = ("valeur", "libelle", "ordre")
    list_editable = ("ordre",)


@admin.register(Distinction)
class DistinctionAdmin(admin.ModelAdmin):
    list_display = ("intitule", "annee", "ordre")
    list_editable = ("ordre",)


@admin.register(Realisation)
class RealisationAdmin(admin.ModelAdmin):
    list_display = ("annee", "titre", "domaine", "a_une_photo", "ordre")
    list_editable = ("ordre",)
    list_filter = ("domaine",)
    search_fields = ("titre", "description", "source_nom")
    fieldsets = (
        (None, {"fields": ("titre", "domaine", "annee", "description")}),
        (
            "Chiffre mis en avant",
            {
                "fields": ("chiffre", "chiffre_libelle"),
                "description": "Facultatif. Un ordre de grandeur marque davantage qu'une phrase.",
            },
        ),
        (
            "Photo",
            {
                "fields": ("photo", "photo_legende"),
                "description": (
                    "N'utiliser que des photos dont vous détenez les droits : "
                    "clichés de votre cabinet ou pris par vos équipes. Les photos "
                    "de presse ne sont pas réutilisables sans autorisation."
                ),
            },
        ),
        (
            "Source",
            {
                "fields": ("source_url", "source_nom"),
                "description": (
                    "Obligatoire. Chaque réalisation affichée renvoie vers la "
                    "publication qui l'atteste."
                ),
            },
        ),
        ("Affichage", {"fields": ("ordre",)}),
    )

    @admin.display(description="Photo", boolean=True)
    def a_une_photo(self, obj):
        return bool(obj.photo)


@admin.register(Rubrique)
class RubriqueAdmin(admin.ModelAdmin):
    list_display = ("nom", "nombre_articles", "ordre")
    list_editable = ("ordre",)
    prepopulated_fields = {"slug": ("nom",)}

    @admin.display(description="Publications")
    def nombre_articles(self, obj):
        return obj.articles.count()


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ("titre", "rubrique", "statut", "publie_le", "a_la_une")
    list_filter = ("statut", "a_la_une", "rubrique")
    search_fields = ("titre", "chapo", "contenu")
    date_hierarchy = "publie_le"
    prepopulated_fields = {"slug": ("titre",)}
    fieldsets = (
        (None, {"fields": ("titre", "rubrique", "chapo", "contenu")}),
        ("Illustration", {"fields": ("image", "image_legende")}),
        (
            "Publication",
            {
                "fields": ("statut", "publie_le", "a_la_une", "slug"),
                "description": (
                    "Un article en brouillon n'est visible de personne d'autre. "
                    "Passez le statut à « Publié » lorsqu'il est prêt."
                ),
            },
        ),
    )
    actions = ["publier", "repasser_en_brouillon"]

    @admin.action(description="Publier les articles sélectionnés")
    def publier(self, request, queryset):
        n = queryset.update(statut=Article.PUBLIE)
        self.message_user(request, f"{n} publication(s) mise(s) en ligne.")

    @admin.action(description="Repasser en brouillon")
    def repasser_en_brouillon(self, request, queryset):
        n = queryset.update(statut=Article.BROUILLON)
        self.message_user(request, f"{n} publication(s) retirée(s) du site.")


@admin.register(Photo)
class PhotoAdmin(admin.ModelAdmin):
    list_display = ("apercu", "legende", "date", "licence", "ordre")
    list_editable = ("ordre",)
    search_fields = ("legende", "credit")
    fieldsets = (
        (None, {"fields": ("image", "legende", "date", "ordre")}),
        (
            "Crédit et licence",
            {
                "fields": ("credit", "licence", "source_url"),
                "description": (
                    "À remplir uniquement si la photo n'est pas de vous : toute "
                    "image sous licence Creative Commons doit être attribuée à son "
                    "auteur. Laisser vide pour vos propres clichés."
                ),
            },
        ),
    )

    @admin.display(description="Aperçu")
    def apercu(self, obj):
        from django.utils.html import format_html

        if obj.src:
            return format_html(
                '<img src="{}" style="height:44px;border-radius:4px">', obj.src
            )
        return "—"


@admin.register(Video)
class VideoAdmin(admin.ModelAdmin):
    list_display = ("titre", "thematique", "est_short", "date", "ordre")
    list_editable = ("ordre",)
    list_filter = ("thematique", "est_short")
    search_fields = ("titre", "legende", "youtube_url")
    fieldsets = (
        (None, {"fields": ("titre", "youtube_url", "thematique", "est_short")}),
        ("Détails", {"fields": ("date", "legende", "ordre")}),
    )


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ("envoye_le", "nom", "organisation", "objet", "lu")
    list_filter = ("lu", "envoye_le")
    search_fields = ("nom", "email", "objet", "contenu")
    readonly_fields = ("nom", "email", "organisation", "objet", "contenu", "envoye_le")
    actions = ["marquer_comme_lu"]

    @admin.action(description="Marquer les messages sélectionnés comme lus")
    def marquer_comme_lu(self, request, queryset):
        queryset.update(lu=True)

    def has_add_permission(self, request):
        return False
