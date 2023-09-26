import discord
import json

# load config.json 
config_file = open('config.json', encoding="utf8")
config = json.load(config_file)


intents = discord.Intents.default()
intents.message_content = True
intents.members = True

client = discord.Client(intents=intents)


server_id = config['server_id']  # your server id for check user
text_channel = config['text_channel_id']  # text channel to send message


@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')
        
        
@client.event
async def on_message(message):
    # block bot message
    if message.author.bot:
        return
    
    # check message is on the bot DM
    if isinstance(message.channel, discord.DMChannel):   
        user_id = message.author.id
        # guild server
        server = client.get_guild(server_id) 
        
        # check members are in the server or not
        if server.get_member(user_id) is not None:        
            # member DM link
            dm_link = f"https://discord.com/channels/@me/DMs/{user_id}"
            
            channel = client.get_channel(text_channel)
            #  make embed for send user link
            embed = discord.Embed()
            embed.description = f" \n `author:` [{message.author}]({dm_link})"
            
            # send member message in text channel
            await channel.send(f" `content:` {message.content} ", embed=embed)
            # send waiting message to members 
            await message.reply(config['reply_message'])
            
        else:
            await message.reply(config['not_joined_server'])

client.run(config['bot_token'])
