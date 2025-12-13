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
