import random

import pandas

import hyperleda

client = hyperleda.HyperLedaClient(endpoint=hyperleda.TEST_ENDPOINT)

table_name = f"test_table_{random.randrange(0, 100000)}"

table_id = client.create_table(
    hyperleda.CreateTableRequestSchema(
        table_name=table_name,
        columns=[
            hyperleda.ColumnDescription(
                name="ra",
                data_type=hyperleda.DataType("double"),
                ucd="pos.eq.ra",
                unit="deg",
                description="Right ascension",
            ),
            hyperleda.ColumnDescription(
                name="dec",
                data_type=hyperleda.DataType("double"),
                ucd="pos.eq.dec",
                unit="deg",
                description="Declination",
            ),
        ],
        bibcode="1992ApJ...400L...1W",
    )
)

print(f"Created table '{table_name}' with ID: {table_id}")

data = pandas.DataFrame(
    [
        {
            "ra": 123.45,
            "dec": 25.56,
        },
        {
            "ra": 52.1,
            "dec": 65.58,
        },
    ]
)

client.add_data(table_id, data)
print(f"Added data to the table '{table_name}':\n{data}")
