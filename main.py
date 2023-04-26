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
    response = ClassTable.scan()
    response_list = response['Items']

    PSdict = helper.calculateprogress(response_list)

    try:
        message = str("""```Hi {name}, your productivity score is {score}```""".format(name=name, score=PSdict[name]))
        await ctx.send(message)
    except:
        await ctx.send("```oooops, user not found```")
    


@bot.command(pass_context=True)
async def getPS(ctx, name):

    response = ClassTable.scan()
    response_list = response['Items']

    PSdict = helper.calculateprogress(response_list)

    try:
        message = str("""```Hi {name}, your productivity score is {score}```""".format(name=name, score=PSdict[name]))
        await ctx.send(message)
    except:
        await ctx.send("```oooops, user not found```")

@bot.command(pass_context=True)
async def getLeaderboard(ctx):
    response = ClassTable.scan()
    response_list = response['Items']

    PSdict = helper.calculateprogress(response_list)
    sortedPSdict = sorted(PSdict.items(), key=lambda x: x[1], reverse=True)

    message = ""
    for itemIdx, (k,v) in enumerate(sortedPSdict):

        message += str("""```Rank {rank}: {name} \nProductivity Score:{score}```""".format(rank=itemIdx+1, name=k, score=v))

    await ctx.send(message)




@bot.command(pass_context=True)
async def getClass(ctx, name, className = None):

    response = ClassTable.scan()
    response_dict = response['Items']
    # message = str("""On going construction command, up soon!""")

    classes = []

    for itemIdx, item in enumerate(response_dict):
        if item['username'] == name:
            classes.append(item['className'])
    # print(response_dict)
    message = ""
    for classinfo in zip(classes):
         message += str("""```Class: {classinfo[0]}\n```""".format(classinfo=classinfo))

    await ctx.send(message)


@bot.command(pass_context=True)
async def getProgress(ctx, name, className = None):

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
    # for classinfo in zip(classes, progress, goal):
    #      message += str("""```Class: {classinfo[0]} Progress: {classinfo[1]} Goal: {classinfo[2]} \
    #         {percent}% \n```""".format(classinfo=classinfo, percent = helper.div_zero(classinfo[1], classinfo[2])*100))

    for classinfo in zip(classes, progress, goal):
         message += str("""```Class: {classinfo[0]} \
            {percent}% \n```""".format(classinfo=classinfo, percent = helper.div_zero(classinfo[1], classinfo[2])*100))

    await ctx.send(message)

@bot.command(pass_context=True)
async def getGoalProgress(ctx, name, className = None):

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

