import threading 
import time
import time
import random
import gpt3
from pynput.keyboard import Controller, Key
import FoxDot


keyboard = Controller()
foxdotcode = FoxDot.FoxDotCode()
running, queue = [], []

prompt = '''play("si-$0-ttt-fff-iii", delay=0.05, dur=0.16, amp=[1,0.5,0.5,0.25,1])
space([1,[2,5,5,5,8]], dur=[4,4,4,2], oct=4, amp=linvar([1,3],28), drive=0.01, sus=8, chop=var([0,4],[12,6]))
play('-', sample=PRand(3), amp=2)
marimba(var([0,1],[3,4,12,3]), amp=[0.5,0.25,0.5,0.75], vib=PRand(5)/5)
bass(P[0,1,3,4,0].stutter(12), dur=[0.5,0.5,0.5,0.5,1], amp=1)
karp(P[[5,5,5,6,6],[4,4,4,6,6]].stutter(16) + var([0,PRand(3)],[3,4]), dur=0.25, oct=5, sus=3, blur=2, amp=linvar([0.25,0.5],16))
pulse(8 + var([0,2],[4,8]), amp=([0,1],[48,16]))
glass(oct=6, rate=linvar([-2,2],16), shape=0.5, amp=1.5, room=0.5)
pasha(dur=12, oct=6, vib=2, tremolo=3, amp=1)
play("@", dur=1/4, sample=P[:8].rotate([0,1,3]), rate=4, pan=-0.5)
dbass(dur=PDur(3,8), sus=2, chop=4, shape=PWhite(0,1/2), pan=PWhite(-1,1)).sometimes("offadd", 4) + var([0,2],4)
space([7,6,4,P*(2,1),0], dur=8, pan=(-1,1))
play("x-o{-[-(-o)]}", sample=0).every([28,4], "trim", 3)
blip([0, 2, [0, 1, 2]], dur=8, sus=4, room=1, oct=6) + [0,0,0,P*(2,4,3,-1)]
pluck([0, 3, 2], dur=[1/2, 1], oct=4)
pads([0, 3, 7, 8, -2], dur=[4, 8], oct=5, amp=0.7)
play("(X )( X)N{ xv[nX]}", drive=0.2, lpf=var([0,40],[28,4]), rate=PStep(P[5:8],[-1,-2],1)).sometimes("sample.offadd", 1, 0.75)
play("e", amp=var([0,1],[PRand(8,16)/2,1.5]), dur=PRand([1/2,1/4]), pan=var([-1,1],2))
sawbass(var([0,1,5,var([4,6],[14,2])],1), dur=PDur(3,8), cutoff=4000, sus=1/2)
'''

prompt = '''space([1,[2,5,5,5,8]], dur=[4,4,4,2], oct=4, amp=linvar([1,3],28), drive=0.01, sus=8, chop=var([0,4],[12,6]))
marimba(var([0,1],[3,4,12,3]), amp=[0.5,0.25,0.5,0.75], vib=PRand(5)/5)
bass(P[0,1,3,4,0].stutter(12), dur=[0.5,0.5,0.5,0.5,1], amp=1)
karp(P[[5,5,5,6,6],[4,4,4,6,6]].stutter(16) + var([0,PRand(3)],[3,4]), dur=0.25, oct=5, sus=3, blur=2, amp=linvar([0.25,0.5],16))
play("si-$0-ttt-fff-iii", delay=0.05, dur=0.16, amp=[1,0.5,0.5,0.25,1])
pulse(8 + var([0,2],[4,8]), amp=([0,1],[48,16]))
glass(oct=6, rate=linvar([-2,2],16), shape=0.5, amp=1.5, room=0.5)
pasha(dur=12, oct=6, vib=2, tremolo=3, amp=1)
dbass(dur=PDur(3,8), sus=2, chop=4, shape=PWhite(0,1/2), pan=PWhite(-1,1)).sometimes("offadd", 4) + var([0,2],4)
space([7,6,4,P*(2,1),0], dur=8, pan=(-1,1))
blip([0, 2, [0, 1, 2]], dur=8, sus=4, room=1, oct=6) + [0,0,0,P*(2,4,3,-1)]
play("x-o{-[-(-o)]}", sample=0).every([28,4], "trim", 3)
pluck([0, 3, 2], dur=[1/2, 1], oct=4)
pads([0, 3, 7, 8, -2], dur=[4, 8], oct=5, amp=0.7)
sawbass(var([0,1,5,var([4,6],[14,2])],1), dur=PDur(3,8), cutoff=4000, sus=1/2)
'''



def type_string_with_delay(string):
    for character in string:  # Loop over each character in the string
        keyboard.type(character)  # Type the character
        time.sleep(0.02)  # Sleep for the amount of seconds generated


def cursor_right():
    keyboard.press(Key.right)
    keyboard.release(Key.right)


def execute():
    keyboard.press(Key.cmd)
    keyboard.press(Key.enter)
    keyboard.release(Key.cmd)
    keyboard.release(Key.enter)


def stop_all():
    keyboard.press(Key.cmd)
    keyboard.press('.')
    keyboard.release(Key.cmd)
    keyboard.release('.')


def newline():
    for _ in range(5):
        cursor_right()
    keyboard.press(Key.enter)
    keyboard.release(Key.enter)
    

def compile_code(code_str, name):
    code_str = '{} >> {};{}.stop()'.format(name, code_str, name)
    response = foxdotcode(code_str, verbose=True, verbose_error=True)
    valid = "Traceback" not in response
    return valid


def run_event(event):
    name, code, action = event['event']['name'], event['event']['code'], event['action']
    
    newline()
    #time.sleep(0.2)
    
    line = ''
    if action == 'start': 
        line = '{} >> {}'.format(name, code)
    elif action == 'stop':
        line = '{}.stop()'.format(name)

    type_string_with_delay(line)

    #time.sleep(0.2)
    execute()
    #time.sleep(0.2)
    newline()


class EventThread(threading.Thread): 

    def __init__(self): 
        threading.Thread.__init__(self) 
 
    def run(self): 
        global queue
        while True:
            curr_time = time.time()
            evts = [evt for evt in queue if evt['time'] < curr_time]
            if len(evts):
                evt = sorted(queue, key=lambda k: k['time'])[0]
                queue = [e for e in queue if e != evt]
                #running.append(evt)
                run_event(evt)
            #time.sleep(1) 
  

thread = EventThread() 
thread.start() 


while True:

    completion = gpt3.complete(
        prompt, 
        stops=None, 
        max_tokens=1050, 
        temperature=0.9, 
        engine='davinci',
        max_completions=1)

    lines = completion.split('\n')
    for line in lines:
        name = 'p%d'%random.randint(1,6)
        valid = compile_code(line, name)
        if valid:
            synth = {'name': name, 'code': line}
            queue.append({'time': time.time(), 'event': synth, 'action': 'start'})
            #queue.append({'time': time.time()+60, 'event': synth, 'action': 'stop'})
            time.sleep(2)
        else:
            time.sleep(0.25)