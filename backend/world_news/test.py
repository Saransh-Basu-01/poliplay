import requests

url = "https://api.worldnewsapi.com/search-news"
headers = {"x-api-key": "485f3822243642158403677b955503a4"}
params = {"text": "Nepal", "language": "en", "number": 5}

response = requests.get(url, headers=headers, params=params)
print(f"Status: {response.status_code}")
print(f"Response: {response.json() if response.status_code == 200 else response.text}")