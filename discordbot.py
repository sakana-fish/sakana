import os
import discord
import datetime
import random
import asyncio
from discord.ext import commands

import gspread
#import json
from oauth2client.service_account import ServiceAccountCredentials 


sheetkey = os.environ['SHEETKEY']
path = os.environ['MAIL']
scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']
credentials = ServiceAccountCredentials.from_json_keyfile_name(path, scope)
gc = gspread.authorize(credentials)
wb = gc.open_by_key(sheetkey)
ws = wb.worksheet("戦績記録")
ws2 = wb.worksheet("交流戦記録")  

#https://ja.wikipedia.org/wiki/Unicode%E3%81%AEEmoji%E3%81%AE%E4%B8%80%E8%A6%A7

#list = []
#apre = 'おさかなのサーバー'

client = commands.Bot(command_prefix='.')
@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')  
    await client.change_presence(activity=discord.Game(name='おさかな天国'))


@client.command()
async def fish3(ctx, about = "🐟🐟🐟 戦績記録使い方 🐟🐟🐟"):
  help1 = discord.Embed(title=about,color=0xe74c3c,description=".p 点数: 個人の結果記録,符号＋点数を入力する(負けた試合は負),例:.p 100,.p -77\n.r 点差 チーム名: 交流戦の結果記録,例:.r 40 IsK,.r -50 Lv\n.revise 点数: 個人の結果修正,例:.p -80を消す→.revise -80\n.stats/.teamstats/.history: 戦績\n.vs チーム名: 対象チームとの戦績確認\n.rename/.teamrename: 名前の変更\n.reset/.teamreset: 戦績(statsの内容)リセット\n.teamdelete: 対戦履歴削除\n作成者: さかな(@sakana8dx)\nさかなBot導入: https://discord.com/oauth2/authorize?client_id=619351049752543234&permissions=473152&scope=bot")
  await ctx.send(embed=help1)


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
  
  
@client.command()
async def c(ctx):
  date=str(datetime.date.today(+9))
  print(date)
  

@client.command()
async def stats(ctx):
  cell=ws.find(str(ctx.author.id+ctx.guild.id))
  b=ws.row_values(cell.row)
  msg = discord.Embed(title="stats",colour=0x1e90ff)
  msg.add_field(name="name", value=b[2], inline=False)
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
async def r(ctx,a,a2):
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
    date=str(datetime.date.today())
    ws2.append_row([date,str(ctx.guild.id),ctx.guild.name,a,a2])

    b[3]=int(b[3])+1
    a=int(a)
    if a>0:
      b[4]=int(b[4])+1      
    else:      
      b[5]=int(b[5])+1
    b[6]=int(b[4])*100//int(b[3])
  for i in range(7):
      ws.update_cell(cell.row,i+1,b[i])
  
  msg = await ctx.send("記録しました")
  await asyncio.sleep(3)
  await msg.delete()
  
  await ctx.channel.purge(limit=1)


@client.command()
async def teamstats(ctx):
  cell=ws.find(str(ctx.guild.id))
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
async def vs(ctx,a):
  w=0
  l=0
  b=''
  cell=ws2.findall(str(ctx.guild.id))
  for i in range(len(cell)):
    c=ws2.row_values(cell[i].row)
    if c[4]==a:
      if int(c[3])>0:
        w+=1
      else:
        l+=1
      b+=c[0]+" "+c[3]+"\n"
  b=f'戦績: vs {a} {w}-{l}\n'+b
  msg = await ctx.send(b)
  await asyncio.sleep(20)
  await msg.delete() 


@client.command()
async def teamreset(ctx):
  cell=ws.find(str(ctx.guild.id))
  for i in range(4):
    ws.update_cell(cell.row,i+4,0)
  msg = await ctx.send("リセットしました")
  await asyncio.sleep(3)
  await msg.delete()


@client.command()
async def teamdelete(ctx):
  cell=ws.find(str(ctx.guild.id))
  for i in range(4):
    ws.update_cell(cell.row,i+4,0)
  cell=ws2.findall(str(ctx.guild.id))
  for i in range(len(cell)):    
    ws2.delete_row(cell[len(cell)-i-1].row)
  msg = await ctx.send("リセットしました")
  await asyncio.sleep(3)
  await msg.delete()


@client.command()
async def history(ctx):
  b=''
  cell=ws2.findall(str(ctx.guild.id))
  a=min(len(cell),100)
  for i in range(a):
    c=ws2.row_values(cell[a-i-1].row)
    b+=c[4]+" "+c[3]+" , "
  b=f'戦績:\n'+b
  msg = await ctx.send(b)


@client.command()
async def teamrename(ctx):
  cell=ws.find(str(ctx.guild.id))
  ws.update_cell(cell.row,2,ctx.guild.name)
  msg = await ctx.send("名前を修正しました")
  await asyncio.sleep(3)
  await msg.delete()
"""

token = os.environ['DISCORD_BOT_TOKEN']
client.run(token)
