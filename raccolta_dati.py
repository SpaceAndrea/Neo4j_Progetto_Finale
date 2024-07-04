import json

def raccogli_dati_persona():
    persona = {
        #informazioni personali
        "nome": input("Inserisci il nome: "),
        "cognome": input("Inserisci il cognome: "),
        "età": int(input("Inserisci l'età: ")),
        "data_di_nascita": input("Inserisci la data di nascita con un formato YYYY-MM-DD: "),
        #indirizzo
        "via": input("Inserisci la via: "),
        "città": input("Inserisci la città: "),
        "cap": input("Inserisci il CAP: "),
        #contatti
        "email": input("Inserisci l'email: "),
        "telefono": input("Inserisci il numero di telefono: ")
    }

    
    with open("dati_persona.json", "w") as file:
        json.dump(persona, file, indent=4)

    print("Dati salvati in dati_persona.json")


raccogli_dati_persona()