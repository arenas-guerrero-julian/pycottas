import duckdb
import cottas

rdf_file_path = 'n-triples-star-tests/ntriples-star-syntax-5.nt'
cottas_file_path = 'ntriples-star-syntax-5.cottas'

cottas.rdf_2_cottas(rdf_file_path, cottas_file_path)
print('Compress file:')
print(duckdb.query(f"SELECT * FROM PARQUET_SCAN('{cottas_file_path}')"))

cottas.create_id(cottas_file_path, expand=True)
print('After expansion:')
print(duckdb.query(f"SELECT * FROM PARQUET_SCAN('{cottas_file_path}')"))

print('Evaluate triple pattern:')
print(cottas.search(cottas_file_path, '<< << <http://example/s1> <http://example/p1> ?o1 >> <http://example/q1> << <http://example/s2> <http://example/p2> <http://example/o2> >> >> ?p ?o2'))

print('Retrieve basic info:')
print(cottas.info(cottas_file_path))

print('\nShrink for archival:')
cottas.remove_id(cottas_file_path, shrink=True)
print(duckdb.query(f"SELECT * FROM PARQUET_SCAN('{cottas_file_path}')"))

print('Uncompress file to N-Triples:')
#cottas.cottas_2_rdf(cottas_file_path, rdf_file_path)