# @author MathieuV
#
# A <s>glorified queue</s> simple discrete simulator

from heapq import heappush as push, heappop as pop



class Simulator(object):

    def __init__(self):
        self._handler = lambda event: None
        self.time = 0
        self._queue = []

    def setHandler(self, handler):
        self._handler = handler

    def emit(self,event,delay=0):
        assert delay>=0, 'Cannot emit events in the past dude'
        push(self._queue, (self.time + delay, event))

    def __iter__(self):
        while len(self._queue):
            self.time, event = pop(self._queue)
            self._handler(event)
            yield