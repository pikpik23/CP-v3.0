# scheduler

from threading import Timer

cont = True


def save():
    if cont:
        s = Timer(5.0, save)
        s.daemon = True
        s.start()
        print("Saved")


save()

x = input()
print(x)
cont = False


'''
import sched
import time
s = sched.scheduler(time.time, time.sleep)


def print_time(a='default'):
    print("From print_time", time.time(), a)


def print_some_times():
    print(time.time())
    s.enter(10, 1, print_time)
    s.enter(5, 2, print_time, argument=('positional',))
    s.enter(5, 1, print_time, kwargs={'a': 'keyword'})
    s.run()
    print(time.time())


print_some_times()
'''
