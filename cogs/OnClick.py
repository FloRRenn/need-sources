from discord.ext import commands
from discord_components import *
from .EmbedCommand import *
from .Ultils.Hentai_Ultils import MoveToNewPpage, showThumnailHen, setNewMessID
from .Ultils.Guilds_Ultils import getLanguage

class OnClick(commands.Cog): 
    def __init__(self, bot):
        self.bot = bot
        
    @commands.Cog.listener()
    async def on_select_option(self, interaction):
        guild = interaction.guild.id
        LANGUAGE = await getLanguage(guild)
        value = interaction.values[0]
        
        if value == '0':
            await interaction.respond(embed = SourceEmbed(LANGUAGE))
            
        elif value == '1':
            await interaction.respond(embed = FaceEmbed(LANGUAGE))
            
        elif value == '2':
            await interaction.respond(embed = WaifuEmbed(LANGUAGE))
            
        elif value == '3':
            await interaction.respond(embed = HentaiEmbed(LANGUAGE))
            
        elif value == '4':
            await interaction.respond(embed = OtherEmbed(LANGUAGE))
            
        elif value == '5':
            await interaction.respond(embed = SetupEmbed(LANGUAGE))
        
    @commands.Cog.listener()
    async def on_button_click(self, interaction):
        channel = interaction.channel
        guild = interaction.guild.id
        mess_id = interaction.message.id
        user = interaction.user
        
        LANGUAGE = await getLanguage(guild)
        msg = await channel.fetch_message(mess_id)
        
        if interaction.component.label in ['Lưu sauce', 'Save sauce']:
            await user.send(embed = msg.embeds[0]) 
            
        elif interaction.component.label in ["Lưu ảnh trên", 'Save this image']:   
            await interaction.respond(content = "Saved this image")
            await user.send(msg.embeds[0].image.proxy_url)
            
        elif interaction.component.label in ['Lưu video trên', 'Save this video']:
            await interaction.respond(content = "Saved this video")
            await user.send(msg.content)
                    
        elif interaction.component.label in ["Lưu info", "Save this info"]: 
            title = msg.embeds[0].title
            button = Button(style = ButtonStyle.URL, label = title + ' bio', url = 'https://www.javdatabase.com/idols/' + title.replace(' ', '-'), emoji = '❤️')
            
            await interaction.respond(content = 'Saved')
            await user.send(embed = msg.embeds[0], components = [button]) 
            
        elif interaction.component.label in ['Lưu phim', 'Save this movie']:
            codeID = msg.embeds[0].fields[1].value
            
            codeButton = Button(style = ButtonStyle.URL, label = f"{codeID}", url = 'https://www.google.com/search?q=' + codeID + '%20jav')
            await interaction.respond(content = 'Saved this movie')
            await user.send(embed = msg.embeds[0], components = [codeButton]) 
            
            
    @commands.Cog.listener()
    async def on_reaction_add(self, reaction, user):
        if user == self.bot.user:
            return
        
        react = reaction.emoji
        
        if react in ['🔽', '💾', '⬅️', '➡️']:
            message = reaction.message
            mess_id = message.id
            channel = reaction.message.channel
            guild_id = reaction.message.guild.id
            msg = await channel.fetch_message(mess_id)
                
            if react == '🔽':
                listEmbed = await MoveToNewPpage(guild_id)
                
                if listEmbed[0] == 0:
                    await msg.reply(content = f'{user.mention}\n**This doujin was deleted.**')
                
                elif listEmbed[0] == 1:
                    for embed in listEmbed[1]:
                        nextmsg = await msg.reply(embed = embed)
                        await nextmsg.add_reaction('💾') 
                    await nextmsg.add_reaction('🔽') 
                
            elif react == '💾':
                await user.send(embed = msg.embeds[0])
                
            elif react == '➡️':
                show =  await showThumnailHen(guild_id, 0)
                await msg.edit(embed = show)
        
                await message.remove_reaction(reaction, user)
                emoji = ['⬅️', '➡️']
                for emo in emoji:
                    await msg.add_reaction(emo)
                    
            elif react == '⬅️':
                show =  await showThumnailHen(guild_id, 1)
                await msg.edit(embed = show)
                    
                await message.remove_reaction(reaction, user)
                emoji = ['⬅️', '➡️']
                for emo in emoji:
                    await msg.add_reaction(emo)
                    
def setup(bot):
    bot.add_cog(OnClick(bot))