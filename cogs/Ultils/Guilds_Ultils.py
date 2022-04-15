from .Database import MyDatabase as db
import re, time

async def getLanguage(serverID : int):
    database = db.getCollection('limitUsage')
    lang = database.find_one({'guildID' :  serverID})
    return lang['lang']

async def setupLanguage(serverID : int, language):
    database = db.getCollection('limitUsage')
    database.update_one({'guildID' :  serverID}, {'$set' : {'lang' : language}})
    
def getAPI(serverID : int):
    database = db.getCollection('limitUsage')
    guild = database.find_one({'guildID' :  serverID})
    return guild['saucenao_api']

def isLoli(tag : str):
    loliList = [' loli ', ' lolicon ', ' lolita ']
    for i in loliList:
        if i in (' ' + tag + ' '):
            return True
    return False

async def checkLimitUsages(guildID : int, cmdName : str, limiCMDdf : str):
    database = db.getCollection('limitUsage')
    find = database.find_one({'guildID' : guildID})
    
    if find['passLimit'] == True:
        return (True, 0)
    
    now = time.time()
    if now >= find['timestamp']:
        reset = {
            'facejp' : 0,
            'faceus' : 0,
            'jav' : 0,
            'anime' : 0,
            'timestamp' : now + 86400
        }
        database.update_one({'guildID' : guildID}, {"$set" : reset})
        return (True, 0)

    limitUsage = find[cmdName]
    if limitUsage == find[limiCMDdf]:
        return (False, find)
    
    limitUsage += 1
    find[cmdName] = limitUsage
    database.update_one({'guildID' : guildID}, {"$set" : {cmdName : limitUsage}})
    return (True, 0)        


async def AllowToUseCommandInThisChannel(ctx, cmd : str):
    database = db.getCollection('SetupCommandsForGuild')
    guild = ctx.message.guild.id
    channel = ctx.message.channel.id
    
    info = {
        'guildID' : guild,
        'command' : cmd
    }

    find = database.find_one(info)
    if not find:
        return (True, [])
    
    find = database.find(info)
    listID = []
    for i in find:
        if channel == i['channelID']:
            return (True, [])
        listID.append(i['channelID'])

    return (False, listID)

async def addCommandAllowForChannel(guildID : int, guildName : str, channelID : int, channelName : str, cmd : str):
    database = db.getCollection('SetupCommandsForGuild')
    
    info = {
        'guildID' : guildID,
        'guildName' : guildName,
        'channelID' : channelID,
        'channelName' : channelName,
        'command' : cmd
    }
    
    find = database.find_one(info)
    
    if not find:
        database.insert_one(info)
        return True
    return False

async def deleteCommandAllowForChannel(guild : int, channel : int, cmd : str):
    database = db.getCollection('SetupCommandsForGuild')
    
    if cmd == 'all':
        database.delete_many({'guildID' : guild, 'channelID' : channel})
        return True
    
    info = {
        'guildID' : guild,
        'channelID' : channel,
        'command' : cmd
    }
    
    find = database.find_one(info)
    
    if find:
        database.delete_one(info)
        return True
    return False

async def GetChannelAllowForCommand(guild : int, cmd : str):
    database = db.getCollection('limitUsage')
    info = {
        'guildID' : guild,
        'command' : cmd
    }
    
    find = database.find(info)
    channelID = []
    for i in find:
        channelID.append(i['channelID'])
    return channelID

def checkSauceNAO_API( guildID : int, api : str):
    from .saucenao_api import SauceNao
    try:
        sauce = SauceNao(api)
        database = db.getCollection('limitUsage')
        database.update_one({'guildID' : guildID} , {'$set' : {'saucenao_api' : api}})
        return True
        
    except:
        return False

async def limitUasgeDefault(guildID : int, guildName : str, member_count : int):
    database = db.getCollection('limitUsage')
    find = database.find_one({'guildID': guildID})
    
    if not find:
        now = time.time() + 86400
        if member_count <= 50:
            facejp = jav = 0
            faceus = 0
            passLimit = False
            
        elif member_count <= 100:
            facejp = 0
            jav = 3
            faceus = 0
            passLimit = False
            
        elif member_count <= 200:
            facejp = 2
            faceus = 1
            jav = 5
            passLimit = False
            
        elif member_count <= 500:
            facejp = 4
            faceus = 2
            jav = 7
            passLimit = False
            
        elif member_count <= 2000:
            facejp = 5
            faceus = 2
            jav = 9
            passLimit = False
            
        else:
            facejp = 5
            faceus = 2
            jav = 12
            passLimit = False
            
        info = {
            'guildID' : guildID,
            'guildName' : guildName,
            'limitFacejpDF' : facejp,
            'limitFaceusDF' : faceus,
            'limitJavDF' : jav,
            'limitAnime' : 50,
            'passLimit' : passLimit,
            'anime' : 0,
            'facejp' : 0,
            'faceus' : 0,
            'jav' : 0,
            'timestamp' : now,
            'lang' : 'en',
            'saucenao_api' : '375640278772d800218b93c6fc5714ca858b097d'
        }
        
        database.insert_one(info)