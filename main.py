import nextcord
from nextcord import Interaction, SlashOption
from nextcord.ext import commands

import sqlite3
import datetime

import image.state_gen as img_tool


sqlite_connection = sqlite3.connect('Data Base/db.db')
cursor = sqlite_connection.cursor()

bot = commands.Bot()


@bot.slash_command(description="Get statistics")
async def state(interaction: Interaction, info: str = SlashOption(description="server|@user", required=True)):

    if info == "server":

        ID = interaction.guild.id
        server = bot.get_guild(ID)
        created_at = server.created_at.strftime("%d %B %Y")

        cursor.execute("""SELECT * from server_state""")
        records = cursor.fetchall()

        for row in records:

            if row[0] == "server":
                messages = row[1]

        img_tool.generate(server.icon, server.name, messages, server.member_count, created_at)

        await interaction.send(file = nextcord.File("result.png"))

    else:

        try:

            messages = 0

            cursor.execute("""SELECT * from server_state""")
            records = cursor.fetchall()

            for row in records:

                if str(row[0]) == info.replace("<@", "").replace(">", ""):
                    messages = row[1]

            await interaction.send(f"User sent {messages} messages.")

        except:

            await interaction.send(f"user specified incorrectly.")


@bot.event
async def on_message(message):

    Checking = False

    cursor.execute("""UPDATE server_state SET messages = messages + 1 WHERE user = 'server'""")
    sqlite_connection.commit()

    cursor.execute("""SELECT * from server_state""")
    records = cursor.fetchall()

    for row in records:

        if str(row[0]) == str(message.author.id):
            cursor.execute(f"""UPDATE server_state SET messages = messages + 1 WHERE user = '{message.author.id}'""")
            sqlite_connection.commit()
            Checking = True

    if Checking == False:
        sqlite_insert_query = f"""INSERT INTO server_state (user, messages) VALUES ({message.author.id}, 1)"""
        cursor.execute(sqlite_insert_query)
        sqlite_connection.commit()


bot.run("OTY3MjY5OTYxMDQxMDgwMzgw.GYRT8k.yDq9szzE9MpsCZ2OgK_OGDCqLzdinXaPJL1LqA")