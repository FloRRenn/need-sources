from argparse import Action
from discord.ext import commands
from discord.ext.commands.core import guild_only
import discord
import aiohttp

from .Ultils.Guilds_Ultils import getLanguage

class FunyInteractor(commands.Cog):
    waifuURL = 'https://api.waifu.pics/'
    
    def __init__(self, bot):
        self.bot = bot
        
    async def getSFW(self, type : str, tag : str):
        URL =  self.waifuURL + type + '/' + tag
        
        async with aiohttp.ClientSession() as session:
            resp = await session.get(URL)
            data = await resp.json()
            return data['url']
        
    async def getNSFW(self, tag):
        URL = 'https://akaneko-api.herokuapp.com/api/' + tag
        
        async with aiohttp.ClientSession() as session:
            resp = await session.get(URL)
            data = await resp.json()
            return data['url']
        
    async def createEmbed(self, owner, action, reason, language, sfw : bool = True):   
        title = f"**{owner} {action[1]}. Lý do: **" + reason
        if sfw:
            image = await self.getSFW('sfw', action[0])
        else:
            image = await self.getNSFW(action[0])
        
        show = discord.Embed(description = title, colour = 0xF39C12)
        show.set_image(url = image)
        return show
    
    def getAction(self, ownerID, member, language):
        withWHO = member.mention if member.id != ownerID else "bản thân"
        return withWHO
        
    @commands.command()
    @commands.guild_only()
    async def bite(self, ctx, member : discord.Member, *, reason : str = "_Thích :)_"):
        LANGUAGE = await getLanguage(ctx.message.guild.id)
        withWHO = self.getAction(ctx.author.id, member, LANGUAGE)
            
        action = ('bite', f'đang cực kỳ muốn cắn {withWHO}')
        embed = await self.createEmbed(ctx.author.mention, action, reason, LANGUAGE)
        await ctx.send(embed = embed)
        
    @commands.command()
    @commands.guild_only()
    async def shy(self, ctx, member : discord.Member, *, reason : str = "_Ngại nói :3_"):
        LANGUAGE = await getLanguage(ctx.message.guild.id)
        withWHO = self.getAction(ctx.author.id, member, LANGUAGE)
        
        action = ('blush', f"cảm thấy xấu hổ với {withWHO}")
        embed = await self.createEmbed(ctx.author.mention, action, reason, LANGUAGE)
        await ctx.send(embed = embed)
      
    @commands.command()
    @commands.guild_only()
    async def bonk(self, ctx, member : discord.Member, *, reason : str = "__Thích :)__"):
        LANGUAGE = await getLanguage(ctx.message.guild.id)
        withWHO = self.getAction(ctx.author.id, member, LANGUAGE)
        
        action = ('bonk', f"muốn gõ đầu {withWHO}")
        embed = await self.createEmbed(ctx.author.mention, action, reason, LANGUAGE)
        await ctx.send(embed = embed)
        
    @commands.command()
    @commands.guild_only()
    async def bully(self, ctx, member : discord.Member, *, reason : str = "__Thích :)__"):
        LANGUAGE = await getLanguage(ctx.message.guild.id)
        withWHO = self.getAction(ctx.author.id, member, LANGUAGE)
        
        action = ('bully', f"muốn bắt nạt {withWHO}")
        embed = await self.createEmbed(ctx.author.mention, action, reason, LANGUAGE)
        await ctx.send(embed = embed)
        
    @commands.command()
    @commands.guild_only()
    async def cringe(self, ctx, member : discord.Member, *, reason : str = "__Vì quá nhục (-.-)__"):
        LANGUAGE = await getLanguage(ctx.message.guild.id)
        withWHO = self.getAction(ctx.author.id, member, LANGUAGE)
        
        action = ('cringe', f"cảm thấy thật khinh bỉ {withWHO}")
        embed = await self.createEmbed(ctx.author.mention, action, reason, LANGUAGE)
        await ctx.send(embed = embed)
        
    @commands.command()
    @commands.guild_only()
    async def cry(self, ctx, member : discord.Member, *, reason : str = "__Vì chạm đến lòng tôi 😭__"):
        LANGUAGE = await getLanguage(ctx.message.guild.id)
        withWHO = self.getAction(ctx.author.id, member, LANGUAGE)
        
        action = ('cry', f"cảm thấy thật xúc động với {withWHO}")
        embed = await self.createEmbed(ctx.author.mention, action, reason, LANGUAGE)
        await ctx.send(embed = embed)
        
    @commands.command()
    @commands.guild_only()
    async def cuddle(self, ctx, member : discord.Member, *, reason : str = "__Vì quá đáng yêu ☺️__"):
        LANGUAGE = await getLanguage(ctx.message.guild.id)
        withWHO = self.getAction(ctx.author.id, member, LANGUAGE)
        
        action = ('cuddle', f"muốn nựng {withWHO}")
        embed = await self.createEmbed(ctx.author.mention, action, reason, LANGUAGE)
        await ctx.send(embed = embed)
        
    @commands.command()
    @commands.guild_only()
    async def dance(self, ctx, member : discord.Member, *, reason : str = "__Vì rất đặc biệt 🥰__"):
        LANGUAGE = await getLanguage(ctx.message.guild.id)
        withWHO = self.getAction(ctx.author.id, member, LANGUAGE)
        
        action = ('dance', f"muốn mời {withWHO} tham gia tiệc nhảy")
        embed = await self.createEmbed(ctx.author.mention, action, reason, LANGUAGE)
        await ctx.send(embed = embed)
        
    @commands.command()
    @commands.guild_only()
    async def handhold(self, ctx, member : discord.Member, *, reason : str = "__Vì không muốn rời xa 🥺__"):
        LANGUAGE = await getLanguage(ctx.message.guild.id)
        withWHO = self.getAction(ctx.author.id, member, LANGUAGE)
        
        action = ('handhold', f"muốn nắm lấy bàn của {withWHO}")
        embed = await self.createEmbed(ctx.author.mention, action, reason, LANGUAGE)
        await ctx.send(embed = embed)
           
    @commands.command()
    @commands.guild_only()
    async def happy(self, ctx, member : discord.Member, *, reason : str = "__Vì một điều tuyệt vời đã xảy ra 😊__"):
        LANGUAGE = await getLanguage(ctx.message.guild.id)
        withWHO = self.getAction(ctx.author.id, member, LANGUAGE)
        
        action = ('happy', f"cảm thấy thật hạnh phúc với {withWHO}")
        embed = await self.createEmbed(ctx.author.mention, action, reason, LANGUAGE)
        await ctx.send(embed = embed)
        
    @commands.command()
    @commands.guild_only()
    async def highfive(self, ctx, member : discord.Member, *, reason : str = "__Vì rất tuyệt 😊__"):
        LANGUAGE = await getLanguage(ctx.message.guild.id)
        withWHO = self.getAction(ctx.author.id, member, LANGUAGE)
        
        action = ('highfive', f"muốn đập tay với {withWHO}")
        embed = await self.createEmbed(ctx.author.mention, action, reason, LANGUAGE)
        await ctx.send(embed = embed)
        
    @commands.command()
    @commands.guild_only()
    async def hug(self, ctx, member : discord.Member, *, reason : str = "__Vì thật ấm áp 🥰__"):
        LANGUAGE = await getLanguage(ctx.message.guild.id)
        withWHO = self.getAction(ctx.author.id, member, LANGUAGE)
        
        action = ('hug', f"muốn ôm {withWHO}")
        embed = await self.createEmbed(ctx.author.mention, action, reason, LANGUAGE)
        await ctx.send(embed = embed)
        
    @commands.command()
    @commands.guild_only()
    async def kick(self, ctx, member : discord.Member, *, reason : str = "__Vì thật khó chịu 😡__"):
        LANGUAGE = await getLanguage(ctx.message.guild.id)
        withWHO = self.getAction(ctx.author.id, member, LANGUAGE)
        
        action = ('kick', f"muốn đá {withWHO}")
        embed = await self.createEmbed(ctx.author.mention, action, reason, LANGUAGE)
        await ctx.send(embed = embed)
    
    @commands.command()
    @commands.guild_only()
    async def kill(self, ctx, member : discord.Member, *, reason : str = "__Vì $#@%#^ ☠️__"):
        LANGUAGE = await getLanguage(ctx.message.guild.id)
        withWHO = self.getAction(ctx.author.id, member, LANGUAGE)
        
        action = ('kill', f"muốn giết {withWHO}")
        embed = await self.createEmbed(ctx.author.mention, action, reason, LANGUAGE)
        await ctx.send(embed = embed)
    
    @commands.command()
    @commands.guild_only()
    async def kiss(self, ctx, member : discord.Member, *, reason : str = "__Vì bạn là trái tim của tui 🤡__"):
        LANGUAGE = await getLanguage(ctx.message.guild.id)
        withWHO = self.getAction(ctx.author.id, member, LANGUAGE)
        
        action = ('kiss', f"muốn hôn {withWHO}")
        embed = await self.createEmbed(ctx.author.mention, action, reason, LANGUAGE)
        await ctx.send(embed = embed)
        
    @commands.command()
    @commands.guild_only()
    async def lick(self, ctx, member : discord.Member, *, reason : str = "__🤭__"):
        LANGUAGE = await getLanguage(ctx.message.guild.id)
        withWHO = self.getAction(ctx.author.id, member, LANGUAGE)
        
        action = ('lick', f"muốn được nếm thử mùi vị của {withWHO}")
        embed = await self.createEmbed(ctx.author.mention, action, reason, LANGUAGE)
        await ctx.send(embed = embed)
        
    @commands.command()
    @commands.guild_only()
    async def pat(self, ctx, member : discord.Member, *, reason : str = "__Vì rất ngoan 👍__"):
        LANGUAGE = await getLanguage(ctx.message.guild.id)
        withWHO = self.getAction(ctx.author.id, member, LANGUAGE)
        
        action = ('pat', f"muốn xoa đầu {withWHO}")
        embed = await self.createEmbed(ctx.author.mention, action, reason, LANGUAGE)
        await ctx.send(embed = embed)
        
    @commands.command()
    @commands.guild_only()
    async def slap(self, ctx, member : discord.Member, *, reason : str = "__Vì nói quá nhiều 👍__"):
        LANGUAGE = await getLanguage(ctx.message.guild.id)
        withWHO = self.getAction(ctx.author.id, member, LANGUAGE)
        
        action = ('slap', f"muốn tát vỡ mồm {withWHO}")
        embed = await self.createEmbed(ctx.author.mention, action, reason, LANGUAGE)
        await ctx.send(embed = embed)
        
    @commands.command()
    @commands.guild_only()
    async def hello(self, ctx, member : discord.Member, *, reason : str = "__Vì thích 😊__"):
        LANGUAGE = await getLanguage(ctx.message.guild.id)
        withWHO = self.getAction(ctx.author.id, member, LANGUAGE)
        
        action = ('wave', f"muốn chào {withWHO}")
        embed = await self.createEmbed(ctx.author.mention, action, reason, LANGUAGE)
        await ctx.send(embed = embed)
        
    @commands.command()
    @commands.guild_only()
    async def wink(self, ctx, member : discord.Member, *, reason : str = "__Vì thích 😊__"):
        LANGUAGE = await getLanguage(ctx.message.guild.id)
        withWHO = self.getAction(ctx.author.id, member, LANGUAGE)
        
        action = ('wink', f"muốn nháy mắt với {withWHO}")
        embed = await self.createEmbed(ctx.author.mention, action, reason, LANGUAGE)
        await ctx.send(embed = embed)
        
    #------------------------------------------------------------------------------------------------
    #------------------------------------------------------------------------------------------------
    #------------------------------------------------------------------------------------------------
    #------------------------------------------------------------------------------------------------
    
    @commands.command(aliases = ['bj'])
    @commands.guild_only()
    @commands.is_nsfw()
    async def blowjob(self, ctx, member : discord.Member, *, reason : str = "__Ghiền__"):
        LANGUAGE = await getLanguage(ctx.message.guild.id)
        withWHO = self.getAction(ctx.author.id, member, LANGUAGE)
        
        action = ('blowjob', f"muốn buscu {withWHO}")
        embed = await self.createEmbed(ctx.author.mention, action, reason, LANGUAGE, False)
        await ctx.send(embed = embed)
    
    @commands.command()
    @commands.guild_only()
    @commands.is_nsfw()
    async def cum(self, ctx, member : discord.Member, *, reason : str = "__Ghiền__"):
        LANGUAGE = await getLanguage(ctx.message.guild.id)
        withWHO = self.getAction(ctx.author.id, member, LANGUAGE)
        
        action = ('cum', f"muốn bắn lên {withWHO}")
        embed = await self.createEmbed(ctx.author.mention, action, reason, LANGUAGE, False)
        await ctx.send(embed = embed)
        
    @commands.command()
    @commands.guild_only()
    @commands.is_nsfw()
    async def orgy(self, ctx, member : discord.Member, *, reason : str = "__Ghiền__"):
        LANGUAGE = await getLanguage(ctx.message.guild.id)
        withWHO = self.getAction(ctx.author.id, member, LANGUAGE)
        
        action = ('orgy', f"muốn orgy với {withWHO}")
        embed = await self.createEmbed(ctx.author.mention, action, reason, LANGUAGE, False)
        await ctx.send(embed = embed)
        
def setup(bot):
    bot.add_cog(FunyInteractor(bot))