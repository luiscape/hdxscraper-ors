#!/usr/bin/python
# -*- coding: utf-8 -*-

from termcolor import colored as color

def item(i):
  '''Adding formatting elements to stdout.'''
  dictionary = {
    'prompt_bullet': color(" →", "blue", attrs=['bold']),
    'prompt_error':  color(" ERROR:", "red", attrs=['bold']),
    'prompt_success': color(" SUCCESS:", "green", attrs=['bold']),
    'bullet_red': color(" →", "red", attrs=['bold']),
    'bullet_green': color(" →", "green", attrs=['bold']),
  }
  return dictionary[i]