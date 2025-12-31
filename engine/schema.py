def ensure_table(conn, table_name, columns):
    cols_sql = []
    for name, coltype in columns.items():
        cols_sql.append(f"{name} {coltype}")

    sql = f"""
    CREATE TABLE IF NOT EXISTS {table_name} (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        {", ".join(cols_sql)}
    )
    """
    conn.execute(sql)
    conn.commit()
