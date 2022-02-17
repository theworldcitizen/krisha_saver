import os


class RabbitMQ:
    RABBIT_MQ_HOST = os.environ.get('RABBIT_MQ_HOST', '192.168.88.147')
    RABBIT_MQ_PORT = os.environ.get('RABBIT_MQ_PORT', 5672)
    RABBIT_HTTP_PORT = os.environ.get('RABBIT_HTTP_PORT', 15672)
    RABBIT_MQ_CONSUMER_QUEUE = os.environ.get('RABBIT_MQ_CONSUMER_QUEUE', 'krisha_publish')
    RABBIT_MQ_PUBLISH_QUEUE = os.environ.get('RABBIT_MQ_PUBLISH_QUEUE', 'krisha_saver')
    RABBIT_MQ_LOGIN = os.environ.get('RABBIT_MQ_LOGIN', 'rabbit')
    RABBIT_MQ_PASSWORD = os.environ.get('RABBIT_MQ_PASSWORD', 'rabbit')
