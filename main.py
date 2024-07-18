import os
from neo4j import GraphDatabase
from generators import CreateDataBase
import ricerche as rc

def carica_dati_iniziali(session):
    ## idealmente potremmo realizzare un file con tutti i dati
    # Dato che il file è stato creato (tramite il modulo raccolta_dati.py)
    # leggo quei dati dal file json
    createDB = CreateDataBase()

    ## pulisce il database
    session.run("""
                MATCH ()-[r]->()DELETE r
                MATCH (n) DETACH DELETE n""")

    try:
        createDB.crea_celle(session)
        createDB.crea_persone(session)
        createDB.crea_sim(session)
        createDB.crea_relazioni_persona_sim(session)
        createDB.crea_relazioni_sim_cella(session)
    except Exception as e:
        print(e)

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

if __name__ == '__main__':
    driver = create_connection() 

    ## carica i dati iniziali
    session = driver.session()
    # carica_dati_iniziali(session)

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
            input('Premi invio per continuare...')

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
                rc.find_form_person_date(session)
            case 2:
                rc.find_fomr_IDcella_date(session)
            case 3:
                rc.find_people_near_location(session)