import json
import time
import random
import requests
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
#from adventure import adventure_game
from pokemon import pokemon_list

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
        post_message("VBot Says: Thank you for using vbot! For a list of commands please use the help or h flag.")

    #help flag
    if("!vbot help" in message.lower() or "!vbot h" in message.lower()):
        post_message("VBot Says: \n time(t): tells amount of time until volleyball (in mere seconds) \n cake(c): Makes you a cake! Happy Day! \n insult(i): insults the requester")

    #cake flag
    if("!vbot cake" in message.lower() or "!vbot c" in message.lower()):
        make_cake(name)    

    #time flag
    if("!vbot time" in message.lower() or "!vbot t" in message.lower()):
        ctime = time.gmtime()
        seconds_left = (18 - ctime[3]) * 3600 + (30 - ctime[4]) * 60 + (60 - ctime[5]) - 60
        if (seconds_left < 0):
            seconds_left = 86400 + seconds_left
        post_message(f'VBot Says: There are merely {seconds_left} seconds until Volley Ball!')

    #insult flag
    if("!vbot insult" in message.lower() or "!vbot i" in message.lower()):
        index = random.randint(0, len(postfix_insults) - 1)
        post_message(name + ' ' + postfix_insults[index])

    #version flag
    if("!vbot version" in message.lower() or "!vbot v" in message.lower()):
        post_message('You are currently using vbot version 0.2.22, thank you for your continued support of vbot.')

    #adventure flag
    #if("!vbot adventure" in message.lower() or "!vbot a" in message.lower()):
        #adventure_game()

    #gamble flag

    #pokemon flag

    ### ------- ADD NEW FLAGS HERE ------- ###

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

#prints cake with string centered
def print_cake(string):
    #center the name
    if len(string) % 2 == 0:
        num_spaces1 = (20 - len(string)/ 2)
        num_spaces2 = num_spaces1
    else:
        num_spaces1 =  int((20 - len(string)/2))
        num_spaces2 = num_spaces1 - 1
        
    spaces1 = ''
    for i in range(int(num_spaces1)):
        spaces1 = spaces1 + ' '
    spaces2 = ''
    for j in range(int(num_spaces2)):
        spaces2 = spaces2 + ' '

    post_message('                           )\\ \n                          (__)\n                           /\\ \n                          [[]]\n                       @@@[[]]@@@\n                 @@@@@@@@@[[]]@@@@@@@@@\n             @@@@@@@      [[]]      @@@@@@@\n         @@@@@@@@@        [[]]        @@@@@@@@@\n        @@@@@@@           [[]]           @@@@@@@\n        !@@@@@@@@@                    @@@@@@@@@!\n        !    @@@@@@@                @@@@@@@    !\n        !        @@@@@@@@@@@@@@@@@@@@@@        !\n        !              @@@@@@@@@@@             !\n        !             ______________           !\n        !' + spaces1 + string + spaces2 + '!\n        !             --------------           !\n        !!!!!!!                          !!!!!!!\n             !!!!!!!                !!!!!!!\n                 !!!!!!!!!!!!!!!!!!!!!!!')

#Converts display name to nickname
def get_nickname(name):
    if name in nicknames:
        return nicknames[name]
    else:
        return name

#Constructs cake with appropriate nickname
def make_cake(name):
        nickname = get_nickname(name)
        print_cake('Happy Day '+ nickname + '!')
        time.sleep(1)

#insults for insult command
postfix_insults = ['is a dumpster fire.', 'SUX!','should just give up already.','is almost as bad as Ethan Zuccola.','stinks.','literally cannot read.','looks like their face caught on fire and someone tried to put it out with a fork.','should slip into a coma.','has no life.','']

#dictionary of nicknames for users
nicknames = {'Ethan Zuccola': 'Shithead',
             'Chrissy Cotton': 'VolleyGod',
             'Collin Werner': 'Idiot',
             'Zach Dudzik': 'BotGod'
            }

while True:
    #gets messages/display names
    message, name = read_message()

    #processes commands
    process_commands(message, name)
    
