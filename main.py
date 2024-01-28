from tkinter import *
from tkinter import messagebox
import time 
import random

words_list = []
typed_words = []
current_word = ''
char = 0
chars_typed = 0
accurate_typed = 0
position = 0
word = ''
timer = None

# Create the main window
window = Tk()
window.title("Typing Speed Test")
window.geometry("300x150")
heading_label = Label(text= "Typing Speed Test", font=("Helvetica", 20), pady=15)
heading_label.pack()

rules_label = Label(text = "Type the words that appear as fast and as accurately as you can in the box below, with one space between each word.  You can backspace and fix an error with no penalty.",  font=("Helvetica", 12), pady=15, wraplength=500 )
rules_label.pack()

def click(key):
    global words_list
    global typed_words
    global current_word
    global char
    global chars_typed
    global accurate_typed
    global position
    global word
    chars_typed += 1

    if key.keysym == 'space':
        typing_box.delete(0, END)
        try:
            typed_words[word] = current_word
        except IndexError:
            typed_words.append(current_word)
        word += 1
        current_word = ''
        chars_typed -= 1
    
    elif key.keysym == 'BackSpace':
        chars_typed -= 1

        length = len(current_word) - 1

        if (len(current_word)) == 0:
            if word > 0:
                word -= 1
                typing_box.insert(0, f"{typed_words[word]}")
                current_word = typed_words[word]
                typed_words = typed_words [:-1]

        elif (len(current_word)) != 0:
            try:
                my_word = words_list[word][length]
                if current_word[-1] == my_word:
                    accurate_typed -=1
            except IndexError:
                pass

            current_word = current_word[:-1]
        
    elif key.char != ' ':
        current_word += key.char

    curr_char = len(current_word) - 1
    selected_word = words_list[word]

    if (len(current_word)) > len(words_list[word]):
        position = len("".join(words_list[:word])) + len(typed_words) + len(selected_word) - 1

    else:
        position = len(''.join(words_list[:word])) + len(typed_words) + len(current_word) - 1

    
    if key.keysym != 'Backspace' and key.keysym != 'space':
        try:
            selected = selected_word[curr_char]
        except IndexError:
            curr_char = len(selected_word) - 1
            selected = selected_word[curr_char]

        if selected == key.char and len(selected_word) >= len(current_word):
            accurate_typed += 1
            text.tag_add("correct", f"1.{position}")
            text.tag_remove("incorrect", f"1.{position}")
        
        if selected != key.char:
            text.tag_add("incorrect", f"1.{position}")
            text.tag_remove("correct", f"1.{position}")
            
    text.tag_configure("correct", foreground="green")
    text.tag_configure("incorrect", foreground="red")

def start_game():
    global word
    global typing_box
    global text
    global position
    global typed_words
    global words_list
    global curr_word
    global chars_typed
    global accurate_typed
    curr_word = ''
    word = 0
    typed_words = []
    words_list = []
    position = 0
    chars_typed = 0
    accurate_typed = 0
    timer = 60
    start_button.pack_forget()

    # Reading words from a file and choosing randomly
    with open('words.txt') as file:
        row = file.readlines()
        for x in range(0, 200):
            chosen_word = random.choice(row).strip()
            words_list.append(chosen_word)
    
    # Setting up the text widget to display the chosen words
    text = Text(window, font=("Helvetica", 12), wrap=WORD)
    text.insert(INSERT, words_list)
    text.pack()

    # Creating an entry for user input
    typing_box = Entry()
    typing_box.pack()
    typing_box.focus()

    # Game timer Loop
    while timer > 0:
        window.update()
        time.sleep(.01)
        timer -= .01
        typing_box.bind("<Key>", click)

    # Handling the end of the game
    if timer < 0:
        for i in range(0, len(typed_words)):
            if (len(typed_words[i])) < len(words_list[i]):
                accurate_typed -= 1
        print(accurate_typed)
        percent = (accurate_typed / chars_typed) * 100
        message = f"You typed CPM: {chars_typed}, WPM: {chars_typed/5}, accuracy: {percent:.2f}%"
        messagebox.showinfo("Information", message)

        # Cleaning up the widgets after the game ends
        typing_box.destroy()
        text.destroy()
        start_button.pack()

start_button = Button(text="Start", command=lambda:start_game())
start_button.pack()

window.mainloop()








