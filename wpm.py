from tkinter import *
import random, time
from threading import *

#   TODO
#       [!] I dont remember how I calculated words per minute but I think it's wrong
#       [X] "Words should shake when you type the wrong letter"
#       [ ] "when you type the right word, flash colors and suprises!""
#       [ ] theme packs with colors!


words = open("./Resources/allWords.txt", 'r').read().splitlines()
    #  bg     fg     type_color   wpm_color
colors = [
    ['tan', 'saddlebrown', 'red', 'brown'],
    ['black', 'lime', 'blue', 'green']
]
color = 1
root = Tk()
root.title("Words Per Minute")
root.geometry('1000x600')
canvas = Canvas(root, highlightthickness = 0, background = colors[color][0])
canvas.pack(fill = BOTH, expand = 1)

wpm = 0
wpm_text = canvas.create_text(500, 400, font = ("Consolas", 200), text = wpm, fill=colors[color][3])

word_text = []
next_word = ''
next_word_texts = []

new = False

wps = []




def word_timer(timer):
    global wpm
    if not new:
        timer = timer + 0.1
        time.sleep(0.1)
        word_timer(timer)
    else:
        if len(wps) > 8:
            wps.remove(wps[0])
            wps.append(60 / timer)
        else:
            wps.append(60 / timer)
        wpm = round(round(sum(wps) / len(wps), 1))
        canvas.itemconfig(wpm_text, text = wpm)
        
def wrong(event):
    c0 = 0
    for i in range(4):
        for word in word_text:
            c = canvas.coords(word)
            if c0 % 2 == 0:
                canvas.coords(word, c[0] - 60, c[1])
            else:
                canvas.coords(word, c[0] + 60, c[1])
        c0 = c0 + 1
        canvas.update()
        time.sleep(0.025)

def type_letter(event, letter_text, num):
    global word_text, new
    if (num == 0):
        new = False
        t1 = Thread(target = word_timer, args = (0,))
        t1.start()
    if (num < len(word_text) - 1):
        canvas.itemconfig(letter_text, fill = colors[color][2])
        root.unbind("<key>")
        root.unbind(str(canvas.itemcget(word_text[num], 'text')).lower())
        root.bind("<Key>", wrong)
        root.bind(str(canvas.itemcget(word_text[num + 1], 'text')).lower(), lambda event, letter_text = word_text[num + 1], num = num + 1: type_letter(event, letter_text, num))
    else:
        root.unbind(str(canvas.itemcget(word_text[num], 'text')).lower())
        root.unbind("<Key>")
        canvas.itemconfig(letter_text, fill = colors[color][2])
        o = ''
        for word_t in word_text:
            o = o + canvas.itemcget(word_t, 'text')
        for letter in word_text:
            canvas.delete(letter)
        word_text = []
        new = True
        create_word()

def create_word():
    global next_word, next_word_texts
    if next_word == "":
        word = random.choice(words)
        while len(word) > 17:
            word = random.choice(words)
        if len(word) <= 12:
            spacing = int(500 - (80 * (len(word) / 2)))
            for x in range(len(word)):
                l = canvas.create_text(x * 80 + spacing + 35, 150, font = ("Consolas", 150), text = word[x], fill = colors[color][1])
                word_text.append(l)
        else:
            spacing = int(500 - (65 * (len(word) / 2)))
            for x in range(len(word)):
                l = canvas.create_text(x * 65 + spacing + 25, 150, font = ("Consolas", 125), text = word[x], fill = colors[color][1])
                word_text.append(l)
        next_word = random.choice(words)
        spacing = int(500 - (34 * (len(next_word) / 2)))
        for x in range(len(next_word)):
            l = canvas.create_text(x * 34 + spacing, 50, font = ("Consolas", 60), fill = colors[color][1], text = next_word[x])
            next_word_texts.append(l)
        root.bind(str(canvas.itemcget(word_text[0], 'text')).lower(), lambda event, letter = word_text[0], num = 0: type_letter(event, letter, num))
    else:
        for next_word_text in next_word_texts:
            canvas.delete(next_word_text)
        word = next_word
        if len(word) <= 12:
            spacing = int(500 - (80 * (len(word) / 2)))
            for x in range(len(word)):
                l = canvas.create_text(x * 80 + spacing + 35, 150, font = ("Consolas", 150), text = word[x], fill = colors[color][1])
                word_text.append(l)
        else:
            spacing = int(500 - (65 * (len(word) / 2)))
            for x in range(len(word)):
                l = canvas.create_text(x * 65 + spacing + 25, 150, font = ("Consolas", 125), text = word[x], fill = colors[color][1])
                word_text.append(l)
        root.bind(str(canvas.itemcget(word_text[0], 'text')).lower(), lambda event, letter = word_text[0], num = 0: type_letter(event, letter, num))
        next_word = random.choice(words)
        next_word_texts = []
            
        while len(next_word) > 17:
            next_word = random.choice(words)
        spacing = int(500 - (34 * (len(next_word) / 2)))
        for x in range(len(next_word)):
            l = canvas.create_text(x * 34 + spacing, 50, font = ("Consolas", 60), fill = colors[color][1], text = next_word[x])
            next_word_texts.append(l)
create_word()
root.mainloop()
