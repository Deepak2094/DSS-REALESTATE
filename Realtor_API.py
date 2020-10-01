import requests

url = "https://realtor.p.rapidapi.com/properties/v2/list-for-sale"

querystring = {"sort": "relevance", "city": "Arlington", "limit": "1000", "offset": "0", "state_code": "VA"}

headers = {
    'x-rapidapi-host': "realtor.p.rapidapi.com",
    'x-rapidapi-key': "ede51666fcmsh9785fa150d39b75p1787e9jsnf48a84ac05c4"
}

response = requests.request("GET", url, headers=headers, params=querystring)
print(response.text)

# writeFile = open('file_name.json', 'w')
#     writeFile.write(your_data)
#     writeFile.close()