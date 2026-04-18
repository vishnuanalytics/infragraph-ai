from app.graph.neo4j_client import neo4j_client

def clear_database():
    neo4j_client.run_query("MATCH (n) DETACH DELETE n")
    print("Database cleared.")

def create_constraints():
    constraints = [
        "CREATE CONSTRAINT IF NOT EXISTS FOR (p:Plant) REQUIRE p.id IS UNIQUE",
        "CREATE CONSTRAINT IF NOT EXISTS FOR (s:System) REQUIRE s.id IS UNIQUE",
        "CREATE CONSTRAINT IF NOT EXISTS FOR (a:Asset) REQUIRE a.id IS UNIQUE",
        "CREATE CONSTRAINT IF NOT EXISTS FOR (sn:Sensor) REQUIRE sn.id IS UNIQUE",
        "CREATE CONSTRAINT IF NOT EXISTS FOR (i:Incident) REQUIRE i.id IS UNIQUE",
        "CREATE CONSTRAINT IF NOT EXISTS FOR (m:MaintenanceEvent) REQUIRE m.id IS UNIQUE",
        "CREATE CONSTRAINT IF NOT EXISTS FOR (f:FailureMode) REQUIRE f.id IS UNIQUE",
    ]
    for c in constraints:
        neo4j_client.run_query(c)
    print("Constraints created.")

def seed_plants_and_systems():
    query = """
    MERGE (p1:Plant {id: 'PLANT-001', name: 'Offshore Platform Alpha', location: 'Gulf of Mexico', type: 'Offshore'})
    MERGE (p2:Plant {id: 'PLANT-002', name: 'Refinery Beta', location: 'Texas', type: 'Onshore'})

    MERGE (s1:System {id: 'SYS-001', name: 'Compression System', plant_id: 'PLANT-001'})
    MERGE (s2:System {id: 'SYS-002', name: 'Cooling System', plant_id: 'PLANT-001'})
    MERGE (s3:System {id: 'SYS-003', name: 'Distillation System', plant_id: 'PLANT-002'})
    MERGE (s4:System {id: 'SYS-004', name: 'Pipeline System', plant_id: 'PLANT-002'})

    MERGE (p1)-[:HAS_SYSTEM]->(s1)
    MERGE (p1)-[:HAS_SYSTEM]->(s2)
    MERGE (p2)-[:HAS_SYSTEM]->(s3)
    MERGE (p2)-[:HAS_SYSTEM]->(s4)
    """
    neo4j_client.run_query(query)
    print("Plants and systems seeded.")

def seed_assets():
    query = """
    MATCH (s1:System {id: 'SYS-001'})
    MATCH (s2:System {id: 'SYS-002'})
    MATCH (s3:System {id: 'SYS-003'})
    MATCH (s4:System {id: 'SYS-004'})

    MERGE (a1:Asset {id: 'ASSET-001', name: 'Compressor C-101', type: 'Compressor',
           manufacturer: 'Siemens', install_year: 2018, status: 'operational'})
    MERGE (a2:Asset {id: 'ASSET-002', name: 'Compressor C-102', type: 'Compressor',
           manufacturer: 'GE', install_year: 2019, status: 'degraded'})
    MERGE (a3:Asset {id: 'ASSET-003', name: 'Heat Exchanger HX-201', type: 'HeatExchanger',
           manufacturer: 'ABB', install_year: 2017, status: 'operational'})
    MERGE (a4:Asset {id: 'ASSET-004', name: 'Distillation Column DC-301', type: 'Column',
           manufacturer: 'KBR', install_year: 2016, status: 'operational'})
    MERGE (a5:Asset {id: 'ASSET-005', name: 'Pipeline Segment PS-401', type: 'Pipeline',
           manufacturer: 'Tenaris', install_year: 2015, status: 'under_maintenance'})
    MERGE (a6:Asset {id: 'ASSET-006', name: 'Compressor C-103', type: 'Compressor',
           manufacturer: 'Siemens', install_year: 2020, status: 'operational'})

    MERGE (s1)-[:CONTAINS]->(a1)
    MERGE (s1)-[:CONTAINS]->(a2)
    MERGE (s2)-[:CONTAINS]->(a3)
    MERGE (s3)-[:CONTAINS]->(a4)
    MERGE (s4)-[:CONTAINS]->(a5)
    MERGE (s1)-[:CONTAINS]->(a6)
    """
    neo4j_client.run_query(query)
    print("Assets seeded.")

