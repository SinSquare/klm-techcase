## Cloud Infra Design ##
![Cloud Infra Design](public/infra.png)


## Starting the containers ##
```bash
docker-compose up
```

## OpenAPI docs ##
public/index.html


## Testing the API ##
```bash
curl -H "Content-Type: application/json" \
  --request POST \
  --data '{"text":"test"}' \
  http://localhost:80/notes
```

## CI/CD Pipeline Design ##
By deafult the main and versioned branches should be protected, any work should be pushed to issu branches, and merged to main/version.
The pipeline should be separated into multiple stages, triggered by different actions.

- Testing/linting
- Building and publishing Docker image
- Deploying the application

Each stage should depend on the previous stage (eg. a failure should stop the pipeline).
General rules:

- testing should run on every push on any branch
- building/publishing might be separated, so that dev images and versioned images are published separately
- building prod images should be triggeres by creating a tag
- deployment should be triggeres by creating a tag

## Design Choices & Justifications ##
I had 3 main ideas: Cloud Function, Cloud Run and Kubernetes. Kubernetes adds some overhead and complexity on development, so I decided to not use it. Between Cloud Function and Cloud Run the deciding factor was that for Function only a single endpoint could be defined, so it would again add some overhead from a code oraganization and testing perspective. Cloud Run runs a containerized application, and for FastApi application it's fairly easy to create one.

I've chosen a managed DB solution (Postgres) as managed services are the main selling point of cloud infrastructure.


Secret management could be done using google_secret_manager_secret, Hashicorp Vault or alternativelt using GitHub secrets

## Testing ##

for running the tests no other service should be running in Docker (will create pg service)

```bash
poetry run pytest --cov-report=term-missing --cov=klm_techcase
```

## Exporting dependencies ##
```bash
poetry export --without-hashes --output requirements.txt
poetry export --without-hashes --only dev --output requirements-dev.txt
```

## Formatting ##
```bash
ruff check
ruff format
```
