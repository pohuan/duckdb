import duckdb

# Create an in-memory DuckDB connection
con = duckdb.connect()

# Create a table with a STRUCT column
con.execute("""
    CREATE TABLE test_data (
        id INTEGER,
        metrics STRUCT(count INTEGER, sum INTEGER)
    )
""")

# Insert sample data into the table
con.execute("""
    INSERT INTO test_data VALUES 
    (1, {'count': 5, 'sum': 100}),
    (2, {'count': 10, 'sum': 250}),
    (3, {'count': 0, 'sum': 0})
""")

# Define a Python UDF that processes the STRUCT type
def compute_average(struct):
    print(type(struct))
    if struct['count'] == 0:
        return 0  # Avoid division by zero
    return struct['sum'] / struct['count']

def compute_avg_agg(struct1, struct2):
    struct1['sum'] = struct1['sum'] + struct2['sum']
    struct1['count'] = struct1['count'] + struct2['count']
    return struct1
    
# Register the function in DuckDB
#con.create_function("compute_avg", compute_average, [duckdb.struct_type({"count": "INTEGER", "sum": "INTEGER"})], "DOUBLE")

con.create_aggregate_function("compute_avg_agg_X", compute_avg_agg, [duckdb.struct_type({"count": "INTEGER", "sum": "INTEGER"}), duckdb.struct_type({"count": "INTEGER", "sum": "INTEGER"})], duckdb.struct_type({"count": "INTEGER", "sum": "INTEGER"}))

# Query DuckDB using the UDF
result = con.execute("SELECT compute_avg_agg_X(metrics) AS avg_value FROM test_data").fetchall()

# Print the results
for row in result:
    print(row)  # Output: (1, 20.0), (2, 25.0), (3, None)

