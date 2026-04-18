from neo4j import GraphDatabase
from dotenv import load_dotenv
import os

load_dotenv()

class Neo4jClient:
    def __init__(self):
        self.driver = GraphDatabase.driver(
            os.getenv("NEO4J_URI"),
            auth=(os.getenv("NEO4J_USERNAME"), os.getenv("NEO4J_PASSWORD"))
        )

    def close(self):
        self.driver.close()

    def run_query(self, query: str, parameters: dict = {}):
        with self.driver.session() as session:
            result = session.run(query, parameters)
            return [record.data() for record in result]

# Singleton
neo4j_client = Neo4jClient()