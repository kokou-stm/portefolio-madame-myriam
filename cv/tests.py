from datetime import timedelta

from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from .models import Article, Message, Photo, Profil, Realisation, Rubrique


class PagesTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        Profil.objects.create(nom="Myriam Dossou d'Almeida", titre="Experte")

    def test_pages_principales_repondent(self):
        for nom in ("accueil", "parcours", "realisations", "galerie", "publications", "contact"):
            with self.subTest(page=nom):
                self.assertEqual(self.client.get(reverse(nom)).status_code, 200)


class ArticleVisibiliteTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        Profil.objects.create(nom="Myriam Dossou d'Almeida", titre="Experte")
        cls.rubrique = Rubrique.objects.create(nom="Tribune")
        cls.publie = Article.objects.create(
            titre="Article publié",
            contenu="Texte.",
            rubrique=cls.rubrique,
            statut=Article.PUBLIE,
            publie_le=timezone.now() - timedelta(days=1),
        )
        cls.brouillon = Article.objects.create(
            titre="Article en brouillon",
            contenu="Texte.",
            statut=Article.BROUILLON,
        )
        cls.programme = Article.objects.create(
            titre="Article programmé",
            contenu="Texte.",
            statut=Article.PUBLIE,
            publie_le=timezone.now() + timedelta(days=3),
        )

    def test_slug_genere_automatiquement(self):
        self.assertEqual(self.publie.slug, "article-publie")

    def test_slug_reste_unique(self):
        autre = Article.objects.create(titre="Article publié", contenu="Texte.")
        self.assertEqual(autre.slug, "article-publie-2")

    def test_seuls_les_articles_publies_sont_listes(self):
        contenu = self.client.get(reverse("publications")).content.decode()
        self.assertIn("Article publié", contenu)
        self.assertNotIn("Article en brouillon", contenu)
        self.assertNotIn("Article programmé", contenu)

    def test_brouillon_inaccessible_au_public(self):
        self.assertEqual(
            self.client.get(self.brouillon.get_absolute_url()).status_code, 404
        )

    def test_article_programme_inaccessible_avant_sa_date(self):
        self.assertEqual(
            self.client.get(self.programme.get_absolute_url()).status_code, 404
        )

    def test_brouillon_visible_par_son_autrice(self):
        User.objects.create_user("myriam", password="motdepasse", is_staff=True)
        self.client.login(username="myriam", password="motdepasse")
        reponse = self.client.get(self.brouillon.get_absolute_url())
        self.assertEqual(reponse.status_code, 200)
        self.assertContains(reponse, "brouillon")

    def test_article_publie_accessible(self):
        self.assertEqual(
            self.client.get(self.publie.get_absolute_url()).status_code, 200
        )

    def test_filtre_par_rubrique(self):
        reponse = self.client.get(reverse("publications"), {"rubrique": "tribune"})
        self.assertContains(reponse, "Article publié")

    def test_mise_en_forme_du_texte(self):
        article = Article.objects.create(
            titre="Mise en forme",
            contenu="## Intertitre\n\nUn mot en **gras**.",
        )
        html = article.contenu_html
        self.assertIn("<h2>", html)
        self.assertIn("<strong>gras</strong>", html)


class ContactTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        Profil.objects.create(nom="Myriam Dossou d'Almeida", titre="Experte")

    def test_message_valide_enregistre(self):
        reponse = self.client.post(
            reverse("contact"),
            {
                "nom": "Jean Dupont",
                "email": "jean@exemple.com",
                "objet": "Invitation",
                "contenu": "Bonjour.",
            },
        )
        self.assertRedirects(reponse, reverse("contact"))
        self.assertEqual(Message.objects.count(), 1)

    def test_pot_de_miel_rejette_les_robots(self):
        self.client.post(
            reverse("contact"),
            {
                "nom": "Robot",
                "email": "robot@exemple.com",
                "objet": "Spam",
                "contenu": "Spam.",
                "site_web": "http://spam.example",
            },
        )
        self.assertEqual(Message.objects.count(), 0)


class RealisationTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        Profil.objects.create(nom="Myriam Dossou d'Almeida", titre="Experte")
        cls.protection = Realisation.objects.create(
            titre="Extension de l'assurance maladie",
            domaine=Realisation.PROTECTION,
            annee="2022",
            description="Description.",
            source_url="https://exemple.tg/article",
            source_nom="Exemple",
        )
        cls.jeunesse = Realisation.objects.create(
            titre="Financement des projets de jeunes",
            domaine=Realisation.JEUNESSE,
            annee="2023",
            chiffre="1 852 projets",
            description="Description.",
            source_url="https://exemple.tg/autre",
            source_nom="Exemple",
        )

    def test_page_repond(self):
        self.assertEqual(self.client.get(reverse("realisations")).status_code, 200)

    def test_la_source_est_affichee(self):
        reponse = self.client.get(reverse("realisations"))
        self.assertContains(reponse, "https://exemple.tg/article")
        self.assertContains(reponse, "Source : Exemple")

    def test_filtre_par_domaine(self):
        reponse = self.client.get(reverse("realisations"), {"domaine": "jeunesse"})
        self.assertContains(reponse, "Financement des projets de jeunes")
        self.assertNotContains(reponse, "Extension de l&#x27;assurance maladie")

    def test_domaine_inconnu_affiche_tout(self):
        """Un paramètre fantaisiste ne doit pas vider la page ni lever d'erreur."""
        reponse = self.client.get(reverse("realisations"), {"domaine": "n-existe-pas"})
        self.assertEqual(reponse.status_code, 200)
        self.assertContains(reponse, "Financement des projets de jeunes")
        self.assertContains(reponse, "Extension de l&#x27;assurance maladie")

    def test_lien_present_dans_la_navigation(self):
        reponse = self.client.get(reverse("accueil"))
        self.assertContains(reponse, reverse("realisations"))

    def test_toutes_les_realisations_chargees_ont_une_source(self):
        from django.core.management import call_command
        call_command("charger_realisations", verbosity=0)
        sans_source = Realisation.objects.filter(source_url="")
        self.assertFalse(sans_source.exists(), "Une réalisation sans source a été chargée")


class GalerieTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        Profil.objects.create(nom="Myriam Dossou d'Almeida", titre="Experte")

    def test_photo_livree_utilise_le_fichier_statique(self):
        photo = Photo.objects.create(
            fichier_statique="img/galerie/evenement-entrepreneurs.jpg",
            legende="Événement",
            credit="Baname Laré",
            licence="CC BY 4.0",
        )
        self.assertIn("img/galerie/evenement-entrepreneurs.jpg", photo.src)
        self.assertEqual(photo.credit_complet, "Baname Laré — CC BY 4.0")

    def test_upload_prime_sur_le_fichier_livre(self):
        photo = Photo(
            image="galerie/uploadee.jpg",
            fichier_statique="img/galerie/evenement-entrepreneurs.jpg",
        )
        self.assertIn("galerie/uploadee.jpg", photo.src)

    def test_credit_affiche_sur_la_page(self):
        Photo.objects.create(
            fichier_statique="img/galerie/x.jpg",
            legende="Cérémonie",
            credit="Auteur",
            licence="CC BY 4.0",
        )
        reponse = self.client.get(reverse("galerie"))
        self.assertContains(reponse, "Auteur — CC BY 4.0")

    def test_lien_present_dans_la_navigation(self):
        reponse = self.client.get(reverse("accueil"))
        self.assertContains(reponse, reverse("galerie"))

    def test_toutes_les_photos_libres_sont_creditees(self):
        from django.core.management import call_command
        call_command("charger_galerie", verbosity=0)
        # Une image sous licence Creative Commons doit toujours porter un crédit.
        for photo in Photo.objects.exclude(licence=""):
            self.assertTrue(
                photo.credit, f"La photo « {photo.legende} » n'a pas de crédit"
            )


class AdminPortalTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.profil = Profil.objects.create(
            nom="Myriam Dossou d'Almeida",
            titre="Experte",
            instagram="https://www.instagram.com/myriamdossoudalmeida/",
            twitter="https://x.com/DossouMyriam",
            facebook="https://www.facebook.com/myriamdossoudalmeida",
            tiktok="https://www.tiktok.com/@myriamdossou",
        )
        cls.user = User.objects.create_superuser(
            username="admin", password="password123"
        )

    def test_page_connexion_accessible(self):
        res = self.client.get(reverse("connexion_admin"))
        self.assertEqual(res.status_code, 200)
        self.assertContains(res, "Connexion")

    def test_dashboard_protege_pour_anonymes(self):
        res = self.client.get(reverse("admin_dashboard"))
        self.assertEqual(res.status_code, 302)

    def test_connexion_et_accès_dashboard(self):
        self.client.login(username="admin", password="password123")
        res = self.client.get(reverse("admin_dashboard"))
        self.assertEqual(res.status_code, 200)
        self.assertContains(res, "Tableau de bord")

    def test_creation_article_via_espace_admin(self):
        self.client.login(username="admin", password="password123")
        res = self.client.post(
            reverse("admin_article_creer"),
            {
                "titre": "Nouvel Événement Importante",
                "chapo": "Résumé de l'événement.",
                "contenu": "Contenu complet de la publication.",
                "statut": Article.PUBLIE,
                "publie_le": timezone.now().strftime("%Y-%m-%dT%H:%M"),
            },
        )
        self.assertEqual(res.status_code, 302)
        self.assertTrue(Article.objects.filter(titre="Nouvel Événement Importante").exists())

    def test_reseaux_sociaux_affiches_sur_le_site(self):
        res = self.client.get(reverse("contact"))
        self.assertContains(res, "https://www.instagram.com/myriamdossoudalmeida/")
        self.assertContains(res, "https://x.com/DossouMyriam")
        self.assertContains(res, "https://www.facebook.com/myriamdossoudalmeida")
        self.assertContains(res, "https://www.tiktok.com/@myriamdossou")

