from tkinter import *
import itertools #, colors

backgroundColor = '#1b1b1b'
primaryColor = '#4f4f4f'


root = Tk()
root.geometry('1205x800')
root.title('Anagrams')
root.resizable(False, False)
canvas = Canvas(root, highlightthickness = 0, background = backgroundColor)
canvas.pack(fill = BOTH, expand = 1)

allWords = open("./Resources/allWords.txt", 'r').read().splitlines()
#allWords = open("allWords.txt", 'r').read().splitlines()
validLetters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']

currentBox = 0
letter_count = 7

printed = False
boxes, word, printedResults = [], [], []

for x in range(2, 1201, int(1200 / letter_count)):
    boxes.append(canvas.create_rectangle(x, 2, x + int(1200 / letter_count), 202, fill = backgroundColor, outline = primaryColor, width = 5))

posX, posY = 100, 250
def reset():
    global printed, word, currentBox, printedResults
    printed = False
    currentBox = 0
    for letter in word:
        canvas.delete(letter)
    for printedResult in printedResults:
        canvas.delete(printedResult)
    word, printedResults = [], []
    
def checkWord(event):
    # this is a very basic algorithm, and struggles at 7 letters.
    global printed
    root.unbind("<Return>")
    if not printed and len(word) == letter_count:
        printed = True
        validWords = []
        for i in range(letter_count, 2, -1):
            finalWord = ''
            for letter in word:
                finalWord = finalWord + canvas.itemcget(letter, 'text')
            results = list( map(''.join, itertools.permutations(finalWord, i)))
            for result in results:
                if result.upper() in allWords and result not in validWords:
                    validWords.append(result)
            
        curr = 0
        for x in range(110, 1200, 200):
            for y in range(250, 760, 50):
                if curr == len(validWords):
                    break
                printedResults.append(canvas.create_text(x, y, text = validWords[curr], font = ("Consolas", 55), fill = primaryColor))
                curr = curr + 1
    elif printed:
        reset()
                        
def typee(event):
    global currentBox, letter_count
    if event.keysym in validLetters and currentBox <= (letter_count - 1):
        boxCoords = canvas.coords(boxes[currentBox])
        word.append(canvas.create_text(boxCoords[0] + int(1200 / letter_count / 2), boxCoords[1] + int(1200 / letter_count / 2), text = str(event.keysym).upper(), font = ("Consolas", 150), fill = primaryColor))
        currentBox = currentBox + 1
    elif event.keysym == 'BackSpace' and len(word) > 0:
        canvas.delete(word[len(word)-1])
        word.remove(word[len(word) - 1])
        currentBox = currentBox - 1

root.bind("<Return>", checkWord)
root.bind("<Key>", typee)
root.mainloop()
