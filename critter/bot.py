# Bot that does Critter actions to test the system

import urllib.request
import random

SERVER = 'http://127.0.0.1:5000'

class Action():
    def do(self):
        print('Undefined action')

class Get(Action):
    def do(self):
        print('Fetching index.html...')
        urllib.request.urlopen(SERVER).read()

class Bot():
    def __init__(self):
        self.actions = [Get()]
        self.weights = [1.0]
    def doAction(self):
        random.choices(self.actions, weights=self.weights)[0].do()

if __name__ == '__main__':
    bot = Bot()
    while True:
        bot.doAction()