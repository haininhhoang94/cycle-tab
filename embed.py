import requests

WORKSPACE_ID = "0fbd1ce5-ae2d-43e9-95ca-9415d341d2f7"
REPORT_ID = "b72755bc-069f-42b8-92b5-e66ce9e86413"


def get_embed_info(access_token):
    url = f"https://api.powerbi.com/v1.0/myorg/groups/{WORKSPACE_ID}/reports/{REPORT_ID}"
    headers = {"Authorization": f"Bearer {access_token}"}

    response = requests.get(url, headers=headers)
    response.raise_for_status()
    data = response.json()

    return {
        "id": data["id"],
        "embedUrl": data["embedUrl"],
        "name": data["name"],  # optional: title of the report
    }
