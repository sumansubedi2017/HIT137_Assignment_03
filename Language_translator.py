#Importing the tkinter library for GUI development
import tkinter as tk
from tkinter import ttk
from googletrans import Translator, LANGUAGES

class TranslatorApp(tk.Tk): #multiple inheritance, inheriting from tk.Tk class it is crucial for creating graphical user interface. 
    def __init__(self):
        super().__init__() #method overriding, calling parent class's __init__ method 
        self.title("Language Translator") # encapsulation, hiding implementation details
        self.geometry("600x500")
        self.configure(bg="#f0f0f0")  #Setting background color

        self.translator = Translator()

        #Frame for language selection
        self.language_frame = ttk.Frame(self, padding=(10, 10))
        self.language_frame.pack()

        self.source_label = tk.Label(self.language_frame, text="From:", bg="#f0f0f0", font=("Arial", 10))
        self.source_label.grid(row=0, column=0, padx=5, pady=5)

        self.source_language = ttk.Combobox(self.language_frame, values=list(LANGUAGES.values()), width=25)
        self.source_language.grid(row=0, column=1, padx=5, pady=5)

        self.target_label = tk.Label(self.language_frame, text="To:", bg="#f0f0f0", font=("Arial", 10))
        self.target_label.grid(row=0, column=2, padx=5, pady=5)

        self.target_language = ttk.Combobox(self.language_frame, values=list(LANGUAGES.values()), width=25)
        self.target_language.grid(row=0, column=3, padx=5, pady=5)

        #Frame for input and output
        self.text_frame = ttk.Frame(self, padding=(10, 5))
        self.text_frame.pack(fill=tk.BOTH, expand=True)

        self.input_label = tk.Label(self.text_frame, text="Enter Text:", bg="#f0f0f0", font=("Arial", 10))
        self.input_label.pack(anchor="w", padx=5)

        self.input_text = tk.Text(self.text_frame, height=5, width=40)
        self.input_text.pack(fill=tk.BOTH, expand=True, padx=5)
        #encapsulation, linking button action to a method
        self.translate_button = tk.Button(self.text_frame, text="Translate", command=self.translate_text,
                                          bg="#4285F4", fg="white", font=("Arial", 10))
        self.translate_button.pack(pady=5)

        self.output_label = tk.Label(self.text_frame, text="Translated Text:", bg="#f0f0f0", font=("Arial", 10))
        self.output_label.pack(anchor="w", padx=5, pady=5)

        self.output_text = tk.Text(self.text_frame, height=5, width=40)
        self.output_text.pack(fill=tk.BOTH, expand=True, padx=5)

    def translate_text(self): #polymorphism, overriding method
        input_text = self.input_text.get("1.0", tk.END)
        source_lang = [lang for lang, lang_name in LANGUAGES.items() if lang_name == self.source_language.get()][0]
        target_lang = [lang for lang, lang_name in LANGUAGES.items() if lang_name == self.target_language.get()][0]
        translated = self.translator.translate(input_text, src=source_lang, dest=target_lang)
        self.output_text.delete("1.0", tk.END)
        self.output_text.insert(tk.END, translated.text)

if __name__ == "__main__":
    #Create an instance of the TranslatorApp class
    app = TranslatorApp()
    #Start the main event loop to run the application
    app.mainloop()
