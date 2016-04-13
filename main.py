import requests
import json
import sys, argparse
from bs4 import BeautifulSoup

# Returns all current days games in an ordered list.
def get_games():
    
    # The Yahoo Sports nba ticker feed updated realtime and contains scores
    # for all games played on the day.
    url='https://ca.sports.yahoo.com/__xhr/sports/scorestrip-gs/?d=full&b=& \
            format=realtime&ncaab_post_season=true&league=nba&'
    
    # Getting the output of the ticker feed.
    html = requests.get(url)
    content = html.json()
    soup = BeautifulSoup(content['content'], 'lxml')
    
    # Getting the html of all the games
    current_games = soup.find_all(attrs={'class': 'nba'})

    # All game information will be stored here.
    games = [['Live Games'],['Completed Games'],['Upcoming Games']]

    # Going through each game and adding the appropriate information
    # to the list above.
    for number,game in enumerate(current_games):
        
        # Get the game name. When the game goes to overtime it doesn't contain
        # the ': ' for some reason so we have to take that into consideration.
        game_title = game.a['title']
        game_title = game_title.split(': ')[1] if ': ' in game_title \
                else game_title

        # 'game_time' determines the current in game time for live games and
        # start time for upcoming games. They need to be handled seperately
        # because the html is drastically different in the feed.
        if game['class'][0] == 'live':
            game_time = game.find(class_='period').string
            games[0].append((number,game_title,game_time))
        elif game['class'][0] == 'final':
            games[1].append((number,game_title,''))
        elif game['class'][0] == 'upcoming':
            game_start = game.em.string
            games[2].append((number,game_title,game_start))

    return games

# Formats and prints the current days games.
def list_games():
    games = get_games()
    
    # Loops through each section of games.
    for i in range(0,len(games)):

        # Prints a blank space in between sections.
        if len(games)-1 >= i > 0 and len(games[i-1]) > 1 and \
                len(games[i]) > 1: print()

        # Print section title.
        if len(games[i]) > 1: print(games[i][0])

        # Loops through each game in the section; formats and prints game.
        for number,game,time in games[i][1:]:
            print(str(number+1) + '. ' + game + (' - ' if time else '') + time)

def parse_args(parser,args):
    if args.game == 'list':
        list_games()

def main():
    # Command line arguments.
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
