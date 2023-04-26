import boto3
from boto3.dynamodb.conditions import Key, Attr
import os
import discord
from discord.ext import commands
from dotenv import load_dotenv
import helper



load_dotenv('environment.env')
TOKEN = os.getenv('DISCORD_TOKEN')


intents = discord.Intents.default()
intents.message_content = True

# connect to the discord client
client = discord.Client(intents=intents)

# Testing models for discord message output
model = ["debugging message sending"]

bot = commands.Bot(command_prefix='$', intents = intents)


dynamodb = boto3.resource('dynamodb')
PSTable = dynamodb.Table("ProductivityScore-p4fhyzhl5zfxxp4oksg3k3kegy-dev")
ClassTable = dynamodb.Table ("Classes-p4fhyzhl5zfxxp4oksg3k3kegy-dev")


@bot.command(pass_context=True)
async def getProductivityScore(ctx, name):

    response = PSTable.scan()
    response_list = response['Items']

    for itemIdx, item in enumerate(response_list):
        if item['userName'] == name:
                PScore = (item['score'])
                message = str("""```Hi {name}, your productivity score is {score}```""".format(name=name, score=PScore))
                await ctx.send(message)
        else:
            await ctx.send("```oooops, user not found```")
            return
    


@bot.command(pass_context=True)
async def getPS(ctx, name):

    response = PSTable.scan()
    response_list = response['Items']

    for itemIdx, item in enumerate(response_list):
        if item['userName'] == name:
                PScore = (item['score'])
                message = str("""```Hi {name}, your productivity score is {score}```""".format(name=name, score=PScore))
                await ctx.send(message)
        else:
            await ctx.send("```oooops, user not found```")
            return

@bot.command(pass_context=True)
async def habithelp(ctx):
    # await ctx.send("https://e7.pngegg.com/pngimages/475/909/png-clipart-miss-kobayashi-s-dragon-maid-internet-meme-meme.png")
    # retStr = str("""```yaml\nThis is some colored Text```""")
    message = str("""On going construction command, up soon!""")
    await ctx.send(message)


@bot.command(pass_context=True)
async def getClass(ctx, name, className = None):
    # await ctx.send("https://e7.pngegg.com/pngimages/475/909/png-clipart-miss-kobayashi-s-dragon-maid-internet-meme-meme.png")
    # retStr = str("""```yaml\nThis is some colored Text```""")

    response = ClassTable.scan()
    response_dict = response['Items']
    # message = str("""On going construction command, up soon!""")

    classes = []
    progress = []
    goal = []

    for itemIdx, item in enumerate(response_dict):
        if item['username'] == name:
            classes.append(item['className'])
            progress.append(item['progress'])
            goal.append(item['goal'])
    # print(response_dict)
    message = ""
    for classinfo in zip(classes, progress, goal):
         message += str("""```Class: {classinfo[0]} Progress: {classinfo[1]} Goal: {classinfo[2]} \
            {percent}% \n```""".format(classinfo=classinfo, percent = helper.div_zero(classinfo[1], classinfo[2])*100))

    await ctx.send(message)




bot.run(TOKEN)

