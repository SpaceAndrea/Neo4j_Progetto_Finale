import os

if __name__ == '__main__':

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
