from .Database import MyDatabase as db
from .Language import ShowHentaiPage, HentaiMess
import time, discord
from hentai import Hentai, Format
from .Guilds_Ultils import isLoli

async def addCommic(info, id):
    nhentai = db.getCollection('nhentai')
    nhentai.update_one({'ID' : id}, {'$set' : info}, upsert = True)
    
async def setNewMessID(msgID : int, username : str, newID : int):
    nhentai = db.getCollection('nhentai')
    nhentai.update_one({'ID' : msgID, 'user' : username}, {'$set' : {'ID' : newID}})
    
async def delCommic():
    nhentai = db.getCollection('nhentai')
    getList = nhentai.find({})
    
    timestampnow = time.time()
    
    for commic in getList:
        messageID = commic['ID']
        if timestampnow - commic['timestamp'] >= 3600:
            nhentai.delete_one({'ID' : messageID})  
    
async def addListIDHen(messID : int, listID : list, language : str):
    info = {
        'ID' : messID,
        'listID' : listID,
        'currentIndex' : 0,
        'length' : len(listID) - 1,
        'isTag' : True,
        'timestamp' : time.time(),
        'lang' : language
    }
    
    nhentai = db.getCollection('nhentai')
    nhentai.update_one({'ID' : messID}, {'$set' : info}, upsert = True)
    
async def MoveToNewPpage(guildID):
    nhentai = db.getCollection('nhentai')
    find = nhentai.find_one({"ID" : guildID})

    if not find:
        return (0, None)
    
    messLang = ShowHentaiPage(find['lang'])
    page = find['currentPage']
    lengtPage = find['lenght']
    
    jump = min(page + 8, lengtPage) 
    nhentai.update_one({'ID' : guildID}, {'$set' : {'currentPage' : jump}})
    
    listEmbed = []
    for pageIndex in range (page, jump - 1):
        show = discord.Embed(title = find['title'], url = find['link'])
        show.set_image(url = find['imageList'][pageIndex])
        show.set_footer(text = f'{messLang[0]} {pageIndex + 1}/{lengtPage} - ID {messLang[1]}: {find["IDcommic"]}\n{messLang[2]}')
        listEmbed.append(show)
    
    show = discord.Embed(title = find['title'], url = find['link'])
    show.set_image(url = find['imageList'][jump - 1])
    show.set_footer(text = f'{messLang[0]} {jump}/{lengtPage} - ID {messLang[1]}: {find["IDcommic"]}\n{messLang[3]}')
    listEmbed.append(show)
        
    if jump >= lengtPage:  
        nhentai.delete_one({'ID' : guildID})
        
    else:
        nhentai.update_one({'ID' : guildID}, {'$set' : {'currentPage' : jump}})
    return (1, listEmbed)

async def showThumnailHen(messID : int, MoveType : int):
    nhentai = db.getCollection('nhentai')
    
    find = nhentai.find_one({'ID' : messID, 'isTag' : True})
    try:
        LANGUAGE = find['lang']
    except:
        LANGUAGE = 'en'
    
    if not find:
        show = discord.Embed(title = '**Data not found.**')
        return show
    
    currnetIndex = find['currentIndex']
    lenght = find['length']
    
    if MoveType == 0:
        if currnetIndex >= lenght:
            nextIndex = 0
        
        else:
            nextIndex = currnetIndex + 1
            
    elif MoveType == 1:
        if currnetIndex <= 0:
            nextIndex = lenght
        
        else:
            nextIndex = currnetIndex - 1
        
    nhentai.update_one({'ID' : messID, 'isTag' : True}, {"$set" : {'currentIndex' : nextIndex}})
    mess = HentaiMess(find['listID'][nextIndex], LANGUAGE)
    
    doujin = Hentai(find['listID'][nextIndex])
    tag = ''
    for i in doujin.tag:
        if isLoli(str(i.name)):
            show = discord.Embed(title = mess[1])
            show.set_footer(text = mess[6])    
            return show
        
        tag += f'`{i.name}` '          
    
    title = doujin.title(Format.Pretty)
    imageList = doujin.image_urls
    
    info = doujin.artist
    if len(info) != 0:
            hyperlink = f'[{info[0].name.title()}]({info[0].url})'

    elif len(info) == 0:
        hyperlink = 'N/A'
        
    length = len(imageList)

    show = discord.Embed()
    show.add_field(name = mess[2], value = f'[{title}](https://nhentai.net/g/{find["listID"][nextIndex]})', inline = True)
    show.add_field(name = mess[3], value = hyperlink, inline = False)
    show.add_field(name = mess[4], value = length, inline = True)
    show.add_field(name = 'ID', value = find['listID'][nextIndex], inline = True)
    show.add_field(name = 'Tag', value = tag, inline = False)
    show.set_image(url = doujin.cover)
    show.set_footer(text = mess[6])    
    return show

def getTag(tag : str, type : str):
    girls3D = db.getCollection("3d_girls")
    
    if tag == '3d':
        a = girls3D.aggregate([{'$match' : {'type' : type, 'tag' : '3d'}}, {"$sample": { "size": 1 }}])
    
    else:
        a = girls3D.aggregate([{'$match' : {'tag' : tag, 'type' : type}}, {"$sample": { "size": 3 }}])
        
    return a