"""Cooperative Asynchronous Event Loop & Task Scheduler.
100% Python Standard Library.
"""

import heapq
import collections
import time

class MiniEventLoop:
    """Cooperative asynchronous event loop with microtask queue and timer heap."""
    class Future:
        def __init__(self):
            self._done = False
            self._result = None
            self._callbacks = []

        def done(self):
            return self._done

        def result(self):
            return self._result

        def set_result(self, val):
            self._result = val
            self._done = True
            for cb in self._callbacks:
                cb(self)

        def add_done_callback(self, cb):
            if self._done:
                cb(self)
            else:
                self._callbacks.append(cb)

    def __init__(self):
        self._ready = collections.deque()
        self._timers = []
        self._counter = 0

    def call_soon(self, callback, *args):
        self._ready.append((callback, args))

    def call_later(self, delay, callback, *args):
        self._counter += 1
        heapq.heappush(self._timers, (time.time() + delay, self._counter, callback, args))

    def run_until_complete(self, target_future):
        while not target_future.done():
            now = time.time()
            while self._timers and self._timers[0][0] <= now:
                _, _, cb, args = heapq.heappop(self._timers)
                self._ready.append((cb, args))

            if self._ready:
                cb, args = self._ready.popleft()
                cb(*args)
            elif not target_future.done() and self._timers:
                time.sleep(0.001)

        return target_future.result()
