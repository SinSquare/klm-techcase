FROM python:3.10
ENV DB_URL=${APP_ENV}
WORKDIR /code
COPY ./requirements.txt /code/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY ./klm_techcase /code/klm_techcase
COPY ./migrations /code/migrations
COPY ./alembic.ini /code/alembic.

ADD startup.sh /
RUN chmod +x /startup.sh

ENTRYPOINT ["/startup.sh"]
