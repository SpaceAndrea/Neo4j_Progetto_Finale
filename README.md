# Neo4j_Progetto_Finale
Progetto per esame Neo4j

<div align="center">
  <img src="https://img.shields.io/badge/Neo4j-018bff?style=for-the-badge&logo=neo4j&logoColor=white">
  <img src="https://img.shields.io/badge/Python-FFD43B?style=for-the-badge&logo=python&logoColor=blue">
  <img src="https://img.shields.io/badge/windows%20terminal-4D4D4D?style=for-the-badge&logo=windows%20terminal&logoColor=white">
  <img src="https://img.shields.io/badge/Docker-2CA5E0?style=for-the-badge&logo=docker&logoColor=white">
</div>

TUTTA LA PARTE SOTTO E' DA MODIFICARE.

---


<div align="center">
  <img src="https://github.com/TongoPatongo/mongoDB_project/assets/145685548/f52bbf32-9b28-48f8-8674-f1f55136fb45" alt="MongoDB Logo" />
</div>

---

Neo4j Project è un applicazione che consente l'acquisto di biglietti per concerti. <br>
Con MongoDB Project, è possibile: <b>


- Registrarsi ed effettuare il login
- Cercare concerti per nome dell'artista
- Cercare concerti per il nome dello spettacolo
- Cercare concerti per intervallo di date
- Cercare concerti in base alla distanza dalla tua abitazione
- Visualizzare tutti i concerti
- Acquistare i biglietti per i concerti
- Menu per vedere i biglietti acquistati

</b>

## Requisiti

Per avviare l'applicazione, è necessario/preferibile avere:

- **Python v.3.12**
- **Docker Desktop** *(In caso non si utilizzi MongoDB Compass)*
- **Un Database MongoDB Compass** *(In caso non si usi Docker)*
  
- Le seguenti librerie Python:
  - `pymongo`
  - `regex`
  - `colorama`
  - `os`
  - `time`
  - `datetime`
  - `geopy`

## Installazione e configurazione MongoDB:


### 1. Clona il repository di MongoDB Project:

   - Apri il terminale e vai nella directory dove vuoi clonare il repository tramite `cd 'yo/ur/path'`
   - Esegui il seguente comando:
     
     ```sh
     git clone https://github.com/TongoPatongo/mongoDB_project
     ```

### 2. Installazione di Python 3.12
1. **Scarica Python 3.12**:
   - Clicca su questo link: [python.org](https://www.python.org/downloads/release/python-3120/)
   - Scarica Python 3.12 per il tuo sistema operativo ed installalo.

2. **Verifica l'installazione**:
   - Apri il terminale.
   - Digita `python --version` per assicurarti di aver installato correttamente Python 3.12.


### 3. Installazione di Docker Desktop

*Solo nel caso si voglia runnare MongoDB in locale*

1. **Scarica Docker Desktop**:
   - Clicca su questo link: [docker.com](https://www.docker.com/products/docker-desktop)
   - Scarica Docker Desktop per il tuo sistema operativo e installalo.

2. **Verifica l'installazione**:
   - Apri il terminale.
   - Digita `docker --version` per assicurarti che Docker sia installato correttamente.

### 4. Installazione di MongoDB Compass

*Opzionale, programma utile per runnare test sui database*

1. **Scarica MongoDB Compass**:
   - Clicca su questo link: [MongoDB Compass](https://www.mongodb.com/products/tools/compass)
   - Scarica MongoDB Compass per il tuo sistema operativo ed installalo.

2. **Effettuare il login**
   - Utilizzare le credenziali leggibili nel main per connettersi al database.

     
### 5. Installazione delle librerie Python

1. **Apri il terminale**:
   - Su Windows, puoi usare il prompt dei comandi o PowerShell.
   - Su macOS e Linux, puoi usare il terminale di default.

2. **Controlla quali librerie sono presenti nel tuo ambiente**
   - Attiva il tuo ambiente virtuale tramite CONDA, VENV ecc.
   - Esegui il comando `pip list` per capire quali delle librerie menzionate sono già presenti.

3. **Installa le librerie mancanti**:
   - Esegui il seguente comando per installare le librerie mancanti:
     ```sh
     pip install pymongo regex colorama
     ```

### Conclusione

Ora dovresti avere tutto il necessario per eseguire MongoDB sul tuo dispositivo.

---
