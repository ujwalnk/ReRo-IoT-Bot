from multiprocessing import Process

class Runner():

    user_process : Process

    def __init__(self, target = None):
        if target:
            self.user_process = Process(target=target)

    def set_target(self, target):
        self.user_process = Process(target)

    def run(self):
        print(self)
        self.user_process.start()

    def kill(self):
        self.user_process.kill()

    