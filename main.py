import os
from neo4j import GraphDatabase

if __name__ == '__main__':
    URI = input('Inserire l\'URI del database (lascia vuoto per inserire "neo4j+s://29b76056.databases.neo4j.io:7687"): ').strip()
    if URI == '':
        URI = "neo4j+s://29b76056.databases.neo4j.io:7687"

    USERNAME = input('Inserire lo username (lascia vuoto per inserire "neo4j"): ').strip()
    if USERNAME == '':
        USERNAME = 'neo4j'

    PASSWORD = input('Inserire la password: ').strip()

    # with GraphDatabase.driver(URI, auth=(USERNAME, PASSWORD)) as driver:
        # driver.verify_connectivity()

    driver = GraphDatabase.driver(URI, auth=(USERNAME, PASSWORD))
    print('Connesione a Neo4j effettuata!')

    while True:
        ## pulisce il terminale
        os.system('cls' if os.name == 'nt' else 'clear')

        print('''
Scegli un opzione:
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
            driver.close()

            break

        try:
            scelta = int(scelta)
            assert scelta <= 3

            if scelta == 1:
                pass

            elif scelta == 2:
                pass

            elif scelta == 3:
                pass

        except:
            print('\nScelta non valida', end='')

        input('\nPremi invio per continuare...')
