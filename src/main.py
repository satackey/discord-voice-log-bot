import discord
import asyncio
import configparser

server_channels = {} # Server channel cache
client = discord.Client()

config = configparser.ConfigParser()
config.read('config.ini')

channel_name = config.get('Attributes', 'CHANNEL_NAME')
BOT_TOKEN = config.get('Attributes', 'BOT_TOKEN')


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
async def on_ready():
    print('\nLogged in as')
    print(client.user.name)
    print(client.user.id)
    print('\n')


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
        # No change
        return

    if voice_channel_before is None:
        # The member was not on a voice channel before the change
        # Discord api sets voice_channel to None if there was no channel to begin with.
        msg = "**%s#%s** joined voice channel **_%s_**" % (member.name, member.discriminator, voice_channel_after.name)
    else:
        # The member was on a voice channel before the change
        if voice_channel_after is None:
            # The member is no longer on a voice channel after the change
            msg = "**%s#%s** left voice channel **_%s_**" % (member.name, member.discriminator, voice_channel_before.name)
        else:
            # The member is still on a voice channel after the change
            msg = "**%s#%s** switched from voice channel **_%s_** to **_%s_**" % (member.name, member.discriminator,
                                                                     voice_channel_before.name, voice_channel_after.name)
    
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
