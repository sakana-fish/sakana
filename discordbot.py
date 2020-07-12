import discord
import datetime
import math
import os
import random
import asyncio
from discord.ext import commands
import gspread
import json
from oauth2client.service_account import ServiceAccountCredentials 

#https://ja.wikipedia.org/wiki/Unicode%E3%81%AEEmoji%E3%81%AE%E4%B8%80%E8%A6%A7

sheet = os.environ['SHEETKEY']
path = os.environ['MAIL']
scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']
credentials = ServiceAccountCredentials.from_json_keyfile_name(path, scope)
gc = gspread.authorize(credentials)
wb = gc.open_by_key(sheet)
ws = wb.worksheet("ラウンジ") 
ws2 = wb.worksheet("ラウンジ記録")  
ws3 = wb.worksheet("レポート記録")
ws4 = wb.worksheet("ランキング")  
ws5 = wb.worksheet("募集")
ws6 = wb.worksheet("募集2")  

#チャンネルid
chboshu=731849352586461235
chboshu2=731852560498950164
chbot=731842666517757992
chupdater=731842705877106780
chteam=731847503325954048
chmember=731847553766785034
chresult=731847038219714640
chreport=731847107853680770

roleud=731844890538934336


client = commands.Bot(command_prefix='.')

@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')  
    await client.change_presence(activity=discord.Game(name='おさかな天国'))

#-----------------------------------------------------
async def check(ctx,a):
  role = discord.utils.find(lambda r: r.name == a, ctx.guild.roles)
  print(role)
  print(ctx.author.roles)
  if role in ctx.author.roles:
    return True
  else:
    return False
"""
#-----------------------------------------------------
@client.command()
async def test(ctx):
  await ctx.channel.purge(limit=10)
"""
#-----------------------------------------------------
@client.command()
async def entry(ctx,a):
  if ctx.channel.id == chbot:
    try:
      list=ws.col_values(1)
      list.index(a)
    except:
      ws.append_row([a,1500,0,0,0,0,str(ctx.author.id),ctx.author.name,0,0,0,0,0,0])
      await ctx.guild.create_role(name=a)
      role = ctx.guild.get_role(roleud) #updaterの役職のIDを入力
      await ctx.message.author.add_roles(role)
      role = discord.utils.find(lambda r: r.name == a, ctx.guild.roles)
      await ctx.message.author.add_roles(role)
      #await ctx.channel.purge(limit=1)
      channel1 = client.get_channel(chteam) #チーム登録
      msg = await channel1.send(f"登録しました チーム: {a} 登録者 :{ctx.author.mention}")
    else:
      msg=await ctx.send(f"チーム {a} は既に登録済みです")
      await asyncio.sleep(3)
      await msg.delete()
      #await ctx.channel.purge(limit=1)
  else:
    msg=await ctx.send("エラー")
    await asyncio.sleep(3)
    await msg.delete()
    #await ctx.channel.purge(limit=1)

#-----------------------------------------------------
@client.command()
async def member(ctx,a):
  if ctx.channel.id == chbot:
    try:
      list=ws.col_values(1)
      row=list.index(a)+1
    except:
      msg=await ctx.send("エラー チーム名を確認してください")
      await asyncio.sleep(3)
      await msg.delete()
      #await ctx.channel.purge(limit=1) 
    else:
      rolecheck = await check(ctx,a)
      if rolecheck==True:
        msg=await ctx.send("既に登録済みです")
        await asyncio.sleep(3)
        await msg.delete()
        #await ctx.channel.purge(limit=1)
      else:
        data=ws.row_values(row)
        #if #登録人数が3名以内なら
        j=0
        for i in range(3):
          if data[2*i+6]=="0":
            j=2*i+7
            break

        if j==0:
          msg=await ctx.send("既に3名登録済みです")
          await asyncio.sleep(3)
          await msg.delete()
          #await ctx.channel.purge(limit=1)

        else:
          #await ctx.channel.purge(limit=1)
          role = ctx.guild.get_role(roleud) #updaterの役職のIDを入力
          await ctx.message.author.add_roles(role)
          role = discord.utils.find(lambda r: r.name == a, ctx.guild.roles)
          await ctx.message.author.add_roles(role)
          ws.update_cell(row,j,str(ctx.author.id))
          ws.update_cell(row,j+1,ctx.author.name)
          channel1 = client.get_channel(chmember) #メンバー登録
          msg=await channel1.send(f"登録しました チーム: {a} 登録者: {ctx.author.mention}")
  else:
    msg=await ctx.send("エラー")
    await asyncio.sleep(3)
    await msg.delete()
    #await ctx.channel.purge(limit=1)

