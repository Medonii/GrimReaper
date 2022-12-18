import sched, time
from random import uniform
s = sched.scheduler(time.time, time.sleep)

def get_position():
    position_x = uniform(19.826880444423622, 20.085362820563827)
    position_y = uniform(50.01209375446622, 50.11138495929301)
    print(position_x)
    print(position_y)
    return '(' + str(position_x) + ', ' + str(position_y) + ')'

def it_moved(sc):
    print("Doing stuff...")
    get_position()
    sc.enter(1, 1, it_moved, (sc,))

s.enter(1, 1, it_moved, (s,))
s.run()