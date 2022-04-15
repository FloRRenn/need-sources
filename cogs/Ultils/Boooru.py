import aiohttp, random, json, requests
from bs4 import BeautifulSoup    

class BooruImage:
    NSFWTag = '__s__'
    SFWTag = '__s__'
    
    NSFWWebName = {
                'danbooru' : [],
                'gelbooru' : [],
                'konachan' : [],
                'yandere' : []
            }
    
    SFWWebName = {
                'danbooru' : [],
                'gelbooru' : [],
                'konachan' : [],
                'yandere' : []
            }
    
    def __init__(self):
        pass
    
    async def _Extract(self, url, tag, web : str, safe : bool):
        if (tag != self.NSFWTag and safe == False) or (tag != self.SFWTag and safe == True):
            async with aiohttp.ClientSession() as session:
                async with session.get(url) as resp:
                    text = await resp.read() 
                        
            if 'yande.re' not in url and 'konachan.com' not in url:    
                wral = BeautifulSoup(text.decode('utf-8'), 'html.parser').find_all('file_url')
            else:
                wral = BeautifulSoup(text.decode('utf-8'), 'html.parser').find_all('post')
                
            if safe == False:
                self.NSFWWebName[web] = wral
            else:
                self.SFWWebName[web] = wral
                
        if safe == False:
            try:
                random_ = random.randint(0, len(self.NSFWWebName[web]) - 1)
                if 'yande.re' not in url and 'konachan.com' not in url: 
                    res = self.NSFWWebName[web][random_].text
                else:
                    res = self.NSFWWebName[web][random_].attrs['file_url']
                return res
            except:
                return None
        
        else:
            try:
                random_ = random.randint(0, len(self.SFWWebName[web]) - 1)
                if 'yande.re' not in url and 'konachan.com' not in url: 
                    res = self.SFWWebName[web][random_].text
                else:
                    res = self.SFWWebName[web][random_].attrs['file_url']
                return res
            except:
                return None
            
    @classmethod
    async def Dan(self, tag : str = None, safe : bool = False):
        #https://danbooru.donmai.us/posts.json?limit=100&tags=-rating:safe%20genshin%20video
        getDATA = False
        if safe == False and tag != self.NSFWTag:
            danbooru = 'https://danbooru.donmai.us/posts.json?limit=100&tags=-rating:safe%20' + tag.replace(' ', '%20')
            getDATA = True

        elif safe == True and tag != self.SFWTag: 
            danbooru = 'https://danbooru.donmai.us/posts.json?limit=100&tags=rating:safe%20' + tag.replace(' ', '%20')
            getDATA = True
        
        if getDATA == True:         
            async with aiohttp.ClientSession() as session:
                async with session.get(danbooru) as resp:
                    text = await resp.read()
         
        if safe == False:  
            if getDATA == True:         
                try:
                    self.NSFWWebName['danbooru'] = json.loads(text)    
                except:
                    return None
            try:  
                return self.NSFWWebName['danbooru'][random.randint(0, len(self.NSFWWebName['danbooru']) - 1)]['file_url']
            except:
                return None
            
        else:
            if getDATA == True:         
                self.SFWWebName['danbooru'] = json.loads(text)    

            try:  
                return self.SFWWebName['danbooru'][random.randint(0, len(self.SFWWebName['danbooru']) - 1)]['file_url']
            except:
                return None
            
    @classmethod
    async def Gel(self, tag : str, safe : bool):
        #https://gelbooru.com/index.php?page=dapi&s=post&limit=100&q=index&tags=-rating:safe%20*genshin_impact*%20*video*
        if safe == False:
            gelbooru = 'https://gelbooru.com/index.php?page=dapi&s=post&limit=100&q=index&tags=-rating:safe%20*' + tag.replace(' ', '*%20*') + '*'
        else:
            gelbooru = 'https://gelbooru.com/index.php?page=dapi&s=post&limit=100&q=index&tags=rating:safe%20*' + tag.replace(' ', '*%20*') + '*'
        return await self._Extract(self, gelbooru, tag, web = 'gelbooru', safe = safe)   

    @classmethod
    async def Kona(self, tag : str, safe : bool):
        #https://konachan.com/post.xml?limit=100&tags=-rating:safe%20*genshin_impact*%20*video*
        if safe == False:
            konachan = 'https://konachan.com/post.xml?limit=100&tags=-rating:safe%20*' + tag.replace(' ', '*%20*') + '*'
        else:
            konachan = 'https://konachan.com/post.xml?limit=100&tags=rating:safe%20*' + tag.replace(' ', '*%20*') + '*'
        return await self._Extract(self, konachan, tag, web = 'konachan', safe = safe)

    @classmethod
    async def Yande(self, tag : str, safe : bool):
        #https://yande.re/post.xml?limit=100&tags=-rating:safe%20*genshin*%20*video*
        if safe == False:
            yandere = f'https://yande.re/post.xml?limit=100&tags=-rating:safe%20*' + tag.replace(' ', '*%20*') + '*'
        else:
            yandere = f'https://yande.re/post.xml?limit=100&tags=rating:safe%20*' + tag.replace(' ', '*%20*') + '*'
        return await self._Extract(self, yandere, tag, web = 'yandere', safe = safe)
    
    @classmethod
    async def Booru(cls, tag : str, safe : bool):
        dan = await cls.Dan(tag, safe)
        gel = await cls.Gel(tag, safe)
        listSend = [dan, gel]
        
        if 'video' not in tag and 'mp4' not in tag:
            yan = await cls.Yande(tag, safe)
            kona = await cls.Kona(tag, safe)
            listSend.append(yan)
            listSend.append(kona)
        
        if safe == False and tag != cls.NSFWTag:
            cls.NSFWTag = tag
            
        elif safe == True and tag != cls.SFWTag:
            cls.SFWTag = tag
        
        return listSend
    
    @classmethod
    def waifuPic(cls, type : str, tag : str):
        NSFWtag = ['ass', 'bdsm', 'cum', 'doujin', 'femdom', 'hentai', 'maid', 'orgy', 'panties', 'netorare','gif','pussy','uglybastard','uniform','gangbang','cumslut', 'glasses','thighs', 'tentacles', 'masturbation', 'school', 'yuri', 'succubus','nsfwwallpapers','nsfwmobilewallpapers']
        if tag in NSFWtag and type == 'nsfw':
            URL1 = 'https://akaneko-api.herokuapp.com/api/' + tag
            resp = requests.get(URL1)
            return json.loads(resp.content)
            
        else:
            URL = 'https://api.waifu.pics/' + type + '/' + tag
            resp = requests.get(URL)
            return json.loads(resp.content)