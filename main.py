import json

import pika
from crawler import Crawler
from config import RabbitMQ

crawler = Crawler()




def callback(ch, method, properties, body):
    link = json.loads(body)
    # print(link)
    result = crawler.get_ad(link)
    # print(result)
    if result:
        ch.basic_publish(exchange='',
                         routing_key=RabbitMQ.RABBIT_MQ_PUBLISH_QUEUE, body=json.dumps(result, ensure_ascii=False),
                         properties=pika.BasicProperties(delivery_mode=2))

    ch.basic_ack(delivery_tag=method.delivery_tag)


if __name__ == "__main__":
    credentials = pika.PlainCredentials(RabbitMQ.RABBIT_MQ_LOGIN,
                                        RabbitMQ.RABBIT_MQ_PASSWORD)
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host=RabbitMQ.RABBIT_MQ_HOST,
                                  port=RabbitMQ.RABBIT_MQ_PORT,
                                  credentials=credentials))

    channel = connection.channel()
    channel.basic_qos(prefetch_count=1)
    channel.queue_declare(queue=RabbitMQ.RABBIT_MQ_PUBLISH_QUEUE)
    channel.basic_consume(RabbitMQ.RABBIT_MQ_CONSUMER_QUEUE, callback, auto_ack=False)
    channel.start_consuming()
