import discord
from poker import *
client = discord.Client()
p_guilds = {}
@client.event
async def on_ready(): 
    print('I am ready')
    #intialize all the guilds and guild members
    guilds = client.guilds
    for guild in guilds:
        p_guilds[guild.id] = Guild(guild.members)

@client.event
async def on_message(message):

    if not message.author.bot:    #we don't want a bot to execute any commands on our bot
        content = message.content
        if content.startswith('-'):
            content = content[1:len(content)] #slice of prefix
            args = content.split(' ')
            cmd = args.pop(0).lower() #cmd is first arg after prefix
        
            if cmd == 'create': #first we identify the guild object Then we use that guild object
                guild = p_guilds[message.guild.id]
                await guild.create(message,args)

            elif cmd == 'join': #first we identify lobby object
                name = ' '.join(args)
                if name in p_guilds[message.guild.id].lobbies:
                    lobby = p_guilds[message.guild.id].lobbies[name]
                    await lobby.join(message)

                else:
                    await message.channel.send('That is an invalid lobby name')

            elif cmd == 'leave': #first we find out if the subject is in a llobby and which one
                lobby = await get_lobby_by_member(message,p_guilds)
                if lobby:
                    await lobby.leave(message)

                else:
                    await message.channel.send("You are not in a lobby")
            
            elif cmd == 'close': #we find if subject is in lobby and which one
                lobby = await get_lobby_by_member(message, p_guilds)
                if lobby:
                    await lobby.close(message)

                else:
                    await message.channel.send('You are not in a lobby')
            
            elif cmd == 'open':
                lobby = await get_lobby_by_member(message, p_guilds)
                if lobby:
                    await lobby.open(message)

                else:
                    await message.channel.send('You are not in a lobby')         
            elif cmd == 'invite':
                lobby = await get_lobby_by_member(message, p_guilds)
                if lobby:
                    await lobby.invite(message)

                else:
                    await message.channel.send('You are not in a lobby') 
            
            elif cmd == 'kick':
                lobby = await get_lobby_by_member(message, p_guilds)
                if lobby:
                    await lobby.open(message)

                else:
                    await message.channel.send('You are not in a lobby') 
            
client.run('')