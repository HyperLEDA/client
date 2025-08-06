from hyperleda import data

client = data.HyperLedaDataClient()

resp = client.query_simple(data.QuerySimpleRequestSchema(pgcs=[123], page_size=25))
print(resp.model_dump_json())
