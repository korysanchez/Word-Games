from tkinter import *
import random

all_words_txt = './Resources/allWords.txt'
alphabet = ['A', 'E', 'I', 'O', 'U', 'B','C','D','F','G','H','J','K','L','M','N','P','Q','R','S','T','V','W','X','Y','Z']


def has_panagram(letters, words):
    letters = list(letters)
    for word in words:
        if(len(word) >= 7):
            valid = True
            for letter in letters:
                if letter not in word:
                    valid = False
                    break
            if valid:
                return True
    return False
def get_panagrams(letters, words):
    panagrams = []
    letters = list(letters)
    for word in words:
        if(len(word) >= 7):
            valid = True
            for letter in letters:
                if letter not in word:
                    valid = False
                    break
            if valid:
                panagrams += [word]
    return panagrams



class WordsScreen():
    found_words = []
    def __init__(self, root):
        self.root = root
        self.tl = Toplevel(self.root)
        self.tl.geometry('300x800+50+50')
        self.tl.title('Found Words')
        self.canvas = Canvas(self.tl, background='#1b1b1b', highlightthickness=0)
        self.canvas.pack(fill=BOTH, expand=1)
    def toggle_enable(self, event):
        if not self.tl.winfo_viewable():
            self.tl.geometry('300x1+50+50')
            self.tl.deiconify()
            for i in range(0, 801, 50):
                self.tl.geometry('300x' + str(i) + '+50+50')
                self.tl.update()
        else:
            for i in range(801, 0, -50):
                self.tl.geometry('300x' + str(i) + '+50+50')
                self.tl.update()
            self.tl.withdraw()
    def add_word(self, word):
        self.found_words.append(word)
        self.found_words = sorted(self.found_words)
        self.tl.title('Found Words (' + str(len(self.found_words)) + ')')
        self.redraw_words()
    def redraw_words(self):
        current_loc = (10, 10)
        for i in self.canvas.find_all():
            self.canvas.delete(i)

        for word in self.found_words:
            self.canvas.create_text(current_loc, text=word, fill='white', font=('Consolas', 18), anchor=W)
            current_loc = (current_loc[0], current_loc[1] + 18)
            if (current_loc[1] >= 792):
                current_loc = (120, 10)
        self.canvas.update()

