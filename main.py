from modernmt import ModernMT
import pyperclip as clip
import tkinter as tk
from tkinter import ttk

mmt = ModernMT('7763DBAD-DB02-9C5C-5DA0-B543BE3D7D34')

root = tk.Tk()
root.title("Easy MT")
root.geometry("400x500")

def return_pressed(event):
    button_clicked()
def button_clicked():
    if entry.get() != "":
        src = entry.get()
        translate(src)

    elif clip.paste() != "":
        src = clip.paste()
        translate(src)
    else:
        outp.delete("1.0", tk.END)  # empty output text box
        comment["text"] = "Nothing to translate!"
        quality["text"] = ""

def translate(src):
    entry.delete("0", tk.END)
    outp.delete("1.0", tk.END)  # empty output text box
    comment["text"] = ""
    lang["text"] = ""
    srcLng = mmt.detect_language(src).detectedLanguage
    lang["text"] = srcLng
    try:
        result = mmt.translate(srcLng, "nl", src)
        trg = result.translation
        outp.insert(tk.END, trg)
        comment["text"] = "Translation copied to clipboard."
        clip.copy(trg)
        qEst = mmt.qe(srcLng, "nl", src, trg)
        quality["text"] = f"Quality estimation: {qEst.score}"
    except:
        comment["text"] = "Error: Source and target language cannot be the same!"

        lang["text"] = ""
        quality["text"] = ""

fields = {}

fields['label'] = tk.Label(text='Enter source text or leave empty to use clipboard:')
fields['entry'] = tk.Entry(width=200)
fields['lbl_lang'] = tk.Label(text='Language detected:')
fields['lang'] = tk.Label()
fields['comment'] = tk.Label(width= 50)
fields['quality'] = tk.Label(width= 20)
fields['button'] = tk.Button(text="Click here to translate or hit RETURN", command=button_clicked)
fields['outp'] = tk.Text()


label = fields['label']
entry = fields['entry']
lbl_lang = fields['lbl_lang']
lang = fields['lang']
comment = fields['comment']
quality = fields['quality']
button = fields['button']
outp = fields['outp']

for field in fields.values():
    field.pack(padx=10, pady=5, fill=tk.X)

'''#bind callback method of window to "<Key>" :
window.bind("<Key>", handle_keypress)
'''
root.bind('<Return>', return_pressed)

root.mainloop()