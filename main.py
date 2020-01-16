import discord
import json
from discord.ext import commands
from datetime import datetime

class UwuThursday(commands.Bot):
	def __init__(self):
		with open("config.json", "r") as file:
			json_file = json.loads(file.read())
			self.token = json_file["token"]
			self.prefix = json_file["prefix"]
			self.owner_id = json_file["owner_id"]
			self.founder_id = json_file["founder_id"]

		self.uwu = {}
		super().__init__(command_prefix=self.prefix, description=f'I\'m a meme bot to count each time someone "uwu\'s" in the chat. But with a little twist, it\'s only allowed on thursdays.')

	async def on_ready(self):
		await self.change_presence(activity=discord.Activity(name="uwu!", type=3))

		if not self.uwu:
			self.prepare_list()

		self._owner = self.get_user(self.owner_id)
		self._founder = self.get_user(self.founder_id)

		print(f"Logged in as {self.user}\nServing {len(self.users)} users and {len(self.guilds)} guilds.")

	async def on_guild_join(self, guild: discord.Guild):
		self.uwu[guild.id] = []

	async def on_guild_remove(self, guild: discord.Guild):
		del self.uwu[guild.id]

	async def on_message(self, message: discord.Message):
		if message.author == self.user or not self.is_ready():
			return

		if message.content in [f"<@!{self.user.id}>", f"<@{self.user.id}>"]:
			await message.channel.send(f"Hey, i'm {self.user.name} my prefix is `{self.prefix}`.\n{self.description}")

		elif message.created_at.strftime("%A") == "Thursday":				
			if message.content.lower() == "uwu":
				if message.author.id not in self.uwu[message.guild.id]:
					await message.channel.send("Successfully uwu'd today!", delete_after=2.5)
					self.uwu[message.guild.id] == self.uwu[message.guild.id].append(message.author.id)
				else:
					await message.channel.send(f"{message.author} already uwu'd today.", delete_after=2.5)

		elif message.created_at.strftime("%A") == "Friday":
			self.uwu = {}
			self.prepare_list()

		await self.process_commands(message)

	def run(self):
		self.load_extension("libneko.extras.superuser")
		super().run(self.token)

	def prepare_list(self):
		for guild in self.guilds:
			self.uwu[guild.id] = []

	@property
	def owner(self):
		return self._owner or self.get_user(self.owner_id)

	@property
	def founder(self):
		return self._founder or self.get_user(self.founder_id)	
		
bot = UwuThursday()

@bot.command()
async def about(ctx: commands.Context):
	"""Information about this bot"""
	owner = bot.owner
	founder = bot.founder

	embed = discord.Embed(color=discord.Color.blurple(), description=bot.description)
	embed.set_author(name=bot.user.name, icon_url=bot.user.avatar_url_as(static_format="png"))
	embed.add_field(name="Mentions:", value=f"{owner.mention} | Bot Creator\n{founder.mention} | Idea source")

	await ctx.send(embed=embed)

@bot.command()
async def count(ctx: commands.Context):
	"""Uwu count per guild"""
	if bot.uwu.get(ctx.guild.id, None):
		await ctx.send(f"`{len(bot.uwu[ctx.guild.id])}` {'person' if len(bot.uwu[ctx.guild.id]) == 1 else 'people'} uwu'd today.")
	else:
		await ctx.send("Nobody uwu'd today. 😟")	

@bot.command()
@commands.is_owner()
async def kys(ctx: commands.Context):
	"""Kills the bot"""
	await ctx.message.add_reaction("👌")
	await bot.logout()

bot.run()