class HintsScreen():
    panagrams = []
    def __init__(self, root, letters, words):
        self.root = root
        self.tl = Toplevel(self.root)
        self.height = 300
        self.tl.geometry('300x'+str(self.height)+'+1100+50')
        self.tl.title('Hints')
        self.canvas = Canvas(self.tl, background='#1b1b1b', highlightthickness=0)
        self.canvas.pack(fill=BOTH, expand=1)
        self.draw_stats(letters, words)
    def toggle_enable(self, event):
        if not self.tl.winfo_viewable():
            self.tl.geometry('300x1+50+50')
            self.tl.deiconify()
            for i in range(0, self.height, 50):
                self.tl.geometry('300x' + str(i) + '+1100+50')
                self.tl.update()
            self.tl.geometry('300x'+str(self.height)+'+1100+50')
        else:
            for i in range(self.height, 0, -50):
                self.tl.geometry('300x' + str(i) + '+1100+50')
                self.tl.update()
            self.tl.withdraw()
    def draw_stats(self, letters, words):
        combine_dict = dict()
        two_letter_dict = dict()
        for word in words:
            if (str(word[0]) + str(len(word))) not in combine_dict.keys():
                combine_dict.update({(str(word[0]) + str(len(word))) : [word]})
            else:
                combine_dict[(str(word[0]) + str(len(word)))] = combine_dict[(str(word[0]) + str(len(word)))] + [word]
            if word[:2] not in two_letter_dict.keys():
                two_letter_dict.update({word[:2] : [word]})
            else:
                two_letter_dict[word[:2]] = two_letter_dict[word[:2]] + [word]
        combine_dict = dict(sorted(combine_dict.items()))


        low, high = 100, 0
        letters_empty = []
        for i in combine_dict:
            if len(i) == 2:
                if int(i[1]) < low:
                    low = int(i[1])
                if int(i[1]) > high:
                    high = int(i[1])
            else:
                if int(i[len(i) - 2:]) > high:
                    high = int(i[len(i)-2:])
            if i[0] not in letters_empty:
                letters_empty += [i[0]]
        for i in range(low - low, high - low+1):
            self.canvas.create_text(i * 20 + 24, 18, fill='white', font=('Consolas', 12), text= str(i + low), anchor=W)
        for i in range(len(letters_empty)):
            self.canvas.create_text(4, i * 18 + 32, fill='white', font=('Consolas', 12), text= letters_empty[i] + ':', anchor=W)
        num = low
        for x in range(28, (high - low + 1) * 20 + 10, 20):
            i = 0
            for y in range(32, (len(letters_empty)+1)*18 + 1, 18):
                try:
                    text = self.canvas.create_text(x, y, fill='white', font=('Consolas', 11), text= len(combine_dict[str(letters_empty[i]) + str(num)]))
                    self.canvas.tag_bind(text, '<Button-1>', lambda event, num=text: self.click_toggle(event, num))
                except:
                    self.canvas.create_text(x, y, fill='#afafaf', font=('Consolas', 11), text='-')
                i += 1
            num += 1




        x, y = 4, 160
        prev = list(two_letter_dict.keys())[0][0]
        for i in two_letter_dict:
            if (i[0] != prev):
                x = 5
                y += 16
                prev = i[0]
            text = self.canvas.create_text(x, y, fill='white', font=("Consolas", 12), text=str(i) + ':' + str(len(two_letter_dict[i])), anchor=W)
            self.canvas.tag_bind(text, '<Button-1>', lambda event, num=text: self.click_toggle(event, num))
            x += 48 if len(two_letter_dict[i]) > 9 else 40
        

        print(get_panagrams(letters, words))
        text = self.canvas.create_text(4, 270, fill='white', font=("Consolas", 12), text='Total Word Count: ' + str(len(words)), anchor=W)
        self.canvas.tag_bind(text, '<Button-1>', lambda event, num=text: self.click_toggle(event, num))
        text = self.canvas.create_text(4, 285, fill='white', font=("Consolas", 12), text='Panagrams: '+str(len(get_panagrams(letters, words))), anchor=W)
        self.canvas.tag_bind(text, '<Button-1>', lambda event, num=text: self.click_toggle(event, num))
        
        
    


    def click_toggle(self, event, num):
        if self.canvas.itemcget(num, 'fill') == 'yellow':
            self.canvas.itemconfig(num, fill='white')
        else:
            self.canvas.itemconfig(num, fill='yellow')

