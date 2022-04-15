from discord.ext import commands
from discord_components import *
import discord, traceback
from re import findall
import difflib

from .Ultils.Guilds_Ultils import limitUasgeDefault, getLanguage
from .Ultils.Language import CommandNotFoundMess, BadArgumentMess \
                            , MissingRequiredArgumentMess, MissingPermissionsMess \
                            , CommandOnCooldownMEss, NoPrivateMessageMess \
                            , NSFWChannelRequiredMess, UnknownErrorMess, TryAgain

class OnEvent(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        show = discord.Embed(title = 'Tui vừa vào một server mới', colour = 0xF39C12)
        show.add_field(name = 'Tên server', value = guild.name, inline = True)
        show.add_field(name = 'ID server', value = guild.id, inline = True)
        show.add_field(name = 'Số lượng thành viên', value = guild.member_count, inline = True)

        await limitUasgeDefault(guild.id, guild.name, guild.member_count)
        channel = self.bot.get_channel(920264636052410398)
        await channel.send(embed = show)
        
    @commands.Cog.listener()
    async def on_guild_remove(self, guild):
        show = discord.Embed(title = 'Tui vừa bị đá ra khỏi 1 server', colour = 0xFF0000)
        show.add_field(name = 'Tên server', value = guild.name, inline = True)
        show.add_field(name = 'ID server', value = guild.id, inline = True)
        show.add_field(name = 'Số lượng thành viên', value = guild.member_count, inline = True)
        
        channel = self.bot.get_channel(920264636052410398)
        await channel.send(embed = show)
        
    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        LANGUAGE = await getLanguage(ctx.message.guild.id)
        
        if isinstance(error, commands.CommandNotFound):
            wrongname = findall('/"+[a-zA-Z0-9]+/"', error.args[0])
            print(wrongname)
            await ctx.reply(CommandNotFoundMess(LANGUAGE))
            
        elif isinstance(error, commands.BadArgument):
            await ctx.reply(BadArgumentMess(LANGUAGE))
            
        elif isinstance(error, commands.MissingRequiredArgument):
            await ctx.reply(MissingRequiredArgumentMess(LANGUAGE))
            
        elif isinstance(error, commands.CommandOnCooldown):
            await ctx.reply(CommandOnCooldownMEss(error.retry_after, LANGUAGE))   
            
        elif isinstance(error, commands.NoPrivateMessage):
            await ctx.reply(NoPrivateMessageMess(LANGUAGE))
            
        elif isinstance(error, commands.NSFWChannelRequired):
            await ctx.reply(NSFWChannelRequiredMess(LANGUAGE))
            
        elif isinstance(error, commands.MissingPermissions):
            await ctx.reply(MissingPermissionsMess(LANGUAGE))
            
        else:
            if 'fewer in length.' in str(error):
                await ctx.reply(TryAgain(LANGUAGE))
            else:
                await ctx.reply(UnknownErrorMess(LANGUAGE))
            
            channel = self.bot.get_channel(909404622278520872)
            myID = '<@660730514533122049>'
            content = f'{myID}, lỗi xuất hiện tại server **{ctx.message.guild.name} (ID: {ctx.message.guild.id})** trong kênh **{ctx.message.channel.name} (ID: {ctx.message.channel.id})** từ **{ctx.author}**\nError Type: {error.__class__.__name__}'
            await channel.send(content)
            await channel.send(error)
                
            try:
                await channel.send(traceback.format_exc())
            except:
                pass
            
def setup(bot):
    bot.add_cog(OnEvent(bot))  