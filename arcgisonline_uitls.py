import requests
import json


def get_token(username, password, expiration=432000):
    endpoint = "https://arcgis.com/sharing/rest/generateToken"
    data = {
        "username": username,
        "password": password,
        "referer": "https://www.arcgis.com",
        "expiration": str(expiration),
        "f": "json",
        "ssl": True,
    }
    try:
        jres = requests.post(endpoint, data=data, verify=False).json()
        return jres["token"]
    except KeyError:
        print("Failed to retrieve token")
        return None


def query_features(fs_url, token, query="1=1", outfields="*"):
    endpoint = "{}/query".format(fs_url)
    data = {"token": token, "f": "json", "where": query, "outfields": outfields}
    jres = requests.post(endpoint, data).json()
    return jres["features"]


def update_features(fs_url, token, attributes):
    endpoint = "{}/UpdateFeatures".format(fs_url)
    attributes = [attributes]

    data = {
        "token": token,
        "features": json.dumps(attributes),
        "f": "json",
        "rollbackOnFailure": True,
    }

    jres = requests.post(endpoint, data=data, verify=False).json()
    return jres
