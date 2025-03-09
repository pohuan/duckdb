PRAGMA threads=4;  -- Ensure parallel execution

CREATE TABLE test_data (id INTEGER, value DOUBLE);
INSERT INTO test_data
SELECT i.generate_series, random()
FROM generate_series(1, 1000000) AS i;  -- Large dataset for parallelism

-- Run an aggregate function that requires state combination
SELECT SUM(value) FROM test_data;

