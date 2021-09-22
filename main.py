import os
import discord
import requests
import json
import random
from replit import db
from keep_alive import keep_alive

my_bot_token = os.environ['BOT_TOKEN']

client = discord.Client()

sad_words = ['sad', 'unhappy', 'cry', 'depress', 'miserable',
'bad', 'blue', 'brokenheart', 'cast down', 'crestfall', 'deject',  'despondent', 'disconsolate', 'doleful', 'down', 'downcast', 'downheart', 'down in the mouth', 'droopy', 'forlorn', 'gloomy', 'glum', 'hangdog', 'heartbr', 'heartsick', 'heartsore', 'heavyheart', 'inconsolable', 'joyless', 'low', 'low-spirit', 'melancholic', 'melancholy', 'miserable', 'mournful', 'sorrowful', 'sorry', 'woebegone', 'woeful', 'wretched']

starter_encouragements = [
  'Cheer up! The world has enough sadness already.',
  'Hang in there. Everybody has weaknesses.',
  'You are a great person! Dont let strangers describe your worth.',
  'Dont worry, everything will be alright!',
  "You make me unbelievably proud, today and every day.",
  "You're amazing and that will never change, no matter what happens today.",
  "Remember: You've worked hard for this, and you couldn't be more prepared if you tried.",
  "I would wish you good luck, but I know you don't need it.",
  "A diamond is just a lump of coal that did well under pressure. You've got this!",
]

if "responding" not in db.keys():
  db["responding"] = True

def get_quote():
  response = requests.get("https://zenquotes.io/api/random")
  json_data = json.loads(response.text)
  quote = json_data[0]['q'] + " -" + json_data[0]['a']
  return quote

# def update_encouragements(encg_msg):
#   if "encouragements" in db.keys():
#     encourgements = db["encouragements"]
#     encourgements.append(encg_msg)
#     db["encouragements"] = encourgements
#   else:
#     db["encouragements"] = [encg_msg]

# def delete_encouragements(index):
#   encouragements = db["encouragements"]
#   if len(list(encouragements)) > index:
#     del encouragements[index]
#     db["encouragements"] = encouragements


@client.event
async def on_ready():
  print('I have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
  if message.author == client.user:
    return
  
  if message.content.startswith('*hello'):
    await message.channel.send("Hi, I'm a bot created by Master Cyrus: The Motivation Bot!")

  if message.content.startswith("*motivate"):
    quote = get_quote()
    await message.channel.send(quote)
  
  if db["responding"]:
    options = starter_encouragements
    # if "encouragements" in db.keys():
    #   options.append(db["encouragements"])

    if any(word in message.content for word in sad_words):
        await message.channel.send(random.choice(options))

  # if message.content.startswith('*new'):
  #   encg_msg = str(message.content.split('*new ', 1)[1].value)
  #   update_encouragements(encg_msg)
  #   await message.channel.send('New motivating message added!')

  # if message.content.startswith('*delete'):
  #   if message.author.name != 'Cy':
  #     await message.channel.send('You are not my master :/')
  #     return

  #   encouragements = []
  #   if "encouragements" in db.keys():
  #     index = int(message.content.split('*delete', 1)[1])
  #     delete_encouragements(index)
  #     encouragements = str(db["encouragements"].value)
  #   await message.channel.send(encouragements)

  # if message.content.startswith('*list'):
  #   eng = []
  #   if "encouragements" in db.keys():
  #     eng = str(db["encouragements"].value)
  #   await message.channel.send(eng)

  if message.content.startswith('*responding'):
    # if message.author.name != 'Cy':
    #   await message.channel.send('You are not my master :/')
    #   return 

    value = message.content.split('*responding ', 1)[1]
    if value.lower() == 'true':
      db['responding'] = True
      await message.channel.send('I will respond to sad words.')
    elif value.lower() == 'false':
      db['responding'] = False
      await message.channel.send('I will not respond to sad words.')


  if 'thank' in message.content:
   await message.channel.send('I only helped you because you have a HUGE ass ;)')

keep_alive()

client.run(my_bot_token)
