import os
from dotenv import load_dotenv
from neo4j import GraphDatabase

load_dotenv()

uri      = os.getenv("NEO4J_URI")
username = os.getenv("NEO4J_USERNAME")
password = os.getenv("NEO4J_PASSWORD")

print(f"URI      : {uri}")
print(f"Username : {username}")
print(f"Password : {'*' * len(password) if password else 'NOT SET'}")
print()

if not uri or not password:
    print("ERROR: NEO4J_URI or NEO4J_PASSWORD is empty in your .env file")
    exit(1)

try:
    driver = GraphDatabase.driver(uri, auth=(username, password))
    driver.verify_connectivity()
    print("SUCCESS: Connected to Neo4j Aura!")

    with driver.session() as session:
        result = session.run("RETURN 'Hello from Neo4j' AS message")
        print("Query result:", result.single()["message"])

    driver.close()

except Exception as e:
    print(f"FAILED: {e}")
    print()
    print("Common fixes:")
    print("  1. URI must start with neo4j+s:// not bolt://")
    print("  2. No quotes around values in .env")
    print("  3. Reset password on Neo4j Aura console if unsure")
    print("  4. Check your internet connection")