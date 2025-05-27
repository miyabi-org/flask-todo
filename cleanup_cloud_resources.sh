#!/bin/bash
# This script deletes the Google Cloud resources associated with the Flask Todo application
# It will delete: 
# - The Cloud Run service
# - The Google Cloud Storage bucket
# - The database (but NOT the Cloud SQL instance itself)

set -e  # Exit on any error

# Color codes for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'  # No Color

echo -e "${GREEN}===== Google Cloud Resources Cleanup Script =====${NC}"
echo -e "This script will delete the deployed Flask TODO application resources:"
echo -e "  - ${YELLOW}Cloud Run service${NC}: flask-todo (region: asia-northeast1)"
echo -e "  - ${YELLOW}Cloud Storage bucket${NC}: todo-app-images"
echo -e "  - ${YELLOW}Database${NC}: 'todo' database (but NOT the SQL instance)"
echo -e "\n${RED}WARNING: This action cannot be undone!${NC}\n"

# Function to check if gcloud is installed
check_gcloud() {
  if ! command -v gcloud &> /dev/null; then
    echo -e "${RED}Error: Google Cloud SDK is not installed.${NC}"
    echo "Please install it from: https://cloud.google.com/sdk/docs/install"
    exit 1
  fi
}

# Check if user is logged into gcloud
check_auth() {
  account=$(gcloud auth list --filter="status:ACTIVE" --format="value(account)" 2>/dev/null)
  if [[ -z "$account" ]]; then
    echo -e "${RED}Error: You are not logged into Google Cloud.${NC}"
    echo "Please run: gcloud auth login"
    exit 1
  fi
  echo -e "${GREEN}Authenticated as:${NC} $account"
}

# Confirm before proceeding
confirm_deletion() {
  read -p "Proceed with deletion? (y/N) " -n 1 -r
  echo
  if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo -e "${YELLOW}Operation cancelled.${NC}"
    exit 0
  fi
}

# Get SQL instance name from user
get_sql_instance() {
  read -p "Enter the SQL instance name (required to delete the database): " sql_instance
  if [[ -z "$sql_instance" ]]; then
    echo -e "${RED}Error: SQL instance name cannot be empty.${NC}"
    exit 1
  fi
}

# Delete Cloud Run service
delete_cloud_run() {
  echo -e "\n${YELLOW}Deleting Cloud Run service 'flask-todo'...${NC}"
  if gcloud run services describe flask-todo --region=asia-northeast1 &>/dev/null; then
    gcloud run services delete flask-todo \
      --region=asia-northeast1 \
      --quiet
    echo -e "${GREEN}Cloud Run service deleted successfully.${NC}"
  else
    echo -e "${YELLOW}Cloud Run service 'flask-todo' not found or already deleted.${NC}"
  fi
}

# Delete GCS bucket
delete_bucket() {
  echo -e "\n${YELLOW}Deleting Cloud Storage bucket 'todo-app-images'...${NC}"
  if gsutil ls gs://todo-app-images &>/dev/null; then
    gsutil -m rm -r gs://todo-app-images
    echo -e "${GREEN}Cloud Storage bucket deleted successfully.${NC}"
  else
    echo -e "${YELLOW}Cloud Storage bucket 'todo-app-images' not found or already deleted.${NC}"
  fi
}

# Delete database, but not the SQL instance
delete_database() {
  echo -e "\n${YELLOW}Deleting database 'todo' from SQL instance '$sql_instance'...${NC}"
  if gcloud sql databases list --instance="$sql_instance" | grep -q "todo"; then
    gcloud sql databases delete todo \
      --instance="$sql_instance" \
      --quiet
    echo -e "${GREEN}Database 'todo' deleted successfully.${NC}"
    echo -e "${GREEN}SQL instance '$sql_instance' has been preserved as requested.${NC}"
  else
    echo -e "${YELLOW}Database 'todo' not found or already deleted.${NC}"
  fi
}

# Main script execution
check_gcloud
check_auth
get_sql_instance
confirm_deletion

# Perform deletions
delete_cloud_run
delete_bucket
delete_database

echo -e "\n${GREEN}Cleanup completed successfully!${NC}"
echo -e "The following resources have been deleted:"
echo -e "  - Cloud Run service: flask-todo"
echo -e "  - Cloud Storage bucket: todo-app-images"
echo -e "  - Database: todo"
echo -e "\nThe SQL Cloud instance '$sql_instance' has been preserved as requested."