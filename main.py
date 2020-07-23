
'''
using discord.py version 1.0.0a
'''
import discord
import asyncio
import re
import multiprocessing
import threading
import concurrent

BOT_OWNER_ROLE = 'RUNNER' # change to what you need
#BOT_OWNER_ROLE_ID = "642539141036507136"
 

 
oot_channel_id_list = [
 "713566564296687637",  #Ninja  (All Game Chat)
 "713566564976295986",  #Ninja (By Pass)
 "708933760695009321",  #Galaxy (Swag iq)
 "708933852365586472",  #Galaxy (Quipp)
 "709105854473044049",  #Galaxy (Hq)
 "712102809721634858",  #Challenge (Hq)
 "712103306515972126",  #Challenge (Quipp)
 "712103432240234559",  #Challenge (swagiq)
 "712103590440730696",  #Challenge (Quipp private)
 "660448418686173185",  #Cool Trivia (Quipp)
 "711582955713200188",  #Viper (Hq)
 "711583041671397386",  #viper (swagiq)
 "711583216489988136",  #Viper (Quipp)
 "710366782677975130",  #Unt (Hq)
 "710366814097637476",  #Unt (Quipp)
 "706404806738051072",  #Eagle (Hq)
 "706404993246429224",  #Eagle (Swagiq)
 "711043327960678453",  #Eagle (Quipp Bot)
 "710928801047117876",  #Eagle (Quipp Text)
 "711827378413895711",  #Ukt  (Hq)
 "711827425662730270",  #Ukt (Quipp)
 "711827457505755178",  #Ukt (swagiq)
 "710217655130259498",  #daynite (Quipp)
 "707120277196242995",  #Pride (Hq)
 "708953517880246332",  #Pride (Hq beta)
 "711735539426132040",  #Pride (Hq Google)
 "701810950516506645",  #Pride (Swag iq)
 "710823260773810286",  #Pride (Quipp)
 "711893040549068810",  #pride (new hq)
 "585618493093969923",  #Tgl (Swagiq)
 "706180094548377640",  #Tgl (hq2)
 "706291324546187264",  #Tgl (hq3)
 "706314114565406751",  #Tgl (hq4)
 "459842150323060736",  #Dimension (hq)
 "691011674181992518",  #Dimension (swagiq)
 "705728638842306592",  #Savage (Hq)
 "705728639689555978",  #Savage (Quipp)
 "705728644986830858",  #Savage (swagiq)
 "711928148786151565",  #Allen (hq)
 "711928272920772660",  #Allen (Quipp)
 "711928454995509314",  #Allen (Swagiq)
 "693960182803333150",  #World (hq)
 "689311945345859795",  #World (swagiq)
 "695775976327610498",  #world (quipp)
 "694032776198094879",  #utilities (hq)
 "699217974946693221",  #phoniex (Hq)
 "699218106144522280",  #phoniex (swagiq)
 "699218251787534377",  #phoniex (Quipp)
 "703621710871658516",  #genius (Quipp)
 "703621709953105921",  #genius (swag iq)
 "703621709005324298",  #genius (hq)
 "706883579312996453",  #nation (swagiq)
 "706883574036693064",  #nation (hq)
 "706883580357378169",  #nation (quipp)
 "710413308632760320",  #Eraser (hq)
 "711236978162663484",  #Eraser (quipp)
 "708869250688745541",  #infinity (hq)
 "708868194697478194",  #infinity (quipp)
]
answer_pattern = re.compile(r'(not|n)?([1-3]{1})(\?)?(cnf|conf|cf|c)?(\?)?$', re.IGNORECASE)

apgscore = 423
nomarkscore = 212
markscore = 149

async def update_scores(content, answer_scores):
    global answer_pattern

    m = answer_pattern.match(content)
    if m is None:
        return False

    ind = int(m[2])-1

    if m[1] is None:
        if m[3] is None:
            if m[4] is None:
                answer_scores[ind] += nomarkscore
            else: # apg
                if m[5] is None:
                    answer_scores[ind] += apgscore
                else:
                    answer_scores[ind] += markscore

        else: # 1? ...
            answer_scores[ind] += markscore

    else: # contains not or n
        if m[3] is None:
            answer_scores[ind] -= nomarkscore
        else:
            answer_scores[ind] -= markscore

    return True