#-----------------------------------------------------
@client.command()
async def deletemember(ctx,a):
  if ctx.channel.id == chupdater:
    rolecheck = await check(ctx,a)
    if rolecheck==False:
        msg=await ctx.send("メンバー登録されていません")
        await asyncio.sleep(3)
        await msg.delete()
        #await ctx.channel.purge(limit=1)
    else:
      list=ws.col_values(1)
      row=list.index(a)+1
      data=ws.row_values(row)
      for i in range(3):
        j=2*i+7
        if data[j-1]==str(ctx.author.id):
          ws.update_cell(row,j,0)
          ws.update_cell(row,j+1,0)
          try:
            ws.find(str(ctx.author.id))
          except:          
            role = ctx.guild.get_role(roleud) #updaterの役職のIDを入力
            await ctx.message.author.remove_roles(role)
          role = discord.utils.find(lambda r: r.name == a, ctx.guild.roles)
          await ctx.message.author.remove_roles(role)
          break
      
      #await ctx.channel.purge(limit=1)
      channel1 = client.get_channel(chmember) #メンバー登録
      msg=await channel1.send(f"登録解除しました チーム: {a} 解除者 :{ctx.author.mention}")
  else:
    msg=await ctx.send("エラー")
    await asyncio.sleep(3)
    await msg.delete()
    #await ctx.channel.purge(limit=1)

#-----------------------------------------------------
@client.command()
async def result(ctx,a,c,d):
  def is_int(s):
    try:
        int(s)
        if int(s)<0:
          return False
        return True
    except ValueError:
        return False
  
  if ctx.channel.id == chupdater:
    rolecheck = await check(ctx,a)
    if rolecheck==False:
      msg=await ctx.send("エラー 勝利チームが報告してください")
      await asyncio.sleep(3)
      await msg.delete()
      #await ctx.channel.purge(limit=1)
    else:
      try:
        list=ws.col_values(1)
        row=list.index(a)+1
        row2=list.index(c)+1
      except:
        msg=await ctx.send("エラー チーム名を確認してください")
        await asyncio.sleep(3)
        await msg.delete()
        #await ctx.channel.purge(limit=1)
      else:
        b=ws.row_values(row)
        b2=ws.row_values(row2)
        old=b[1]
        old2=b2[1]
        if is_int(d)==False:
          msg = await ctx.send("エラー 点差を確認してください")
          await asyncio.sleep(3)
          await msg.delete()
        else:
          msg=await ctx.send("集計中")
          b[4]=int(b[4])+1
          b2[4]=int(b2[4])+1
          d=int(d)
          if d==0:
            b[3]=int(b[3])+1
            b2[3]=int(b2[3])+1
          else:      
            b[2]=int(b[2])+1
            b2[3]=int(b2[3])+1
          W=1/(pow(10,(int(b[1])-int(b2[1]))/400)+1)
          if d==0:
            e=e=math.floor(100*W)
          else:
            e=math.floor(100*W*(1+pow(d/200,2))) #レートの計算式、いい式を募集
          b[1]=int(b[1])+e
          b2[1]=int(b2[1])-e
          b[5]=int(b[2])*100//int(b[4])
          b2[5]=int(b2[2])*100//int(b2[4])
          b[13]=b[12]
          b[12]=c
          b2[13]=b2[12]
          b2[12]=a
          for i in range(14):
            ws.update_cell(row,i+1,b[i])
          for i in range(14):
            ws.update_cell(row2,i+1,b2[i])          
          time = str(datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=9))))
          ws2.append_row([len(ws2.col_values(1)),time,a,c,d,e,old,old2,b[1],b2[1]])
          await msg.delete()
          #await ctx.channel.purge(limit=1)
          role = discord.utils.find(lambda r: r.name == a, ctx.guild.roles)
          role2 = discord.utils.find(lambda r: r.name == c, ctx.guild.roles)
          role='<@&'+str(role.id)+'>'
          role2='<@&'+str(role2.id)+'>'
          embed=discord.Embed(title="result",color=0x000000)
          text=f"{a} vs {c} (点差: {d} 点)"
          embed.add_field(name=f"No. {len(ws2.col_values(1))-1}", value=text, inline=False) 
          text2=f"{a}: {old} → {b[1]}\n{c}: {old2} → {b2[1]}"
          embed.add_field(name=f"レート変動 (±{e})", value=text2, inline=False)      
          embed.add_field(name=f"報告者", value=ctx.author.mention, inline=False)
          channel1 = client.get_channel(chresult) #リザルト      
          await channel1.send(embed=embed)
          msg = await channel1.send(f"記録しました 結果に誤りがある場合は報告してください {role} {role2}")
          await asyncio.sleep(10)
          await msg.delete()
  else:
    msg=await ctx.send("エラー")
    await asyncio.sleep(3)
    await msg.delete()
    #await ctx.channel.purge(limit=1)

