import json
import time
import random
import requests
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
#from adventure import adventure_game
from pokemon import pokemon_list
from pokemon import pokemon_active

bearer_token = 'h6phkma4ibnr3fpdayutxpy7wh'
#intern channel qrfhyetwutnnucb3uuoe3ka1fh
#for test channel use the token for your dms
#test channel h6phkma4ibnr3fpdayutxpy7wh

LISTEN_URL = 'https://mattermost.hyland.com/api/v4/channels/' + bearer_token + '/posts'
POST_URL = 'https://mattermost.hyland.com/api/v4/posts'
AUTH_TOKEN = 'h6s5cmnp5pr77kx6s7ao3huwzh'

#Checks for valid commands
def process_commands(message, name):
    #no flag response
    if(message.lower() == "!vbot"):
        post_message("PokeBot Says: Thank you for using PokeBot! For a list of commands please use the help or h flag.")

    #help flag
    if("!vbot h" in message.lower()):
        post_message("PokeBot Says: ")

    #catch poke
    if(message.lower() in pokemon_list):
        if pokemon_active[message.lower()] == 1:
            post_message('VolleyBot Says: ' + name + ' caught ' + message.lower() +'!')
            pokemon_active[message.lower()] = 0
            if(name.lower() in trainers):
                trainers[name.lower()].append(message.lower())
            else:
                new_pokemon_list = [message.lower()]
                trainers[name.lower()] = new_pokemon_list

    #check pokemon flag
    if("!pbot p" in message.lower()):
        if(name.lower() in trainers):
            mypokemon = ''
            for pokemon in trainers[name.lower()]:
                mypokemon = mypokemon + ' :' + pokemon + ': '
            post_message('VolleyBot Says: Displaying ' + name + '\'s Pokemon.')
            post_message(mypokemon)

#posts a message in the channel
def post_message(s):
    data = {'channel_id': bearer_token, 'message': s}
    headers = {'Authorization': 'Bearer ' + AUTH_TOKEN}
    requests.post(POST_URL, json= data, headers= headers, verify= False)

#gets a message/display name of messages sent in the channel
def read_message():
    headers = {'Authorization': 'Bearer ' + AUTH_TOKEN}
    resp = requests.get(LISTEN_URL, headers= headers, verify= False)
    if(resp.status_code==200):
        #gets the message text
        info = json.loads(resp.text)
        post = info['order'][0]

        #gets the user's display name
        userid = info['posts'][post]['user_id']
        profile = requests.get('https://mattermost.hyland.com/api/v4/users/' + userid, headers= headers, verify= False)
        user = json.loads(profile.text)
        display_name = user['first_name'] + ' ' + user['last_name']

        #returns message, display name
        return (info['posts'][post]['message'], display_name)

#sends a random pokemon to the channel and flags it as active
def send_pokemon(pokedex):
    index = random.randint(0, len(pokedex) - 1)
    pokemon = pokedex[index].lower()
    pokemon_active[pokemon] = 1
    post_message('# :' + pokemon + ':')


trainers = {'zach dudzik':['mega_gengar','pikachu']}

start = time.gmtime()
while True:

    #populate with pokemon
    minute_wait = random.randint(2, 5)
    if(time.gmtime()[4] > start[4] + minute_wait or time.gmtime()[3] > start[3]):
        send_pokemon(pokemon_list)
        start = time.gmtime()

    #gets messages/display names
    message, name = read_message()

    #processes commands
    process_commands(message, name)
