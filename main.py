import customtkinter as ctk
import tkinter as tk
from tkinter import ttk
import pandas as pd
from PIL import Image, ImageTk

class RecipeMatchApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("RetseptMatch")
        self.geometry("800x600")

        # Lae toiduained CSV-failist
        self.ingredients = self.load_ingredients()

        # Peamised raamid
        self.main_frame = ctk.CTkFrame(self)
        self.main_frame.pack(pady=20, padx=60, fill="both", expand=True)

        self.create_widgets()

    def load_ingredients(self):
        df = pd.read_csv('toiduained.csv')
        return df['ingredient'].tolist()

    def create_widgets(self):
        # Koostisosade sisestamise sektsioon
        self.ingredients_label = ctk.CTkLabel(self.main_frame, text="Sisesta koostisosad:")
        self.ingredients_label.pack(pady=10)

        # Rippmenüü populaarsete toiduainetega
        self.ingredients_var = tk.StringVar(value="Vali toiduaine")
        self.ingredients_menu = ttk.Combobox(self.main_frame, textvariable=self.ingredients_var, values=self.ingredients)
        self.ingredients_menu.pack(pady=10)
        self.ingredients_menu.bind('<KeyRelease>', self.filter_ingredients)

        self.add_button = ctk.CTkButton(self.main_frame, text="Lisa", command=self.add_ingredient)
        self.add_button.pack(pady=10)

        # Nupp retseptide hindamise lehele liikumiseks
        self.next_button = ctk.CTkButton(self.main_frame, text="Hinda retsepte", command=self.show_recipe_page)
        self.next_button.pack(pady=20)

    def filter_ingredients(self, event):
        value = event.widget.get()
        if value == '':
            self.ingredients_menu['values'] = self.ingredients
        else:
            data = []
            for item in self.ingredients:
                if value.lower() in item.lower():
                    data.append(item)
            self.ingredients_menu['values'] = data

    def add_ingredient(self):
        ingredient = self.ingredients_var.get()
        # Lisa loogika koostisosa lisamiseks ja retseptide otsimiseks
        print(f"Koostisosa lisatud: {ingredient}")

    def show_recipe_page(self):
        # Peida alguslehe raam
        self.main_frame.pack_forget()

        # Loo retseptide hindamise leht
        self.recipe_frame = ctk.CTkFrame(self)
        self.recipe_frame.pack(pady=20, padx=60, fill="both", expand=True)

        self.recipe_label = ctk.CTkLabel(self.recipe_frame, text="Retseptid:")
        self.recipe_label.pack(pady=10)

        self.recipe_text = ctk.CTkTextbox(self.recipe_frame)
        self.recipe_text.pack(pady=10)

        # Jah/Ei nupud
        self.yes_button = ctk.CTkButton(self.recipe_frame, text="Jah", command=self.yes_action)
        self.yes_button.pack(side=tk.LEFT, padx=20, pady=10)

        self.no_button = ctk.CTkButton(self.recipe_frame, text="Ei", command=self.no_action)
        self.no_button.pack(side=tk.RIGHT, padx=20, pady=10)

    def yes_action(self):
        # Lisa loogika, mis juhtub, kui kasutaja valib "Jah"
        print("Retsept valitud: Jah")

    def no_action(self):
        # Lisa loogika, mis juhtub, kui kasutaja valib "Ei"
        print("Retsept valitud: Ei")

if __name__ == "__main__":
    app = RecipeMatchApp()
    app.mainloop()
