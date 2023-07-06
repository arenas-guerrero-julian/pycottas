import duckdb

print(duckdb.query("SELECT * FROM read_parquet('dir/file.cottas')"))

