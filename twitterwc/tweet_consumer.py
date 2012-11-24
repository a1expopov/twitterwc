#!/usr/bin/env python

import pika
import redis
import threading as th
import re
import dateutil.parser as date_parser
import time
import MySQLdb
import json
import tpconf


class Worker(th.Thread):
    
    def __init__(self, connection):
        th.Thread.__init__(self)
        self.store = MySQLdb.connect(
            db=tpconf.FREQUENCY_STORE['db'],
            **tpconf.FREQUENCY_STORE['connpar'])
        self.cursor = self.store.cursor()
        self.channel = connection.channel()
        self.channel.queue_declare(tpconf.QUEUE_NAME)
        self.channel.basic_consume(self.process_tweet, queue=tpconf.QUEUE_NAME)

    def run(self):
        print '{} starting work!'.format(self.name)
        self.channel.start_consuming()

    def process_tweet(self, ch, method, properties, body):
        
        try: 
            tweet = json.loads(body)
            
            if 'text' in tweet:        

                # filter out words that are >= 5 alpahnumeric characters            
                text = [w.lower() for w in tweet['text'].split()
                        if re.search(r'\w{5,}', w)
                        and not 'http://' in w
                        and all(ord(c) < 127 for c in w)
                        and not w.startswith('@')]
                
                time = date_parser.parse(tweet['created_at'])

                seen = set()
                
                query = 'INSERT INTO {} VALUES (%s, %s, %s, %s, %s, %s)'.format(
                    tpconf.FREQUENCY_STORE['table']['name'])   
                
                db_tuples = []

                for i, word in enumerate(text):
                    
                    # increase total count of word
                    server.incr('{}:total'.format(word), 1)                

                    # increase unique count of word
                    if not word in seen:
                        server.incr('{}:tweets'.format(word), 1)
                        seen.add(word)

                    # keep track of the words it commonly appears with
                    for j, other_word in enumerate(text):
                        if not j == i:
                            server.zadd(word, other_word, 1)
                    
                    db_tuples.append(
                        (time.year, time.month, time.day,
                         time.hour, time.minute, word))
                               
                self.cursor.executemany(query, db_tuples)
                self.store.commit()
        except:
            raise


if __name__ == '__main__':

    server = redis.Redis()

    connection = pika.BlockingConnection(pika.ConnectionParameters(
        tpconf.RABBIT_SERVER))
    
    for i in range(tpconf.PER_CONSUMER_THREADS):
        Worker(connection).start()
    



