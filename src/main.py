import discord
from discord import *
from discord.ext import commands
import configparser

server_channels = {} # Server channel cache
# client = discord.Client()

config = configparser.ConfigParser()
config.read('config.ini')

channel_name = config.get('Attributes', 'CHANNEL_NAME')
BOT_TOKEN = config.get('Attributes', 'BOT_TOKEN')
PLAYING_GAME = config.get('Attributes', 'PLAYING_GAME')

BOT_PREFIX = '~~'

# Setting the bot's prefix to $
client = commands.Bot(command_prefix=BOT_PREFIX)

# For custom help command, remove the existing one.
client.remove_command('help')


class Main_Commands():

    def __init(self, client):
        self.client = client


@client.event
async def on_ready():
    await client.change_presence(activity=Game(name=PLAYING_GAME))
    print('\nLogged in as')
    print(client.user.name)
    print('\n')


@client.command(pass_context=True)
async def help(ctx):

    embed = discord.Embed(colour=discord.Colour.red())

    embed.set_author(
        name="This bot was created for the sole purpose of event-logging,\n"
             "Original author:  Beskhue\nForked by: briansukhnandan\n"
             '\nAdmins: Set up a text-channel named "voice-log". \n'
             "Obviously give the Bot permissions to access the channel if necessary. \n")

    await ctx.send(embed=embed)


def find_channel(channel_object, refresh = False):
    """
    Find and return the channel to log the voice events to.
    
    :param channel_object: A Channel Object to search for and return.
    :param refresh: Whether to refresh the channel cache for this server.
    """

    # If we aren't refreshing server cache and our specified server
    if not refresh and channel_object in server_channels:
        return server_channels[channel_object]
        
    for channel in client.get_all_channels():
        if channel.guild == channel_object and channel.name == channel_name:
            print("%s: refreshed destination log channel" % channel.guild)
            server_channels[channel_object] = channel
            return channel
            
    return None

@client.event
async def on_member_update(before, after):
    print(before, after)

@client.event
async def on_voice_state_update(member, member_before_voice_state, member_after_voice_state):
    """
    Called when the voice state of a member on a server changes.
    
    :param member: The member object that triggered some sort of activity.
    :param member_before_voice_state: The voice state prior to the changes.
    :param member_after_voice_state: The voice state after to the changes.
    """
    server = member.guild
    channel = find_channel(server)
    
    voice_channel_before = member_before_voice_state.channel
    voice_channel_after = member_after_voice_state.channel
    
    if voice_channel_before == voice_channel_after:
        if member_before_voice_state.self_deaf != member_after_voice_state.self_deaf:
            changed_after = 'deafened' if member_after_voice_state.self_deaf else 'undeafened'
            await channel.send(f"{member.mention} {changed_after} theirself")
            return

        if member_before_voice_state.self_mute != member_after_voice_state.self_mute:
            changed_after = 'muted' if member_after_voice_state.self_mute else 'unmuted'
            await channel.send(f"{member.mention} {changed_after} theirself")
            return
        return

    if voice_channel_before is None:
        print(voice_channel_after)
        # The member was not on a voice channel before the change
        # Discord api sets voice_channel to None if there was no channel to begin with.
        msg = "%s joined voice channel <#%s>" % (member.mention, voice_channel_after.id)
    else:
        # The member was on a voice channel before the change
        if voice_channel_after is None:
            # The member is no longer on a voice channel after the change
            msg = "%s left voice channel <#%s>" % (member.mention, voice_channel_before.id)
        else:
            # The member is still on a voice channel after the change
            msg = "%s switched from voice channel <#%s> to <#%s>" % (member.mention, voice_channel_before.id, voice_channel_after.id)
    
    # Try to log the voice event to the channel
    try:
        await channel.send(msg)

    except:
        # No message could be sent to the channel; force refresh the channel cache and try again
        channel = find_channel(server, refresh=True)
        if channel is None:
            # The channel could not be found
            print("Error: channel #%s does not exist on server %s." % (channel_name, server))
        else:
            # Try sending a message again
            try:
                await channel.send(msg)
            except discord.DiscordException as exception:
                # Print the exception
                print("Error: no message could be sent to channel #%s on server %s. Exception: %s" % (channel_name, server, exception))

client.run(BOT_TOKEN)