#-----------------------------------------------------
@client.command()
async def revise(ctx,n):
  if ctx.channel.id == chupdater:
    try:
      list=ws2.col_values(1)
      row=list.index(str(int(n)))+1
      b=ws2.row_values(row)
      rolecheck1=await check(ctx,b[2])
      rolecheck2=await check(ctx,b[3])
      if rolecheck1==False and rolecheck2==False:
        msg = await ctx.send("対戦番号を確認してください")
        await asyncio.sleep(3)
        await msg.delete()
        #await ctx.channel.purge(limit=1)
      elif int(b[5]) < 0:
        msg = await ctx.send("修正の修正はできません")
        await asyncio.sleep(3)
        await msg.delete()
        #await ctx.channel.purge(limit=1)
      else:
        msg=await ctx.send("修正中")
        a=b[2]
        c=b[3]
        d=int(b[4])
        e=int(b[5])
        list=ws.col_values(1)
        row=list.index(a)+1
        row2=list.index(c)+1
        b=ws.row_values(row)
        b2=ws.row_values(row2)
        old=b[1]
        old2=b2[1]
        b[4]=int(b[4])-1
        b2[4]=int(b2[4])-1
        if d==0:
          b[3]=int(b[3])-1
          b2[3]=int(b2[3])-1
        else:      
          b[2]=int(b[2])-1
          b2[3]=int(b2[3])-1
        b[1]=int(b[1])-e
        b2[1]=int(b2[1])+e
        if int(b[2])==0:
          b[5]=0
        else:
          b[5]=int(b[2])*100//int(b[4])
        if int(b2[2])==0:
          b2[5]=0
        else:
          b2[5]=int(b2[2])*100//int(b2[4])
        for i in range(14):
          ws.update_cell(row,i+1,b[i])
        for i in range(14):
          ws.update_cell(row2,i+1,b2[i])          
        time = str(datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=9))))
        ws2.append_row([len(ws2.col_values(1)),time,a,c,-d,-e,old,old2,b[1],b2[1]])
        await msg.delete()
        #await ctx.channel.purge(limit=1)
        role = discord.utils.find(lambda r: r.name == a, ctx.guild.roles)
        role2 = discord.utils.find(lambda r: r.name == c, ctx.guild.roles)
        role='<@&'+str(role.id)+'>'
        role2='<@&'+str(role2.id)+'>'
        embed=discord.Embed(title="revision",color=0xff0000)
        text=f"{a} vs {c} (点差: {d} 点)"
        embed.add_field(name=f"No. {len(ws2.col_values(1))-1} : No. {n}の修正", value=text, inline=False) 
        text2=f"{a}: {old} → {b[1]}\n{c}: {old2} → {b2[1]}"
        embed.add_field(name=f"レート変動 ({-1*e})", value=text2, inline=False)  
        embed.add_field(name=f"報告者", value=ctx.author.mention, inline=False)
        channel1 = client.get_channel(chresult) #リザルト     
        await channel1.send(embed=embed)
        msg = await channel1.send(f"修正しました。誤りがある場合は報告してください {role} {role2}")
        await asyncio.sleep(10)
        await msg.delete()
    except:
      msg = await ctx.send("エラー")
      await asyncio.sleep(10)
      await msg.delete()

#-----------------------------------------------------
@client.command()
async def stats(ctx,a):
  if ctx.channel.id == chbot:
    list=ws.col_values(1)
    row=list.index(a)+1
    b=ws.row_values(row)
    c=ws4.row_values(row)
    msg = discord.Embed(title="stats",colour=0x1e90ff)
    msg.add_field(name="name", value=b[0], inline=True)
    msg.add_field(name="rate", value=b[1], inline=True)
    msg.add_field(name="rank", value=c[2], inline=True)
    msg.add_field(name="play", value=b[4], inline=True)
    msg.add_field(name="win rate", value=b[5]+"%", inline=True)
    #await ctx.channel.purge(limit=1)
    msg = await ctx.send(embed=msg)  
    await asyncio.sleep(15)
    await msg.delete()

