import os
from neo4j import GraphDatabase
from generators import CreateDataBase


def carica_dati_iniziali(session, file_path):
    ## idealmente potremmo realizzare un file con tutti i dati
    # Dato che il file è stato creato (tramite il modulo raccolta_dati.py)
    # leggo quei dati dal file json
    createDB = CreateDataBase()

    ## pulisce il database
    session.run("MATCH (n) DETACH DELETE n")

    try:
        createDB.crea_celle(session)
        createDB.crea_persone(session)
        createDB.crea_sim(session)
        createDB.crea_relazioni_persona_sim(session)
        createDB.crea_relazioni_sim_cella(session)
    except Exception as e:
        print(e)

    print("Dati iniziali caricati nel database Neo4j")


if __name__ == '__main__':
    createDB = CreateDataBase()


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
            cognome = input('Inserire il cognome della persona: ').strip()

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
            cell_id = input('Inserire l\'ID della cella: ').strip()
            data = input('Inserire la data (YYYY-MM-DD): ').strip()
            orario = input('Inserire l\'orario (HH:MM:SS): ').strip()

            result = session.run(
                """
                MATCH (p:Person)-[:OWNS]->(s:SIM)-[r:CONNECTED_TO]->(c:Cell)
                WHERE c.id = $cell_id AND r.date = $data AND r.time = $orario
                RETURN p.nome AS nome, p.cognome AS cognome, s.number AS numero
                """,
                cell_id=cell_id, data=data, orario=orario
            )

            persone = []
            for record in result:
                persone.append({
                    "nome": record["nome"],
                    "cognome": record["cognome"],
                    "numero": record["numero"]
                })

            if persone:
                print("\nPersone trovate:")
                for persona in persone:
                    print(f"{persona['nome']} {persona['cognome']} (numero: {persona['numero']})")
            else:
                print("\nNessun riscontro trovato.")

        elif scelta == 3:
            longitudine = input("Inserire la longitudine: ").strip()
            latitudine = input("Inserire la latitudine: ").strip()

            result = session.run(
                """
                WITH point({latitude: $latitudine, longitude: $longitudine}) AS myLocation
                MATCH (c:Cella)
                WHERE c.location IS NOT NULL
                RETURN c, point.distance(c.location, myLocation) AS dist
                ORDER BY dist ASC
                LIMIT 1
                """,
                longitudine=float(longitudine), latitudine=float(latitudine)
            )

            for record in result:
                cella = record["c"]
                distanza = record["dist"]
                print(distanza)
                # print(f"Closest place: {cella['id']}, Distance: {distanza}")

        input('\nPremi invio per continuare...')