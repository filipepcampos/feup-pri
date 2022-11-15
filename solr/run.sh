#!/bin/sh

docker stop goodreads || true
docker build -t goodreads .
docker run -d --rm --name goodreads -p 8983:8983 goodreads
