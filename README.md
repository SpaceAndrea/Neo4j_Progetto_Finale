# Neo4j_Progetto_Finale
Progetto per esame Neo4j

<div align="center">
  <img src="https://img.shields.io/badge/Neo4j-018bff?style=for-the-badge&logo=neo4j&logoColor=white">
  <img src="https://img.shields.io/badge/Python-FFD43B?style=for-the-badge&logo=python&logoColor=blue">
  <img src="https://img.shields.io/badge/windows%20terminal-4D4D4D?style=for-the-badge&logo=windows%20terminal&logoColor=white">
  <img src="https://img.shields.io/badge/Docker-2CA5E0?style=for-the-badge&logo=docker&logoColor=white">
</div>

---

<div align="center">
  <img src="https://github.com/SpaceAndrea/Neo4j_Progetto_Finale/assets/145685548/a2c1c3eb-4dad-47e6-80a0-a5e18234b406" alt="Neo4j Logo" />
</div>

---

Neo4j Project è un applicazione che consente di controllare se uno dei telefoni di proprietà di una persona si è collegato ad una cella. <br>
Con Neo4j Project, è possibile: <b>

- Localizzare una persona sospetta: 
   -
   - [LV1] Con una data, un orario e una persona, elencare le celle telefoniche alle quali le SIM intestate a quella persona erano collegate.

- Trovare sospetti in una zona di reato, in particolare:
   - 
   - [Lv2] Con una data, un orario ed una cella, elencare le persone intestatarie selle SIM collegate a quella cella in quel momento
   Cercare concerti per intervallo di date
   - [Lv3] Date delle coordinate geografiche, una data e un orario elencare le persone intestatarie delle SIM collegate alle celle che si trovano in un certo raggio dalle coordinate date


</b>

## Requisiti

Per avviare l'applicazione, è necessario/preferibile avere:

- **Python v.3.12**
- **Docker Desktop** *(In caso non si utilizzi Neo4j Aura o Neo4j Desktop)*
- **Un Database su Neo4j** *(In caso non si usi Docker)*
  
- Le seguenti librerie Python:
  - `neo4j`
  - `json`
  - `random`
  - `datetime`
  - `os`

## Installazione e configurazione Neo4j:


### 1. Clona il repository di Neo4j Project:

   - Apri il terminale e vai nella directory dove vuoi clonare il repository tramite `cd 'yo/ur/path'`
   - Esegui il seguente comando:
     
     ```sh
     git clone https://github.com/SpaceAndrea/Neo4j_Progetto_Finale
     ```

### 2. Installazione di Python 3.12
1. **Scarica Python 3.12**:
   - Clicca su questo link: [python.org](https://www.python.org/downloads/release/python-3120/)
   - Scarica Python 3.12 per il tuo sistema operativo ed installalo.

2. **Verifica l'installazione**:
   - Apri il terminale.
   - Digita `python --version` per assicurarti di aver installato correttamente Python 3.12.


### 3. Installazione di Docker Desktop

*Solo nel caso si voglia runnare Neo4j in locale*

1. **Scarica Docker Desktop**:
   - Clicca su questo link: [docker.com](https://www.docker.com/products/docker-desktop)
   - Scarica Docker Desktop per il tuo sistema operativo e installalo.

2. **Verifica l'installazione**:
   - Apri il terminale.
   - Digita `docker --version` per assicurarti che Docker sia installato correttamente.

### 4. Aprire Neo4j Aura sul browser

*Opzionale, utile per vedere i vari nodi all'interno del database*

1. **Andare sul sito di Neo4j Aura o scaricare la versione Desktop**:
   - Clicca su questo link: [Neo4j Aura](https://neo4j.com/cloud/platform/aura-graph-database/)
   - Alternativamente, è possibile scaricare Neo4j Desktop sul proprio dispositivo.

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
     pip install neo4j json random datetime
     ```

### Conclusione

Ora dovresti avere tutto il necessario per eseguire Neo4j sul tuo dispositivo.

---