#-----------------------------------------------------
@client.command()
async def ranking(ctx):
  if ctx.channel.id == chbot:
    text=""
    for i in range(10):
      c=ws4.row_values(2+i)
      text+=f"{c[6]} | {c[5]} {c[4]}\n"
    msg = discord.Embed(title="ranking",colour=0x1e90ff,description=text)
    #await ctx.channel.purge(limit=1)
    msg = await ctx.send(embed=msg)  
    await asyncio.sleep(15)
    await msg.delete()

#-----------------------------------------------------
@client.command()
async def history(ctx,a):
  if ctx.channel.id == chbot:
    list=ws2.col_values(3)
    row=[i for i, x in enumerate(list) if x == a]
    list=ws2.col_values(4)
    row2=[i for i, x in enumerate(list) if x == a]
    row3=row+row2
    c=''
    row3.sort()
    d=min(len(row3),100)
    for i in range(d):
      b=ws2.row_values(row3[len(row3)-i-1]+1)
      if row3[i] in row:
        c+="No. "+b[0]+", " +b[3]+" +" +str(b[4])+" | "
      else:
        c+="No. "+b[0]+", " +b[2]+" -" +str(b[4])+" | "
    c=f'チーム {a} 戦績:\n'+c
    #await ctx.channel.purge(limit=1)
    msg = await ctx.send(c)  
    await asyncio.sleep(30)
    await msg.delete()

#-----------------------------------------------------
@client.command()
async def report(ctx,a):
  #違反した人を報告する
  if ctx.channel.id == chupdater:    
    b=a.replace('<','')
    b=b.replace('!','')
    b=b.replace('&','')
    b=b.replace('@','')
    b=b.replace('>','')
    c=client.get_user(int(b))
    #await ctx.channel.purge(limit=1)
    if c=='None':
      msg = await ctx.send('エラー')  
      await asyncio.sleep(3)
      await msg.delete()
    else:
      channel1 = client.get_channel(chreport) #レポート
      msg = await channel1.send(f"{ctx.author.mention}が{a}を報告しました")
      try:
        list=ws3.col_values(1)
        row=list.index(str(c.id))+1
        b=ws3.row_values(row)
      except ValueError:
        ws3.append_row([str(c.id),c.name,1,str(ctx.author.id)])
      else:
        b[2]=int(b[2])+1
        b.append(str(ctx.author.id))
        ws3.update_cell(row,3,b[2])
        ws3.update_cell(row,len(b),b[len(b)-1])
  else:
    msg=await ctx.send("エラー")
    await asyncio.sleep(3)
    await msg.delete()
    #await ctx.channel.purge(limit=1)

#-----------------------------------------------------
@client.command()
async def c(ctx,a,n):
  def is_int(s):
    try:
        int(s)
        if int(s)>0 and int(s)<500:
          return True
        return False
    except ValueError:
        return False

  if ctx.channel.id == chupdater:
    await ctx.channel.purge(limit=1)
    rolecheck = await check(ctx,a)
    if rolecheck==False:
      msg=await ctx.send("エラー チーム名を確認してください")
      await asyncio.sleep(3)
      await msg.delete()
    else:
      if is_int(n)==False:
        msg=await ctx.send("エラー レート差を確認してください")
        await asyncio.sleep(3)
        await msg.delete()
      else:
        try:
          list2=ws5.col_values(1)
          row=list2.index(a)+1
        except:
          now=datetime.datetime.now()
          now=now.day*24*60+now.hour*60+now.minute
          n=int(n)
          list=ws.col_values(1)
          row=list.index(a)+1    
          b=ws.row_values(row)
          min=int(b[1])-n
          max=int(b[1])+n
          d=0
          e=0
          for i in range(len(list2)-1):
            b2=ws5.row_values(i+2)
            if abs(now-int(b2[8]))>60:#
              ws5.delete_row(i+2)
              e+=1
            else:
              if b2[5]==a or b2[6]==a:
                pass
              else:
                if min<int(b2[1]) and int(b2[1])<max and int(b2[2])<int(b[1]) and int(b[1])<int(b2[3]):
                  channel1 = client.get_channel(chboshu)
                  await channel1.send(f"対戦相手が決まりました\n{b2[0]} vs {a} {b2[5]} {ctx.author.mention}" )
                  await channel1.send(f"{len(list2)-2-e}チームが募集中" )
                  d=1
                  ws5.delete_row(i+2)
                  break
          if d==0:
            ws5.append_row([a,b[1],min,max,str(ctx.author.id),ctx.author.mention,b[12],b[13],now])
            channel1 = client.get_channel(chboshu)
            msg = await channel1.send(f"募集開始しました {len(list2)-e}チームが募集中")
        else:
          msg=await ctx.send(f"募集中です")
          await asyncio.sleep(3)
          await msg.delete()
          #await ctx.channel.purge(limit=1)

