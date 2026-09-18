#!/usr/bin/env bash
# Préparation unique du projet Google Cloud pour le portfolio.
# À lancer une seule fois, depuis la racine du dépôt :
#   bash deploy/cloudrun/setup-gcp.sh
#
# Compte et projet sont fixés pour ce seul script (variables CLOUDSDK_*) :
# la configuration gcloud active du poste n'est pas modifiée.
set -euo pipefail

export CLOUDSDK_CORE_ACCOUNT="ablamawunyosekpona@gmail.com"
export CLOUDSDK_CORE_PROJECT="project-03951071-0256-4496-8a1"

PROJECT_ID="$CLOUDSDK_CORE_PROJECT"
REGION="europe-west1"
REPOSITORY="portfolio"
BUCKET="myriam-portfolio-medias-120815833998"
GITHUB_REPO="kokou-stm/portefolio-madame-myriam"
RUNTIME_SA_NAME="portfolio-run"
DEPLOY_SA_NAME="portfolio-deploy"
POOL="github"
PROVIDER="portfolio"

PROJECT_NUMBER=$(gcloud projects describe "$PROJECT_ID" --format='value(projectNumber)')
RUNTIME_SA="${RUNTIME_SA_NAME}@${PROJECT_ID}.iam.gserviceaccount.com"
DEPLOY_SA="${DEPLOY_SA_NAME}@${PROJECT_ID}.iam.gserviceaccount.com"

if [ "$(gcloud billing projects describe "$PROJECT_ID" --format='value(billingEnabled)')" != "True" ]; then
  echo "✗ Facturation désactivée sur ${PROJECT_ID}."
  echo "  La réactiver : https://console.cloud.google.com/billing/linkedaccount?project=${PROJECT_ID}"
  exit 1
fi

echo "→ API"
gcloud services enable run.googleapis.com artifactregistry.googleapis.com \
  secretmanager.googleapis.com storage.googleapis.com iamcredentials.googleapis.com \
  sts.googleapis.com

echo "→ Dépôt d'images"
gcloud artifacts repositories describe "$REPOSITORY" --location "$REGION" >/dev/null 2>&1 \
  || gcloud artifacts repositories create "$REPOSITORY" \
       --repository-format docker --location "$REGION" \
       --description "Images du portfolio Myriam Dossou d'Almeida"

echo "→ Bucket des médias (lecture publique, écriture réservée au service)"
gcloud storage buckets describe "gs://${BUCKET}" >/dev/null 2>&1 \
  || gcloud storage buckets create "gs://${BUCKET}" \
       --location "$REGION" --uniform-bucket-level-access
gcloud storage buckets add-iam-policy-binding "gs://${BUCKET}" \
  --member allUsers --role roles/storage.objectViewer >/dev/null

echo "→ Comptes de service"
gcloud iam service-accounts describe "$RUNTIME_SA" >/dev/null 2>&1 \
  || gcloud iam service-accounts create "$RUNTIME_SA_NAME" --display-name "Portfolio — exécution Cloud Run"
gcloud iam service-accounts describe "$DEPLOY_SA" >/dev/null 2>&1 \
  || gcloud iam service-accounts create "$DEPLOY_SA_NAME" --display-name "Portfolio — déploiement GitHub Actions"

# Exécution : lire les secrets, écrire dans le bucket des médias. Rien d'autre.
gcloud storage buckets add-iam-policy-binding "gs://${BUCKET}" \
  --member "serviceAccount:${RUNTIME_SA}" --role roles/storage.objectAdmin >/dev/null

# Déploiement : publier des images, gérer Cloud Run, agir en tant que compte d'exécution.
for ROLE in roles/run.admin roles/artifactregistry.writer; do
  gcloud projects add-iam-policy-binding "$PROJECT_ID" \
    --member "serviceAccount:${DEPLOY_SA}" --role "$ROLE" --condition None >/dev/null
done
gcloud iam service-accounts add-iam-policy-binding "$RUNTIME_SA" \
  --member "serviceAccount:${DEPLOY_SA}" --role roles/iam.serviceAccountUser >/dev/null

echo "→ Secrets (saisie masquée ; Entrée vide = conserver la valeur existante)"
for PAIRE in \
  "portfolio-database-url:DATABASE_URL" \
  "portfolio-django-secret-key:DJANGO_SECRET_KEY" \
  "portfolio-email-host-user:EMAIL_HOST_USER" \
  "portfolio-email-host-password:EMAIL_HOST_PASSWORD"; do
  SECRET="${PAIRE%%:*}"
  LIBELLE="${PAIRE##*:}"
  gcloud secrets describe "$SECRET" >/dev/null 2>&1 \
    || gcloud secrets create "$SECRET" --replication-policy automatic >/dev/null
  read -r -s -p "  ${LIBELLE} : " VALEUR; echo
  if [ -n "$VALEUR" ]; then
    printf '%s' "$VALEUR" | gcloud secrets versions add "$SECRET" --data-file=- >/dev/null
  fi
  gcloud secrets add-iam-policy-binding "$SECRET" \
    --member "serviceAccount:${RUNTIME_SA}" --role roles/secretmanager.secretAccessor >/dev/null
done

echo "→ Workload Identity Federation (GitHub → Google, sans clé stockée)"
gcloud iam workload-identity-pools describe "$POOL" --location global >/dev/null 2>&1 \
  || gcloud iam workload-identity-pools create "$POOL" --location global --display-name "GitHub Actions"
gcloud iam workload-identity-pools providers describe "$PROVIDER" \
    --location global --workload-identity-pool "$POOL" >/dev/null 2>&1 \
  || gcloud iam workload-identity-pools providers create-oidc "$PROVIDER" \
       --location global --workload-identity-pool "$POOL" \
       --issuer-uri "https://token.actions.githubusercontent.com" \
       --attribute-mapping "google.subject=assertion.sub,attribute.repository=assertion.repository" \
       --attribute-condition "assertion.repository=='${GITHUB_REPO}'"
gcloud iam service-accounts add-iam-policy-binding "$DEPLOY_SA" \
  --role roles/iam.workloadIdentityUser \
  --member "principalSet://iam.googleapis.com/projects/${PROJECT_NUMBER}/locations/global/workloadIdentityPools/${POOL}/attribute.repository/${GITHUB_REPO}" >/dev/null

echo
echo "✓ Terminé. Secrets à créer dans GitHub (Settings → Secrets → Actions) :"
echo "  GCP_WORKLOAD_IDENTITY_PROVIDER = projects/${PROJECT_NUMBER}/locations/global/workloadIdentityPools/${POOL}/providers/${PROVIDER}"
echo "  GCP_DEPLOY_SA                  = ${DEPLOY_SA}"
