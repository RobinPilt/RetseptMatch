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