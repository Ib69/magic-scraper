import discum, time

# Emoji Config.
# Exemple: staff_emoji = ":staff:"

staff_emoji = ""
partner_emoji = ""
hypesquad_emoji = ""
bughunter_emoji = ""
bughunter2_emoji = ""
early_emoji = ""
dev_emoji = ""
moderator_emoji = ""

# ---------------------------

print(f"""\n\n╔═╗╔═╗──────────╔═══╗
║║╚╝║║──────────║╔═╗║
║╔╗╔╗╠══╦══╦╦══╗║╚══╦══╦═╦══╦══╦══╦═╗
║║║║║║╔╗║╔╗╠╣╔═╝╚══╗║╔═╣╔╣╔╗║╔╗║║═╣╔╝
║║║║║║╔╗║╚╝║║╚═╗║╚═╝║╚═╣║║╔╗║╚╝║║═╣║
╚╝╚╝╚╩╝╚╩═╗╠╩══╝╚═══╩══╩╝╚╝╚╣╔═╩══╩╝
────────╔═╝║────────────────║║
────────╚══╝────────────────╚╝\n""")

# ---------------------------

token = input("\nDiscord token ?\n")
guild_id = input("\nServer id ? (id of the server that you want to scrap)\n")
channel_id = input("\nChannel id ? (id of a channel that everyone can see)\n")

print("----- Starting scraping... -----")
bot = discum.Client(token= token, log=True)

bot.gateway.fetchMembers(guild_id, channel_id, keep=['public_flags','username','discriminator','premium_since'],startIndex=0, method='overlap')
@bot.gateway.command
def memberTest(resp):
    if bot.gateway.finishedMemberFetching(guild_id):
        lenmembersfetched = len(bot.gateway.session.guild(guild_id).members)
        print(str(lenmembersfetched)+' members fetched')
        bot.gateway.removeCommand(memberTest)
        bot.gateway.close()

bot.gateway.run()


def __get_badges(flags) -> list[str]:
    
        BADGES = {
            1 << 0:  staff_emoji,
            1 << 1:  partner_emoji,
            1 << 2:  hypesquad_emoji,
            1 << 3:  bughunter_emoji,
            1 << 9:  early_emoji,
            1 << 14: bughunter2_emoji,
            1 << 17: dev_emoji,
            1 << 18: moderator_emoji
        }

        badges = []

        for badge_flag, badge_name in BADGES.items():
            if flags & badge_flag == badge_flag:
                badges.append(badge_name)

        return badges

with open('result.txt', 'w', encoding="utf-8") as file :
    for memberID in bot.gateway.session.guild(guild_id).members:
        id = str(memberID)
        temp = bot.gateway.session.guild(guild_id).members[memberID].get('public_flags')
        user = str(bot.gateway.session.guild(guild_id).members[memberID].get('username'))
        disc = str(bot.gateway.session.guild(guild_id).members[memberID].get('discriminator'))
        username = f'{user}#{disc}'
        creation_date = str(time.strftime('%d-%m-%Y %H:%M:%S', time.localtime(((int(id) >> 22) + 1420070400000) / 1000)))
        if temp != None:
            z = __get_badges(temp)
            if len(z) != 0:
                badges = ', '.join(z)
                print(f'ID: <@{id}> | Username: {username} | Badges: {badges} | Creation Date: {creation_date}')
                file.write(f'<@{id}> | {username} | {badges}\n')
            
