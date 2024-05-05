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
print(client.create_bibliography("2001quant.ph..1003R", "Quantum Physics", ["R. R. Ross"], 2000))
```
