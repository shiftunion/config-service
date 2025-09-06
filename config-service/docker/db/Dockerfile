FROM postgres:16-alpine

ENV POSTGRES_DB=configsvc-alpha
ENV POSTGRES_USER=postgres
ENV POSTGRES_PASSWORD=postgres

EXPOSE 5432

COPY migrations/*.sql /docker-entrypoint-initdb.d/

