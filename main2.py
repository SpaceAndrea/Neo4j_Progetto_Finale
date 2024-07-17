import os
from neo4j import GraphDatabase
from datetime import datetime
import json
import time



def carica_dati_iniziali(session, file_path):
    ## idealmente potremmo realizzare un file con tutti i dati
    # Dato che il file è stato creato (tramite il modulo raccolta_dati.py)
    # leggo quei dati dal file json
    with open(file_path, 'r') as file:
        persone = json.loads(file.read())

    ## pulisce il database
    session.run("MATCH (n) DETACH DELETE n")

    # Crea un nodo Person utilizzando i dati dal JSON
    for persona in persone:

        session.run(
            "CREATE (:Person {nome: $nome, cognome: $cognome, età: $età, data_di_nascita: $data_di_nascita, via: $via, città: $città, cap: $cap, email: $email, telefono: $telefono})",
            nome=persona['nome'], cognome=persona['cognome'], età=persona['eta'],
            data_di_nascita=persona['data_di_nascita'],
            via=persona['via'], città=persona['citta'], cap=persona['cap'], email=persona['email'],
            telefono=persona['telefono']
        )

        # Esempio di creazione di una cella e una SIM e delle loro relazioni
        # Questi dati potrebbero venire da un altro file o input dell'utente
        cell_id = "1234"
        location = "34.3N, 56.4W"
        sim_number = persona['telefono']
        date = "2022-10-04"
        time = "12:33:00"

        # Crea un nodo Cell
        session.run(
            "CREATE (:Cell {id: $id, location: $location})",
            id=cell_id, location=location
        )

        # Crea un nodo SIM
        session.run(
            "CREATE (:SIM {number: $number})",
            number=sim_number
        )

        # Crea la relazione OWNS tra Person e SIM
        session.run(
            """
            MATCH (p:Person {telefono: $telefono}), (s:SIM {number: $number})
            CREATE (p)-[:OWNS]->(s)
            """,
            telefono=persona['telefono'], number=sim_number
        )

        # Crea la relazione CONNECTED_TO tra SIM e Cell
        session.run(
            """
            MATCH (s:SIM {number: $number}), (c:Cell {id: $cell_id})
            CREATE (s)-[:CONNECTED_TO {date: $date, time: $time}]->(c)
            """,
            number=sim_number, cell_id=cell_id, date=date, time=time
        )
        # session.run(
        #     """
        #     MATCH (s:SIM {number: $number}), (c:Cell {id: $cell_id})
        #     CREATE (s)-[:CONNECTED_TO {date: $date}]->(c)
        #     """,
        #     number=sim_number, cell_id=cell_id, date=date, time=time
        # )

    print("Dati iniziali caricati nel database Neo4j")

def create_connection():
    
    ## pulisce il terminale
    os.system('cls' if os.name == 'nt' else 'clear')

    URI = "neo4j+s://91e10090.databases.neo4j.io:7687"
    
    USERNAME = 'neo4j'

    PASSWORD = "tjZTPh4DaLFy84_W2RoSM1F_EW9RaGOBJ-SefdLUgrs"

    try:
        driver = GraphDatabase.driver(URI, auth=(USERNAME, PASSWORD))
        driver.verify_connectivity()  
        print('Connesione a Neo4j effettuata')
        return driver

    except:
        print('Impossibile effetturare la connessione, riprovare')
       
def main_menu(session):
    while True:
        ## pulisce il terminale
        os.system('cls' if os.name == 'nt' else 'clear')

        print('''Scegli un opzione:

1. Localizza una persona in base alla data
2. Localizza più persone in base ad una cella telefonica 
3. Localizza più persone in base alla vicinanza ad un luogo
q. Esci
''')

        scelta = input('Scelta: ').lower().strip()
        if scelta == 'q':
            print('\nStai uscendo dal programma')

            ## chiude la connessione con neo4j
            session.close()
            driver.close()

            break

        try:
            scelta = int(scelta)
            assert scelta <= 3
        except:
            print('\nScelta non valida', end='')
            
        match scelta:
            case 1:
                find_form_person_date(session)
            case 2:
                find_fomr_IDcella_date(session)              

def format_date(iso_date_str):
    
    dt = datetime.fromisoformat(iso_date_str.replace("Z", "+00:00"))
    
    return dt.strftime("%Y-%m-%d %H:%M")

def neo4j_datetime_to_string(neo4j_dt):
    
    dt = datetime(
        neo4j_dt.year, 
        neo4j_dt.month, 
        neo4j_dt.day, 
        neo4j_dt.hour, 
        neo4j_dt.minute, 
        neo4j_dt.second, 
        neo4j_dt.nanosecond // 1000,  
        tzinfo=neo4j_dt.tzinfo
    )
    
    return dt.strftime("%Y-%m-%d %H:%M")
     
