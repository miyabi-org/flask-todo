# Google Cloud Resource Cleanup Instructions

This document provides instructions for cleaning up Google Cloud resources associated with the Flask Todo application as part of the repository deletion process.

## Resources to be Deleted

The cleanup script will delete the following resources:

1. **Cloud Run service**: `flask-todo` in region `asia-northeast1`
2. **Google Cloud Storage bucket**: `todo-app-images`
3. **Database**: The `todo` database (but NOT the SQL Cloud instance itself)

## Prerequisites

Before running the cleanup script, ensure you have:

1. [Google Cloud SDK](https://cloud.google.com/sdk/docs/install) installed
2. Authenticated with Google Cloud: `gcloud auth login`
3. Proper permissions to delete the resources
4. The name of your SQL Cloud instance

## Running the Cleanup Script

1. Make sure the cleanup script is executable:
   ```
   chmod +x cleanup_cloud_resources.sh
   ```

2. Run the script:
   ```
   ./cleanup_cloud_resources.sh
   ```

3. When prompted, enter your SQL Cloud instance name and confirm the deletion.

## Manual Cleanup (if script doesn't work)

If you prefer to clean up resources manually, follow these steps:

### Delete Cloud Run Service

```bash
gcloud run services delete flask-todo --region=asia-northeast1
```

### Delete Cloud Storage Bucket

```bash
gsutil -m rm -r gs://todo-app-images
```

### Delete Database (but not the SQL instance)

```bash
gcloud sql databases delete todo --instance=YOUR_SQL_INSTANCE_NAME
```

## Verification

After running the cleanup script, you can verify that resources have been removed:

1. Check if the Cloud Run service exists:
   ```
   gcloud run services describe flask-todo --region=asia-northeast1
   ```

2. Check if the GCS bucket exists:
   ```
   gsutil ls gs://todo-app-images
   ```

3. Check if the database exists:
   ```
   gcloud sql databases list --instance=YOUR_SQL_INSTANCE_NAME
   ```

## Note

As per requirements, the SQL Cloud instance itself is NOT deleted, only the database within it.