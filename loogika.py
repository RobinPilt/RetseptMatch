# Siia tuleb programmi loogikat hõlmavad funktsioonid.
# Näiteks algoritm, mis arvutab kasutaja sisestatud andmete põhjal välja sobivama retsepti.

koostisosad_list = []
jah_retseptid = []
ei_retseptid = []

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

def arvuta_sobivus(retsept_koostisosad, kasutaja_koostisosad):
    retsept_koostisosad = set(retsept_koostisosad.split(', '))
    kasutaja_koostisosad = set(kasutaja_koostisosad)
    kattuvus = retsept_koostisosad.intersection(kasutaja_koostisosad)
    sobivus_protsent = (len(kattuvus) / len(retsept_koostisosad)) * 100
    return sobivus_protsent

def sorteeri_retseptid(retseptid, kasutaja_koostisosad):
    retseptid['sobivus'] = retseptid['koostisosad'].apply(lambda x: arvuta_sobivus(x, kasutaja_koostisosad))
    sorteeritud_retseptid = retseptid[retseptid['sobivus'] >= 30].sort_values(by='sobivus', ascending=False)
    return sorteeritud_retseptid