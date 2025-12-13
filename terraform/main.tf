# Configure the Google Provider
provider "google" {
  project = var.project_id
  region  = var.region
}

# --- 1. Enable Required APIs ---
# These are the APIs required for Cloud Run and Cloud SQL
resource "google_project_service" "apis" {
  for_each                   = toset([
    "cloudresourcemanager.googleapis.com",
    "run.googleapis.com",
    "sqladmin.googleapis.com",
    "iam.googleapis.com" # Required to manage service accounts/IAM
  ])
  project                    = var.project_id
  service                    = each.key
  disable_on_destroy         = false # Set to true to disable APIs on destroy
  disable_dependent_services = false
}

# --- 2. Cloud SQL PostgreSQL Instance ---
resource "google_sql_database_instance" "postgres_instance" {
  database_version = "POSTGRES_18"
  name             = var.db_instance_name
  project          = var.project_id
  region           = var.region
  settings {
    tier = "db-f1-micro" # Smallest size for testing
    # Use private IP only for better security and performance
    ip_configuration {
      ipv4_enabled    = false
      private_network = "default"
    }
    disk_size = 10
  }

  depends_on = [google_project_service.apis]
}

# Create a database within the instance
resource "google_sql_database" "database" {
  instance = google_sql_database_instance.postgres_instance.name
  name     = var.db_name
  project  = var.project_id
}

# Create a database user
resource "google_sql_user" "db_user" {
  instance = google_sql_database_instance.postgres_instance.name
  name     = var.db_user
  password = var.db_password
  project  = var.project_id
}

# --- 3. Cloud Run Service Account and IAM ---

# Cloud Run uses a default service account in the format PROJECT_NUMBER-compute@developer.gserviceaccount.com
# To grant permissions explicitly, we'll create a new service account.
resource "google_service_account" "cloud_run_sa" {
  account_id   = "${var.cloud_run_service_name}-sa"
  display_name = "Service Account for Cloud Run ${var.cloud_run_service_name}"
  project      = var.project_id

  depends_on = [google_project_service.apis]
}

# Grant the Cloud SQL Client role to the Cloud Run service account.
# This is crucial for the built-in Cloud SQL proxy to connect.
resource "google_project_iam_member" "cloud_sql_client_role" {
  project = var.project_id
  role    = "roles/cloudsql.client"
  member  = "serviceAccount:${google_service_account.cloud_run_sa.email}"

  depends_on = [google_project_service.apis]
}

# --- 4. Cloud Run v2 Service Deployment ---

resource "google_cloud_run_v2_service" "cloud_run_service" {
  name     = var.cloud_run_service_name
  location = var.region
  project  = var.project_id

  template {
    # Refer to the service account created above
    service_account = google_service_account.cloud_run_sa.email
    revision = var.app_revision

    containers {
      image = var.docker_image
      ports {
        container_port = 8080 # Update this to your application's port
      }
      env {
        name  = "DB_URL"
        value =  var.db_url
      }
    }

    # Connect Cloud Run to Cloud SQL using the instance connection name
    # The image below illustrates this secure connection pattern.
    
    volumes {
      name = "cloudsql"
      cloud_sql_instance {
        # The full connection name of the Cloud SQL instance
        instance = google_sql_database_instance.postgres_instance.connection_name
      }
    }
  }

  lifecycle {
    ignore_changes = [
      template[0].containers[0].image,
      client,
      client_version,
    ]
  }

  # Allow unauthenticated access (make it public)
  traffic {
    type    = "TRAFFIC_TARGET_ALLOCATION_TYPE_LATEST"
    percent = 100
  }

  depends_on = [
    google_project_iam_member.cloud_sql_client_role,
    google_sql_database.database
  ]
}

# --- 5. Output ---

output "cloud_run_url" {
  description = "The URL of the deployed Cloud Run service"
  value       = google_cloud_run_v2_service.cloud_run_service.uri
}

output "db_connection_name" {
  description = "The connection name for the Cloud SQL instance"
  value       = google_sql_database_instance.postgres_instance.connection_name
}
