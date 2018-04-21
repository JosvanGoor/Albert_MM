import threading as thread

'''
    Represents a Task object which can be used to push jobs on the workerthreads.
    The task must make sure any results appear at the right location themselves, the task does not stores any return value
'''

class Task:

    ''' Initializes with a function and unnamed arguments '''
    def __init__(self, func, *args):
        self.function = func
        self.arguments = args
        self.state = "waiting"
        self.tasklock = thread.Lock()
        self.finished = False

    def set_finished(self):
        with self.tasklock:
            self.finished = True
            self.state = "done"

    def set_state(self, state):
        with self.tasklock:
            self.state = state

    def finished(self):
        with self.tasklock:
            return self.finished

    def state(self):
        with self.tasklock:
            return self.state

    def name(self):
        return self.function.__name__

    def run(self):
        self.set_state("running " + self.function.__name__)
        self.function(*self.arguments)
        self.set_finished()