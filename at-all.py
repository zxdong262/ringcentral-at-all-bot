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
  txt = bot.rc.get(f'/restapi/v1.0/glip/groups/{groupId}')
  return json.loads(txt.text)

def arraySplit(arr, n):
  len0 = math.ceil(len(arr) / n)
  res = []
  for x in range(len0):
    start = 0 + x * n
    end = 0 + (x + 1) * n
    arr0 = arr[start:end]
    res.append(arr0)
  return res

def removeBots(bot, members, creatorId):
  ids = members
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

  return arraySplit(filtered, 90)

def hello():
  return 'Hello, I am @all bot. Please post any message with "@all" or "#all" if you want to @all.'

def hasAtAll(txt, ref):
  reped = txt.replace(ref, '').strip()
  if len(reped) > 0 and ref in txt:
    return True
  arr = txt.split('\n')
  for x in arr:
    if not x.startswith('> ') and ('@all' in x or '#all' in x):
      return True
  return False

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
  handledByExtension,
  event
):
  """
  This is invoked when the user sends a message to the bot.
  """
  if handledByExtension:
    return
  if text is None:
    text = ''
  ref = f'![:Person]({bot.id})'
  if hasAtAll(text, ref):
    txt = fetchGroupInfo(bot, groupId)
    ids = removeBots(bot, txt['members'], creatorId)
    len0 = len(ids)
    rest = '''
-------------
You can do @all by post message with "@all" or "#all".
'''
    stripped = text.replace(f'@all', '').replace(f'#all', '').replace(ref, '').strip()
    for x in range(len0):
      ids0 = filter(lambda ss: not ss == creatorId, ids[x])
      at = reduce(reducer, ids0, '').strip()
      text = f'''![:Person]({creatorId}) says:
{stripped}
{at}
'''
      if x == len0 - 1:
        text = f'{text}{rest}'
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
