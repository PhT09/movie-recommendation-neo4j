import os
from neo4j import GraphDatabase
from dotenv import load_dotenv

load_dotenv()

URI = os.getenv("NEO4J_URI")
USERNAME = os.getenv("NEO4J_USERNAME")
PASSWORD = os.getenv("NEO4J_PASSWORD")

driver = GraphDatabase.driver(URI, auth=(USERNAME, PASSWORD))

def check_db():
    query = """
    MATCH (u:User) RETURN keys(u) LIMIT 1
    """
    records, _, _ = driver.execute_query(query, database_="neo4j")
    for r in records: print("User:", r[0])

    query2 = """
    MATCH (m:Movie) RETURN keys(m) LIMIT 1
    """
    records, _, _ = driver.execute_query(query2, database_="neo4j")
    for r in records: print("Movie:", r[0])

    query3 = """
    MATCH (g:Genre) RETURN keys(g) LIMIT 1
    """
    records, _, _ = driver.execute_query(query3, database_="neo4j")
    for r in records: print("Genre:", r[0])

    query4 = """
    MATCH ()-[r:RATED]->() RETURN keys(r) LIMIT 1
    """
    records, _, _ = driver.execute_query(query4, database_="neo4j")
    for r in records: print("RATED:", r[0])

if __name__ == "__main__":
    check_db()
    driver.close()
