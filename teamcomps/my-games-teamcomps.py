import logging
import requests
from collections import defaultdict

logger = logging.getLogger(__name__)


def get_teamcomp(url):
	game = requests.get(url).json()
	blue_team = [player['name'] for player in game['teams']['blue']]

	hero_playtime = {p: defaultdict(int) for p in blue_team}
	lasthero = {p: None for p in blue_team}
	lastseen = {p: 0 for p in blue_team}
	for timestamp, type, hero_l, player_l, hero_r, player_r, assisters, ability in game['killfeed']:

		# res means both players can be on the same team
		player_hero_pairs = []
		if player_l in blue_team:
			player_hero_pairs.append((hero_l, player_l))
		if player_r in blue_team:
			player_hero_pairs.append((hero_r, player_r))

		for hero, player in player_hero_pairs:
			if lasthero[player] == hero:
				hero_playtime[player][hero] += timestamp - lastseen[player]

			lasthero[player] = hero
			lastseen[player] = timestamp

	teamcomp = [max(hero_playtime[p].keys(), key=lambda hero: hero_playtime[p][hero]) if hero_playtime[p] else 'unk' for p in blue_team]
	return '_'.join(sorted(teamcomp))


def main():
	share_key = input('OverTrack share key? ')
	if share_key.endswith('/'):
		share_key = share_key[:-1]
	if '/' in share_key:
		share_key = share_key.split('/')[-1]

	endpoint = 'https://api.overtrack.gg/games/%s' % share_key

	games = requests.get(endpoint).json()['games']

	for game in games:
		result = game['result']
		if result not in ['WIN', 'LOSS', 'DRAW']:
			continue

		try:
			teamcomp = get_teamcomp(game['url'])
		except Exception as e:
			logger.error('Error reading game %s', game['key'], exc_info=e)
			continue

		if game['start_sr'] and game['end_sr']:
			sr_change = str(game['end_sr'] - game['start_sr'])
		else:
			sr_change = ''

		print(', '.join((teamcomp, result, sr_change)))

if __name__ == '__main__':
	main()
