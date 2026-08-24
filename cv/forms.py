from django import forms

from .models import Article, EmailAutorise, Message, Photo, Rubrique, Video


class MessageForm(forms.ModelForm):
    # Champ leurre : invisible pour un humain, rempli par la plupart des robots.
    site_web = forms.CharField(required=False, widget=forms.HiddenInput)

    class Meta:
        model = Message
        fields = ["nom", "email", "organisation", "objet", "contenu"]
        widgets = {
            "nom": forms.TextInput(attrs={"placeholder": "Nom et prénom"}),
            "email": forms.EmailInput(attrs={"placeholder": "vous@exemple.com"}),
            "organisation": forms.TextInput(
                attrs={"placeholder": "Institution, entreprise, média…"}
            ),
            "objet": forms.TextInput(
                attrs={"placeholder": "Objet de votre demande"}
            ),
            "contenu": forms.Textarea(
                attrs={"rows": 7, "placeholder": "Votre message"}
            ),
        }

    def clean_site_web(self):
        if self.cleaned_data.get("site_web"):
            raise forms.ValidationError("Envoi refusé.")
        return ""


class ConnexionForm(forms.Form):
    username = forms.CharField(
        label="Identifiant ou Adresse e-mail",
        widget=forms.TextInput(
            attrs={
                "placeholder": "contact@myriamdossou.com",
                "autofocus": True,
                "class": "form-input form-input--icon",
                "autocomplete": "username",
            }
        ),
    )
    password = forms.CharField(
        label="Mot de passe",
        widget=forms.PasswordInput(
            attrs={
                "placeholder": "••••••••••••",
                "class": "form-input form-input--icon",
                "autocomplete": "current-password",
                "id": "input-password",
            }
        ),
    )


class ArticleForm(forms.ModelForm):
    nouvelle_rubrique = forms.CharField(
        required=False,
        label="Ou créer une nouvelle rubrique",
        widget=forms.TextInput(
            attrs={"placeholder": "Ex: Sommets, Conférences… (si non trouvée dans la liste)"}
        ),
    )

    class Meta:
        model = Article
        fields = [
            "titre",
            "rubrique",
            "nouvelle_rubrique",
            "chapo",
            "contenu",
            "image",
            "image_legende",
            "statut",
            "publie_le",
            "a_la_une",
        ]
        labels = {
            "titre": "Titre de la publication",
            "rubrique": "Rubrique",
            "chapo": "Résumé (Accroche)",
            "contenu": "Corps du texte",
            "image": "Image d'illustration",
            "image_legende": "Légende du visuel",
            "statut": "Statut de parution",
            "publie_le": "Date et heure de publication",
            "a_la_une": "Mettre cette publication à la une",
        }
        widgets = {
            "titre": forms.TextInput(
                attrs={
                    "placeholder": "Ex: Discours officiel sur l'extension de l'assurance maladie...",
                    "class": "form-input form-input--lg",
                }
            ),
            "chapo": forms.Textarea(
                attrs={
                    "rows": 3,
                    "placeholder": "Brève synthèse de 2 à 3 phrases pour capter l'attention dans la liste d'actualités et sur les réseaux sociaux...",
                    "class": "form-textarea",
                }
            ),
            "contenu": forms.Textarea(
                attrs={
                    "rows": 12,
                    "placeholder": "Rédigez ou collez ici le texte complet. Vous pouvez structurer votre texte avec du Markdown simple (**gras**, *italique*, ## Titre de section...)",
                    "class": "form-textarea form-textarea--editor",
                    "id": "editor-contenu",
                }
            ),
            "image_legende": forms.TextInput(
                attrs={
                    "placeholder": "Ex: Cérémonie officielle de signature, Lomé le 12 août...",
                    "class": "form-input",
                }
            ),
            "publie_le": forms.DateTimeInput(
                attrs={"type": "datetime-local", "class": "form-input"},
                format="%Y-%m-%dT%H:%M",
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.pk and self.instance.publie_le:
            self.initial["publie_le"] = self.instance.publie_le.strftime("%Y-%m-%dT%H:%M")

    def save(self, commit=True):
        nouvelle = self.cleaned_data.get("nouvelle_rubrique")
        if nouvelle and nouvelle.strip():
            rubrique_obj, _ = Rubrique.objects.get_or_create(nom=nouvelle.strip())
            self.instance.rubrique = rubrique_obj
        return super().save(commit=commit)


class VideoForm(forms.ModelForm):
    class Meta:
        model = Video
        fields = ["titre", "youtube_url", "thematique", "est_short", "date", "legende", "ordre"]
        widgets = {
            "titre": forms.TextInput(
                attrs={"placeholder": "Ex: Intervention à l'Assemblée Nationale", "class": "form-input"}
            ),
            "youtube_url": forms.URLInput(
                attrs={
                    "placeholder": "Ex: https://www.youtube.com/watch?v=... ou https://youtu.be/... ou https://youtube.com/shorts/...",
                    "class": "form-input",
                }
            ),
            "thematique": forms.Select(attrs={"class": "form-select"}),
            "est_short": forms.CheckboxInput(attrs={"class": "form-checkbox"}),
            "date": forms.TextInput(attrs={"placeholder": "Ex: Juin 2024", "class": "form-input"}),
            "legende": forms.TextInput(
                attrs={"placeholder": "Description rapide ou résumé de la vidéo...", "class": "form-input"}
            ),
            "ordre": forms.NumberInput(attrs={"class": "form-input"}),
        }


class PhotoForm(forms.ModelForm):
    class Meta:
        model = Photo
        fields = ["image", "legende", "date", "credit", "licence", "source_url", "ordre"]
        widgets = {
            "legende": forms.TextInput(
                attrs={"placeholder": "Légende ou lieu de la photo...", "class": "form-input"}
            ),
            "date": forms.TextInput(attrs={"placeholder": "Ex: Mai 2024", "class": "form-input"}),
            "credit": forms.TextInput(
                attrs={"placeholder": "Ex: Cabinet / Ministère", "class": "form-input"}
            ),
            "licence": forms.TextInput(
                attrs={"placeholder": "Ex: CC BY 4.0", "class": "form-input"}
            ),
            "source_url": forms.URLInput(attrs={"placeholder": "https://...", "class": "form-input"}),
            "ordre": forms.NumberInput(attrs={"class": "form-input"}),
        }


class Code2FAForm(forms.Form):
    code = forms.CharField(
        label="Code de sécurité 2FA à 6 chiffres",
        max_length=6,
        min_length=6,
        widget=forms.TextInput(
            attrs={
                "placeholder": "• • • • • •",
                "maxlength": "6",
                "pattern": "[0-9]{6}",
                "autocomplete": "one-time-code",
                "autofocus": True,
                "class": "form-input form-input--code-2fa",
            }
        ),
    )


class EmailAutoriseForm(forms.ModelForm):
    class Meta:
        model = EmailAutorise
        fields = ["email", "nom_utilisateur"]
        widgets = {
            "email": forms.EmailInput(
                attrs={"placeholder": "adresse@exemple.com", "class": "form-input"}
            ),
            "nom_utilisateur": forms.TextInput(
                attrs={"placeholder": "Ex: Madame Myriam Dossou, Collaborateur...", "class": "form-input"}
            ),
        }




