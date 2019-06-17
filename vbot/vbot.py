import json
import time
import requests
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


bearer_token = 'qrfhyetwutnnucb3uuoe3ka1fh'
#intern channel qrfhyetwutnnucb3uuoe3ka1fh
#test channel h6phkma4ibnr3fpdayutxpy7wh

LISTEN_URL = 'https://mattermost.hyland.com/api/v4/channels/' + bearer_token + '/posts'
POST_URL = 'https://mattermost.hyland.com/api/v4/posts'

def post_message(s):
    data = {'channel_id': bearer_token, 'message': s}
    headers = {'Authorization': 'Bearer jjn1xqx4dpd8zkg8xg3scqgppa'}
    requests.post(POST_URL, json= data, headers= headers, verify= False)

def read_message():
    headers = {'Authorization': 'Bearer jjn1xqx4dpd8zkg8xg3scqgppa'}
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

        return (info['posts'][post]['message'], display_name)

def print_cake(string):
    post_message('                           )\\ \n                          (__)\n                           /\\ \n                          [[]]\n                       @@@[[]]@@@\n                 @@@@@@@@@[[]]@@@@@@@@@\n             @@@@@@@      [[]]      @@@@@@@\n         @@@@@@@@@        [[]]        @@@@@@@@@\n        @@@@@@@           [[]]           @@@@@@@\n        !@@@@@@@@@                    @@@@@@@@@!\n        !    @@@@@@@                @@@@@@@    !\n        !        @@@@@@@@@@@@@@@@@@@@@@        !\n        !              @@@@@@@@@@@             !\n        !             ______________           !\n        !    ' + string + '            \n        !             --------------           !\n        !!!!!!!                          !!!!!!!\n             !!!!!!!                !!!!!!!\n                 !!!!!!!!!!!!!!!!!!!!!!!')

def make_cake(name):
    if (name == 'Ethan Zuccola'):
        print_cake('        Happy Day Shithead!')
        time.sleep(1)
    elif(name == 'Collin Werner'):
        print_cake('        Happy Day Idiot!')
        time.sleep(1)
    elif(name == 'Chrissy Cotton'):
        print_cake('      Happy Day VolleyGod!')
        time.sleep(1)
    elif(name == 'Zach Dudzik'):
        print_cake('        Happy Day BotGod!')
        time.sleep(1)
    else:
        print_cake('      Happy Day '+ name + '!')
        time.sleep(1)

insults = ['is a dumpster fire.', 'SUX!','should just give up already.','is almost as bad as Ethan Zuccola.','stinks.','literally cannot read.']

while True:
    #updates time
    true_time = time.time()
    ctime = time.gmtime()
    seconds_left = (18 - ctime[3]) * 3600 + (30 - ctime[4]) * 60 + (60 - ctime[5]) - 60

    #gets messages/display names
    message, name = read_message()
    message.lower()

    if(message.lower() == "!vbot"):
        post_message("VBot Says: Thank you for using vbot! For a list of commands please use the help or h flag.")

    if("!vbot help" in message.lower() or "!vbot h" in message.lower()):
        post_message("VBot Says: \n time(t): tells amount of time until volleyball (in mere seconds) \n cake(c): Makes you a cake! Happy Day! \n insult(i): insults the requester")

    if("!vbot cake" in message.lower() or "!vbot c" in message.lower()):
        make_cake(name)    

    if("!vbot time" in message.lower() or "!vbot t" in message.lower()):
        if (seconds_left < 0):
            seconds_left = 86400 + seconds_left
        post_message(f'VBot Says: There are merely {seconds_left} seconds until Volley Ball!')

    if("!vbot insult" in message.lower() or "!vbot i" in message.lower()):
        post_message(name + ' ' + insults[ (int)(ctime[5]/6) ])