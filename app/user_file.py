from app.header.header import dump
import signal
import time

def main():
    dump("hello")
    while True:
        time.sleep(5)
        dump("asdf")


def __runner__():
    def handler(signum, frame):
        raise TimeoutError("Function execution timed out")

    signal.signal(signal.SIGALRM, handler)
    signal.alarm(1800)

    try:
        main()
    except TimeoutError as e:
        dump("Exception:" + str(e))
    finally:
        signal.alarm(0)
