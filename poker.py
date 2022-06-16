import asyncio

class Player():
    def __init__(self, lobby, member):
        self.lobby =lobby
        self.member = member
        self.hand = {}

async def add(member,lobby,guild): #command that adds a player to guild and lobby dictionaries
    player = Player(lobby, member)
    lobby.players[member.id] = player   
    guild.players[member.id] = player
async def get_one(dict):
    for i in dict:
        return i
        
async def get_lobby_by_member(message,p_guilds):
    if message.author.id in p_guilds[message.guild.id].players:
        return p_guilds[message.guild.id].players[message.author.id].lobby
    
class Lobby():
    def __init__(self,leader_id, guild, channel,name):
        self.name = name
        self.channel  = channel#the lobby will only exist in one channel
        self.players = {}
        self.closed = False
        self.leader_id = leader_id
        self.guild = guild
        self.invites = set() #set of ids

    async def join(self, message):
        author_id = message.author.id
        #first we check if the author is already in a game

        if author_id in self.guild.players:
            await message.channel.send('You are already in a lobby')
    
        elif self.closed and not author_id in self.invites:
            await message.channel.send('This lobby is closed. Get an invite in order to join.')
        
        else:
            #we need make a player object and add this to the lobby and guild
            member = self.guild.members[author_id]
            guild = self.guild
            await add(member,self,guild)
            await message.channel.send('You joined "{}"'.format(self.name))
        
    async def leave(self, message):
        author_id = message.author.id
        del self.players[author_id]
        del self.guild.players[author_id]
        if len(self.players) == 0:
            del self.guild.lobbies[self.name] #will this break?

        elif self.leader_id == author_id:
            self.leader_id = await get_one(self.players)

        await message.channel.send('You left "{}"'.format(self.name))
    
    async def close(self, message):
        author_id = message.author.id
        if author_id == self.leader_id:
            self.closed = True
            await message.channel.send('Lobby is now closed')
        
        else:
            await message.channel.send('You are not the lobby owner')
    
    async def open(self, message):
        author_id = message.author.id
        if author_id == self.leader_id:
            self.closed = False
            await message.channel.send('Lobby is now open')
        
        else:
            await message.channel.send('You are not the lobby owner')
    
    async def invite(self,message): # create an invite to a player that lasts for sometime in which a player can join and bypass
        if len(message.mentions) > 0:
            mention = message.mentions[0]
            self.invites.add(mention.id)
            await message.channel.send('Sent an invite to {}'.format(mention.name))
            await asyncio.sleep(15)
            await message.channel.send('Invites have timed out')
            if mention.id in self.invites:
                self.invites.remove(mention.id)

        else:
            await message.channel.send('You need to ping someone')


    async def kick(self,message):
        author_id = message.author.id
        if self.leader_id != author_id:
            await message.channel.send('You do not have the permission to kick')
        
        else:
            if len(message.mentions) > 0:
                mention = message.mentions[0]
                if mention.id == author_id: #if leader is trying to kick himself, deny
                    await message.channel.send(' you can\'t kick yourself')
                elif mention.id in self.players:
                    del self.players[mention.id]
                    del self.guild.players[mention.id]
                    await message.channel.send('Kicked {}'.format(mention.name))
                else:
                    await message.channel.send('{} is not in lobby'.format(mention.name))

            else:
                await message.channel.send('You need to mention someone to kick')
                
class Member():
    def __init__(self,id):
        self.bank = 10000
        self.id = id

class Guild():
    def __init__(self,members):
        self.lobbies = {}
        self.members = {}
        for member in members:
            self.members[member.id] = Member(member.id)
        self.players = {} #we need to easily access whoever is in game and where

    async def create(self,message,args): #creates a lobby
            author_id = message.author.id
            if author_id in self.players:
                await message.channel.send('You are already in a lobby')

            else:
                if len(args) == 0: #if the user has inputted a valid name
                    await message.channel.send('You need to enter a name')
                else:
                    name = ' '.join(args) #we want to use all args in this case
                    if name in self.lobbies:
                        await message.channel.send('A lobby with this name already exists')
                    
                    else:
                        self.lobbies[name] = Lobby(author_id, self, message.channel.id,name)

                        #we also need to make this guy a player, and add him to lobby and guild player dict

                        lobby = self.lobbies[name]
                        member = self.members[author_id]
                        await add(member,lobby,self)
                        await message.channel.send('Successfully created "{}"'.format(name))