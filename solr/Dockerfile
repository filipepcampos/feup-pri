FROM solr:8.10

COPY data/goodreads_milestone03.json /data/dataset.json

COPY startup.sh /scripts/startup.sh

COPY schema_milestone03.json /data/schema.json

EXPOSE 8983

ENTRYPOINT /scripts/startup.sh
