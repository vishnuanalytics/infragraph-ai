# ============================================================
# All graph queries live here — separated from business logic
# This is the "knowledge layer" you explain to the interviewer
# ============================================================

# ---------- ASSET QUERIES ----------

GET_ALL_ASSETS = """
MATCH (p:Plant)-[:HAS_SYSTEM]->(s:System)-[:CONTAINS]->(a:Asset)
RETURN 
    a.id AS id,
    a.name AS name,
    a.type AS type,
    a.manufacturer AS manufacturer,
    a.install_year AS install_year,
    a.status AS status,
    s.name AS system_name,
    p.name AS plant_name
ORDER BY a.name
"""

GET_ASSET_BY_ID = """
MATCH (p:Plant)-[:HAS_SYSTEM]->(s:System)-[:CONTAINS]->(a:Asset {id: $asset_id})
OPTIONAL MATCH (a)-[:HAS_SENSOR]->(sn:Sensor)
OPTIONAL MATCH (a)-[:INVOLVED_IN]->(i:Incident)
OPTIONAL MATCH (a)-[:HAD_MAINTENANCE]->(m:MaintenanceEvent)
RETURN 
    a.id AS id,
    a.name AS name,
    a.type AS type,
    a.manufacturer AS manufacturer,
    a.install_year AS install_year,
    a.status AS status,
    s.name AS system_name,
    p.name AS plant_name,
    collect(DISTINCT {
        id: sn.id, name: sn.name, type: sn.type, unit: sn.unit
    }) AS sensors,
    collect(DISTINCT {
        id: i.id, title: i.title, date: i.date,
        severity: i.severity, status: i.status
    }) AS incidents,
    collect(DISTINCT {
        id: m.id, type: m.type, date: m.date,
        description: m.description, cost_usd: m.cost_usd
    }) AS maintenance_history
"""

GET_ASSETS_BY_STATUS = """
MATCH (p:Plant)-[:HAS_SYSTEM]->(s:System)-[:CONTAINS]->(a:Asset {status: $status})
RETURN 
    a.id AS id,
    a.name AS name,
    a.type AS type,
    a.status AS status,
    s.name AS system_name,
    p.name AS plant_name
ORDER BY a.name
"""

GET_ASSETS_BY_TYPE = """
MATCH (p:Plant)-[:HAS_SYSTEM]->(s:System)-[:CONTAINS]->(a:Asset {type: $asset_type})
RETURN 
    a.id AS id,
    a.name AS name,
    a.type AS type,
    a.status AS status,
    s.name AS system_name,
    p.name AS plant_name
ORDER BY a.name
"""

# ---------- INCIDENT QUERIES ----------

GET_ALL_INCIDENTS = """
MATCH (a:Asset)-[:INVOLVED_IN]->(i:Incident)
OPTIONAL MATCH (i)-[:CAUSED_BY]->(f:FailureMode)
MATCH (p:Plant)-[:HAS_SYSTEM]->(s:System)-[:CONTAINS]->(a)
RETURN 
    i.id AS id,
    i.title AS title,
    i.date AS date,
    i.severity AS severity,
    i.status AS status,
    i.description AS description,
    a.id AS asset_id,
    a.name AS asset_name,
    a.type AS asset_type,
    f.name AS failure_mode,
    f.severity AS failure_severity,
    p.name AS plant_name
ORDER BY i.date DESC
"""

GET_INCIDENTS_BY_SEVERITY = """
MATCH (a:Asset)-[:INVOLVED_IN]->(i:Incident {severity: $severity})
OPTIONAL MATCH (i)-[:CAUSED_BY]->(f:FailureMode)
MATCH (p:Plant)-[:HAS_SYSTEM]->(s:System)-[:CONTAINS]->(a)
RETURN 
    i.id AS id,
    i.title AS title,
    i.date AS date,
    i.severity AS severity,
    i.status AS status,
    i.description AS description,
    a.name AS asset_name,
    f.name AS failure_mode,
    p.name AS plant_name
ORDER BY i.date DESC
"""

GET_INCIDENTS_BY_DATE_RANGE = """
MATCH (a:Asset)-[:INVOLVED_IN]->(i:Incident)
WHERE i.date >= $start_date AND i.date <= $end_date
OPTIONAL MATCH (i)-[:CAUSED_BY]->(f:FailureMode)
MATCH (p:Plant)-[:HAS_SYSTEM]->(s:System)-[:CONTAINS]->(a)
RETURN 
    i.id AS id,
    i.title AS title,
    i.date AS date,
    i.severity AS severity,
    i.status AS status,
    a.name AS asset_name,
    a.type AS asset_type,
    f.name AS failure_mode,
    p.name AS plant_name
ORDER BY i.date DESC
"""

