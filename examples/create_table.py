import random

import pandas

import hyperleda

client = hyperleda.HyperLedaClient(endpoint=hyperleda.TEST_ENDPOINT)

table_name = f"test_table_{random.randrange(0, 100000)}"

table_id = client.create_table(
    hyperleda.CreateTableRequest(
        table_name=table_name,
        columns=[
            hyperleda.ColumnDescription(
                name="ra",
                data_type=hyperleda.DatatypeEnum.double,
                ucd="pos.eq.ra",
                unit="deg",
                description="Right ascension",
            ),
            hyperleda.ColumnDescription(
                name="dec",
                data_type=hyperleda.DatatypeEnum.double,
                ucd="pos.eq.dec",
                unit="deg",
                description="Declination",
            ),
            hyperleda.ColumnDescription(
                name="id",
                data_type=hyperleda.DatatypeEnum.str,
                ucd="meta.id;meta.main",
            ),
            hyperleda.ColumnDescription(
                name="obscure_column",
                data_type=hyperleda.DatatypeEnum.float,
            ),
        ],
        bibcode="1992ApJ...400L...1W",
        datatype=hyperleda.DataType.regular,
        description="",
    )
)

print(f"Created table '{table_name}' with ID: {table_id}")

data = pandas.DataFrame(
    [
        {
            "ra": 123.45,
            "dec": 25.56,
            "id": "1234-haha",
        },
        {"ra": 52.1, "dec": 65.58, "id": "4321-1234", "obscure_column": 0.00647372},
    ]
)

client.add_data(table_id, data)
print(f"Added data to the table '{table_name}':\n{data}")

table_info = client.get_table(table_name)
print(f"\nTable information for '{table_name}':")
print(f"  ID: {table_info.id}")
print(f"  Description: {table_info.description}")
print(f"  Number of rows: {table_info.rows_num}")
print(f"  Number of columns: {len(table_info.column_info)}")
print("  Columns:")
for col in table_info.column_info:
    print(f"    - {col.name} ({col.data_type}) - {col.description or 'No description'}")
if table_info.statistics:
    print(f"  Statistics: {table_info.statistics}")
