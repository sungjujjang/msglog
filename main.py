import discord
import sqlite3
from discord import ui, app_commands
import datetime

# cur.execute("CREATE TABLE Msg(message TEXT, username TEXT, userid INTEGER, channelid INTEGER, time TEXT);")
# con.commit()
# con.close()

intents = discord.Intents.all()
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)

@client.event
async def on_ready():
    await tree.sync()
    print(f'We have logged in as {client.user}')

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    else:
        now = datetime.datetime.now()
        con = sqlite3.connect('./message.db')
        cur = con.cursor()
        cur.execute('INSERT INTO Msg VALUES(?, ?, ?, ?, ?);', (message.content, message.author.name, message.author.id, message.channel.id, now))
        con.commit()
        con.close()

@tree.command(name='로그')
async def logs(interaction: discord.Interaction, query: str):
    if interaction.user.guild_permissions.administrator:
        con = sqlite3.connect('./message.db')
        cur = con.cursor()
        strq = query.split(".")
        if strq[0] == "userid":
            cur.execute(f"SELECT * FROM Msg WHERE userid == {strq[1]}")
            data = cur.fetchall()
            if data:
                string = "\n".join(map(str, data))
                await interaction.response.send_message(f"```{string}```")
            else:
                await interaction.response.send_message("데이터가 없습니다.")
        elif strq[0] == "chid":
            cur.execute(f"SELECT * FROM Msg WHERE channelid == {strq[1]}")
            data = cur.fetchall()
            if data:
                string = "\n".join(map(str, data))
                await interaction.response.send_message(f"```{string}```")
            else:
                await interaction.response.send_message("데이터가 없습니다.")
        else:
            await interaction.response.send_message("(chid, userid).(data) 형식으로 입력하여 주세요")

# 디스코드 봇 토큰을 사용하여 봇 로그인
# 여기에는 본인이 발급받은 디스코드 봇 토큰을 입력해야 합니다.
client.run('')