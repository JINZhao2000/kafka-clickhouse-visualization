from kafka import KafkaProducer

producer = KafkaProducer(bootstrap_servers='aliyunserver:9092')
f = open('./kdata/spotify_youtube.csv', 'r')
f.readline()
l = f.readline()
while l != "":
    producer.send(topic='spotify-youtube', value=l.encode("utf-8"))
    l = f.readline()

f.close()
