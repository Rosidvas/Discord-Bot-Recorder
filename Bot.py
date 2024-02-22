
# installed Discord
import discord
from discord import app_commands
from  Recording import recordVoiceChat

intents = discord.Intents.default()
intents.message_content = True
guild_ids = [1030746627113230367]

class MyClient(discord.Client):
    
    def __init__(self, intents):
        super().__init__(intents=intents)
        self.tree = app_commands.CommandTree(self)

    async def on_ready(self):

        for guild_id in guild_ids:
            await self.tree.sync(guild=discord.Object(id=guild_id))
        print(f'Logged on as {self.user}!')

    async def on_message(self, message):
        user = message.author
        await self.reply_message(message, user) 
        print(f'Message from {user.nick}: {message.content}')

    async def reply_message(self, message, user):  
        if user.bot:
            return
                  
        response = acquireResponse(message.content, user) 
        await message.channel.send(response)
        
    async def join_voice(self, message):
        user = message.user
        if user.voice:
            channel = user.voice.channel
            voice_client = await channel.connect()

            return voice_client
        else:
            await message.channel.send("You need to be in a voice channel to use this command.")
            return None 
        
client = MyClient(intents=intents)

def acquireResponse(message, user):
        
    return f"Your message was recorded {user.nick}"

### Join the voicechat and records the convo 
@client.tree.command(name = "record-voice", description = "joins call and records it", guild=discord.Object(id=1030746627113230367))
async def joinVoice(interaction): 
    user = interaction.user

    if user.name != "jeffrey6487":
        await interaction.response.send_message("You are not permitted to record")
        return

    onCall = await client.join_voice(interaction)

    if onCall:
        await interaction.response.send_message("Joined voice channel.")
        ## Recording Audio
        output_file = "recorded_audio.wav"
        await recordVoiceChat(onCall, output_file, duration=60)
    else:
        await interaction.response.send_message("Command unsuccessful")


### Leaves the Voice call
@client.tree.command(name = "leave-voice", description = "ends voice recording", guild=discord.Object(id=1030746627113230367))
async def leaveVoice(context): 
    voice_client = discord.utils.get(client.voice_clients, guild=context.guild)
    user = context.user

    if user.name != "jeffrey6487":
        await context.response.send_message("You are not permitted to stop the recording")
        return
    
    if voice_client and voice_client.is_connected():
        await voice_client.disconnect()
        await context.response.send_message("Left voice channel.")
    else:
        await context.response.send_message("The bot is not connected to a voice channel.")


client.run('') # 💪💪💪 Token here


    


