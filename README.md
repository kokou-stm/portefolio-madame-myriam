# Portfolio — Myriam Dossou d'Almeida

Site vitrine professionnel : présentation, parcours et formulaire de contact.
Django 6, SQLite, aucune dépendance front externe (police système, CSS unique).

## Démarrage

```bash
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
.venv/bin/python manage.py migrate
.venv/bin/python manage.py charger_cv        # contenu initial issu du CV
.venv/bin/python manage.py createsuperuser   # accès à l'administration
.venv/bin/python manage.py runserver
```

Le site est alors sur http://127.0.0.1:8000/, l'administration sur `/admin/`.

## Modifier le contenu

Tout le contenu est éditable depuis `/admin/`, sans toucher au code :

| Section de l'admin | Ce qu'elle pilote |
| --- | --- |
| Profil | Nom, titres, accroche, biographie, portrait, coordonnées |
| Chiffres clés | Les quatre indicateurs de la page d'accueil |
| Domaines d'expertise | Les cartes « Domaines d'intervention » |
| Expériences professionnelles | La chronologie (une mission par ligne dans « Missions ») |
| Formations et diplômes | La liste du cursus |
| Distinctions & engagements | Prix, mandats, enseignement |
| Publications | Les articles : tribunes, actualités, discours |
| Rubriques | Les catégories de publication |
| Messages reçus | Les envois du formulaire de contact |

Le champ `ordre` définit l'affichage, du plus petit au plus grand.

## Réalisations et engagements

La page `/realisations/` liste les actions menées. Chaque entrée porte un
**lien de source obligatoire** : sur le site d'une élue, une réalisation qu'on
ne peut pas rattacher à une publication devient une affirmation invérifiable.
Le contenu initial se charge avec :

```bash
.venv/bin/python manage.py charger_cv
.venv/bin/python manage.py charger_realisations
```

Ces deux commandes sont idempotentes : les relancer met à jour sans dupliquer.

### Photos des réalisations et des expériences

Les champs existent, mais **aucune photo n'est fournie**. Les clichés
disponibles en ligne (ministère, presse togolaise, agences) sont protégés par
le droit d'auteur et ne peuvent pas être republiés ici. Wikimedia Commons ne
propose que deux portraits, aucune photo d'événement.

Les photos doivent donc venir des archives du cabinet et se téléversent depuis
l'administration, sur chaque réalisation et chaque expérience. La mise en page
est conçue pour rester soignée sans photo : une fiche sans image occupe toute
la largeur, elle ne laisse pas de moitié vide.

## Galerie

La page `/galerie/` affiche les photos avec apparition au défilement, zoom au
survol et agrandissement au clic (lightbox). Le JavaScript est autonome
(`static/js/galerie.js`, aucune bibliothèque externe) et se dégrade proprement :
sans lui, les images restent visibles et l'accessibilité clavier fonctionne.

Chaque photo vient soit d'un **téléversement admin** (clichés du cabinet), soit
d'un **fichier livré** avec le site (champ « Fichier livré », réservé aux images
Wikimedia). Le téléversement prime.

Trois images libres sont fournies (`charger_galerie`), toutes créditées :

```bash
.venv/bin/python manage.py charger_galerie
```

> **Droits.** N'ajouter que des photos dont Mme Dossou d'Almeida détient les
> droits, ou sous licence libre dûment créditée. Les photos de presse et du
> ministère sont protégées : les republier exposerait le site à une réclamation.
> Les champs « Crédit » et « Licence » de l'admin servent à cette attribution.

## Publier un article

Dans `/admin/` → **Publications** → *Ajouter*.

- **Titre** et **Texte** suffisent, tout le reste est facultatif.
- Le texte s'écrit normalement, un paragraphe par bloc séparé d'une ligne vide.
  Mise en forme facultative : `**gras**`, `*italique*`, `## Intertitre`,
  `[texte](https://adresse)`, `> citation`, listes à tirets.
- **Statut** : un article reste en *brouillon* tant qu'il n'est pas prêt. Il est
  alors invisible du public, mais consultable par son autrice une fois connectée,
  ce qui permet de se relire dans la mise en page réelle du site.
- **Date de publication** : une date future programme la parution.
- **À la une** : met l'article en tête de la page Publications.

L'adresse de la page se crée automatiquement à partir du titre.

### Articles de démonstration

Le site est livré avec trois articles fictifs, écrits pour valider la mise en
page. **Ce ne sont pas de vrais textes de Mme Dossou d'Almeida** et ils doivent
être supprimés avant la mise en ligne :

```bash
.venv/bin/python manage.py purger_demo --rubriques
```

`charger_cv` peut être relancée à tout moment : elle réécrit le contenu initial.
Attention, elle écrase les modifications faites dans l'admin.

## Coordonnées

Les champs e-mail et téléphone du profil sont volontairement vides. Le CV source
contient une adresse de domicile et des numéros personnels, à ne pas publier tels
quels. Renseigner depuis l'admin une adresse de contact professionnelle.

## Arrière-plan de l'accueil

`static/img/assemblee-nationale.jpg` montre l'entrée du **nouveau bâtiment de
l'Assemblée nationale**, photographiée en janvier 2019 par Kayi Lawson pour
Voice of America. Œuvre d'une agence fédérale américaine, elle est dans le
**domaine public** : aucune attribution n'est requise.

Elle est recadrée en panoramique sur l'arcade, légèrement désaturée, puis
assombrie côté CSS par un dégradé dense sous le texte et transparent à droite.
Les contrastes du bloc d'accueil restent au-delà du niveau AA (13,3:1 pour le
paragraphe, 8,1:1 pour la fonction) en desktop comme en mobile.

Pour la remplacer par une autre vue, téléverser le fichier dans le champ
« Image d'arrière-plan » du profil, dans l'admin — il prend automatiquement le
pas sur l'image livrée. Format paysage large, 1920 px minimum.

> Si l'image de remplacement est claire ou peu contrastée, revérifier la
> lisibilité du titre : le dégradé est calibré pour une façade de tons moyens.

## Portrait

`static/img/myriam-dossou.png` provient de Wikimedia Commons (auteur : Fdimpact),
sous licence **CC BY-SA 4.0**. L'attribution figure dans le pied de page via le
champ « Crédit photo » du profil. Le fond blanc d'origine a été détouré.
Remplacer par une photo officielle supprime cette contrainte : il suffit de
téléverser le portrait dans l'admin et de vider le champ « Crédit photo ».

## Mise en production

Variables d'environnement à définir :

```bash
DJANGO_SECRET_KEY=<clé aléatoire longue>
DJANGO_DEBUG=0
DJANGO_ALLOWED_HOSTS=exemple.tg,www.exemple.tg
DJANGO_CSRF_TRUSTED_ORIGINS=https://exemple.tg,https://www.exemple.tg
```

Puis `python manage.py collectstatic` et un serveur WSGI (gunicorn) derrière
nginx. Avec `DJANGO_DEBUG=0`, HTTPS, HSTS et les cookies sécurisés sont activés
automatiquement.
