from neo4j import GraphDatabase

def get_driver(uri, user, password):
    """
    Initialize and return the Neo4j driver.
    """
    return GraphDatabase.driver(uri, auth=(user, password))
