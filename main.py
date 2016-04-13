import requests
import json
import sys, argparse
from bs4 import BeautifulSoup

def get_games():
    url='https://ca.sports.yahoo.com/__xhr/sports/scorestrip-gs/?d=full&b=& \
            format=realtime&ncaab_post_season=true&league=nba&'

    html = requests.get(url)
    content = html.json()
    soup = BeautifulSoup(content['content'], 'lxml')
    current_games = soup.find_all(attrs={'class': 'nba'})

    games = [['Live Games'],['Completed Games'],['Upcoming Games']]

    for number,game in enumerate(current_games):
        
        # Get the game name. When the game goes to overtime it doesn't contain
        # the ': ' for some reason so we have to take that into consideration.
        game_title = game.a['title']
        game_title = game_title.split(': ')[1] if ': ' in game_title \
                else game_title

        if game['class'][0] == 'live':
            game_time = game.find(class_='period').string
            games[0].append((number,game_title,game_time))
        elif game['class'][0] == 'final':
            games[1].append((number,game_title,''))
        elif game['class'][0] == 'upcoming':
            game_start = game.em.string
            games[2].append((number,game_title,game_start))

    return games

def list_games():
    games = get_games()
    
    for i in range(0,len(games)):
        if len(games)-1 >= i > 0 and len(games[i-1]) > 1 and \
                len(games[i]) > 1: print()
        if len(games[i]) > 1: print(games[i][0])
        for number,game,time in games[i][1:]:
            print(str(number+1) + '. ' + game + (' - ' if time else '') + time)

def parse_args(parser,args):
    if args.game == 'list':
        list_games()

def main():
    # command line
    parser = argparse.ArgumentParser(
            description='Get live score updates for the NBA')
    parser.add_argument('-g', '--game',
            help='List the current live games',
            required=True)
    
    args = parser.parse_args()
    parse_args(parser,args)

if __name__ == '__main__': main()

'''
theurl = 'https://ca.sports.yahoo.com/__xhr/sports/match/gs/?gid=nba.g.2016041027&league_id=nba&format=realtime&entity_type=unit_competition&flavor=mini&dynamicModules=MediaModuleMatchHeaderGrandSlam,MediaSportsLineScore,MediaSportsMatchLastPlay,MediaSportsPlayByPlay,MediaSportsMatchStatsByPlayer&d=full&enable_cards=1'
html = requests.get(theurl)
content = html.json()

soup = BeautifulSoup(content['content']['mediasportsmatchstatsbyplayer'], 'lxml')

players = soup.find_all(attrs={'class': 'athlete'})

for player in players:
    name = list(player.stripped_strings)[0]
    print(name)

    for stats in player.parent.find_all('td'):
        if (stats.has_attr('title')):
            print(stats['title'] + ': ' + stats.string)

    print()
    '''
