# PySymvea - Python Client

Python client for Symvea server.

## Installation

```bash
pip install -e .
```

## Usage

```bash
# Upload file
pysymvea upload myfile.txt

# Download file  
pysymvea download myfile.txt

# Verify file
pysymvea verify myfile.txt

# Connect to different server
pysymvea --host 192.168.1.100:24096 upload myfile.txt
```

## Programmatic Usage

```python
from pysymvea import SymveaClient

client = SymveaClient("127.0.0.1", 24096)
client.connect()

# Upload
with open("file.txt", "rb") as f:
    data = f.read()
original_size, compressed_size = client.upload("file.txt", data)

# Download
data = client.download("file.txt")

# Verify
is_valid = client.verify("file.txt")

client.close()
```