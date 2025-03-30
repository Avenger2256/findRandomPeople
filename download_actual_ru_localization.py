from requests import get

url = 'https://raw.githubusercontent.com/Avenger2256/findRandomPeople/refs/heads/main/strings.json'

with open('actual_localization.json', 'wb') as file:
    file.write(get(url).content)