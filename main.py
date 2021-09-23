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

if "bully_mode" not in db.keys():
  db["bully_mode"] = True

if "victim" not in db.keys():
  db["victim"] = "suweshhh"

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
    await message.channel.send("Hi, I'm a bot created by Master Cyrus: The Motivation Bot and I bully people as a side-job! :grin:")

  if message.content.startswith("*motivate"):
    quote = get_quote()
    await message.channel.send(quote)

  #instructions:
  if message.content.startswith('*tips'):
    tips = "WELCOME TO MOTIVATION BOT 2.0 :grin:\n*hello -> say hi to the bot\n*motivate -> get a random motivational quote\n*bully<space>(true/false) -> toggle bully mode\n*responding<space>(true/false) -> toggle response to sad words\n*victim<space>(name) -> bot bullies this person now"
    await message.channel.send(tips)

  #bully toggle----------------------------------------------
  if message.content.startswith('*bully'):
    if message.author.name != 'Cy':
      await message.channel.send('You are not my master, you dumb fuck! :rofl:')
      return 

    value = message.content.split('*bully ', 1)[1]
    if value.lower() == 'true':
      db['bully_mode'] = True
      await message.channel.send('I will bully {}. :stuck_out_tongue: '.format(db["victim"].upper()))
    elif value.lower() == 'false':
      db['bully_mode'] = False
      await message.channel.send('I will not bully {}. :pensive:'.format(db["victim"].upper()))

  #victim setter--------------------------------------------
  if message.content.startswith('*victim'):
    if message.author.name != 'Cy':
      await message.channel.send('You are not my master, you dumb fuck! :joy:')
      return 

    value = message.content.split('*victim ', 1)[1]
    db['victim'] = value.lower()
    await message.channel.send('I will bully {} now. :stuck_out_tongue: '.format(db["victim"].upper()))

  #bully module--------------------------------------------
  if db['bully_mode']:
    if message.author.name.lower() == db["victim"]:
      await message.channel.send('shut up {} you dumb fuck i wont listen to you :joy:'.format(db["victim"].upper()))
      return
 
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

   
  #responding toggle---------------------------------------
  if message.content.startswith('*responding'):
    if message.author.name != 'Cy':
      await message.channel.send('You are not my master, you dumb fuck! :joy:')
      return 

    value = message.content.split('*responding ', 1)[1]
    if value.lower() == 'true':
      db['responding'] = True
      await message.channel.send('I will respond to sad words. :+1:')
    elif value.lower() == 'false':
      db['responding'] = False
      await message.channel.send('I will not respond to sad words. :-1:')
  
  #tagging module------------------------------------------
  if message.content.startswith('*tag'):
    value = message.content.send()
#thanks module------------------------------------------------
  if 'thank' in message.content:
   await message.channel.send('Mention not! I only helped you because you have a HUGE ass :wink:')

keep_alive()

client.run(my_bot_token)
