FROM solr:8.10

COPY data/goodreads_milestone02.json /data/dataset.json

COPY startup.sh /scripts/startup.sh

COPY schema_milestone02.json /data/schema.json

EXPOSE 8983

ENTRYPOINT /scripts/startup.sh
