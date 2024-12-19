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
# Mõningane eeskuju: Tinder
#
# Käivitamisjuhend: Lae alla kõik vajalikud dependecies (nimekirja leiab requirements.txt failist) 
# ja käivita main.py
#
##################################################

import customtkinter as ctk
from customtkinter import CTkImage
import tkinter as tk
import pandas as pd
from PIL import Image
from loogika import saa_koostisosad, lisa_jah_retsept, lisa_ei_retsept, arvuta_sobivus, sorteeri_retseptid, kuva_puuduolevad_koostisosad_hinnad

class RetseptMatchApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        #Sätime kujunduse moodi
        ctk.set_appearance_mode("light")
        ctk.set_default_color_theme("green")

        #Ikooni muutmine
        self.wm_iconbitmap("ressursid/pildid/logo_notext.ico")

        #Keelame akna suuruse muutmise
        self.resizable(False, False)

        #Kohandatud fondid
        self.vaike_font = ctk.CTkFont(family="Segoe UI", size=14)
        self.keskmine_font = ctk.CTkFont(family="Segoe UI Semibold", size=16)
        self.suur_font = ctk.CTkFont(family="Segoe UI Semibold", size=24)

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
        csv_fail = pd.read_csv('ressursid/andmed/koostisosad.csv')
        return csv_fail['koostisosa'].tolist()
    
    def lae_retseptid(self):
        csv_fail = pd.read_csv('ressursid/andmed/retseptid.csv')
        return csv_fail

    #Avaleht
    def avaleht(self):
        #Loome frameid elementide paigutamiseks
        self.main_section = ctk.CTkFrame(self.main_frame)
        self.main_section.pack(pady=20, padx=20, fill="both", expand=True)
        self.left_frame = ctk.CTkFrame(self.main_section)
        self.left_frame.pack(side="left", padx=20, pady=20, fill="y", expand=True)
        self.right_frame = ctk.CTkFrame(self.main_section)
        self.right_frame.pack(side="right", padx=20, pady=20, fill="y", expand=True)

        #Koostisosade sisestamise sektsioon
        self.koostisosa_label = ctk.CTkLabel(self.left_frame, text="Sisesta koostisosad:", font=self.vaike_font)
        self.koostisosa_label.pack(pady=10)

        #Koostisosade otsimise funktsionaalsus
        self.search_var = tk.StringVar()
        self.search_box = ctk.CTkEntry(self.left_frame, textvariable=self.search_var, font=self.vaike_font)
        self.search_box.pack(pady=10)
        self.search_box.bind('<KeyRelease>', self.filtreeri_koostisosad)

        #Keritav frame koostisosade jaoks
        self.scrollable_frame = ctk.CTkScrollableFrame(self.left_frame, width=200, height=400, corner_radius=0)
        self.scrollable_frame.pack(pady=10)
        self.koostisosa_buttons = []
        for koostisosa in self.koostisosad:
            button = ctk.CTkButton(self.scrollable_frame, text=koostisosa, command=lambda k=koostisosa: self.lisa_koostisosa_main(k), font=self.vaike_font)
            button.pack(pady=5)
            self.koostisosa_buttons.append(button)

        #Kuvame lisatud koostisosad
        self.koostisosad_label = ctk.CTkLabel(self.right_frame, text="Lisatud koostisosad:", font=self.vaike_font)
        self.koostisosad_label.pack(pady=10)
        self.koostisosad_listbox = ctk.CTkTextbox(self.right_frame, height=300, width=200, font=self.vaike_font, corner_radius=0)
        self.koostisosad_listbox.pack(pady=10)
        self.koostisosad_listbox.configure(state="disabled")

        #Nupp retseptide hindamise lehele liikumiseks
        self.retsept_nupp = ctk.CTkButton(self.right_frame, text="Leia oma retsept!", command=self.retsept_leht, font=self.keskmine_font)
        self.retsept_nupp.pack(side="bottom", pady=20)

    #Koostisosade otsimise funktsioon
    def filtreeri_koostisosad(self, event):
        search_term = self.search_var.get().lower()
        for button in self.koostisosa_buttons:
            button.pack_forget()
        for button in self.koostisosa_buttons:
            if search_term in button.cget("text").lower():
                button.pack(pady=5)
            else:
                button.pack_forget()

    def lisa_koostisosa_main(self, koostisosa):
        if koostisosa in self.koostisosad:
            #Lisame koostisosa järjendisse loogika.py failis
            from loogika import lisa_koostisosa
            lisa_koostisosa(koostisosa)
            tekst = f"Koostisosa lisatud: {koostisosa}."
            print(tekst)
            self.koostisosad_listbox.configure(state="normal")
            self.koostisosad_listbox.insert(tk.END, f"{koostisosa}\n")  #Lisame koostisosa uuele reale
            self.koostisosad_listbox.configure(state="disabled")
        else:
            tekst = f"Koostisosa '{koostisosa}' ei ole lubatud."
            print(tekst)

    #Retsepti valimise lehekülg
    def retsept_leht(self):
        self.main_frame.pack_forget()

        self.retsept_frame = ctk.CTkFrame(self, width=600, height=400)
        self.retsept_frame.pack(pady=20, padx=60, fill="both", expand=True)
        self.retsept_frame.pack_propagate(False) 

        self.retsept_pealkiri = ctk.CTkLabel(self.retsept_frame, text="", font=self.suur_font)
        self.retsept_pealkiri.pack(pady=55)

        self.retsept_pilt_label = ctk.CTkLabel(self.retsept_frame, text="")
        self.retsept_pilt_label.pack(pady=10)

        #Sorteerime ja filtreerime retseptid sobivuse järgi
        kasutaja_koostisosad = saa_koostisosad()
        self.retseptid = sorteeri_retseptid(self.retseptid, kasutaja_koostisosad)

        #Kuvame esimese retsepti
        self.kuva_retsept()

    def kuva_retsept(self):
        if self.praegune_retsept < len(self.retseptid):
            retsept = self.retseptid.iloc[self.praegune_retsept]
            self.retsept_pealkiri.configure(text=retsept['retsept'])

            #Kuvame retsepti pildi
            image_path = retsept['pilt']
            image = Image.open(image_path)
            image = image.resize((200, 200))
            foto = CTkImage(light_image=image, size=(200, 200))

            self.retsept_pilt_label.configure(image=foto, text="")
            self.retsept_pilt_label.image = foto
            
            self.jah_nupp = ctk.CTkButton(self.retsept_frame, text="Jah", command=self.jah_action, width=80, height=80, corner_radius=10, font=self.suur_font)
            self.jah_nupp.place(x=65, y=220)
            self.ei_nupp = ctk.CTkButton(self.retsept_frame, text="Ei", command=self.ei_action, width=80, height=80, corner_radius=10, font=self.suur_font)
            self.ei_nupp.place(x=530, y=220)

            #Arvutame ja kuvame sobivust protsentuaalselt
            kasutaja_koostisosad = saa_koostisosad()
            sobivus_protsent = arvuta_sobivus(retsept['koostisosad'], kasutaja_koostisosad)
            
            if hasattr(self, 'sobivus_label'):
                self.sobivus_label.configure(text=f"{sobivus_protsent:.0f}%")
            else:
                self.sobivus_label = ctk.CTkLabel(self.retsept_frame, text=f"{sobivus_protsent:.0f}%", font=ctk.CTkFont(family="Segoe UI Semibold", size=30))
                self.sobivus_label.place(x=400, y=130)  #Absoluutne positsioneerimine pildi elemendi peal

        #Kui kõik retseptid on otsas
        else:
            self.retsept_frame.pack_forget()  #Peidame retseptide lehe
            self.jah_retseptid_leht()

    def jah_retseptid_leht(self):
        self.main_frame.pack_forget()
        if hasattr(self, 'retsept_frame'):
            self.retsept_frame.pack_forget()

        self.jah_retseptid_frame = ctk.CTkScrollableFrame(self)
        self.jah_retseptid_frame.pack(pady=20, padx=60, fill="both", expand=True)

        if not self.jah_retseptid:
            ei_leitud_label = ctk.CTkLabel(self.jah_retseptid_frame, text="Ei leitud ühtegi sobilikku retsepti.", font=self.suur_font)
            ei_leitud_label.pack(pady=200)
        else:
            for retsept in self.jah_retseptid:
                retsept_frame = ctk.CTkFrame(self.jah_retseptid_frame)
                retsept_frame.pack(pady=10, padx=10, fill="x")

                retsept_label = ctk.CTkLabel(retsept_frame, text=retsept, font=self.keskmine_font)
                retsept_label.pack(side="left", padx=10)

                detailid_nupp = ctk.CTkButton(retsept_frame, text="Kuva detailid", command=lambda r=retsept: self.kuva_jah_retsepti_detailid(r))
                detailid_nupp.pack(side="right", padx=10)

    def kuva_jah_retsepti_detailid(self, retsept_nimi):
        #Leiame retsepti CSV failist
        retsept = self.retseptid[self.retseptid['retsept'] == retsept_nimi].iloc[0]

        #Arvutame sobivuse ja puuduolevad koostisosad
        kasutaja_koostisosad = saa_koostisosad()
        retsept_koostisosad = set(retsept['koostisosad'].split(', '))
        puuduolevad_koostisosad = retsept_koostisosad - set(kasutaja_koostisosad)
        olemasolevad_koostisosad = retsept_koostisosad.intersection(set(kasutaja_koostisosad))

        #Kuvame detailse vaate
        self.jah_retseptid_frame.pack_forget()

        self.detailne_retsept_frame = ctk.CTkFrame(self)
        self.detailne_retsept_frame.pack(pady=20, padx=60, fill="both", expand=True)

        self.detailne_retsept_label = ctk.CTkLabel(self.detailne_retsept_frame, text=retsept['retsept'], font=self.keskmine_font)
        self.detailne_retsept_label.pack(pady=30)

        self.detailne_retsept_juhised = ctk.CTkLabel(self.detailne_retsept_frame, text=f"Juhised: {retsept['juhised']}", font=self.vaike_font, wraplength=400, justify="left", bg_color="white", width=420, height=90)
        self.detailne_retsept_juhised.pack(pady=10, padx=50)

        self.olemasolevad_label = ctk.CTkLabel(self.detailne_retsept_frame, text=f"Olemasolevad koostisosad: {', '.join(olemasolevad_koostisosad)}", font=self.keskmine_font, text_color="green")
        self.olemasolevad_label.pack(pady=10)

        self.puuduolevad_label = ctk.CTkLabel(self.detailne_retsept_frame, text=f"Puuduolevad koostisosad: {', '.join(puuduolevad_koostisosad)}", font=self.keskmine_font, text_color="red")
        self.puuduolevad_label.pack(pady=10)

        #Kuvame puuduolevate koostisosade hinnad
        hinnad = kuva_puuduolevad_koostisosad_hinnad(puuduolevad_koostisosad)
        hinnad_tekst = "\n".join([f"{koostisosa}: {hind}" for koostisosa, hind in hinnad.items()])
        self.hinnad_label = ctk.CTkLabel(self.detailne_retsept_frame, text=f"Puuduolevate koostisosade hinnad:\n{hinnad_tekst}", font=self.keskmine_font)
        self.hinnad_label.pack(pady=10)

        self.tagasi_nupp = ctk.CTkButton(self.detailne_retsept_frame, text="Tagasi", command=self.tagasi_jah_retseptid_leht)
        self.tagasi_nupp.pack(pady=20)

    def tagasi_jah_retseptid_leht(self):
        self.detailne_retsept_frame.pack_forget()
        self.jah_retseptid_leht()

    #Lisa retsept "jah" järjendisse
    def jah_action(self):
        retsept = self.retseptid.iloc[self.praegune_retsept]
        lisa_jah_retsept(retsept['retsept'])
        self.jah_retseptid.append(retsept['retsept'])
        print(f"Retsept valitud: Jah - {retsept['retsept']}")
        self.praegune_retsept += 1
        self.kuva_retsept()

    #Lisa retsept "ei" järjendisse
    def ei_action(self):
        retsept = self.retseptid.iloc[self.praegune_retsept]
        lisa_ei_retsept(retsept['retsept'])
        print(f"Retsept valitud: Ei - {retsept['retsept']}")
        self.praegune_retsept += 1
        self.kuva_retsept()

if __name__ == "__main__":
    app = RetseptMatchApp()
    app.mainloop()