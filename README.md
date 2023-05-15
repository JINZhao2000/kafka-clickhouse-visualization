# Kafka-Clickhouse-Visualisation

## Modify ip config
1. `clickhouse/clickhouse_config.xml` line 66
2. `grafana/provisioning/datasources/clickhhouse.yml` line 8
3. `kafka-producer.py` line 3
4. This file line 19, 24, 71

In visual machine, do
```bash
export EXPOSED_HOSTNAME=innerip
```
## Preparation

1.   Kafka

     >   Kafka manager
     >
     >   publicip:9000
     >
     >   Add cluster
     >
     >   -   name: spotify-youtube
     >   -   zk: publicip:2181
     >   -   enable JMX
     >

     In container kafka

     ```bash
     docker exec -it kafka bash
     unset JMX_PORT
     cd /opt/kafka
     ./bin/kafka-topics.sh --create --zookeeper zookeeper:2181 --replication-factor 1 --partitions 1 --topic spotify-youtube
     ./bin/kafka-topics.sh --list --zookeeper zookeeper:2181
     ```

2.    In clickhouse

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
       kafka_broker_list = 'innerip:9092',
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

In the remote machine

```bash
 # pip3 install kafka-python
 python3 kafka-producer.py
```

## Run
1. modify all config of ip
2. copy this directory to remote machine
3. export EXPOSED_HOSTNAME as your inner ip address
4. use `docker compose create`
5. use `docker compose start`
6. do the part of preparation
7. do import data
8. visualize in grafana