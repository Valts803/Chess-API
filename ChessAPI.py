from chessdotcom import get_player_game_archives, get_player_profile
import pprint
import requests
import sqlite3
import html

printer = pprint.PrettyPrinter()

print("Chess API impoted")

dbFileName = "Player Nationalities.db"
connection = sqlite3.connect(dbFileName)
cursor = connection.cursor()
cursor.execute('CREATE TABLE IF NOT EXISTS players (name, nationality)')

#def by_number(dic):
#	return dic[nat]

def get_player_nationality(username):
	data = get_player_profile(username).json
	#printer.pprint(data)
	url = data['player']['country']
	country_api = requests.get(url).json()
	country = country_api['name']

	cursor.execute('INSERT INTO players VALUES (?, ?)', (username, country))
	connection.commit()
	#printer.pprint(data)
	return country

def get_game_ratings(username):
	dic = {
	'rating': [],
	'no.': []
	}

	i = 1

	data = get_player_game_archives(username).json
	#printer.pprint(data)
	for url in data['archives']:
		games = requests.get(url).json()
		for game in games['games']:
			if (game['rules'] == 'chess' and game['time_class'] == 'blitz'):
				if (game['black']['username'] == username):
					dic['rating'].append(game['black']['rating'])
					dic['no.'].append(i)
					i +=1
					#print(game['black']['rating'])
				if (game['white']['username'] == username):
					dic['rating'].append(game['white']['rating'])
					dic['no.'].append(i)
					i +=1
					#print(game['white']['rating'])
	return dic

def get_oponent_nationalities(username):
	dic = {}
	wr_dic = {}
	total_games = 0
	data = get_player_game_archives(username).json
	for url in data['archives']:
		games = requests.get(url).json()
		for game in games['games']:
			#printer.pprint(game)
			if (game['black']['username'] == username):
				pname = game["white"]["username"]
				#printer.pprint(pname)
				cursor.execute('SELECT nationality FROM players WHERE name = ?', (pname,))
				#print(cursor.fetchone())
				nationality = cursor.fetchone()
				if nationality is None:
					nat = get_player_nationality(game['white']['username'])
					if nat not in dic:
						dic[nat] = [1, 0]
						total_games += 1
						if (game['black']['result'] == "win"):
							dic[nat][1] += 1
					else:
						dic[nat][0] += 1
						total_games += 1
						if (game['black']['result'] == "win"):
							dic[nat][1] += 1
				else:
					nat = ''.join(nationality)
					#print(type(nat))
					if nat not in dic:
						dic[nat] = [1, 0]
						total_games += 1
						if (game['black']['result'] == "win"):
							dic[nat][1] += 1
					else:
						dic[nat][0] += 1
						total_games += 1
						if (game['black']['result'] == "win"):
							dic[nat][1] += 1


			if (game['white']['username'] == username):
				pname = game["black"]["username"]
				#printer.pprint(pname)
				cursor.execute('SELECT nationality FROM players WHERE name = ?', (pname,))
				#print(cursor.fetchone())
				nationality = cursor.fetchone()
				if nationality is None:
					nat = get_player_nationality(game['black']['username'])
					if nat not in dic:
						dic[nat] = [1, 0]
						total_games += 1
						if (game['white']['result'] == "win"):
							dic[nat][1] += 1

					else:
						dic[nat][0] += 1
						total_games += 1
						if (game['white']['result'] == "win"):
							dic[nat][1] += 1
				else:
					nat = ''.join(nationality)
					#print(type(nat))
					if nat not in dic:
						dic[nat] = [1, 0]
						total_games += 1
						if (game['white']['result'] == "win"):
							dic[nat][1] += 1
					else:
						dic[nat][0] += 1
						total_games += 1
						if (game['white']['result'] == "win"):
							dic[nat][1] += 1
	
	for country, l in dic.items():
		wr_dic[country] = (l[1]/l[0])*100

	sorted_dic = sorted(wr_dic.items(), key = lambda x: x[1], reverse=True)

	#printer.pprint(sorted_dic)
	
	countries = []
	wr = []

	for country, percent in sorted_dic:
		countries.append(country)
		wr.append(percent)
	
	lst = [countries, wr, total_games]

	return lst

	


				




#get_player_nationality('Valts_IZV')
#print(get_game_ratings('Valts_IZV'))

#print_leaderboards()
#get_player_rating('Valts_IZV')
#print(get_oponent_nationalities('Valts_IZV'))
#print(get_oponent_nationalities('Latvian_maffia'))
#cursor.execute('INSERT INTO players VALUES (?, ?)', ("Frontier123135", "NZ"))

#cursor.execute('SELECT nationality FROM players WHERE name = ?', ("Frontier123135",))
#print(cursor.fetchone())