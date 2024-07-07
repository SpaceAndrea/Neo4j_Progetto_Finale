#conversione della data da stringa a data vera e propria

import json
from datetime import datetime

file_json = "dati_persona.json"                                 # File JSON da cui caricare i dati

# caricamento dei dati dal json
def carica_dati(file_json):
    try:
        with open(file_json, "r") as f:
            data = json.load(f)
            print("file aperto con successo")
        return data
    except FileNotFoundError:
        print(f"Il file {file_json} non è stato trovato.")
        return []
    except json.JSONDecodeError:
        print(f"Errore nel decodificare {file_json}")
        return []

    
# Funzione per convertire la data di nascita
def converti_data_nascita(data):
    for persona in data:
        try:
            data_di_nascita_str = persona["data_di_nascita"]
            # Convertire la stringa della data in un oggetto datetime.date
            data_di_nascita_date = datetime.strptime(data_di_nascita_str, "%Y-%m-%d").date()
            persona["data_di_nascita"] = data_di_nascita_date
        except KeyError:
            print(f"Chiave 'data_di_nascita' non trovata per la persona: {persona}")
        except ValueError as e:
            print(f"Errore nella conversione della data per {persona['nome']} {persona['cognome']}: {e}")

    return data



dati = carica_dati(file_json)                           # Caricare i dati dal file JSON

#print("Dati caricati dal file JSON:")
#print(dati)  # Stampa i dati per debug

date_convertite = converti_data_nascita(dati)           # Convertire la data di nascita in oggetti datetime.date

for persona in date_convertite:
    print(persona)

if date_convertite:
    print(date_convertite[0]["data_di_nascita"])