def seed_sensors():
    query = """
    MATCH (a1:Asset {id: 'ASSET-001'})
    MATCH (a2:Asset {id: 'ASSET-002'})
    MATCH (a3:Asset {id: 'ASSET-003'})
    MATCH (a5:Asset {id: 'ASSET-005'})

    MERGE (sn1:Sensor {id: 'SENS-001', name: 'Pressure Sensor P-101', type: 'Pressure',
           unit: 'bar', threshold_min: 10.0, threshold_max: 85.0})
    MERGE (sn2:Sensor {id: 'SENS-002', name: 'Vibration Sensor V-101', type: 'Vibration',
           unit: 'mm/s', threshold_min: 0.0, threshold_max: 7.1})
    MERGE (sn3:Sensor {id: 'SENS-003', name: 'Temperature Sensor T-102', type: 'Temperature',
           unit: 'C', threshold_min: -10.0, threshold_max: 120.0})
    MERGE (sn4:Sensor {id: 'SENS-004', name: 'Pressure Sensor P-201', type: 'Pressure',
           unit: 'bar', threshold_min: 5.0, threshold_max: 60.0})
    MERGE (sn5:Sensor {id: 'SENS-005', name: 'Flow Sensor F-401', type: 'Flow',
           unit: 'L/min', threshold_min: 100.0, threshold_max: 5000.0})

    MERGE (a1)-[:HAS_SENSOR]->(sn1)
    MERGE (a1)-[:HAS_SENSOR]->(sn2)
    MERGE (a2)-[:HAS_SENSOR]->(sn3)
    MERGE (a3)-[:HAS_SENSOR]->(sn4)
    MERGE (a5)-[:HAS_SENSOR]->(sn5)
    """
    neo4j_client.run_query(query)
    print("Sensors seeded.")

def seed_failure_modes():
    query = """
    MERGE (f1:FailureMode {id: 'FM-001', name: 'Seal Degradation',
           description: 'Mechanical seal wear causing pressure loss', severity: 'high'})
    MERGE (f2:FailureMode {id: 'FM-002', name: 'Bearing Failure',
           description: 'Rolling element bearing damage from vibration', severity: 'critical'})
    MERGE (f3:FailureMode {id: 'FM-003', name: 'Fouling',
           description: 'Deposit buildup on heat transfer surfaces', severity: 'medium'})
    MERGE (f4:FailureMode {id: 'FM-004', name: 'Corrosion',
           description: 'Material degradation from corrosive fluids', severity: 'high'})
    MERGE (f5:FailureMode {id: 'FM-005', name: 'Overpressure',
           description: 'Pressure exceeds design limit', severity: 'critical'})
    """
    neo4j_client.run_query(query)
    print("Failure modes seeded.")

