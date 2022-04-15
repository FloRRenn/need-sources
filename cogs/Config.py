from discord.ext import commands
import discord
from discord.ext.commands.core import guild_only
from discord_components import *
from .Ultils.Guilds_Ultils import getLanguage, addCommandAllowForChannel, setupLanguage \
                                , deleteCommandAllowForChannel, GetChannelAllowForCommand, checkSauceNAO_API
from .Ultils.Language import SetupCMD, setupSucessful, delCMDMess, SauceNao_checkAPI

class SetUpCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.listCMDname = ['src','anime', 'jav', 'facejp', 'faceus', 'waifu', 'nwaifu','rule34', 'quote', 'code', 'debut', 'henbyid', 'henbytag','booru','nbooru','gelbooru','ngelbooru','danbooru','ndanbooru','konachan','nkonachan','yandere','nyandere']
        
    @commands.guild_only()
    @commands.has_permissions(administrator = True, manage_channels = True, manage_guild = True)
    @commands.command()
    async def setup(self, ctx, cmds : str):
        LANGUAGE = await getLanguage(ctx.message.guild.id)
        
        guild = ctx.message.guild.id
        guildName = ctx.message.guild.name
        channel = ctx.message.channel.id
        channelName = ctx.message.channel.name
        
        listCMD = cmds.split(',')
        successful = []
        
        for cmd in listCMD:
            mess = SetupCMD(cmd, LANGUAGE)
            if cmd in self.listCMDname:
                check = await addCommandAllowForChannel(guild, guildName, channel, channelName,cmd)
                if not check:
                    await ctx.send(mess[0])
                else:
                    successful.append(cmd)
                    
            else:
                await ctx.send(mess[1])
                
        if successful:
            await ctx.send(f'{setupSucessful(successful, LANGUAGE)} {self.bot.get_channel(channel).mention}')
        
    @commands.guild_only()
    @commands.has_permissions(administrator = True, manage_channels = True, manage_guild = True)
    @commands.command(aliases = ['drop'])
    async def delCMD(self, ctx, cmd : str = None):
        guild = ctx.message.guild.id
        channel = ctx.message.channel.id
        LANGUAGE = await getLanguage(guild)
        mess = delCMDMess(LANGUAGE)
        
        if cmd == None or cmd not in self.listCMDname:
            await ctx.send(mess[0])
            return
        
        check = await deleteCommandAllowForChannel(guild, channel, cmd)
        if check:
            await ctx.send(mess[1])
        else:
            await ctx.send(mess[2])
            
    @commands.guild_only()
    @commands.command(aliases = ['manage'])
    async def ManageCommands(self, ctx):
        async with ctx.message.channel.typing():
            guild = ctx.message.guild.id
            show = discord.Embed(color = 0xDEFC01)
            for cmd in self.listCMDname:
                channelID = await GetChannelAllowForCommand(guild, cmd)
                mess = ''
                if channelID:
                    for channel in channelID:
                        channelName = self.bot.get_channel(channel).mention
                        mess += f'{channelName} '
                    show.add_field(name = f'{cmd}', value = mess, inline = True)
                
                else:
                    show.add_field(name = f'{cmd}', value = '`All channels`', inline = True)
            await ctx.send(embed = show)
     
    @commands.guild_only()       
    @commands.command(aliases = ['lang'])
    @commands.has_permissions(administrator = True)
    async def Language(self, ctx, *, language : str = ''):
        language = language.lower()
        language = language.strip()  
        
        if language in ['vi', 'vietnam', 'vietnamese', 'v']:
            await setupLanguage(ctx.message.guild.id, 'vi')
            await ctx.send('Bạn đã chọn ngôn ngữ là **Tiếng Việt**')
            
        elif language in ['en', 'english', 'us', 'uk', 'e']:
            await setupLanguage(ctx.message.guild.id, 'en')
            await ctx.send('Your language now is **English**')
            
        else:
            await ctx.send('Please, choose your language correctly!!\n```s.lang vi\en```')
            
    @commands.guild_only()       
    @commands.command(aliases = ['saucenao', 'key', 'api'])
    @commands.has_permissions(administrator = True)       
    async def SauceNaoAPI(self, ctx, api : str):
        checkAPI = checkSauceNAO_API(ctx.message.guild.id, api)
        LANGUAGE = await getLanguage(ctx.message.guild.id)
        mess = SauceNao_checkAPI(LANGUAGE)
        
        if checkAPI:
            await ctx.send(mess[0])
            
        else:
            await ctx.send(mess[1])

            
def setup(bot):
    bot.add_cog(SetUpCommand(bot))
    