def find_form_person_date(session):
    
    def trova_relazioni_sim_cella(session, nome, cognome, start_datetime, end_datetime):
        result = session.run(
            "MATCH (p:Persona {nome: $nome, cognome: $cognome})-[:OWNS]->(s:Sim)-[r:CONNECTED_TO]->(c:Cella) "
            "WHERE datetime(r.start) >= datetime($start) AND datetime(r.end) <= datetime($end) "
            "RETURN s.numero AS simNumero, r.start AS start, r.end AS end, c.nome AS cellaNome",
            nome=nome,
            cognome=cognome,
            start=start_datetime,
            end=end_datetime
        )
        start_datetime = format_date(start_datetime)
        end_datetime = format_date(end_datetime)
        relazioni = []
        for record in result:
            relazioni.append({
                "simNumero": record["simNumero"],
                "start": record["start"],
                "end": record["end"],
                "cellaNome": record["cellaNome"]
            })
            
        if relazioni:
            print(f"Connessioni trovate per le SIM di {nome} {cognome} nell'intervallo {start_datetime} - {end_datetime}:")
            for relazione in relazioni:
                print(f"SIM: {relazione['simNumero']}, Start: {neo4j_datetime_to_string(relazione['start'])}, End: {neo4j_datetime_to_string(relazione['end'])}, Cella: {relazione['cellaNome']}")
        else:
            print(f"Nessuna relazione trovata per le SIM di {nome} {cognome} nell'intervallo {start_datetime} - {end_datetime}.")
            
            
    nome = input("Inserici nome: ").capitalize()
    cognome = input("Inserici cognome:").capitalize()
    result = session.run(
    """MATCH p=({nome: $nome, cognome: $cognome})-[:OWNS]->(s:Sim) RETURN s.numero as number;""",
    nome=nome,
    cognome=cognome)
    sim = result.single()
    if sim is None:
        print("\nNessuna SIM trovata, riprovare.")
    else:
        print("inserci l'intervallo di date")
        start_date = input("Data iniziale (yyyy-mm-dd): ")
        start_hour = input("Ora (HH:MM): ")
        end_date = input("Data di fine (yyyy-mm-dd): ")
        end_hour = input("Ora (HH:MM): ")
        start_datetime_str = f"{start_date}T{start_hour}:00Z"
        end_datetime_str = f"{end_date}T{end_hour}:00Z"
        trova_relazioni_sim_cella(session, nome, cognome, start_datetime_str, end_datetime_str)
        input("continua")
        


def find_fomr_IDcella_date(session):
    def trova_relazioni_sim_cella(session, cella_nome, start_datetime, end_datetime):
        result = session.run(
        "MATCH (c:Cella {nome: $cella_nome})<-[r:CONNECTED_TO]-(s:Sim)<-[:OWNS]-(p:Persona) "
        "WHERE datetime(r.start) >= datetime($start) AND datetime(r.end) <= datetime($end) "
        "RETURN s.numero AS simNumero, r.start AS start, r.end AS end, c.nome AS cellaNome, p.nome AS personaNome, p.cognome AS personaCognome",
            cella_nome=cella_nome,
            start=start_datetime,
            end=end_datetime
    )
        
        relazioni = []
        for record in result:
            relazioni.append({
                "simNumero": record["simNumero"],
                "start": neo4j_datetime_to_string(record["start"]),
                "end": neo4j_datetime_to_string(record["end"]),
                "cellaNome": record["cellaNome"],
                "personaNome": record["personaNome"],
                "personaCognome": record["personaCognome"]
            })
        start_datetime = format_date(start_datetime)
        end_datetime = format_date(end_datetime)  
        if relazioni:
            print(f"Connessioni trovate per la cella con Nome {cella_nome} nell'intervallo {start_datetime} - {end_datetime}:")
            for relazione in relazioni:
                print(f"SIM: {relazione['simNumero']}, Nome: {relazione['personaNome'].capitalize()}  {relazione['personaCognome'].capitalize()}, Start: {relazione['start']}, End: {relazione['end']}, Cella: {relazione['cellaNome']}")
        else:
            print(f"Nessuna relazione trovata per la cella con Nome {cella_nome} nell'intervallo {start_datetime} - {end_datetime}.")

    
    def print_celle(session):
        result = session.run(
            "MATCH (c:Cella) "
            "RETURN  c.nome AS cella_nome"
        )
        for record in result:
            print(f"Nome: {record['cella_nome']}")
    while True:
       
        print_celle(session)
        nome = str(input("Inserisci il nome: ")).lower().strip()
        
        print("inserci l'intervallo di date")
        start_date = input("Data iniziale (yyyy-mm-dd): ")
        start_hour = input("Ora (HH:MM): ")
        end_date = input("Data di fine (yyyy-mm-dd): ")
        end_hour = input("Ora (HH:MM): ")
        start_datetime_str = f"{start_date}T{start_hour}:00Z"
        end_datetime_str = f"{end_date}T{end_hour}:00Z"
        
        try:
            trova_relazioni_sim_cella(session, nome, start_datetime_str, end_datetime_str)
            scelta = int(input("1: Continua le ricerche\n0: Torna al menù\nScelta "))
            match scelta:
                case 1: 
                    pass
                case 0: 
                    break
                case _:
                    print("scela non valida")
        except Exception as e:
            print(e)
            print("Errore nell'iserimento")
            time.sleep(1)
        
if __name__ == '__main__':
    driver = create_connection()

    session = driver.session()
   
    main_menu(session)
    
    
   