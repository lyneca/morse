from time import time
from tkinter import *
from tkinter.ttk import *
import keyboard
import serial
import threading

last_change = time()
dit_length = 0.1
dah_length = dit_length * 3
space_length = dit_length * 7
allowance = 0.05
char_buffer = ''
is_on = False
was_backspace = False
stop_thread = False

root = Tk()
root.title('Morse Translator')
root.resizable(width=False, height=False)
root.iconbitmap(r'.\morse.ico')
root.geometry('270x25')

def toggle():
    global is_on
    is_on = not is_on
    if is_on:
        toggle_btn.config(text='Turn OFF')
    else:
        toggle_btn.config(text='Turn ON')


toggle_btn = Button(master=root, command=toggle, text="Turn ON")
toggle_btn.pack(fill=BOTH, expand=1)

morse = {
    '---...': ':', '--..--': ',', '-....-': '-', '.----.': '\'',
    '.--.-.': '@', '.-.-.-': '.', '.-..-.': '"', '-..-.': '/', '-...-': '=',
    '..--..': '?', '-----': '0', '----.': '9', '---..': '8', '--...': '7',
    '-....': '6', '.----': '1', '..---': '2', '...--': '3', '....-': '4',
    '.....': '5', '--.-': 'q', '--..': 'z', '-.--': 'y', '-.-.': 'c',
    '-..-': 'x', '-...': 'b', '.---': 'j', '.--.': 'p', '.-..': 'l',
    '..-.': 'f', '...-': 'v', '....': 'h', '---': 'o', '--.': 'g', '-.-': 'k',
    '-..': 'd', '.--': 'w', '.-.': 'r', '..-': 'u', '...': 's', '--': 'm',
    '-.': 'n', '.-': 'a', '..': 'i', '-': 't', '.': 'e'
}

def handle(state):
    global last_change, was_backspace
    if not state:
        if dah_length - allowance * 3 < time() - last_change < space_length - allowance * 3:
            was_backspace = False
            dah()
        if dit_length - allowance < time() - last_change < dit_length + allowance:
            was_backspace = False
            dit()
    last_change = time()

def translate(buf):
    if buf in morse:
        return morse[buf]
    else:
        return False

def enter(key):
    if key:
        keyboard.press_and_release(key)

def word_pause():
    enter('space')

def backspace():
    enter('backspace')

def dah():
    global char_buffer
    char_buffer += '-'
    enter('-')

def dah_pause():
    global char_buffer
    for i in range(len(char_buffer)):
        enter('backspace')
    enter(translate(char_buffer))
    char_buffer = ''

def dit():
    global char_buffer
    char_buffer += '.'
    enter('.')

def dit_pause():
    pass

if __name__ == '__main__':
    ser = serial.Serial('COM4', 9600, timeout=1)
    while True:
        try:
            state = ser.read().decode('utf-8')
        except UnicodeDecodeError:
            continue
        break

    state = ''
    last_state = 0
def main():
    global last_change, stop_thread, was_backspace
    while True:
        if stop_thread:
            break
        pass
        if is_on:
            if ser.in_waiting > 0:
                state = ser.read().decode('utf-8')
                handle(int(state))
                last_state = int(state)
            if dah_length - allowance < time() - last_change < dah_length + allowance:
                if not last_state:
                    dah_pause()
                print('char')
            if space_length - allowance < time() - last_change < space_length + allowance:
                print('word')
                if last_state:
                    backspace()
                    last_change -= 10
                    was_backspace = True
                else:
                    if not was_backspace:
                        word_pause()
                        last_change -= 10
                        was_backspace = False

thread = threading.Thread(target=main)
thread.start()

def close():
    global stop_thread
    stop_thread = True
    root.destroy()
    sys.exit()

root.protocol("WM_DELETE_WINDOW", close)
root.mainloop()
