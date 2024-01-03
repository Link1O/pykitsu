import requests
def update_latest_id():
   response = requests.get('https://kitsu.io/api/edge/anime', params={'sort': '-id', 'page[limit]': 1})
   data = response.json()
   latest_id = data['data'][0]['id']
   return latest_id
print(update_latest_id())