class SelfBot(discord.Client):

    def __init__(self, update_event, answer_scores):
        super().__init__()
        global oot_channel_id_list
        #global wrong
        self.oot_channel_id_list = oot_channel_id_list
        self.update_event = update_event
        self.answer_scores = answer_scores

    async def on_ready(self):
        print("======================")
        print("Nelson Trivia Self Bot")
        print("Connected to discord.")
        print("User: " + self.user.name)
        print("ID: " + str(self.user.id))

#     @bot.event
#     async def on_message(message):
#      if message.content.startswith('rswag'):
#       await message.delete()
#       await message.channel.send("Swag Iq Bot Restaert Successfully")
          
        def is_scores_updated(message):
            if message.guild == None or \
                str(message.channel.id) not in self.oot_channel_id_list:
                return False

            content = message.content.replace(' ', '').replace("'", "")
            m = answer_pattern.match(content)
            if m is None:
                return False

            ind = int(m[2])-1

            if m[1] is None:
                if m[3] is None:
                    if m[4] is None:
                        self.answer_scores[ind] += nomarkscore
                    else: # apg
                        if m[5] is None:
                            self.answer_scores[ind] += apgscore
                        else:
                            self.answer_scores[ind] += markscore

                else: # 1? ...
                    self.answer_scores[ind] += markscore

            else: # contains not or n
                if m[3] is None:
                    self.answer_scores[ind] -= nomarkscore
                else:
                    self.answer_scores[ind] -= markscore

            return True

        while True:
            await self.wait_for('message', check=is_scores_updated)
            self.update_event.set()

class Bot(discord.Client):

    def __init__(self, answer_scores):
        super().__init__()
        self.bot_channel_id_list = []
        self.embed_msg = None
        self.embed_channel_id = None
        #global wrong
        self.answer_scores = answer_scores

        # embed creation
        self.embed=discord.Embed(title="**__ᴛʀɪᴠɪᴀ ɴɪɴᴊᴀ || ᴘʀᴏ__**", description="**<a:emoji_3:713592275078348840>𝙲𝚘𝚗𝚗𝚎𝚌𝚝𝚎𝚍 𝚃𝚘 𝙱𝚊𝚌𝚔𝚞𝚙**", color=0x00ffff)
        self.embed.set_author(name ='',url=' ',icon_url='')
        self.embed.add_field(name="Option 1", value="0", inline=False)
        self.embed.add_field(name="Option 2", value="0", inline=False)
        self.embed.add_field(name="Option 3", value="0", inline=False)
        self.embed.set_footer(text=f"ᴛʀɪᴠɪᴀ ɴɪɴᴊᴀ || ᴘʀᴏ",\
            icon_url="https://media.discordapp.net/attachments/662974806550904853/698143826564612176/NJ.jpeg?width=269&height=269")
        self.embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/698486250604331039/712159593320415252/CC_20200518_230257.png")
        self.embed.add_field(name="Best Answer:", value="0", inline=True)

        #await self.bot.add_reaction(embed,':spy:')


    async def clear_results(self):
        for i in range(len(self.answer_scores)):
            self.answer_scores[i]=0

    async def update_embeds(self):
      #  global wrong

         

        one_check = ""
        two_check = ""
        three_check = ""
        bold1 = ""
        bold2 = ""
        bold3 = ""
        best_answer = "Searching:- <a:emoji_9:713607700801388564>"
        

        lst_scores = list(self.answer_scores)
        

        highest = max(lst_scores)
        best_answer = "Searching :- <a:emoji_9:713607700801388564>"
        # lowest = min(lst_scores)
        answer = lst_scores.index(highest)+1           

        if highest >0:
          if answer ==1:
            one_check= "<:emoji_10:713608783947104306>"
            best_answer="**Answer :- 1️⃣**"
          if answer==1:
            bold3= ":x:"
          else:
            lol=""

          if answer ==2:
            two_check= "<:emoji_10:713608783947104306>"
            best_answer="**Answer :- 2️⃣**"
          if answer ==2:
            bold1= ":x:"
          else:
            lol=""

          
          if answer ==3:
            three_check= "<:emoji_10:713608783947104306>"
            best_answer="**Answer :- 3️⃣**"
          if answer ==3:
            bold2= ":x:"
          else:
            lol=""

        # if lowest < 0:
        #     if answer == 1 :
        #         one_check = ":x:"
        #     if answer == 2:
        #         two_check = ":x:"
        #     if answer == 3:
        #         three_check = ":x:"             

          
        self.embed.set_field_at(0, name="**__Aɴsᴡᴇʀ ❶__**", value="**{0}**{1}{2}".format(lst_scores[0],one_check,bold1))
        self.embed.set_field_at(1, name="**__Aɴsᴡᴇʀ ❷__**", value="**{0}**{1}{2}".format(lst_scores[1],two_check,bold2))
        self.embed.set_field_at(2, name="**__Aɴsᴡᴇʀ ❸__**", value="**{0}**{1}{2}".format(lst_scores[2],three_check,bold3))
        self.embed.set_field_at(3, name="**__Best Result__**", value=best_answer, inline=True)


        if self.embed_msg is not None:
            await self.embed_msg.edit(embed=self.embed)

    async def on_ready(self):
        print("==============")
        print("Nelson Trivia")
        print("Connected to discord.")
        print("User: " + self.user.name)
        print("ID: " + str(self.user.id))

        await self.clear_results()
        await self.update_embeds()
        
        await asyncio.sleep(5)
        await self.change_presence(activity=discord.Activity(type=1,name="with Backup"))
        await asyncio.sleep(5)

    async def on_message(self, message):

        # if message is private
        if message.author == self.user or message.guild == None:
            return

        if message.content.lower() == "+bc":
            await message.delete()
            if BOT_OWNER_ROLE in [role.name for role in message.author.roles]:
                self.embed_msg = None
                await self.clear_results()
                await self.update_embeds()
                self.embed_msg = \
                    await message.channel.send('',embed=self.embed)
                await self.embed_msg.add_reaction("<:VERIFIED:682907220740276235>")
                await self.embed_msg.add_reaction("<:mast:706502154306846811>")
                self.embed_channel_id = message.channel.id
            else:
                await message.channel.send("**Fuck You Bitch** You Dont Have Permission To Do This.")
            return

        if message.content.startswith('*bc'):
          await message.delete()
          if BOT_OWNER_ROLE in [role.name for role in message.author.roles]:
           embed = discord.Embed(title="> **Backup Bot Is Restarted Successfully. <a:ticksah:701742569532424202>**")
           await message.channel.send(embed=embed)
          

        # process votes
        if message.channel.id == self.embed_channel_id:
            content = message.content.replace(' ', '').replace("'", "")
            updated = await update_scores(content, self.answer_scores)
            if updated:
                await self.update_embeds()

