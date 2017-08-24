# -*- coding: utf-8 -*-
"""
Created on Thu Aug 24 19:22:07 2017

Get informations from a payload
@author: Darkness4
"""


def get_round_phase(payload):
    """Get round phase"""
    if 'round' in payload and 'phase' in payload['round']:
        return payload['round']['phase']


def get_state(payload):
    """Get player status"""
    if 'player' in payload and 'state' in payload['player']:
        return {'health': payload['player']['state']['health'],
                'armor': payload['player']['state']['armor'],
                'round_kills': payload['player']['state']['round_kills'],
                'round_killhs': payload['player']['state']['round_killhs'],
                'money': payload['player']['state']['money']}


def get_bomb(payload):
    """Get bomb status"""
    if 'round' in payload and 'bomb' in payload['round']:
        return payload['round']['bomb']
