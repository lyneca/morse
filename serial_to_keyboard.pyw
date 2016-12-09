import serial
import keyboard
from tkinter import *
from tkinter.ttk import *
import threading
import sys

root = Tk()
root.title('Morse Interface')
root.resizable(width=False, height=False)
root.iconbitmap(r'.\morse.ico')
root.geometry('270x50')

def toggle():
    global is_on
    is_on = not is_on
    if is_on:
        key_entry.config(state='normal')
        toggle_btn.config(text='Turn OFF')
    else:
        key_entry.config(state='disabled')
        toggle_btn.config(text='Turn ON')


toggle_btn = Button(master=root, command=toggle, text="Turn ON")
toggle_btn.pack(fill=BOTH, expand=1)

key_entry = Entry(master=root, exportselection=False)
key_entry.insert(0, 'down')
key_entry.config(state='disabled')
key_entry.pack(fill=BOTH, expand=1)

stop_thread = False
is_on = False

ser = serial.Serial('COM3', 9600, timeout=1)
while True:
    try:
        state = ser.read().decode('utf-8')
    except UnicodeDecodeError:
        continue
    break

state = ''
def read():
    while True:
        global is_on
        global stop_thread
        if stop_thread:
            break
        if is_on:
            while ser.in_waiting == 0:
                if stop_thread:
                    break
                pass
            state = ser.read().decode('utf-8')
            if int(state):
                keyboard.press(key_entry.get())
            else:
                keyboard.release(key_entry.get())

thread = threading.Thread(target=read)
thread.start()

def close():
    global stop_thread
    stop_thread = True
    root.destroy()
    sys.exit()

root.protocol("WM_DELETE_WINDOW", close)
root.mainloop()
