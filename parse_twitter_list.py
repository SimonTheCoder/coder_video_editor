import tkinter as tk
import json
from tkinter import messagebox

def handle_input():
    input_text = text_box.get("1.0", "end-1c")
    #print(input_text)

    #split input_text with "\n", then find all lines begin with "@"
    lines = input_text.split("\n")
    lines = [line[1:] for line in lines if line.startswith("@")]
    print(lines)

    # store lines in the json file  "./twitter_list.json"
    with open("twitter_list.json", "w") as file:
        json.dump(lines, file)
    
    # show a messagebox to inform the user that the work is done
    messagebox.showinfo("Done!", f"{len(lines)} twitters found.")


root = tk.Tk()

text_box = tk.Text(root, height=10, width=50)
text_box.pack()

button = tk.Button(root, text="处理输入", command=handle_input)
button.pack()

root.mainloop()
