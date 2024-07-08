Install latest version:

```
pip install git+https://github.com/HyperLEDA/client.git
```

Usage:

```python
import os
import hyperleda

token = os.getenv("HYPERLEDA_TOKEN") # token is optional for non-admin handlers
client = hyperleda.HyperLedaClient(token=token)
print(client.create_table(hyperleda.CreateTableRequestSchema(
    table_name="test_table",
    columns=[
        hyperleda.ColumnDescription(
            name="ra",
            data_type="double",
            unit="deg",
            description="Right ascension",
        ),
        hyperleda.ColumnDescription(
            name="dec",
            data_type="double",
            unit="deg",
            description="Declination",
        ),
    ],
    bibcode="1992ApJ...400L...1W",
)))
```
