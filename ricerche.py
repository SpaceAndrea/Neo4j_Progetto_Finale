import os
from neo4j import GraphDatabase
from datetime import datetime
import time

def __format_date(iso_date_str):
    
    dt = datetime.fromisoformat(iso_date_str.replace("Z", "+00:00"))
    
    return dt.strftime("%Y-%m-%d %H:%M")

def __neo4j_datetime_to_string(neo4j_dt):
    
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
        start_datetime = __format_date(start_datetime)
        end_datetime = __format_date(end_datetime)
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
                print(f"SIM: {relazione['simNumero']}, Start: {__neo4j_datetime_to_string(relazione['start'])}, End: {__neo4j_datetime_to_string(relazione['end'])}, Cella: {relazione['cellaNome']}")
        else:
            print(f"Nessuna relazione trovata per le SIM di {nome} {cognome} nell'intervallo {start_datetime} - {end_datetime}.")
            
    while True:  
        os.system('cls' if os.name == 'nt' else 'clear')     
        nome = input("Inserici nome: ").lower().strip()
        cognome = input("Inserici cognome:").lower().strip()
        result = session.run(
        """MATCH p=({nome: $nome, cognome: $cognome})-[:OWNS]->(s:Sim) RETURN s.numero as number;""",
        nome=nome,
        cognome=cognome)
        sim = result.single()
        if sim is None:
            print("\nNessuna SIM trovata, riprovare.")
            break
        else:
            print("inserisci l'intervallo di date")
            start_date = input("Data iniziale (yyyy-mm-dd): ")
            start_hour = input("Ora (HH:MM): ")
            end_date = input("Data di fine (yyyy-mm-dd): ")
            end_hour = input("Ora (HH:MM): ")
            start_datetime_str = f"{start_date}T{start_hour}:00Z"
            end_datetime_str = f"{end_date}T{end_hour}:00Z"
            try:
                os.system('cls' if os.name == 'nt' else 'clear')
                trova_relazioni_sim_cella(session, nome, cognome, start_datetime_str, end_datetime_str)
                scelta = int(input("1: Continua le ricerche\n0: Torna al menù\nScelta "))
                match scelta:
                    case 1: 
                        pass
                    case 0: 
                        break
                    case _:
                        print("scelta non valida")
            except Exception as e:
                print("Errore nell'iserimento")
                time.sleep(1) 

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
                "start": __neo4j_datetime_to_string(record["start"]),
                "end": __neo4j_datetime_to_string(record["end"]),
                "cellaNome": record["cellaNome"],
                "personaNome": record["personaNome"],
                "personaCognome": record["personaCognome"]
            })
        start_datetime = __format_date(start_datetime)
        end_datetime = __format_date(end_datetime)  
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
        os.system('cls' if os.name == 'nt' else 'clear')
        print_celle(session)
        nome = str(input("Inserisci il nome: ")).lower().strip()
        
        print("inserisci l'intervallo di date")
        start_date = input("Data iniziale (yyyy-mm-dd): ")
        start_hour = input("Ora (HH:MM): ")
        end_date = input("Data di fine (yyyy-mm-dd): ")
        end_hour = input("Ora (HH:MM): ")
        start_datetime_str = f"{start_date}T{start_hour}:00Z"
        end_datetime_str = f"{end_date}T{end_hour}:00Z"
        
        try:
            os.system('cls' if os.name == 'nt' else 'clear')
            trova_relazioni_sim_cella(session, nome, start_datetime_str, end_datetime_str)
            scelta = int(input("1: Continua le ricerche\n0: Torna al menù\nScelta "))
            match scelta:
                case 1: 
                    pass
                case 0: 
                    break
                case _:
                    print("scelta non valida")
        except Exception as e:
            print(e)
            print("Errore nell'iserimento")
            time.sleep(1) 


def find_people_near_location(session):
    def print_location(session):
        result = session.run(
            "MATCH (c:Cella) "
            "RETURN  c.nome AS cella_nome, c.location AS cella_location"
        )
        for record in result:
            print(f"Nome: {record['cella_nome']} - {record['cella_location']}")
    os.system('cls' if os.name == 'nt' else 'clear')        
    print_location(session)
    luogo = input('A quale luogo sei interessato? (formato: longitudine,latitudine): ').strip()
    try:
        lon, lat = map(float, luogo.split(','))
    except ValueError:
        print("Formato non valido. Utilizza il formato: longitudine,latitudine (es. 9.1900,45.4642)")
        return

    print("inserisci l'intervallo di date")
    start_date = input("Data iniziale (yyyy-mm-dd): ")
    start_hour = input("Ora (HH:MM): ")
    end_date = input("Data di fine (yyyy-mm-dd): ")
    end_hour = input("Ora (HH:MM): ")
    start_datetime_str = f"{start_date}T{start_hour}:00Z"
    end_datetime_str = f"{end_date}T{end_hour}:00Z"

    raggio = int(input("Inserisci il raggio (Km): "))*1000
    try:
        result = session.run(
            """
            MATCH (c:Cella)
            WHERE point.distance(c.location, point({latitude: $lat, longitude: $lon})) <= $raggio
            WITH c
            MATCH (p:Persona)-[:OWNS]->(s:Sim)-[r:CONNECTED_TO]->(c)
            WHERE datetime(r.start) >= datetime($start) AND datetime(r.end) <= datetime($end)
            RETURN p.nome AS nome, p.cognome AS cognome, s.numero AS numero 
            """,
            lat=lat, lon=lon, raggio=raggio, start=start_datetime_str, end=end_datetime_str
        )
        
        persone = []
        for record in result:
            persone.append({
                "nome": record["nome"],
                "cognome": record["cognome"],
                "numero": record["numero"]
            })

        if persone:
            os.system('cls' if os.name == 'nt' else 'clear')
            print("\nPersone trovate:")
            for persona in persone:
                print(f"{persona['nome']} {persona['cognome']} (numero: {persona['numero']})")
        else:
            print("\nNessun riscontro trovato.")
    except Exception as e:
        print(f"Errore durante l'esecuzione della query: {e}")

    input("\nPremi invio per continuare...")       