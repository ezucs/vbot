import json
import time
import random
import requests
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
from vbot import post_message
from vbot import read_message
from vbot import get_nickname

def adventure_game():
