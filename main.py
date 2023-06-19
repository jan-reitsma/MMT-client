from modernmt import ModernMT
import pyperclip as clip
import tkinter as tk
from time import sleep
mmt = ModernMT('7763DBAD-DB02-9C5C-5DA0-B543BE3D7D34')

window = tk.Tk()

#def handle_keypress(event):
#    print(event.char)
def button_clicked():
    if entry.get() != "":
        src = entry.get()
        translate(src)

    elif clip.paste() != "":
        src = clip.paste()
        translate(src)
    else:
        pass

def translate(src):
    outp.delete("1.0", tk.END)  # empty output text box
    srcLng = mmt.detect_language(src).detectedLanguage
    lang["text"] = srcLng
    try:
        result = mmt.translate(srcLng, "nl", src)
        trg = result.translation
        outp.insert(tk.END, trg)
        comment["text"] = "translation copied to clipboard"
        clip.copy(trg)
    except:
        comment["text"] = "source and target language cannot be the same"

label = tk.Label(text="MMT translator")
entry = tk.Entry(width=100)
lbl_lang = tk.Label(text="Lang detected:")
lang = tk.Label(width=10)
comment = tk.Label(width=50)
outp = tk.Text()
button = tk.Button(
    text="click here to translate",
    command=button_clicked
)

label.pack()
entry.pack()
lbl_lang.pack()
lang.pack()
outp.pack()
comment.pack()
button.pack()

'''#bind callback method of window to "<Key>" :
window.bind("<Key>", handle_keypress)
'''

window.mainloop()