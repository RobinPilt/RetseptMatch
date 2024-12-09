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
from loogika import lisa_koostisosa, saa_koostisosad, lisa_jah_retsept, lisa_ei_retsept, arvuta_sobivus, sorteeri_retseptid

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

        self.lisa_nupp = ctk.CTkButton(self.main_frame, text="Lisa", command=self.lisa_koostisosa_main)
        self.lisa_nupp.pack(pady=10)

        self.tekst_label = ctk.CTkLabel(self.main_frame, text="")
        self.tekst_label.pack(pady=10)

        # Kuvame lisatud koostisosad
        self.koostisosad_frame = ctk.CTkFrame(self.main_frame)
        self.koostisosad_frame.pack(pady=10)
        self.koostisosad_label = ctk.CTkLabel(self.koostisosad_frame, text="Lisatud koostisosad:")
        self.koostisosad_label.pack(pady=10)
        self.koostisosad_listbox = tk.Listbox(self.koostisosad_frame, height=10, width=50)
        self.koostisosad_listbox.pack(pady=10)

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

    def lisa_koostisosa_main(self):
        koostisosa = self.koostisosad_var.get()
        if koostisosa in self.koostisosad:
            # Lisa koostisosa järjendisse loogika.py failis
            from loogika import lisa_koostisosa
            lisa_koostisosa(koostisosa)
            tekst = f"Koostisosa lisatud: {koostisosa}."
            print(tekst)
            self.tekst_label.configure(text=tekst)
            self.koostisosad_listbox.insert(tk.END, koostisosa)  # Lisa koostisosa listboxi
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

        # Sorteeri ja filtreeri retseptid sobivuse järgi
        kasutaja_koostisosad = saa_koostisosad()
        self.retseptid = sorteeri_retseptid(self.retseptid, kasutaja_koostisosad)

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

            # Arvuta ja kuva sobivus protsentuaalselt
            kasutaja_koostisosad = saa_koostisosad()
            sobivus_protsent = arvuta_sobivus(retsept['koostisosad'], kasutaja_koostisosad)
            print(f"Sobivus retseptiga '{retsept['retsept']}': {sobivus_protsent:.2f}%")

            # Kuvame sobivuse protsendi UI-s kasti sees
            if hasattr(self, 'sobivus_frame'):
                self.sobivus_label.configure(text=f"Sobivus: {sobivus_protsent:.2f}%")
            else:
                self.sobivus_frame = ctk.CTkFrame(self.retsept_frame)
                self.sobivus_frame.pack(pady=10)
                self.sobivus_label = ctk.CTkLabel(self.sobivus_frame, text=f"Sobivus: {sobivus_protsent:.2f}%")
                self.sobivus_label.pack(pady=10)
            
            # Arvuta ja kuva puuduolevad koostisosad
            retsept_koostisosad = set(retsept['koostisosad'].split(', '))
            puuduolevad_koostisosad = retsept_koostisosad - set(kasutaja_koostisosad)
            if hasattr(self, 'puuduolevad_frame'):
                self.puuduolevad_label.configure(text=f"Puuduolevad koostisosad: {', '.join(puuduolevad_koostisosad)}")
            else:
                self.puuduolevad_frame = ctk.CTkFrame(self.retsept_frame)
                self.puuduolevad_frame.pack(pady=10)
                self.puuduolevad_label = ctk.CTkLabel(self.puuduolevad_frame, text=f"Puuduolevad koostisosad: {', '.join(puuduolevad_koostisosad)}")
                self.puuduolevad_label.pack(pady=10)

        # Kui kõik retseptid on otsas
        else:
            self.retsept_frame.pack_forget()  # Peidame retseptide lehe
            self.jah_retseptid_leht()

    def jah_retseptid_leht(self):
        self.main_frame.pack_forget()
        if hasattr(self, 'retsept_frame'):
            self.retsept_frame.pack_forget()

        self.jah_retseptid_frame = ctk.CTkFrame(self)
        self.jah_retseptid_frame.pack(pady=20, padx=60, fill="both", expand=True)

        self.jah_retseptid_label = ctk.CTkLabel(self.jah_retseptid_frame, text="Jah vastatud retseptid:", font=("Arial", 16))
        self.jah_retseptid_label.pack(pady=10)

        if not self.jah_retseptid:
            ei_leitud_label = ctk.CTkLabel(self.jah_retseptid_frame, text="Te ei leidnud ühtegi sobilikku retsepti.", font=("Arial", 14))
            ei_leitud_label.pack(pady=10)
        else:
            for retsept in self.jah_retseptid:
                retsept_frame = ctk.CTkFrame(self.jah_retseptid_frame)
                retsept_frame.pack(pady=10, padx=10, fill="x")

                retsept_label = ctk.CTkLabel(retsept_frame, text=retsept, font=("Arial", 14))
                retsept_label.pack(side="left", padx=10)

                detailid_nupp = ctk.CTkButton(retsept_frame, text="Kuva detailid", command=lambda r=retsept: self.kuva_jah_retsepti_detailid(r))
                detailid_nupp.pack(side="right", padx=10)

    def kuva_jah_retsepti_detailid(self, retsept_nimi):
        # Leia retsept andmebaasist
        retsept = self.retseptid[self.retseptid['retsept'] == retsept_nimi].iloc[0]

        # Arvuta sobivus ja puuduolevad koostisosad
        kasutaja_koostisosad = saa_koostisosad()
        sobivus_protsent = arvuta_sobivus(retsept['koostisosad'], kasutaja_koostisosad)
        retsept_koostisosad = set(retsept['koostisosad'].split(', '))
        puuduolevad_koostisosad = retsept_koostisosad - set(kasutaja_koostisosad)

        # Kuvame detailse vaate
        self.jah_retseptid_frame.pack_forget()

        self.detailne_retsept_frame = ctk.CTkFrame(self)
        self.detailne_retsept_frame.pack(pady=20, padx=60, fill="both", expand=True)

        self.detailne_retsept_label = ctk.CTkLabel(self.detailne_retsept_frame, text=retsept['retsept'], font=("Arial", 16))
        self.detailne_retsept_label.pack(pady=10)

        self.detailne_retsept_koostisosad = ctk.CTkLabel(self.detailne_retsept_frame, text=f"Koostisosad: {retsept['koostisosad']}", font=("Arial", 14))
        self.detailne_retsept_koostisosad.pack(pady=10)

        self.detailne_retsept_juhised = ctk.CTkLabel(self.detailne_retsept_frame, text=f"Juhised: {retsept['juhised']}", font=("Arial", 14))
        self.detailne_retsept_juhised.pack(pady=10)

        self.sobivus_label = ctk.CTkLabel(self.detailne_retsept_frame, text=f"Sobivus: {sobivus_protsent:.2f}%", font=("Arial", 14))
        self.sobivus_label.pack(pady=10)

        self.puuduolevad_label = ctk.CTkLabel(self.detailne_retsept_frame, text=f"Puuduolevad koostisosad: {', '.join(puuduolevad_koostisosad)}", font=("Arial", 14))
        self.puuduolevad_label.pack(pady=10)

        self.tagasi_nupp = ctk.CTkButton(self.detailne_retsept_frame, text="Tagasi", command=self.tagasi_jah_retseptid_leht)
        self.tagasi_nupp.pack(pady=20)


    def tagasi_jah_retseptid_leht(self):
        self.detailne_retsept_frame.pack_forget()
        self.jah_retseptid_leht()

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
        self.jah_retseptid.append(retsept['retsept'])
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