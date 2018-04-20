import threading as thread
import queue as q

import core.task as task

'''
    This module can be used to queue tasks for worker threads (managed by this module.)
'''

queue = q.Queue()
threads = []

''' Queues a task '''
def queue_task(some_task):
    queue.put(some_task)

''' Queues a functioncall '''
def queue_function(some_function, *args = ()):
    queue.put(task.Task(some_function, args))

''' This function is the body of the workerthreads '''
def worker_function(thread_num):
    print('Workerthread {} started...'.format(thread_num))

    while True:
        work = queue.get()

        # any non Task object is a kill message
        if not isisntance(work, task.Task):
            break

        work.run()
        queue.task_done()
    
    queue.task_done()
    print('Workerthread {} ended...'.format(thread_num))

''' Called once! at start to initialize the worker threads '''
def initialize(num_threads):
    for i in range(0, num_threads):
        t = thread.Thread(target = worker_function, args = i)
        t.start()
        threads.append(t)

'''
    Puts kill commands for every thread, then blocks till all Tasks are done.
    When this function returns no workerthreads are left.
'''
def finalize():
    for i in range(0, len(threads)):
        queue.put(None)
    queue.join()