# This query is KEY — shows graph traversal depth.
# "Which assets share the same failure mode?"
GET_ASSETS_WITH_SAME_FAILURE_MODE = """
MATCH (a1:Asset)-[:INVOLVED_IN]->(:Incident)-[:CAUSED_BY]->(f:FailureMode)
      <-[:CAUSED_BY]-(:Incident)<-[:INVOLVED_IN]-(a2:Asset)
WHERE a1.id <> a2.id
RETURN DISTINCT
    a1.name AS asset_1,
    a2.name AS asset_2,
    f.name AS shared_failure_mode,
    f.severity AS severity
ORDER BY f.severity DESC
"""

# ---------- PLANT OVERVIEW QUERY ----------

GET_PLANT_SUMMARY = """
MATCH (p:Plant)-[:HAS_SYSTEM]->(s:System)-[:CONTAINS]->(a:Asset)
OPTIONAL MATCH (a)-[:INVOLVED_IN]->(i:Incident)
OPTIONAL MATCH (a)-[:HAD_MAINTENANCE]->(m:MaintenanceEvent)
RETURN 
    p.id AS plant_id,
    p.name AS plant_name,
    p.location AS location,
    p.type AS plant_type,
    count(DISTINCT s) AS total_systems,
    count(DISTINCT a) AS total_assets,
    count(DISTINCT i) AS total_incidents,
    count(DISTINCT m) AS total_maintenance_events,
    sum(m.cost_usd) AS total_maintenance_cost_usd
ORDER BY p.name
"""

# ---------- RISK QUERY ----------
# "Find all assets that have open critical incidents"
# This is exactly the kind of query a Knowledge Engineer writes

GET_HIGH_RISK_ASSETS = """
MATCH (p:Plant)-[:HAS_SYSTEM]->(s:System)-[:CONTAINS]->(a:Asset)
MATCH (a)-[:INVOLVED_IN]->(i:Incident)
WHERE i.severity IN ['critical', 'high'] AND i.status IN ['open', 'in_progress']
OPTIONAL MATCH (i)-[:CAUSED_BY]->(f:FailureMode)
RETURN 
    a.id AS asset_id,
    a.name AS asset_name,
    a.type AS asset_type,
    a.status AS asset_status,
    p.name AS plant_name,
    collect({
        incident_id: i.id,
        title: i.title,
        severity: i.severity,
        status: i.status,
        failure_mode: f.name
    }) AS open_incidents,
    count(i) AS open_incident_count
ORDER BY open_incident_count DESC
"""

# ---------- GRAPH CONTEXT FOR RAG ----------
# This query feeds the AI — it gets full context for a given asset
# so the LLM can answer questions grounded in graph data

GET_ASSET_FULL_CONTEXT_FOR_RAG = """
MATCH (p:Plant)-[:HAS_SYSTEM]->(s:System)-[:CONTAINS]->(a:Asset)
OPTIONAL MATCH (a)-[:HAS_SENSOR]->(sn:Sensor)
OPTIONAL MATCH (a)-[:INVOLVED_IN]->(i:Incident)-[:CAUSED_BY]->(f:FailureMode)
OPTIONAL MATCH (a)-[:HAD_MAINTENANCE]->(m:MaintenanceEvent)
RETURN 
    a.id AS asset_id,
    a.name AS asset_name,
    a.type AS asset_type,
    a.manufacturer AS manufacturer,
    a.install_year AS install_year,
    a.status AS asset_status,
    s.name AS system_name,
    p.name AS plant_name,
    p.location AS location,
    collect(DISTINCT sn.name + ' (' + sn.type + ', unit: ' + sn.unit + ')') AS sensors,
    collect(DISTINCT {
        title: i.title, date: i.date,
        severity: i.severity, status: i.status,
        failure_mode: f.name, description: i.description
    }) AS incidents,
    collect(DISTINCT {
        type: m.type, date: m.date,
        description: m.description, cost_usd: m.cost_usd
    }) AS maintenance
"""

GET_GRAPH_STATS = """
MATCH (n)
RETURN labels(n)[0] AS label, count(n) AS count
ORDER BY count DESC
"""