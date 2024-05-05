import time
from threading import Thread
from statemachine import StateMachine, State

def timer(sm, seconds, action):
    s = 0
    while s < seconds:
        s += 1
        time.sleep(1)
    
    sm.send(action)

class VolumeStateMachine(StateMachine):
    idle = State(initial=True)
    changing_volume = State()

    enter_change_volume = idle.to(changing_volume)
    leave_change_volume = changing_volume.to(idle)

    def on_enter_changing_volume(self):
        Thread(target=timer, args=(self, 5, "leave_change_volume")).start()