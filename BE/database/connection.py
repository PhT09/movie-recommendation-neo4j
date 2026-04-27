import os
from neo4j import GraphDatabase
from dotenv import load_dotenv

load_dotenv()

class Neo4jConnection:
    def __init__(self):
        uri = os.getenv("NEO4J_URI", "neo4j://localhost:7687")
        user = os.getenv("NEO4J_USERNAME", "neo4j")
        password = os.getenv("NEO4J_PASSWORD", "password")
        self.driver = GraphDatabase.driver(uri, auth=(user, password))

    def close(self):
        if self.driver:
            self.driver.close()

    def get_driver(self):
        return self.driver

# Create a single instance to be shared across the application
neo4j_conn = Neo4jConnection()
driver = neo4j_conn.get_driver()
