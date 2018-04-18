import atexit
import queue as q
import threading as thread
import time

class Task:

    def __init__(self, func, *args):
        self.killtask = False
        self.function = func
        self.arguments = args
        self.state = "waiting"
        self.tasklock = thread.Lock()
        self.done = False
        self.rval = None # function rval

    def set_done(self):
        with self.tasklock:
            self.done = True
            self.state = "done"

    def set_state(self, state):
        with self.tasklock:
            self.state = state

    def is_done(self):
        with self.tasklock:
            return self.done

    def state(self):
        with self.tasklock:
            return self.state

    def run(self):
        self.set_state("running " + self.function.__name__)
        print("running " + self.function.__name__)
        self.rval = self.function(*self.arguments)
        self.set_done()

class Worker:
    queue = q.Queue()
    threads = []
    max_threads = 4

    @classmethod
    def run_func(klass):
        while True:
            task = klass.queue.get()
            if task.killtask:
                break
            
            task.run()
            klass.queue.task_done()
        
        print('quitted!')
        klass.queue.task_done()

    @classmethod
    def static_init(klass):
        for i in range(0, klass.max_threads):
            t = thread.Thread(target=klass.run_func)
            t.start()
            klass.threads.append(t)

    @classmethod
    def static_quit(klass):
        for i in range(0, klass.max_threads):
            task = Task(None, None)
            task.killtask = True
            klass.queue.put(task)
            klass.queue.join()

    def wait(self, var):
        task = Task(time.sleep, var)
        Worker.queue.put(task)


Worker.static_init()
if __name__ == "__main__":
    w = Worker()
    for i in range(1, 7):
        w.wait(i)
    
Worker.static_quit()