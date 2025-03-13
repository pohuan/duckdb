import duckdb
import random
from duckdb.typing import *
import time
import os

# Define database file
db_file = "sales.duckdb"

# Check if the database already exists
if os.path.exists(db_file):
    # Reuse existing database
    con = duckdb.connect(database=db_file)
    print("Database loaded from disk.")
else:
    # Create a new database and insert data
    con = duckdb.connect(database=db_file)
    # Create a temporary table
    con.execute(
        """
            CREATE TABLE sales (
                id INTEGER,
                category TEXT,
                amount DOUBLE
            )
        """
    )

    # Generate 10,000 rows
    categories = ['Electronics', 'Clothing', 'Books']
    data = [(i, random.choice(categories), random.randint(1, 100)) for i in range(1, 1000001)]

    # Insert data using parameterized queries for efficiency
    con.executemany("INSERT INTO sales (id, category, amount) VALUES (?, ?, ?)", data)
    con.close()
    print("Database created and saved.")

con = duckdb.connect(database=db_file)
row_count = con.execute("SELECT COUNT(*) FROM sales").fetchone()[0]
print(f"Total rows available: {row_count}")



def test_combine_udf(d1, d2):
    return d1 + d2 + d1 + d2 + d1 + d2


def test_finalize_udf(d1,d2):
    d2 = d1;
    return d2;


con.create_aggregate_function("udf_demo", test_combine_udf, [DOUBLE, DOUBLE], DOUBLE, test_finalize_udf, [DOUBLE, DOUBLE], DOUBLE)

start_time = time.time()
result = con.execute(
    """
        SELECT udf_demo(amount) FROM sales
        """
).fetchall()
end_time =  time.time()
print(result)
print(f"Python UDF Query Execution Time: {end_time - start_time:.6f} seconds")

start_time2 = time.time()
resultFromNormalSum = con.execute(
    """
                SELECT SUM(amount) FROM sales
        """
).fetchall()
end_time2 = time.time()
print(f"Duckdb original sum Query Execution Time: {end_time2 - start_time2:.6f} seconds")
print(resultFromNormalSum)

start_time3 = time.time()
resultFromNormalSum = con.execute(
    """
                SELECT SUM(amount) FROM sales
        """
).fetchall()
end_time3 = time.time()
print(f"Duckdb original sum Query 2 Execution Time: {end_time3 - start_time3:.6f} seconds")
print(resultFromNormalSum)

start_time4 = time.time()
result = con.execute(
    """
        SELECT udf_demo(amount) FROM sales
        """
).fetchall()
end_time4 =  time.time()
print(result)
print(f"Python UDF Query Execution Time: {end_time4 - start_time4:.6f} seconds")
