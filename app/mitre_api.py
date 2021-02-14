#from stix2 import TAXIICollectionSource
#from stix2 import Filter
#from taxii2client.v20 import Collection # only specify v20 if your installed version is >= 2.0.0
from taxii2client.v20 import Server # only specify v20 if your installed version is >= 2.0.0

server = Server("https://cti-taxii.mitre.org/taxii/")
api_root = server.api_roots[0]
# Print name and ID of all ATT&CK domains available as collections
for collection in api_root.collections:
    print(collection.title.ljust(20) + collection.id)

'''
collections = {
    "enterprise_attack": "95ecc380-afe9-11e4-9b6c-751b66dd541e",
    "mobile_attack": "2f669986-b40b-4423-b720-4396ca6a462b",
    "ics-attack": "02c3ef24-9cd4-48f3-a99f-b74ce24f1d34"
}


collection = Collection(f"https://cti-taxii.mitre.org/stix/collections/{collections['enterprise_attack']}/")
src = TAXIICollectionSource(collection)
phish = src.query([ Filter("external_references.external_id", "=", "T1566") ])[0]

print(phish['name']) #print name of technique phishing
print(phish['description']) #print description of technique phishing 

'''