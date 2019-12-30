import os
from twitchio.ext import commands
import srcomapi, srcomapi.datatypes as dt

game_name = "dave mirra freestyle bmx 2"
# set up the bot
TMI_TOKEN=""
CLIENT_ID=""
BOT_NICK=""
BOT_PREFIX="!"
CHANNEL=""
bot = commands.Bot(
    irc_token=TMI_TOKEN,
    client_id=CLIENT_ID,
    nick=BOT_NICK,
    prefix=BOT_PREFIX,
    initial_channels=[CHANNEL]
)
def convert(seconds): 
    seconds = seconds % (24 * 3600) 
    hour = seconds // 3600
    seconds %= 3600
    minutes = seconds // 60
    seconds %= 60
      
    return "%d:%02d:%02d" % (hour, minutes, seconds) 

api = srcomapi.SpeedrunCom()
_ = api.search(srcomapi.datatypes.Game, {"name": game_name})
game = _[0]
try:
    gxpro = convert(game.records[0].runs[0]['run'].times['primary_t'])
except IndexError:
    gxpro = "N/A"

try:
    pspro = convert(game.records[1].runs[0]['run'].times['primary_t'])
except IndexError:
    pspro = "N/A"

@bot.event
async def event_ready():
    ws = bot._ws  # this is only needed to send messages within event_ready
    await ws.send_privmsg(CHANNEL, f"/me is online!")

@bot.event
async def event_message(ctx):
    """
    checks for ! commands
    """

    # make sure the bot ignores itself and the streamer
    # if ctx.author.name.lower() == "{}".format(BOT_NICK).lower():
    #     return

    await bot.handle_commands(ctx)


@bot.command(name='wr')
async def dm2wr(ctx):
    await ctx.send('GCN/XBOX All Pro WR is {}'.format(gxpro))
    await ctx.send('PS2 All Pro WR is {}'.format(pspro))

if __name__ == "__main__":
    bot.run()
