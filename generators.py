import random
from datetime import datetime, timedelta
from neo4j import GraphDatabase

class Cella:
    def __init__(self, nome, latitudine, longitudine):
        self.nome = nome
        self.latitudine = latitudine
        self.longitudine = longitudine

    def __str__(self):
        return f"{self.nome} (Lat: {self.latitudine}, Lon: {self.longitudine})"

class Persona:
    def __init__(self, nome, cognome, eta):
        self.nome = nome
        self.cognome = cognome
        self.eta = eta

    def __str__(self):
        return f"{self.nome} {self.cognome}, Età: {self.eta}"
    
class CreateDataBase:
    def __init__(self):
        self.luoghi = [
            Cella("Milano", 45.4642, 9.1900),
            Cella("Bergamo", 45.6983, 9.6773),
            Cella("Brescia", 45.5416, 10.2118),
            Cella("Como", 45.8081, 9.0852),
            Cella("Cremona", 45.1332, 10.0227),
            Cella("Lecco", 45.8566, 9.3977),
            Cella("Lodi", 45.3146, 9.5033),
            Cella("Mantova", 45.1564, 10.7914),
            Cella("Monza", 45.5845, 9.2744),
            Cella("Pavia", 45.1847, 9.1582),
            Cella("Sondrio", 46.1699, 9.8782),
            Cella("Varese", 45.8184, 8.8232),
            Cella("Busto Arsizio", 45.6110, 8.8494),
            Cella("Legnano", 45.5961, 8.9113),
            Cella("Sesto San Giovanni", 45.5332, 9.2356),
            Cella("Cinisello Balsamo", 45.5543, 9.2145),
            Cella("Gallarate", 45.6603, 8.7913),
            Cella("Rho", 45.5303, 9.0356),
            Cella("Vigevano", 45.3184, 8.8588),
            Cella("Paderno Dugnano", 45.5615, 9.1691),
            Cella("Seregno", 45.6543, 9.2012),
            Cella("Desio", 45.6169, 9.2036),
            Cella("Limbiate", 45.5905, 9.1278),
            Cella("Cremella", 45.7421, 9.2971)
        ]
        
        self.persone = [
            Persona("Mario", "Rossi", 30),
            Persona("Luca", "Bianchi", 25),
            Persona("Giulia", "Verdi", 28),
            Persona("Francesca", "Neri", 35),
            Persona("Marco", "Bruno", 40),
            Persona("Laura", "Gialli", 22),
            Persona("Alessandro", "Blu", 45),
            Persona("Martina", "Rosa", 31),
            Persona("Paolo", "Grigi", 37),
            Persona("Elena", "Viola", 29),
            Persona("Giorgio", "Arancioni", 50),
            Persona("Chiara", "Marroni", 33),
            Persona("Fabio", "Bianchi", 27),
            Persona("Sara", "Rossi", 24),
            Persona("Andrea", "Verdi", 39),
            Persona("Anna", "Neri", 26),
            Persona("Davide", "Bruno", 34),
            Persona("Federica", "Gialli", 32),
            Persona("Simone", "Blu", 38),
            Persona("Valentina", "Rosa", 30),
            Persona("Roberto", "Grigi", 42),
            Persona("Silvia", "Viola", 36),
            Persona("Giovanni", "Arancioni", 47),
            Persona("Angela", "Marroni", 41),
            Persona("Nicola", "Bianchi", 28),
            Persona("Marta", "Rossi", 33),
            Persona("Enrico", "Verdi", 35),
            Persona("Giovanna", "Neri", 43),
            Persona("Tommaso", "Bruno", 29),
            Persona("Tongo", "Patongo", 20)

        ]

        self.numeri = [
        '6446676756', '2905565801', '1173856741', '0449327257', '8145700871',
        '2146308417', '4476507331', '0218426274', '4421935721', '2834768773',
        '5236530275', '4044291382', '3204440778', '1114648849', '9115565867',
        '8095307585', '7444670071', '3343205007', '9934631731', '7524777964',
        '7721342371', '0414284823', '5604778164', '7154337429', '1436791963',
        '8357544089', '7924845590', '0202952000', '6178229356', '1207622554',
        '0932593809', '3665271826', '6756629401', '1780565881', '2586582064',
        '3432090807', '6127329451', '3172624888', '7564676233', '1320796875'
]
        
    def crea_celle(self, tx, srid=4326):
        for luogo in self.luoghi:
            tx.run(
                "CREATE (:Cella { nome: $nome, location: point({ latitude: $latitude, longitude: $longitude, srid: $srid }) })",
                nome=luogo.nome, latitude=luogo.latitudine, longitude=luogo.longitudine, srid=srid
        )
            
    def crea_persone(self, tx):
        for persona in self.persone:
            tx.run(
                "CREATE (:Persona { nome: $nome, cognome: $cognome, eta: $eta })",
                nome=persona.nome, cognome=persona.cognome, eta=persona.eta
            )

    def crea_sim(self, tx):
        for numero in self.numeri:
            tx.run(
                "CREATE (:Sim { numero: $numero})",
                numero= numero
        )
            
    def crea_relazioni_persona_sim(self, tx):
        sim_indices = list(range(len(self.numeri)))
        random.shuffle(sim_indices)
        
        for i, persona in enumerate(self.persone):
            if not sim_indices:
                break
            sim_index = sim_indices.pop()
            sim_numero = self.numeri[sim_index]
            tx.run(
                "MATCH (p:Persona {nome: $nome, cognome: $cognome}), (s:Sim {numero: $numero}) "
                "CREATE (p)-[:OWNS]->(s)",
                nome=persona.nome, cognome=persona.cognome, numero=sim_numero
            )
            
                
    def crea_relazioni_sim_cella(self, tx):
        for numero in self.numeri:
            num_connections = random.randint(1, 10)
            assigned_cells = random.sample(self.luoghi, num_connections)
            for cella in assigned_cells:
                start_time = datetime.now() - timedelta(days=random.randint(1, 1000))
                end_time = start_time + timedelta(hours=random.randint(1, 48))
                try:
                    tx.run(
                        "MATCH (s:Sim {numero: $numero}), (c:Cella {nome: $nome}) "
                        "CREATE (s)-[:CONNECTED_TO {start: datetime($start), end: datetime($end)}]->(c)",
                        numero=numero, nome=cella.nome, start=start_time.isoformat(), end=end_time.isoformat()
                    )
                except Exception as e:
                    print(f"Error creating relationship for Sim {numero} and Cella {cella.nome}: {e}")


            
if __name__ == '__main__':
    
    URI = "neo4j+s://91e10090.databases.neo4j.io:7687"
    USERNAME = 'neo4j'
    PASSWORD = "tjZTPh4DaLFy84_W2RoSM1F_EW9RaGOBJ-SefdLUgrs"

    try:
        driver = GraphDatabase.driver(URI, auth=(USERNAME, PASSWORD))
        driver.verify_connectivity()  
        print('Connesione a Neo4j effettuata')
    except:
            print('Impossibile effetturare la connessione, riprovare')
    session = driver.session()
    createDB = CreateDataBase()
    try:
        # createDB.crea_celle(session)
        # createDB.crea_persone(session)
        # createDB.crea_sim(session)
        createDB.crea_relazioni_persona_sim(session)
        createDB.crea_relazioni_sim_cella(session)
    except Exception as e:
        print(e)