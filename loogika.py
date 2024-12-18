#Siin asuvad programmi loogikat hõlmavad funktsioonid.

import requests
import unicodedata
from bs4 import BeautifulSoup

koostisosad_list = []
jah_retseptid = []
ei_retseptid = []
salvestatud_hinnad = {}

def lisa_koostisosa(koostisosa):
    koostisosad_list.append(koostisosa)

def saa_koostisosad():
    return koostisosad_list

def lisa_jah_retsept(retsept):
    jah_retseptid.append(retsept)

def saa_jah_retseptid():
    return jah_retseptid

def lisa_ei_retsept(retsept):
    ei_retseptid.append(retsept)

def saa_ei_retseptid():
    return ei_retseptid

#Arvutame retsepti sobivuse kasutaja koostisosadega
def arvuta_sobivus(retsept_koostisosad, kasutaja_koostisosad):
    retsept_koostisosad = set(retsept_koostisosad.split(', '))
    kasutaja_koostisosad = set(kasutaja_koostisosad)
    kattuvus = retsept_koostisosad.intersection(kasutaja_koostisosad)
    sobivus_protsent = (len(kattuvus) / len(retsept_koostisosad)) * 100
    return sobivus_protsent

#Sorteerime retseptid sobivuse järgi
def sorteeri_retseptid(retseptid, kasutaja_koostisosad):
    retseptid['sobivus'] = retseptid['koostisosad'].apply(lambda x: arvuta_sobivus(x, kasutaja_koostisosad))
    sorteeritud_retseptid = retseptid[retseptid['sobivus'] >= 50].sort_values(by='sobivus', ascending=False)
    return sorteeritud_retseptid

def teisenda_tapitahed(tekst):
    return ''.join((c for c in unicodedata.normalize('NFD', tekst) if unicodedata.category(c) != 'Mn'))

#Scrape-ime koostisosade hinnad
def leia_koostisosa_hind(koostisosa):
    if koostisosa in salvestatud_hinnad:
        return salvestatud_hinnad[koostisosa]
    
    koostisosa_url = teisenda_tapitahed(koostisosa)
    url = f"https://ostukorvid.ee/kategooriad/{koostisosa_url}?price=item"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    #Otsime esimese tulemuse hinna ja poe
    hind_elem = soup.find('div', class_='text-xl font-bold')
    pood_elem = soup.find('span', class_=lambda x: x and x.startswith('inline-block whitespace-nowrap rounded px-1 text-center text-xs font-bold uppercase'))
    
    if hind_elem and pood_elem:
        hind = hind_elem.text.strip().replace('▼', '').strip()
        pood = pood_elem.text.strip()
        hind_pood = f"{hind} ({pood})"
        salvestatud_hinnad[koostisosa] = hind_pood
        return hind_pood
    else:
        return "Hind puudub"

def kuva_puuduolevad_koostisosad_hinnad(puuduolevad_koostisosad):
    hinnad = {}
    for koostisosa in puuduolevad_koostisosad:
        hind = leia_koostisosa_hind(koostisosa)
        hinnad[koostisosa] = hind
    return hinnad