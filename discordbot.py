import discord
import datetime
import os
import keep_alive
import re
import random
import asyncio
import gspread
import json
from oauth2client.service_account import ServiceAccountCredentials 
from discord.ext import commands

client = commands.Bot(command_prefix='.')
@client.event
async def on_ready():
    print('Logged in')
    print('------')  
"""    
scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']
credentials = ServiceAccountCredentials.from_json_keyfile_name('/home/runner/FH/spreadsheet-test-282320-a54e87c8c929.json', scope)
gc = gspread.authorize(credentials)
wb = gc.open_by_key(os.getenv('Sheetkey'))
ws = wb.worksheet("さかなテスト")
ws2 = wb.worksheet("交流戦記録")


@client.command()
async def p(ctx,a):

  def is_int(s):
    try:
        int(s)
        return True
    except ValueError:
        return False

  try:
    cell=ws.find(str(ctx.author.id+ctx.guild.id)) 
  except:
    ws.append_row([str(ctx.author.id+ctx.guild.id),ctx.guild.name,ctx.author.name])
    cell=ws.find(str(ctx.author.id+ctx.guild.id))
    for i in range(10):
      ws.update_cell(cell.row,len(ws.row_values(cell.row))+1,0)

  #C2:totalnum	D3:winnum	E4:losenum	F5:winrate	G6:ave	H7:winave	I8:loseave	J9:total	K10:wintotal	L11:losetotal

  b=ws.row_values(cell.row)
  if is_int(a)==False:
    msg = await ctx.send("エラー")
    await asyncio.sleep(3)
    await msg.delete()
  else:
    b[3]=int(b[3])+1
    a=int(a)
    if a>0:
      b[4]=int(b[4])+1
      b[11]=int(b[11])+a
      b[8]=b[11]//b[4]
    else:
      a=-1*int(a)
      b[5]=int(b[5])+1
      b[12]=int(b[12])+a
      b[9]=b[12]//b[5]
    b[10]=int(b[10])+a
    b[6]=int(b[4])*100//b[3]
    b[7]=b[10]//b[3]
    for i in range(13):
      ws.update_cell(cell.row,i+1,b[i])
 
    msg = await ctx.send("記録しました")
    await asyncio.sleep(3)
    await msg.delete()
  
  await ctx.channel.purge(limit=1)
"""
  
@client.command()
async def c(ctx):
  print(ctx.author.id,ctx.guild.id,ctx.author.id+ctx.guild.id)
  await ctx.send(os.path.abspath('spreadsheet-test-282320-a54e87c8c929.json'))
  
