from rlcard.games.blackjack import *
from rlcard.envs.env import Env
from rlcard.games.blackjack.game import BlackjackGame as Game
from rlcard.utils.utils import * 
import numpy as np

import random

class BlackjackEnv(Env):
    """
    Blackjack Environment
    """

    def __init__(self):
        ''' Initialize the Blackjack environment
        '''
        super().__init__(Game())
        self.rank2score = {"A":10, "2":2, "3":3, "4":4, "5":5, "6":6, "7":7, "8":8, "9":9, "10":10, "J":10, "Q":10, "K":10}
        self.actions = ['hit', 'stand']

    def get_actions(self):
        ''' Get all of available actions

        Returns:
            encoded_action_list (list): return encoded action list (from str to int)
        '''
        return self.encode_action(self.actions)

    def extract_state(self, state):
        ''' Extract the state representation from state dictionary for agent
        
        Args:
            state (dict): Original state from the game

        Returns:
            observation (list): combine the player's score and dealer's observable score for observation
        '''
        cards = state['state']
        my_cards = cards[0]
        dealer_cards = cards[1]

        def get_scores_and_A(hand):
            score = 0
            has_a = 0
            for card in hand:
                score += self.rank2score[card[1:]]
                if card[1] == 'A':
                    has_a = 1
            if score > 21 and has_a == 1:
                score -= 9
            return score, has_a

        my_score, has_a = get_scores_and_A(my_cards)
        dealer_score, _ = get_scores_and_A(dealer_cards)
        obs = [my_score, dealer_score]
        return obs

    def encode_action(self, actions):
        ''' Encode the action into action ids
            
        Args:
            actions (list[str]): list of actions

        Returns:
            encoded_actions (list[int]): list of action ids
        '''
        a = []
        for i, act in enumerate(actions):
            a.append(i)
        return a

    def get_payoffs(self):
        '''Get the payoff of a game 

        Returns:
           payoffs (list): list of payoffs 
        '''
        if self.game.winner['player'] == 0 and self.game.winner['dealer'] == 1:
            return [-1]
        elif self.game.winner['dealer'] == 0 and self.game.winner['player'] == 1:
            return [1]
        elif self.game.winner['player'] == 1 and self.game.winner['dealer'] == 1:
            return [0]
        else:
            raise "There are some bugs!"
 
    def decode_action(self, action_id):
        '''Decode the action for applying to the game

        Args:
            action id (int): action id

        Returns:
            action (str): action for the game 
        '''
        return self.actions[action_id]
 