def seed_incidents():
    query = """
    MATCH (a1:Asset {id: 'ASSET-001'})
    MATCH (a2:Asset {id: 'ASSET-002'})
    MATCH (a3:Asset {id: 'ASSET-003'})
    MATCH (a5:Asset {id: 'ASSET-005'})
    MATCH (f1:FailureMode {id: 'FM-001'})
    MATCH (f2:FailureMode {id: 'FM-002'})
    MATCH (f3:FailureMode {id: 'FM-003'})
    MATCH (f4:FailureMode {id: 'FM-004'})
    MATCH (f5:FailureMode {id: 'FM-005'})

    MERGE (i1:Incident {id: 'INC-001', title: 'Compressor C-101 Pressure Drop',
           date: '2024-11-15', severity: 'high', status: 'resolved',
           description: 'Sudden pressure drop detected on compressor C-101. Seal degradation confirmed after inspection.'})
    MERGE (i2:Incident {id: 'INC-002', title: 'Compressor C-102 High Vibration',
           date: '2024-12-03', severity: 'critical', status: 'open',
           description: 'Vibration levels exceeded threshold on C-102. Bearing failure suspected. Unit operating at reduced capacity.'})
    MERGE (i3:Incident {id: 'INC-003', title: 'Heat Exchanger HX-201 Fouling',
           date: '2025-01-20', severity: 'medium', status: 'resolved',
           description: 'Reduced thermal efficiency on HX-201. Fouling detected on tube bundle. Cleaning completed.'})
    MERGE (i4:Incident {id: 'INC-004', title: 'Pipeline PS-401 Corrosion',
           date: '2025-02-10', severity: 'high', status: 'in_progress',
           description: 'Internal corrosion detected on pipeline segment PS-401. Integrity inspection scheduled.'})
    MERGE (i5:Incident {id: 'INC-005', title: 'Compressor C-101 Overpressure Event',
           date: '2025-03-05', severity: 'critical', status: 'resolved',
           description: 'Pressure relief valve activated on C-101. Overpressure event traced to blocked downstream valve.'})

    MERGE (a1)-[:INVOLVED_IN]->(i1)
    MERGE (a2)-[:INVOLVED_IN]->(i2)
    MERGE (a3)-[:INVOLVED_IN]->(i3)
    MERGE (a5)-[:INVOLVED_IN]->(i4)
    MERGE (a1)-[:INVOLVED_IN]->(i5)

    MERGE (i1)-[:CAUSED_BY]->(f1)
    MERGE (i2)-[:CAUSED_BY]->(f2)
    MERGE (i3)-[:CAUSED_BY]->(f3)
    MERGE (i4)-[:CAUSED_BY]->(f4)
    MERGE (i5)-[:CAUSED_BY]->(f5)
    """
    neo4j_client.run_query(query)
    print("Incidents seeded.")

def seed_maintenance():
    query = """
    MATCH (a1:Asset {id: 'ASSET-001'})
    MATCH (a2:Asset {id: 'ASSET-002'})
    MATCH (a5:Asset {id: 'ASSET-005'})

    MERGE (m1:MaintenanceEvent {id: 'MAINT-001', type: 'Corrective',
           date: '2024-11-20', technician: 'Ravi Kumar',
           description: 'Replaced mechanical seal on C-101. Pressure restored to normal range.',
           cost_usd: 12500})
    MERGE (m2:MaintenanceEvent {id: 'MAINT-002', type: 'Preventive',
           date: '2025-01-10', technician: 'Priya Sharma',
           description: 'Scheduled bearing inspection on C-102. Lubrication performed. Replacement ordered.',
           cost_usd: 3200})
    MERGE (m3:MaintenanceEvent {id: 'MAINT-003', type: 'Corrective',
           date: '2025-02-15', technician: 'Arjun Singh',
           description: 'Pipeline section PS-401 isolated. Corrosion inhibitor treatment applied.',
           cost_usd: 45000})

    MERGE (a1)-[:HAD_MAINTENANCE]->(m1)
    MERGE (a2)-[:HAD_MAINTENANCE]->(m2)
    MERGE (a5)-[:HAD_MAINTENANCE]->(m3)
    """
    neo4j_client.run_query(query)
    print("Maintenance events seeded.")

def run_all():
    print("Starting database seed...")
    clear_database()
    create_constraints()
    seed_plants_and_systems()
    seed_assets()
    seed_sensors()
    seed_failure_modes()
    seed_incidents()
    seed_maintenance()
    print("\nAll seed data loaded successfully!")
    print("Graph summary:")
    result = neo4j_client.run_query("""
        MATCH (n)
        RETURN labels(n)[0] as label, count(n) as count
        ORDER BY count DESC
    """)
    for row in result:
        print(f"  {row['label']}: {row['count']} nodes")

if __name__ == "__main__":
    run_all()