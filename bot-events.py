import json

import discord

import config
from config import settings


client = discord.Client()


# The function prints once client is getting started.
@client.event
async def on_ready():
    print('Client was started!')


# The function makes something when user sends a message.
@client.event
async def on_message(message):
    with open('data.json', mode='r') as file:
        data = json.load(file)

    client_id = str(message.author.id)

    # The function checks users in 'data' variable.
    async def update_data(user):
        if user not in data:
            data[user] = {}
            data[user]['money'] = 100
            data[user]['property'] = []
            data[user]['lvl'] = 1
            data[user]['exp'] = 0

    # The function gives exp to users, when they send messages.
    async def add_exp(user):
        data[user]['exp'] += 0.1

    # The function gives a new level once exp reaches new level-milestone.
    async def add_lvl(user):
        if data[user]['exp'] >= data[client_id]['lvl']:
            data[user]['exp'] = 0
            data[user]['lvl'] += 1
            emb = discord.Embed(description=f'{message.author} Повысил свой уровень!', color=0xf2db0a)
            await message.channel.send(embed=emb)

    await update_data(client_id)
    await add_exp(client_id)
    await add_lvl(client_id)

    with open('data.json', mode='w') as file:
        json.dump(data, file)


# The function gives a role once user gives a reaction.
@client.event
async def on_raw_reaction_add(payload: discord.RawReactionActionEvent):
    message_id = payload.message_id

    if message_id == config.POST_ID:
        guild_id = payload.guild_id
        guild = discord.utils.find(lambda g: g.id == guild_id, client.guilds)

        role = discord.utils.get(guild.roles, id=config.roles[payload.emoji.name])

        if role:
            member = payload.member
            if member:
                await member.add_roles(role)
                print(f'{member.display_name} had role: {role}')
            else:
                print('Member not found')
        else:
            print('Role not found')
    else:
        pass


# The function takes the role back once user unclicks the reaction.
@client.event
async def on_raw_reaction_remove(payload: discord.RawReactionActionEvent):
    message_id = payload.message_id

    if message_id == config.POST_ID:
        guild_id = payload.guild_id
        guild = discord.utils.find(lambda g: g.id == guild_id, client.guilds)

        role = discord.utils.get(guild.roles, id=config.roles[payload.emoji.name])
        member = await (await client.fetch_guild(payload.guild_id)).fetch_member(payload.user_id)

        if role:
            if member:
                await member.remove_roles(role)
                print(f'{member.display_name} removed role: {role}')
            else:
                print('Member not found')
        else:
            print('Role not found')
    else:
        pass

client.run(settings['token'])
