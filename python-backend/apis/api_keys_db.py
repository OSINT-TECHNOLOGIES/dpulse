import sqlite3

conn = sqlite3.connect('api_keys.db')
cursor = conn.cursor()
cursor.execute("""
    CREATE TABLE IF NOT EXISTS api_keys (
        id INTEGER PRIMARY KEY,
        api_name TEXT,
        api_key TEXT,
        limitations TEXT
    )
""")
cursor.execute("INSERT INTO api_keys (id, api_name, api_key, limitations) VALUES (1, 'VirusTotal', 'YOUR_API_KEY', 'Free tier: 4 req/min')")
cursor.execute("INSERT INTO api_keys (id, api_name, api_key, limitations) VALUES (2, 'SecurityTrails', 'YOUR_API_KEY', 'Free tier: 50 req/month')")
cursor.execute("INSERT INTO api_keys (id, api_name, api_key, limitations) VALUES (3, 'HudsonRock', 'YOUR_API_KEY', 'No key required actually')")
conn.commit()
conn.close()
print("api_keys.db created successfully")