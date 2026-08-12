from django import forms

from .models import Article, Message, Rubrique


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
        label="Nom d'utilisateur",
        widget=forms.TextInput(
            attrs={"placeholder": "Ex. admin", "autofocus": True}
        ),
    )
    password = forms.CharField(
        label="Mot de passe",
        widget=forms.PasswordInput(attrs={"placeholder": "••••••••"}),
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


