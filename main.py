import boto3
from boto3.dynamodb.conditions import Key, Attr
import os
import discord
from discord.ext import commands
from dotenv import load_dotenv




load_dotenv('environment.env')
TOKEN = os.getenv('DISCORD_TOKEN')


intents = discord.Intents.default()
intents.message_content = True

# connect to the discord client
client = discord.Client(intents=intents)

# Testing models for discord message output
model = ["debugging message sending"]

bot = commands.Bot(command_prefix='$', intents = intents)

user_dict = {
    "katrinajurczyk": "316ab908-e03d-47db-9398-be75dc84bf43",
    "Jeff": "c8c2c905-f610-465b-90a9-127708e313d1",
    "ryansequeira": "6c227a8d-5155-4722-b635-7aee5615f346",
    "testuser1": "114afad1-8aad-4fe9-ad96-5bb73e0c5ab6",
    "tianlecai": "a421d4d3-ef9f-418a-9da0-addad5ccffa9"
}
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table("ProductivityScore-p4fhyzhl5zfxxp4oksg3k3kegy-dev")


@bot.command(pass_context=True)
async def getProductivityScore(ctx, name):
    # await ctx.send("https://e7.pngegg.com/pngimages/475/909/png-clipart-miss-kobayashi-s-dragon-maid-internet-meme-meme.png")
    # retStr = str("""```yaml\nThis is some colored Text```""")
    try:
        id = user_dict[name]
    except:
        await ctx.send("```oooops, user not found```")
        return

    response = table.query(
        KeyConditionExpression=Key('id').eq(id)
        # FilterExpression=Attr('<attr>').eq('<value>')
    )

    

    score = response['Items'][0]['score']
    print(score)
    message = str("""```Hi {name}, your productivity score is {score}```""".format(name=name, score=score))
    await ctx.send(message)

bot.run(TOKEN)
# DynamoDB

# print(response)

