import random
import time
import collections
import sys
from queue import Queue

import threading

def io_bound(n=3, name="name"):
    time.sleep(1)
    print(n, name)
    return n

def number_generator(n):
    """ A co-routine that generates numbers in range 1... n """
    
    for i in range(1, n+1):
        yield i

def square_mapper(numbers):
    """ A co-routine task for converting numbers to squares """
    
    for n in numbers:
        yield io_bound, (n*n, "square_mapper", )
    
def prime_filter(numbers):
    """ A co-routine which yields prime numbers """
    
    primes = []
    for n in numbers:
        if n % 2 == 0: continue
        flag = True
        for i in range(3, int(n**0.5+1), 2):
            if n % i == 0:
                flag = False
                break
        if flag:
            yield io_bound, (n, "prime_filter",)

def scheduler(tasks, runs=10000):
    """ Basic task scheduler for co-routines """
    
    results = collections.defaultdict(list)
    
    for i in range(runs):
        for t in tasks:
            try:
                results['task'].append(t)
            except StopIteration:
                break
    return results

class EventLoop(Queue):
    def adds(self, tasks):
        for task in tasks:
            self.put(task)

    def start(self):
        while True:
            coro = self.get()
            try:
                print('hi: ', coro.start())
            except RuntimeError as e:
                break

if __name__ == "__main__":
    tasks = []
    start = time.clock()
    limit = 100
    for task, params in square_mapper(number_generator(limit)):
        tasks.append(threading.Thread(target=task, args=params))
    for task, params in prime_filter(number_generator(limit)):
        tasks.append(threading.Thread(target=task, args=params))

    results = scheduler(tasks, runs=limit)
    eventLoop = EventLoop()
    t = threading.Thread(target=eventLoop.start, daemon=True)
    t.start()

    for task_name, tasks in results.items():
        for task in tasks:
            eventLoop.put(task)
    print("Thread Join")
    t.join()
    end = time.clock()
    print("Time taken=>", end-start)
    for i in range(100):
        time.sleep(0.01)
        print('Another dummy task: ', i)