def bot_with_cyclic_update_process(update_event, answer_scores):

    def cyclic_update(bot, update_event):
        f = asyncio.run_coroutine_threadsafe(bot.update_embeds(), bot.loop)
        while True:
            update_event.wait()
            update_event.clear()
            f.cancel()
            f = asyncio.run_coroutine_threadsafe(bot.update_embeds(), bot.loop)
            #res = f.result()

    bot = Bot(answer_scores)

    upd_thread = threading.Thread(target=cyclic_update, args=(bot, update_event))
    upd_thread.start()

    loop = asyncio.get_event_loop()
    loop.create_task(bot.start('NzExOTk1NzgyOD0HlplP5gXmAj6mkc'))
    loop.run_forever()


def selfbot_process(update_event, answer_scores):

    selfbot = SelfBot(update_event, answer_scores)

    loop = asyncio.get_event_loop()
    loop.create_task(selfbot.start('NjYyNTA1NDQ1NTY2NzA7E3YOattk0iMs',
                                   bot=False))
    loop.run_forever()

if __name__ == '__main__':

    # running bot and selfbot in separate OS processes

    # shared event for embed update
    update_event = multiprocessing.Event()

    # shared array with answer results
    answer_scores = multiprocessing.Array(typecode_or_type='i', size_or_initializer=3)

    p_bot = multiprocessing.Process(target=bot_with_cyclic_update_process, args=(update_event, answer_scores))
    p_selfbot = multiprocessing.Process(target=selfbot_process, args=(update_event, answer_scores))

    p_bot.start()
    p_selfbot.start()

    p_bot.join()
    p_selfbot.join()
