# Kafka-Clickhouse-Visualisation

## Preparation

1.   Kafka

     >   Kafka manager
     >
     >   aliyunserver:9000
     >
     >   Add cluster
     >
     >   -   name: spotify-youtube
     >   -   zk: aliyunserver:2181
     >   -   enable JMX
     >

     Dans container kafka

     ```bash
     docker exec -it kafka bash
     unset JMX_PORT
     cd /opt/kafka
     ./bin/kafka-topics.sh --create --zookeeper zookeeper:2181 --replication-factor 1 --partitions 1 --topic spotify-youtube
     ./bin/kafka-topics.sh --list --zookeeper zookeeper:2181
     ```

2.    Dans clickhouse

      ```sql
      CREATE TABLE queue (
       	ind UInt64,
           artist String,
           url_spotify String,
           track String,
           album String,
           album_type String,
           uri String,
           danceability Float64,
           energy Float64,
           _key Int64,
           loudness Float64,
           speechiness Float64,
           acousticness Float64,
           instrumentalness Float64,
           liveness Float64,
           valence Float64,
           tempo Float64,
           duration_ms UInt64,
           url_youtube String,
           title String, 
           channel String,
           _views UInt64,
           likes UInt64,
           comments UInt64,
           licensed String,
           official_video String,
           stream UInt64
       ) ENGINE = Kafka
       SETTINGS
       kafka_broker_list = '172.17.60.3:9092',
       kafka_topic_list = 'spotify-youtube',
       kafka_group_name = 'group1',
       kafka_format = 'CSV',
       kafka_num_consumers = 1,
       kafka_max_block_size = 65536,
       kafka_skip_broken_messages = 1;
       
       CREATE TABLE spotify_youtube on cluster cluster_1 (
       	ind UInt64,
           artist String,
           url_spotify String,
           track String,
           album String,
           album_type String,
           uri String,
           danceability Float64,
           energy Float64,
           _key Int64,
           loudness Float64,
           speechiness Float64,
           acousticness Float64,
           instrumentalness Float64,
           liveness Float64,
           valence Float64,
           tempo Float64,
           duration_ms UInt64,
           url_youtube String,
           title String, 
           channel String,
           _views UInt64,
           likes UInt64,
           comments UInt64,
           licensed String,
           official_video String,
           stream UInt64
       ) ENGINE = SummingMergeTree()
       order by ind;
       
       CREATE MATERIALIZED VIEW consumer TO spotify_youtube
       AS select * from queue;
      ```

3.    Visualization

## Import data

Dans le répertoire

```bash
 # pip3 install kafka-python
 python3 kafka-producer.py
```
