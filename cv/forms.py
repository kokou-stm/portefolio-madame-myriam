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
        widgets = {
            "titre": forms.TextInput(
                attrs={"placeholder": "Ex: Rencontre et échange sur l'assurance inclusive…"}
            ),
            "chapo": forms.Textarea(
                attrs={
                    "rows": 3,
                    "placeholder": "Court résumé d'accroche pour la liste et les réseaux…",
                }
            ),
            "contenu": forms.Textarea(
                attrs={
                    "rows": 12,
                    "placeholder": "Rédigez ici le texte complet. Vous pouvez utiliser du texte simple ou du Markdown (**gras**, *italique*, ## Intertitre…)",
                }
            ),
            "image_legende": forms.TextInput(
                attrs={"placeholder": "Ex: Cérémonie d'ouverture, Lomé le 12 août…"}
            ),
            "publie_le": forms.DateTimeInput(
                attrs={"type": "datetime-local"}, format="%Y-%m-%dT%H:%M"
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


