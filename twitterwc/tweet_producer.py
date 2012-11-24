#!/usr/bin/env python

import pika
import tweetstream
import json
import tpconf


def create_channel():
    connection = pika.BlockingConnection(pika.ConnectionParameters(
        tpconf.RABBIT_SERVER))
    channel = connection.channel()
    channel.queue_declare(tpconf.QUEUE_NAME)
    return channel


def create_stream():
    return tweetstream.SampleStream(tpconf.USERNAME, tpconf.PASSWORD)


def enqueue_tweets(stream, channel):
    for tweet in stream:
        channel.basic_publish(
            exchange='', routing_key=tpconf.QUEUE_NAME, body=json.dumps(tweet))        


if __name__ == '__main__':
    
    restart = True

    channel = create_channel()
    
    while restart:
        stream = create_stream()
        try:
            enqueue_tweets(stream, channel)
        except tweetstream.ConnectionError:
            print 'Restarting twitter connection'
        else:
            restart = False
    
    connection.close()

