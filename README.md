=========
twitterwc
=========


Description
=========

This is a simple twitter word count script. 

The producer module connects to the twitter streaming API and consumes tweets as
they are issued, storing them to a message queue.

The consumer module connects to the queue, takes a message from it,
extracts the text portion of the tweet contained therein, and increments the
count for each word in the tweet (conditional on that word satisfying a very
simple set of constraints).

Although there is a single producer, multiple consumers can connect to the
queue and read tweets from it.

Initially, the idea was to multi-thread each consumer, but due to the limitations
of multi-threading in Python (as well as the difficulty of getting multiple
threads to work with MySQLdb), I abandoned the idea. You can still see the
remnants of threading constructs within the consumer code.


