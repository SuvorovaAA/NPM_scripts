import requests
import json

# Define searched text
proteome_id = 'UP000006548'
# Define request URL
request_url = 'https://mobidb.org/api/download_page'
# Perform GET request, retrieve response object
json_response = requests.get(
        request_url, params={'proteome': proteome_id}
    )

with open("arabidopsis_proteome.json", "w") as f:
    json.dump(json_response.json(), f, indent=4)

# Print number of retrieved entries
print(f'Retrieved {json_response.json()["metadata"].get("count", 0)} entries for proteome {proteome_id}')