################################################
# Programmeerimine I
# 2024/2025 sügissemester
#
# Projekt Meda
# Teema: RetseptMatch
#
#
# Autorid: Robin Sander Pilt, Kristjan Peil
#
# mõningane eeskuju: Tinder
#
# Lisakommentaar: Käivita main.py
#
##################################################

import customtkinter as ctk
from customtkinter import CTkImage
import tkinter as tk
from tkinter import ttk
import pandas as pd
from PIL import Image
from loogika import lisa_koostisosa, saa_koostisosad, lisa_jah_retsept, lisa_ei_retsept

class RetseptMatchApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("RetseptMatch")
        self.geometry("800x600")

        self.koostisosad = self.lae_koostisosad()
        self.retseptid = self.lae_retseptid()
        self.praegune_retsept = 0

        self.jah_retseptid = []
        self.ei_retseptid = []

        self.main_frame = ctk.CTkFrame(self)
        self.main_frame.pack(pady=20, padx=60, fill="both", expand=True)

        self.avaleht()

    def lae_koostisosad(self):
        df = pd.read_csv('ressursid/andmed/koostisosad.csv')
        return df['koostisosa'].tolist()
    
    def lae_retseptid(self):
        df = pd.read_csv('ressursid/andmed/retseptid.csv')
        return df

    # Avalehe elemendid
    def avaleht(self):
        # Koostisosade sisestamise sektsioon
        self.koostisosa_label = ctk.CTkLabel(self.main_frame, text="Sisesta koostisosad:")
        self.koostisosa_label.pack(pady=10)

        self.koostisosad_var = ctk.StringVar(value="Vali toiduaine")
        self.koostisosa_menu = ctk.CTkComboBox(self.main_frame, variable=self.koostisosad_var, values=self.koostisosad)
        self.koostisosa_menu.pack(pady=10)
        self.koostisosa_menu.bind('<KeyRelease>', self.filtreeri_koostisosad)

        self.lisa_nupp = ctk.CTkButton(self.main_frame, text="Lisa", command=self.lisa_koostisosa)
        self.lisa_nupp.pack(pady=10)

        self.tekst_label = ctk.CTkLabel(self.main_frame, text="")
        self.tekst_label.pack(pady=10)

        # Nupp retseptide hindamise lehele liikumiseks
        self.retsept_nupp = ctk.CTkButton(self.main_frame, text="Leia oma retsept!", command=self.retsept_leht)
        self.retsept_nupp.pack(pady=20)

    def filtreeri_koostisosad(self, event):
        väärtus = event.widget.get()
        if väärtus == '':
            self.koostisosa_menu['values'] = self.koostisosad
        else:
            andmed = []
            for item in self.koostisosad:
                if väärtus.lower() in item.lower():
                    andmed.append(item)
            self.koostisosa_menu['values'] = andmed

    def lisa_koostisosa(self):
        koostisosa = self.koostisosad_var.get()
        if koostisosa in self.koostisosad:
            # Lisa koostisosa järjendisse loogika.py failis
            lisa_koostisosa(koostisosa)
            tekst = f"Koostisosa lisatud: {koostisosa}."
            print(tekst)
            self.tekst_label.configure(text=tekst)
        else:
            tekst = f"Koostisosa '{koostisosa}' ei ole lubatud."
            print(tekst)
            self.tekst_label.configure(text=tekst)

    # Retsepti valimise lehekülje elemendid
    def retsept_leht(self):
        self.main_frame.pack_forget()

        self.retsept_frame = ctk.CTkFrame(self)
        self.retsept_frame.pack(pady=20, padx=60, fill="both", expand=True)

        self.retsept_label = ctk.CTkLabel(self.retsept_frame, text="Retseptid:", font=("Arial", 16))
        self.retsept_label.pack(pady=10)

        self.retsept_pealkiri = ctk.CTkLabel(self.retsept_frame, text="", font=("Arial", 14))
        self.retsept_pealkiri.pack(pady=10)

        self.retsept_pilt_label = ctk.CTkLabel(self.retsept_frame, text="")
        self.retsept_pilt_label.pack(pady=10)

        self.juhised_nupp = ctk.CTkButton(self.retsept_frame, text="Kuva juhised", command=self.rohkem_infot)
        self.juhised_nupp.pack(pady=10)

        self.retsepti_tekst = ctk.CTkTextbox(self.retsept_frame, height=400, width=300)
        self.retsepti_tekst.pack(pady=10)
        self.retsepti_tekst.pack_forget()  # Peidame alguses

        self.jah_nupp = ctk.CTkButton(self.retsept_frame, text="Jah", command=self.jah_action)
        self.jah_nupp.pack(side=tk.LEFT, padx=20, pady=10)

        self.ei_nupp = ctk.CTkButton(self.retsept_frame, text="Ei", command=self.ei_action)
        self.ei_nupp.pack(side=tk.RIGHT, padx=20, pady=10)

        # Kuvame esimese retsepti
        self.kuva_retsept()

    def kuva_retsept(self):
        if self.praegune_retsept < len(self.retseptid):
            retsept = self.retseptid.iloc[self.praegune_retsept]
            self.retsept_pealkiri.configure(text=retsept['retsept'])

            # Kuvame retsepti pildi
            image_path = retsept['pilt']
            image = Image.open(image_path)
            image = image.resize((200, 200))
            foto = CTkImage(light_image=image, size=(200, 200))

            self.retsept_pilt_label.configure(image=foto, text="")
            self.retsept_pilt_label.image = foto

            self.retsepti_tekst.pack_forget()
            self.juhised_nupp.pack(pady=10)
            self.jah_nupp.pack(side=tk.LEFT, padx=20, pady=10)
            self.ei_nupp.pack(side=tk.RIGHT, padx=20, pady=10)

        # Kui kõik retseptid on otsas
        else:
            self.retsept_pealkiri.configure(text="Kõik retseptid on läbi vaadatud.")
            self.retsept_pilt_label.configure(image='', text='')
            self.juhised_nupp.pack_forget()
            self.retsepti_tekst.pack_forget()
            self.jah_nupp.pack_forget()
            self.ei_nupp.pack_forget()

    def rohkem_infot(self):
        retsept = self.retseptid.iloc[self.praegune_retsept]
        self.retsepti_tekst.configure(state='normal')
        self.retsepti_tekst.delete(1.0, tk.END)
        self.retsepti_tekst.insert(tk.END, f"Koostisosad: {retsept['koostisosad']}\n")
        self.retsepti_tekst.insert(tk.END, f"Juhised: {retsept['juhised']}\n")
        self.retsepti_tekst.configure(state='disabled')
        self.retsepti_tekst.pack(pady=10)
        self.juhised_nupp.pack_forget()

    # Lisa retsept "jah" järjendisse
    def jah_action(self):
        retsept = self.retseptid.iloc[self.praegune_retsept]
        lisa_jah_retsept(retsept['retsept'])
        print(f"Retsept valitud: Jah - {retsept['retsept']}")
        self.praegune_retsept += 1
        self.kuva_retsept()

    # Lisa retsept "ei" järjendisse
    def ei_action(self):
        retsept = self.retseptid.iloc[self.praegune_retsept]
        lisa_ei_retsept(retsept['retsept'])
        print(f"Retsept valitud: Ei - {retsept['retsept']}")
        self.praegune_retsept += 1
        self.kuva_retsept()

if __name__ == "__main__":
    app = RetseptMatchApp()
    app.mainloop()