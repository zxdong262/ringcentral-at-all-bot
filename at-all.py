"""
Sample Parrot Bot

This bot responds to any message by repeated what was said to it. 
"""
__name__ = 'localConfig'
__package__ = 'ringcentral_bot_framework'

import copy
import json
import math
from functools import reduce
from requests_toolbelt.multipart import decoder

def reducer(x, y):
  '''@user reducer'''
  st = f'![:Person]({y}) '
  return f'{x}{st}'

def fetchGroupInfo(bot, groupId):
  txt = bot.rc.get(f'/restapi/v1.0/glip/chats/{groupId}')
  return json.loads(txt.text)

def removeBots(bot, members):
  ids = list(map(lambda x: x['id'], members))
  size = 30
  len0 = math.ceil(len(ids) / size)
  filtered = []
  for x in range(len0):
    start = 0 + x * size
    end = 0 + (x + 1) * size
    arr = ids[start:end]
    idsStr = ','.join(arr)
    res = bot.rc.get(f'/restapi/v1.0/glip/persons/{idsStr}')
    multipart_data = decoder.MultipartDecoder.from_response(res)

    for part in multipart_data.parts:
      user = json.loads(part.text)
      if 'email' in user and not 'bot.glip.net' in user['email']:
        filtered.append(user['id'])

  return filtered

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
    txt = fetchGroupInfo(bot, groupId)
    ids = removeBots(bot, txt['members'])
    at = reduce(reducer, ids, '')
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
