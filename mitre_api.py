from stix2 import TAXIICollectionSource
from stix2 import Filter
from taxii2client.v20 import Collection # only specify v20 if your installed version is >= 2.0.0
from taxii2client.v20 import Server # only specify v20 if your installed version is >= 2.0.0

server = Server("https://cti-taxii.mitre.org/taxii/")
api_root = server.api_roots[0]
# Print name and ID of all ATT&CK domains available as collections
for collection in api_root.collections:
    print(collection.title.ljust(20) + collection.id)