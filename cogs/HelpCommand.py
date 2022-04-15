from discord.ext import commands
from discord_components import *
from .EmbedCommand import *
from .Ultils.Guilds_Ultils import getLanguage
import discord

class HelpCMD(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    @commands.command(aliases = ['h'])
    async def help(self, ctx, cmd : str = None):  
        setupType = ['setup', 'drop', 'manage', 's.setup', 's.drop', 's.manage', 's.lang', 'lang', 'language']
        sourceType = ['a', 'jav', 'anime', 's.a', 's.jav']
        faceType = ['face', 'faceus', 'facejp', 's.facejp', 's.faceus']
        waifuType = ['waifu', 'sfwwaifu', 'nsfwwaifu', 's.sfwwaifu', 's.nsfwwaifu', 'booru', 'danbooru', 'gelbooru', 'konachan', 'yandere', 'booru', 'ndanbooru', 'ngelbooru', 'nkonachan', 'nyandere', 'booru', 'nbooru']
        otherType = ['rule34', 'debut', 'quote', 'code', 's.rule34', 's.debut', 's.quote', 's.code', 'card', 's.card']
        henTai = ['id', 'henbyid', 'henbytag', 's.id', 's.henbyid', 's.henbytag']
        
        LANGUAGE = await getLanguage(ctx.message.guild.id)
        
        if cmd in sourceType:
            await ctx.send(embed = SourceEmbed(LANGUAGE))
            
        elif cmd in faceType:
            await ctx.send(embed = FaceEmbed(LANGUAGE))
            
        elif cmd in waifuType:
            await ctx.send(embed = WaifuEmbed(LANGUAGE))
            
        elif cmd in otherType:
            await ctx.send(embed = OtherEmbed(LANGUAGE))
            
        elif cmd in henTai:
            await ctx.send(embed = HentaiEmbed(LANGUAGE))
            
        elif cmd in setupType:
            if ctx.author.guild_permissions.administrator == False or ctx.author.guild_permissions.manage_channels == False or ctx.author.guild_permissions.manage_guild == False:
                await ctx.send(JustADMIN(LANGUAGE))
                return
            await ctx.send(embed = SetupEmbed(LANGUAGE))
            
        
        else:
            mess = HelpEmbed(LANGUAGE)
            helpBoard = discord.Embed(title = mess[0], color = 0x1CFC01)
            helpBoard.set_author(name = mess[1], icon_url = 'https://i.imgur.com/647ZHPS.jpg')
            helpBoard.set_thumbnail(url = 'https://i.imgur.com/k3cPgqk.jpg') 
             
            options = [
                        SelectOption(label= mess[2], value = '0', emoji = "🔍"),
                        SelectOption(label= mess[3], value = '1', emoji = "🕵🏻‍♂️"),
                        SelectOption(label= mess[5], value = '2', emoji = "🎴"),
                        SelectOption(label= 'Hanime', value = '3', emoji = "😈"),
                        SelectOption(label= mess[4], value = '4', emoji = "🧐"),   
                    ]
            
            if ctx.author.guild_permissions.administrator == True or ctx.author.guild_permissions.manage_channels == True or ctx.author.guild_permissions.manage_guild == True:
                options.append(SelectOption(label= 'Setup', value = '5', emoji = "🛠️"))
             
            await ctx.send(embed = helpBoard, components = [
                                    Select(
                                        placeholder = "Commands",
                                        options = options,
                                        custom_id="select1"
                                    )
                                ])
            
    @commands.command(aliases = ['inv'])
    async def invite(ctx): 
        show = discord.Embed(colour = 0x36FC01)
        #show.add_field(name = 'Cảm ơn bạn đã có lòng mời tui vào server của bạn', value = '[Link mời](https://discord.com/api/oauth2/authorize?client_id=773045224984936449&permissions=414465383616&scope=bot)', inline = True)
        show.add_field(name = 'Hiện tại tui không thể vào server của bạn được, nếu có thắc mắc gì xin hãy vào server của mình', value = '[Link server](https://discord.gg/27ttfuPAcr)', inline = True)
        await ctx.send(embed = show) 
        
def setup(bot):
    bot.add_cog(HelpCMD(bot))