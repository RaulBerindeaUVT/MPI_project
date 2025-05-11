import os
from itertools import combinations
import time
from multiprocessing import Process, Queue
import re


def resolution_worker(clauses, queue):
    result = resolution(clauses)
    queue.put(result)


def run_resolution_with_timeout(clauses, timeout=10):
    queue = Queue()
    p = Process(target=resolution_worker, args=(clauses, queue))
    p.start()
    p.join(timeout)

    if p.is_alive():
        p.terminate()
        p.join()
        return None
    else:
        return queue.get()

def resolve(ci, cj):
    resolvents = []
    for li in ci:
        if -li in cj:
            resolvent = (ci - {li}) | (cj - {-li})
            if not contains_complementary_literals(resolvent):
                resolvents.append(resolvent)
    return resolvents

def contains_complementary_literals(clause):
    return any(-l in clause for l in clause)

def resolution(clauses, time_limit=10):
    start_time = time.time()
    new = set()
    clauses = [frozenset(c) for c in clauses]
    processed = set(clauses)

    while True:

        if time.time() - start_time > time_limit:
            print("Resolution timed out.")
            return None

        pairs = list(combinations(processed, 2))
        for (ci, cj) in pairs:
            resolvents = resolve(ci, cj)
            for r in resolvents:
                if not r:
                    return False
                if r not in processed:
                    new.add(frozenset(r))
        if new.issubset(processed):
            return True
        processed.update(new)
        new.clear()