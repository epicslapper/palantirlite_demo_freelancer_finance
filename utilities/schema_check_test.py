from engine.schema_check import check_schema
from engine.db import get_connection
from engine.model_loader import load_models

conn = get_connection()
models = load_models()

report = check_schema(conn, models)

for table, messages in report.items():
    print(f"\nTable: {table}")
    for msg in messages:
        print(" ", msg)

conn.close()