"""
@client.command()
async def stats(ctx):
  cell=ws.find(str(ctx.author.id+ctx.guild.id))
  b=ws.row_values(cell.row)
  msg = discord.Embed(title="stats",colour=0x1e90ff)
  msg.add_field(name="name", value=b[1], inline=False)
  msg.add_field(name="play", value=b[3], inline=False)
  msg.add_field(name="win rate", value=b[6]+"%", inline=False)
  msg.add_field(name="average", value=b[7], inline=False)
  msg.add_field(name="win-ave", value=b[8], inline=False)
  msg.add_field(name="lose-ave", value=b[9], inline=False)
  await ctx.channel.purge(limit=1)  
  msg = await ctx.send(embed=msg)  
  await asyncio.sleep(15)
  await msg.delete() 


@client.command()
async def rename(ctx):
  cell=ws.find(str(ctx.author.id+ctx.guild.id))
  ws.update_cell(cell.row,2,ctx.author.name)
  msg = await ctx.send("名前を修正しました")
  await asyncio.sleep(3)
  await msg.delete()


@client.command()
async def revise(ctx,a):
  def is_int(s):
    try:
        int(s)
        return True
    except ValueError:
        return False

  try:
    cell=ws.find(str(ctx.author.id+ctx.guild.id)) 
  except:
    ws.append_row([str(ctx.author.id+ctx.guild.id),ctx.guild.name,ctx.author.name])
    cell=ws.find(str(ctx.author.id+ctx.guild.id))
    for i in range(10):
      ws.update_cell(cell.row,len(ws.row_values(cell.row))+1,0)

  #C2:totalnum	D3:winnum	E4:losenum	F5:winrate	G6:ave	H7:winave	I8:loseave	J9:total	K10:wintotal	L11:losetotal

  b=ws.row_values(cell.row)
  if is_int(a)==False:
    msg = await ctx.send("エラー")
    await asyncio.sleep(3)
    await msg.delete()
  else:
    b[3]=int(b[3])-1
    a=int(a)
    if a>0:
      b[4]=int(b[4])-1
      b[11]=int(b[11])-a
      b[8]=b[11]//b[4]
    else:
      a=-1*int(a)
      b[5]=int(b[5])-1
      b[12]=int(b[12])-a
      b[9]=b[12]//b[5]
    b[10]=int(b[10])-a
    b[6]=int(b[4])*100//b[3]
    b[7]=b[10]//b[3]
    for i in range(13):
      ws.update_cell(cell.row,i+1,b[i])
 
    msg = await ctx.send("修正しました")
    await asyncio.sleep(3)
    await msg.delete()
  
  await ctx.channel.purge(limit=1)


@client.command()
async def result(ctx):
  cell=ws.find(str(ctx.guild.id))
  b=ws.row_values(cell.row)
  msg = discord.Embed(title="stats",colour=0x1e90ff)
  msg.add_field(name="name", value=b[2], inline=False)
  msg.add_field(name="play", value=b[3], inline=False)
  msg.add_field(name="win rate", value=b[6]+"%", inline=False)
  await ctx.channel.purge(limit=1)  
  msg = await ctx.send(embed=msg)  
  await asyncio.sleep(15)
  await msg.delete() 


@client.command()
async def reset(ctx):
  cell=ws.find(str(ctx.author.id+ctx.guild.id))
  for i in range(10):
    ws.update_cell(cell.row,i+4,0)

  msg = await ctx.send("リセットしました")
  await asyncio.sleep(3)
  await msg.delete()

@client.command()
async def r(ctx,a,b):
  def is_int(s):
    try:
        int(s)
        return True
    except ValueError:
        return False

  try:
    cell=ws.find(str(ctx.guild.id)) 
  except:
    ws.append_row([str(ctx.guild.id),ctx.guild.name,"None"])
    cell=ws.find(str(ctx.guild.id))
    for i in range(4):
      ws.update_cell(cell.row,len(ws.row_values(cell.row))+1,0)

  b=ws.row_values(cell.row)
  if is_int(a)==False:
    msg = await ctx.send("エラー")
    await asyncio.sleep(3)
    await msg.delete()
  else:
    b[3]=int(b[3])+1
    a=int(a)
    if a>0:
      b[4]=int(b[4])+1      
    else:      
      b[5]=int(b[5])+1
    b[6]=b[3]*100//int(b[4])
  for i in range(7):
      ws.update_cell(cell.row,i+1,b[i])


@client.command()
async def teamstats(ctx):
  cell=ws.find(str(ctx.author.id+ctx.guild.id))
  b=ws.row_values(cell.row)
  msg = discord.Embed(title="stats",colour=0x1e90ff)
  msg.add_field(name="name", value=b[1], inline=False)
  msg.add_field(name="play", value=b[3], inline=False)
  msg.add_field(name="win rate", value=b[6]+"%", inline=False)
  await ctx.channel.purge(limit=1)  
  msg = await ctx.send(embed=msg)  
  await asyncio.sleep(15)
  await msg.delete() 


@client.command()
async def a(ctx):
  print(ctx.channel.id)
  try:
    await client.wait_for('message',timeout=10)
  except asyncio.TimeoutError:
    print("Timeout")
  else:
    print("OK")
"""

token = os.environ['DISCORD_BOT_TOKEN']
client.run(token)