#-----------------------------------------------------
@client.command()
async def d(ctx,a):
  if ctx.channel.id == chupdater:
    await ctx.channel.purge(limit=1)
    rolecheck = await check(ctx,a)
    if rolecheck==False:
      msg=await ctx.send("エラー チーム名を確認してください")
      await asyncio.sleep(3)
      await msg.delete()
    else:
      try:
        list2=ws5.col_values(1)
        row=list2.index(a)+1
      except:
        msg=await ctx.send(f"募集していません")
        await asyncio.sleep(3)
        await msg.delete()
      else:
        ws5.delete_row(row)
        msg=await ctx.send(f"募集を取り消しました")
        await asyncio.sleep(3)
        await msg.delete()
        channel1 = client.get_channel(chboshu)
        await channel1.send(f"{len(list2)-2}チームが募集中")

#-----------------------------------------------------
@client.command()
async def c2(ctx,a,n):
  def is_int(s):
    try:
        int(s)
        if int(s)>0 and int(s)<500:
          return True
        return False
    except ValueError:
        return False

  if ctx.channel.id == chupdater:
    await ctx.channel.purge(limit=1)
    rolecheck = await check(ctx,a)
    if rolecheck==False:
      msg=await ctx.send("エラー チーム名を確認してください")
      await asyncio.sleep(3)
      await msg.delete()
    else:
      if is_int(n)==False:
        msg=await ctx.send("エラー レート差を確認してください")
        await asyncio.sleep(3)
        await msg.delete()
      else:
        try:
          list2=ws6.col_values(1)
          row=list2.index(a)+1
        except:
          now=datetime.datetime.now()
          now=now.day*24*60+now.hour*60+now.minute
          n=int(n)
          list=ws.col_values(1)
          row=list.index(a)+1    
          b=ws.row_values(row)
          min=int(b[1])-n
          max=int(b[1])+n
          d=0
          e=0
          for i in range(len(list2)-1):
            b2=ws6.row_values(i+2)
            if abs(now-int(b2[8]))>60:#
              ws6.delete_row(i+2)
              e+=1
            else:
              if b2[5]==a or b2[6]==a:
                pass
              else:
                if min<int(b2[1]) and int(b2[1])<max and int(b2[2])<int(b[1]) and int(b[1])<int(b2[3]):
                  channel1 = client.get_channel(chboshu2)
                  await channel1.send(f"対戦相手が決まりました\n{b2[0]} vs {a} {b2[5]} {ctx.author.mention}" )
                  await channel1.send(f"{len(list2)-2-e}チームが募集中" )
                  d=1
                  ws6.delete_row(i+2)
                  break
          if d==0:
            ws6.append_row([a,b[1],min,max,str(ctx.author.id),ctx.author.mention,b[12],b[13],now])
            channel1 = client.get_channel(chboshu2)
            msg = await channel1.send(f"募集開始しました {len(list2)-e}チームが募集中")
        else:
          msg=await ctx.send(f"募集中です")
          await asyncio.sleep(3)
          await msg.delete()
          #await ctx.channel.purge(limit=1)

#-----------------------------------------------------
@client.command()
async def d2(ctx,a):
  if ctx.channel.id == chupdater:
    await ctx.channel.purge(limit=1)
    rolecheck = await check(ctx,a)
    if rolecheck==False:
      msg=await ctx.send("エラー チーム名を確認してください")
      await asyncio.sleep(3)
      await msg.delete()
    else:
      try:
        list2=ws6.col_values(1)
        row=list2.index(a)+1
      except:
        msg=await ctx.send(f"募集していません")
        await asyncio.sleep(3)
        await msg.delete()
      else:
        ws6.delete_row(row)
        msg=await ctx.send(f"募集を取り消しました")
        await asyncio.sleep(3)
        await msg.delete()
        channel1 = client.get_channel(chboshu2)
        await channel1.send(f"{len(list2)-2}チームが募集中")

#-----------------------------------------------------


token = os.environ['DISCORD_BOT_TOKEN']
client.run(token)
