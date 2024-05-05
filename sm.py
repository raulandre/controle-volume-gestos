import time
from threading import Thread
from statemachine import StateMachine, State

def timer(sm, seconds, action):
    try:
        s = 0
        while s < seconds:
            s += 1
            time.sleep(1)
    
        sm.send(action)

    except:
        pass

class VolumeStateMachine(StateMachine):
    idle = State(initial=True)
    changing_volume_timeout = State()
    pause_timeout = State()
    changing_volume = State()

    enter_change_volume = idle.to(changing_volume)
    enter_change_volume_timeout = changing_volume.to(changing_volume_timeout)
    enter_pause_timeout = idle.to(pause_timeout)
    leave_change_volume = changing_volume_timeout.to(idle)
    leave_pause_timeout = pause_timeout.to(idle)

    def on_enter_changing_volume(self):
        Thread(target=timer, args=(self, 10, "enter_change_volume_timeout")).start()
    
    def on_enter_changing_volume_timeout(self):
        Thread(target=timer, args=(self, 2, "leave_change_volume")).start()

    def on_enter_pause_timeout(self):
        Thread(target=timer, args=(self, 2, "leave_pause_timeout")).start()