"""
Sample Parrot Bot

This bot responds to any message by repeated what was said to it. 
"""
__name__ = 'localConfig'
__package__ = 'ringcentral_bot_framework'

import copy
import json
from functools import reduce

def reducer(x, y):
  '''@user reducer'''
  st = f'![:Person]({y}) '
  return f'{x}{st}'

def hello():
  return 'Hello, I am a @all bot. Please post any message with "@all" if you want to @all.'

def botJoinPrivateChatAction(bot, groupId, user, dbAction):
  """
  This is invoked when the bot is added to a chat group.
  """
  bot.sendMessage(
    groupId,
    {
      'text': hello()
    }
  )

def botGotPostAddAction(
  bot,
  groupId,
  creatorId,
  user,
  text,
  dbAction,
  handledByExtension
):
  """
  This is invoked when the user sends a message to the bot.
  """
  if handledByExtension:
    return

  if '@all' in text:
    r = bot.rc.get(f'/restapi/v1.0/glip/groups/{groupId}')
    txt = json.loads(r.text)
    at = reduce(reducer, txt['members'], '')
    stripped = text.replace(f'@all', '')
    text = f'''{stripped}

{at}

-------------
You can do @all by post message with "@all".
-------------
'''
    bot.sendMessage(
      groupId,
      {
        'text': text
      }
    )
  elif f'![:Person]({bot.id})' in text:
    bot.sendMessage(
      groupId,
      {
        'text': hello()
      }
    )
