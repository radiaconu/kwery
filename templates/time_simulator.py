# -*- coding: utf-8 -*-
"""
Created on Tue Apr 28 19:14:06 2015

@author: Raluca Diaconu (diaconu.raluca@gmail.com)

A time correct simulator after simulator.py
"""


from heapq import heappush as push, heappop as pop
from time import time

class Simulator(object):

    def __init__(self, _start_event_time):
        self._handler = lambda event: None
        self.start_real_time = time.time()
        self.start_event_time= _start_event_time
        self._queue = []

    def setHandler(self, handler):
        self._handler = handler

    def emit(self,event,delay=0):
        assert delay>=0, 'Cannot emit events in the past dude'
        push(self._queue, (self.time + delay, event))

    def __iter__(self):
        while len(self._queue):
            event_time, event = pop(self._queue)
            if event_time - self.start_event_time > time.time() - self.start_time:
                self._handler(event)
            else:
                push(self._queue, (event_time, event))
            yield