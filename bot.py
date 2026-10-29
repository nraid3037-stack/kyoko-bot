import discord
from discord.ext import commands
import random
import json
import os

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

DATA_FILE = "economy_data.json"

def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

def save_data(data):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

@bot.event
async def on_ready():
    print(f"البوت {bot.user} شغال وجاهز!")

@bot.command(aliases=["bal", "رصيد"])
async def balance(ctx, member: discord.Member = None):
    member = member or ctx.author
    data = load_data()
    uid = str(member.id)
    bal = data.get(uid, {}).get("balance", 1000)
    await ctx.send(f"💰 رصيد {member.mention} هو: **{bal:,} 🪙**")

@bot.command(aliases=["رهان"])
async def bet(ctx, amount: int):
    data = load_data()
    uid = str(ctx.author.id)
    
    if uid not in data:
        data[uid] = {"balance": 1000}
        
    bal = data[uid]["balance"]
    
    if amount <= 0:
        await ctx.send("❌ يجب أن يكون المبلغ أكبر من صفر.")
        return
    if bal < amount:
        await ctx.send(f"❌ رصيدك غير كافٍ! رصيدك الحالي: **{bal:,} 🪙**")
        return
        
    won = random.choice([True, False])
    if won:
        data[uid]["balance"] += amount
        await ctx.send(f"🎉 مبروك! ربحت **{amount:,} 🪙**\nرصيد إجمالي: **{data[uid]['balance']:,} 🪙**")
    else:
        data[uid]["balance"] -= amount
        await ctx.send(f"💀 هاردلك! خسرت **{amount:,} 🪙**\nرصيدك الآن: **{data[uid]['balance']:,} 🪙**")
        
    save_data(data)

bot.run("MTU2NTM1NjIzNTgxMTcyMTMyOA.GfG3Ef.my3Eyk_g4XU7YutIG_ZozbtyqSj9NREWqMFW4s") 
