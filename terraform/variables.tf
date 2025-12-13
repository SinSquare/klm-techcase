variable "project_id" {
  description = "The ID of the GCP project"
  type        = string
}

variable "region" {
  description = "The GCP region for Cloud Run and Cloud SQL"
  type        = string
  default     = "us-central1"
}

variable "cloud_run_service_name" {
  description = "Name for the Cloud Run service"
  type        = string
  default     = "klm-app"
}

variable "docker_image" {
  description = "The full path to your Docker image (e.g., gcr.io/my-project/my-image:latest)"
  type        = string
}

variable "db_instance_name" {
  description = "Name for the Cloud SQL instance"
  type        = string
  default     = "klm-postgres-db"
}

variable "db_url" {
  description = "Database URL"
  type        = string
  sensitive   = true # Mark as sensitive

variable "app_revision" {
  description = "Deployment revision"
  type        = string
}
