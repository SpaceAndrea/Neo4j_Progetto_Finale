import os
from neo4j import GraphDatabase
import json


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
        time = "12:33````:00"

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
        # session.run(
        #     """
        #     MATCH (s:SIM {number: $number}), (c:Cell {id: $cell_id})
        #     CREATE (s)-[:CONNECTED_TO {date: $date, time: $time}]->(c)
        #     """,
        #     number=sim_number, cell_id=cell_id, date=date, time=time
        # )
        session.run(
            """
            MATCH (s:SIM {number: $number}), (c:Cell {id: $cell_id})
            CREATE (s)-[:CONNECTED_TO {date: $date}]->(c)
            """,
            number=sim_number, cell_id=cell_id, date=date, time=time
        )

    print("Dati iniziali caricati nel database Neo4j")


if __name__ == '__main__':

    while True:
        ## pulisce il terminale
        os.system('cls' if os.name == 'nt' else 'clear')

        URI = input(
            'Inserire l\'URI del database (lascia vuoto per inserire "neo4j+s://29b76056.databases.neo4j.io:7687"): ').strip()
        if URI == '':
            URI = "neo4j+s://29b76056.databases.neo4j.io:7687"
            URI = "neo4j+s://a9fd4bc7.databases.neo4j.io"

        USERNAME = input('Inserire lo username (lascia vuoto per inserire "neo4j"): ').strip()
        if USERNAME == '':
            USERNAME = 'neo4j'

        PASSWORD = input(
            'Inserire la password (lascia vuoto per inserire "ACVoeucPiAGAB55HVjcRMKW8cnALwVx2E4Qj8jWDJHI": ').strip()
        if PASSWORD == '':
            PASSWORD = 'ACVoeucPiAGAB55HVjcRMKW8cnALwVx2E4Qj8jWDJHI'
            PASSWORD = "gCjs4B5x88IIhbRC1f6eLQ21H9QtGcCCyulaChCaH6c"

        try:
            driver = GraphDatabase.driver(URI, auth=(USERNAME, PASSWORD))
            driver.verify_connectivity()  ## senza questa funzione anche se la connessione al db non e' avvenuta non dava errore
            print('Connesione a Neo4j effettuata')

            break

        except:
            print('Impossibile effetturare la connessione, riprovare')
            input('\nPremi invio per continuare...')

    ## carica i dati iniziali
    session = driver.session()
    carica_dati_iniziali(session, 'dati_persona.json')
    print('Caricati i dati iniziali')
    input('\nPremi invio per continuare...')

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

        if scelta == 1:
            nome = input('Inserire il nome della persona: ').strip()
            cognome = input('Inserire il cognnome della persona: ').strip()

            ## trova la sim della persona
            result = session.run(
                """MATCH p=({nome: $nome, cognome: $cognome})-[:OWNS]->(s:SIM) RETURN s.number as number;""",
                nome=nome,
                cognome=cognome
            )

            sim = result.single()
            if sim is None:
                print("\nNessuna SIM trovata, riprovare.")

            else:
                numero = sim['number']

                start_date = input("Inserire la data di inizio (YYYY-MM-DD): ").strip()
                end_date = input("Inserire la data di fine (YYYY-MM-DD): ").strip()
                result = session.run(
                    """
                    MATCH (s:SIM {number: $numero})-[r:CONNECTED_TO]->(c:Cell)
                    WHERE r.date >= $start_date AND r.date <= $end_date
                    RETURN c.id AS cell_id, c.location AS cell_location
                    """,
                    numero=numero, start_date=start_date, end_date=end_date
                )

                cells = []
                for record in result:
                    cells.append({
                        "id": record["cell_id"],
                        "location": record["cell_location"]
                    })

                if cells: print("\nCelle trovate:")
                else: print("\nNessun riscontro trovato.")

                i = 1
                for c in cells:
                    print(f"[{i}] ID: {c['id']}, COORDINATE: {c['location']}")

        elif scelta == 2:
            pass

        elif scelta == 3:
            pass


        input('\nPremi invio per continuare...')
