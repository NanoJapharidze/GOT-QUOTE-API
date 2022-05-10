import sqlite3
import requests
import json

url = 'https://game-of-thrones-quotes.herokuapp.com/v1/random'
r = requests.get(url)
res = r.json()

# # N1

print(json.dumps(res, indent=4))
print(r.text)
if str(r.status_code) == '200':
    print(f"Request ended successfully. Status code: {r.status_code}")
else:
    print(f"Error. Status code: {r.status_code}")
print(f"Response date: {r.headers['Date']}")
print(f"Response content type: {r.headers['Content-Type']}")


# # N2

with open('got_quotes.json', 'w') as got_quotes:
    json.dump(res, got_quotes, indent=4)


# # N3

house = res['character']['house']['name']
character_name = res['character']['name'].split()
character_lastname = house.split()[1]


family_name_words = {'Baratheon': 'Ours is fury!', 'Tully': 'Family, Duty, Honor.', 'Stark': 'Winter is coming',
                   'Tyrell': 'Growing Strong', 'Greyjoy': 'We Do Not Sow', 'Martell': 'Unbowed, Unbent, Unbroken',
                   'Lannister': 'Hear Me Roar!', 'Frey': 'We Stand Together', 'Hornwood': 'Righteous in Wrath',
                   'Arryn': 'As High as Honor', 'Targaryen': 'Fire and Blood', 'Bolton': 'Our Blades are Sharp',
                   'Karstark': 'The sun of winter', 'Tallhart': 'Proud and Free', 'Mormont': 'Here We Stand',
                     'Tarly': 'First in Battle'}


if house is None:
    print(f"{res['character']['name']} once said: \"{res['sentence']}\"")
else:
    print(f"{character_name[0]} of {house} once said: \"{res['sentence']}\"")

if character_lastname in family_name_words.keys():
    print(f"Words of {house} are: \"{family_name_words[character_lastname]}\"")
elif house is None:
    print(f"{res['character']['name']} has no family name")
else:
    print(f"{res['character']['name']} has no house words")


# # N4

# ცხრილში ემატება პერსონაჟის სახელი, საგვარეულო და მის მიერ ნათქვამი მნიშვნელოვანი ფრაზა
conn = sqlite3.connect('quotes.sqlite3')
cursor = conn.cursor()

cursor.execute('''CREATE TABLE IF NOT EXISTS got_quotes
                (id INTEGER PRIMARY KEY AUTOINCREMENT,
                Name VARCHAR(50),
                House VARCHAR(100),
                Quote VARCHAR(500))
                ''')

quotes_list = []
quotes_list.append((res['character']['name'], res['character']['house']['name'], res['sentence']))

cursor.executemany("INSERT INTO got_quotes (Name, House, Quote) values (?, ?, ?)", quotes_list)
conn.commit()
