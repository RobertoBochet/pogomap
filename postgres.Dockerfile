FROM mdillon/postgis:11-alpine

COPY ./pogomap/sql/* /docker-entrypoint-initdb.d/