class App():
    letters = []
    words = []
    found_words = []
    typed_letters = []
    drawn_letters = []
    def __init__(self):
        self.root = Tk()
        self.root.geometry('750x800+350+50')
        self.root.resizable(False, False)
        self.root.title('Spelling Bee')
        self.canvas = Canvas(self.root, background='#1b1b1b', highlightthickness=0)
        self.canvas.pack(fill=BOTH, expand=1)

        while (len(self.words) < 40 or len(self.words) > 800) or not has_panagram(self.letters, self.words):
            self.new_letters()
            self.find_words()
        print(self.words)
        self.root.update()
        self.draw_letters()
        self.type_text = self.canvas.create_text(self.root.winfo_width()/2, self.root.winfo_height()*1/6, fill='white', font=('Consolas', 100), text='')
        for letter in self.letters:
            self.root.bind(str.lower(letter), self.type_letter)

        self.words_screen = WordsScreen(self.root)
        self.hints_screen = HintsScreen(self.root, self.letters, self.words)
        self.root.bind('<Return>', self.enter_letter)
        self.root.bind('<BackSpace>', self.delete_letter)
        button = self.canvas.create_rectangle(0, 0, 60, 20, fill='#3b3b3b')
        self.canvas.tag_bind(button, '<Button-1>', self.words_screen.toggle_enable)
        button = self.canvas.create_rectangle(self.root.winfo_width()-60, 0, self.root.winfo_width(), 20, fill='#3b3b3b')
        self.canvas.tag_bind(button, '<Button-1>', self.hints_screen.toggle_enable)
        button = self.canvas.create_oval(self.root.winfo_width()/2+10, self.root.winfo_height()-30, self.root.winfo_width()/2-10, self.root.winfo_height()-10, fill='#3b3b3b')
        self.canvas.tag_bind(button, '<Button-1>', self.shuffle_letters)
        self.root.mainloop()

    def check_entered_word(self, word):
        if str.upper(word) in self.words and str.upper(word) not in self.found_words:
            self.found_words.append(str.upper(word))
            self.words_screen.add_word(str.upper(word))
            self.check_won()
        else:
            x, y = self.root.winfo_x(), self.root.winfo_y()
            for i in range(random.randint(8, 22)):
                if i % 2 == 0:
                    self.root.geometry('750x800+'+str(x-random.randint(8, 14))+'+'+str(y-random.randint(0, 3)))
                else:
                    self.root.geometry('750x800+'+str(x+random.randint(8, 14))+'+'+str(y+random.randint(0, 3)))
                self.root.update()
            self.root.geometry('750x800+'+str(x)+'+'+str(y))
    

    def check_won(self):
        if len(set(self.words) - set(self.words_screen.found_words)) == 0:
            for i in self.canvas.find_all():
                self.canvas.delete(i)
            obj = self.canvas.create_text(self.root.winfo_width()/2, 0, fill='yellow', font=("Consolas", 60), text='You\'re the queen bee!')
            for i in range(120, 0, -2):
                self.canvas.moveto(obj, 35, self.root.winfo_height()/2 + 20*(i*i/120) - 40)
                self.canvas.update()




    def type_letter(self, event):
        i = self.canvas.create_text(0,0, fill='yellow' if str.upper(event.char) == self.letters[0] else 'white', font=('Consolas', 100), text=str.upper(event.char), anchor=W)
        self.typed_letters = self.typed_letters + [i]
        self.center_letters()
    def enter_letter(self, event):
        word = ''
        for i in self.typed_letters:
            word += self.canvas.itemcget(i, 'text')
        self.check_entered_word(word)
        for i in self.typed_letters:
            self.canvas.delete(i)
        self.typed_letters = []
    def delete_letter(self, event):
        try:
            self.canvas.delete(self.typed_letters[len(self.typed_letters)-1])
            self.typed_letters.remove(self.typed_letters[len(self.typed_letters)-1])
            self.center_letters()
        except:
            pass
    def center_letters(self):
        letter_space = 50
        for i in range(len(self.typed_letters)):
            self.canvas.moveto(self.typed_letters[i], 370 + i * letter_space - (len(self.typed_letters)*letter_space/2), 80)
        self.canvas.update()


    def draw_letters(self):
        h = 45 #Controls the size of the individual hexagons
        cx, cy = (self.root.winfo_width()/2, self.root.winfo_height()*5/8) #where do u want these to be placed. This will be the center
        hl = 2.5*h #Controls how far apart each hexagon is from the center hexagon
        placements = [(cx, cy), (cx-(1.275*hl), cy-(0.76*hl)), (cx+(1.275*hl), cy-(0.76*hl)), (cx, cy-(1.51*hl)), (cx-(1.275*hl), cy+(0.76*hl)), (cx+(1.27*hl), cy+(0.76*hl)), (cx, cy+(1.52*hl))]
        for i in range(7):
            x, y = placements[i][0], placements[i][1]
            points = [(x-(1*h), y-(1.9*h)), (x+(1*h), y-(1.9*h)), (x+(2.2*h), y), (x+(1*h), y+(1.9*h)), (x-(1*h), y+(1.9*h)), (x-(2.2*h), y)]
            self.canvas.create_polygon(points, fill='yellow' if i==0 else 'white', outline='black', width=3)
            self.drawn_letters.append(self.canvas.create_text(x, y, fill='black', font=('Consolas', h+10), text=self.letters[i]))
    def new_letters(self):
        self.letters = []
        vowels = random.randint(1, 3)
        self.letters += random.sample(alphabet[:5], vowels)
        self.letters += random.sample(alphabet[5:], 7 - vowels)
        random.shuffle(self.letters)
        #self.letters = ['C', 'N', 'A', 'Y', 'T', 'I', 'R']
    def shuffle_letters(self, event):
        last = self.letters[1:]
        random.shuffle(last)
        ls = [self.letters[0]] + list(last)
        for i in range(len(self.drawn_letters)):
            self.canvas.itemconfig(self.drawn_letters[i], text=ls[i])
    def find_words(self):
        center_letter = self.letters[0]
        wrong_letters = [l for l in alphabet if l not in self.letters ]
        self.words, self.found_words = [], []
        for word in open(all_words_txt):
            if len(word) > 4:
                if center_letter in word:
                    valid_word = True
                    for letter in wrong_letters:
                        if letter in word:
                            valid_word = False
                            break
                    if valid_word:
                        self.words.append(word[:len(word)-1])


                    
                

if __name__ == "__main__":
    app = App()
