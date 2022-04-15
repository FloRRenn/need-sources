from discord.ext import commands
import asyncio
from discord_components import *
from .Ultils.Guilds_Ultils import getLanguage
from .Ultils.Language import lengthError, Feedback, FeedbackError

class GuildsInfo(commands.Cog):
    def __init__(self, bot) -> None:
        self.bot = bot
        
    @commands.command(aliases = ['t'])
    @commands.has_permissions(administrator = True, manage_channels = True, manage_guild = True)
    async def tell(self, ctx, id : str, *, content):
        listID = id.split(',')
        
        for ID in listID:
            channel = self.bot.get_channel(int(ID))
            await channel.send(content)
            await channel.send('Gõ **s.rep <tin nhắn>** để rep lại')
            await ctx.send(f'Đã gửi tin nhắn đến channel **{channel.name}**')
        
    @commands.command(aliases = ['rep', 'ib', 'rp', 'report', 'feedback', 'feed', 'f', 'fb'])
    @commands.cooldown(3, 7200, commands.BucketType.guild)
    async def reply(self, ctx, *, content : str = ''):
        myID = '<@660730514533122049>'
        LANGUAGE = await getLanguage(ctx.message.guild.id)
        
        if len(content) < 2:
            await ctx.send(FeedbackError(LANGUAGE))
            return
            
        Replychannel = self.bot.get_channel(912961538090999848)
        if len(content) > 2000:
            await ctx.send(lengthError(LANGUAGE))
            return
        
        await Replychannel.send(f'{myID}```{ctx.author} từ {ctx.message.channel.name} - {ctx.message.channel.id} ({ctx.message.guild.name} - {ctx.message.guild.id})```')
        await Replychannel.send(f'{content}')
        await ctx.send(Feedback(LANGUAGE))
        
    @commands.command()
    @commands.has_permissions(administrator = True, manage_channels = True, manage_guild = True)
    async def CreateInvite(self, ctx, channelID : int):
        channel = self.bot.get_channel(channelID)
        link = await channel.create_invite(xkcd = True, max_age = 0, max_uses = 0)
        await ctx.send(link)
        
    @commands.command()
    @commands.has_permissions(administrator = True, manage_channels = True, manage_guild = True)
    async def listGuilds(self, ctx):
        message = ""
        for guild in self.bot.guilds:
            if len(message) <= 1980:
                pass
                
            else:
                await ctx.send(message)
                message = ''
                
            message += f"{guild.name} - {guild.id}\n"
        
        await ctx.send(message)
        
    @commands.command()
    @commands.has_permissions(administrator = True, manage_channels = True, manage_guild = True)
    async def getChannelID(self, ctx, guildID : int):
        message = ""
        guild = self.bot.get_guild(guildID)
        for channel in guild.channels:
            if len(message) <= 1800:
                pass
                
            else:
                await ctx.send(message)
                message = ''
                
            message += f"{channel.name} - {channel.id}\n"
                    
        await ctx.send(message)
        
    @commands.command()
    @commands.has_permissions(administrator = True, manage_channels = True, manage_guild = True)
    async def leaveSV(self, ctx, guildID : int):
        try:
            toleave = self.bot.get_guild(guildID)
            
            await ctx.send(f'Bạn có chắc sẽ để tui rời khỏi server `{toleave.name}` không? Y/N')
            try:
                mess =  await self.bot.wait_for('message', check=lambda message: message.author == ctx.author, timeout = 30)
            except asyncio.TimeoutError:
                await ctx.send(f'Hủy quá trình rời khỏi server `{toleave.name}`')
                return
                
            if mess.content.lower() == 'y':
                await toleave.leave()
                await ctx.send(f'Đã rời khỏi server `{toleave.name}`')
                
            else:
                await ctx.send(f'Hủy quá trình rời khỏi server `{toleave.name}`')
                
        except Exception as e:
            await ctx.send(f'Lỗi\n{e}')
        
def setup(bot):
    bot.add_cog(GuildsInfo(bot))