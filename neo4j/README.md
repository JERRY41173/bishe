```
docker run -d --name neo4j \
-p 7474:7474 -p 7687:7687 \
-v /srv/bishe/neo4j/data:/data \
-v /srv/bishe/neo4j/logs:/logs \
-v /srv/bishe/neo4j/conf:/var/lib/neo4j/conf \
-v /srv/bishe/neo4j/import:/var/lib/neo4j/import \
--env NEO4J_PLUGINS='["apoc"]' \
--volume=/srv/bishe/neo4j/plugins:/plugins \
--env NEO4J_AUTH=neo4j/password \
neo4j:5.26.5-community
```