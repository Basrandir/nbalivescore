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
        game_title = game.a['title'].split(': ')[1]

        # 'game_time' determines the current in game time for live games and
        # start time for upcoming games. They need to be handled seperately
        # because the html is drastically different in the feed.
        if game['class'][0] == 'live':
            game_time = game.find(class_='status').span.string
            games[0].append([number,game_title,game_time])
        elif game['class'][0] == 'final':
            games[1].append([number,game_title,''])
        elif game['class'][0] == 'upcoming':
            game_start = game.em.string
            games[2].append([number,game_title,game_start])
    
    return games

# Formats and prints the current days games.
def list_games():
    games = []

    # Loops through each section of games. Formats the data and
    # adds it to a new list.
    for section in get_games():
        
        if len(section) > 1:

            # Adds section title.
            games.append([section[0]])

            # Loops through the data of each game. Formats it and adds it to
            # the list.
            for number,game,time in section[1:]:
                games[len(games)-1].append(str(number+1) +
                        '. ' + game + (' - ' if time else '') + time)

    # Adds a new line between each games and time and 2 between each section.
    print('\n\n'.join('\n'.join(map(str,seq)) for seq in games))

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
