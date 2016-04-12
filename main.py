import requests
import json
import sys, argparse
from bs4 import BeautifulSoup

def get_games():
    url='https://ca.sports.yahoo.com/__xhr/sports/scorestrip-gs/?d=full&b=&format=realtime&ncaab_post_season=true&league=nba&'

    html = requests.get(url)
    content = html.json()
    soup = BeautifulSoup(content['content'], 'lxml')
    return soup.find_all(attrs={'class': 'nba'})

def parse_args(parser,args):
    if args.game == 'list':
        games = [['Live Games'],['Completed Games'],['Upcoming Games']]

        for number,game in enumerate(get_games()):
            if game['class'][0] == 'live':
                games[0].append((number,game.a['title'].split(': ')[1]))
            elif game['class'][0] == 'final':
                games[1].append((number,game.a['title'].split(': ')[1]))
            elif game['class'][0] == 'upcoming':
                games[2].append((number,game.a['title'].split(': ')[1]))
        
        for i in range(0,len(games)):
            if len(games)-1 > i > 0 and len(games[i-1]) > 1 and len(games[i+1]) > 1: print()
            if len(games[i]) > 1: print(games[i][0])
            for number,game in games[i][1:]:
                print(str(number + 1) + '. ' + game)
            
    else:
        live_games = get_games()

        for number,game in enumerate(live_games):
            if number+1 == int(args.game):
                print(game.a['title'].split(': ')[1])
                break

def main():
    # command line
    parser = argparse.ArgumentParser(description='Get live score updates for the NBA')
    parser.add_argument('-g', '--game', choices=['list']+[str(x) for x in list(range(1,len(get_games())+1))], help='List the current live games', required=True)
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
