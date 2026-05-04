#MIS310 Group 1 Yusuf Chowdhury, Mansoor Bilal, Daniel Seeley, Aliana Williams
import os
import fitz
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from openai import OpenAI

client = OpenAI(api_key="put-your-real-api-key-here") #cut out the contents of the qyotes and insert your api

def browse_file():
    path = filedialog.askopenfilename(filetypes=[("PDF files", "*.pdf")])
    if path:
        entry.delete(0, tk.END)
        entry.insert(0, path)

def delete_file():
    entry.delete(0, tk.END)

def reset():
    entry.delete(0, tk.END)
    combo.current(0)
    output.delete("1.0", tk.END)

def summarize_pdf():
    path = entry.get()
    if not path:
        messagebox.showerror("Error", "Please select a PDF file first.")
        return

    try:
        doc = fitz.open(path)
        
        text = "".join(page.get_text() for page in doc)
        doc.close()

        words = text.split()
        chunks = [" ".join(words[i:i+1000]) for i in range(0, len(words), 1000)]

        level = combo.get()
        if level == "Short":
            prompt = "Summarize this into 5 to 8 short bullet points."
        elif level == "Medium":
            prompt = "Summarize this into 8 to 12 clear bullet points."
        else:
            prompt = "Summarize this into detailed bullet-point notes."


        notes = ""
        for chunk in chunks:
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "user", "content": f"{prompt}\n\n{chunk}"}
                ]
            )
            notes += response.choices[0].message.content + "\n\n"

        output.delete("1.0", tk.END)
        output.insert(tk.END, notes)

    except Exception as e:
        messagebox.showerror("Error", str(e))

#making it look nice
root = tk.Tk()
root.title("Lecture-to-Notes Summarizer")
root.geometry("900x550")

tk.Label(root, text="Lecture-to-Notes Summarizer",
         font=("Arial", 18, "bold")).pack(pady=15)


frame = tk.Frame(root)
frame.pack(padx=30, pady=10, fill="x")

tk.Label(frame, text="Browse/Select File from Computer:",
         font=("Arial", 11)).grid(row=0, column=0, sticky="w", pady=(0, 8))

entry = tk.Entry(frame, width=70)
entry.grid(row=1, column=0, padx=(0, 10), pady=5)

tk.Button(frame, text="Browse", width=12, command=browse_file).grid(row=1, column=1, padx=5)
tk.Button(frame, text="Delete", width=12, command=delete_file).grid(row=1, column=2, padx=5)

tk.Label(frame, text="Summary Level:",
         font=("Arial", 11)).grid(row=2, column=0, sticky="w", pady=(20, 8))

combo = ttk.Combobox(frame, values=["Short", "Medium", "Long"], width=12, state="readonly")
combo.grid(row=3, column=0, sticky="w")
combo.current(0)

btn_frame = tk.Frame(root)
btn_frame.pack(pady=15)

tk.Button(btn_frame, text="Summarize", bg="#1f6fe5", fg="white",
          width=16, command=summarize_pdf).pack(side="left", padx=8)

tk.Button(btn_frame, text="Reset", width=16,
          command=reset).pack(side="left", padx=8)

output = tk.Text(root, height=18, width=100, font=("Arial", 11))
output.pack(padx=30, pady=10, fill="both", expand=True)

root.mainloop()