import openai
import discord
import keys
import time

openai.api_key = keys.openai

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)


def ask_gpt(question, model):
    openai.api_key = keys.openai
    response = openai.ChatCompletion.create(
        model=model,
        messages=[
            {"role": "system", "content": f"You are a chatbot named '{keys.bot_name}'"},
            {"role": "user", "content": question},
        ]
    )

    result = ''
    for choice in response.choices:
        result += choice.message.content

    return (result)


async def reply_to_message(message, model):
    try:
        async with message.channel.typing():
            question = message.content.replace(
                keys.bot_discord_mention, "")
            answer = ask_gpt(question, model)
            await message.channel.send(answer)
    except Exception as e:
        print(e)
        print("sleeping 2 seconds and trying again")
        time.sleep(2)
        await reply_to_message(message, model)


def generate_image(chat_prompt):
    response = openai.Image.create(
        prompt=chat_prompt,
        n=1,
        size="1024x1024"
    )
    return response['data'][0]['url']


async def reply_with_image(message):
    try:
        async with message.channel.typing():
            chat_prompt = message.content.replace(
                keys.bot_discord_mention, "").replace("!generate", "")
            image_link = generate_image(chat_prompt)
            await message.channel.send(image_link)
    except Exception as e:
        print(e)
        if (str(e).find("request was rejected") > -1):
            await message.channel.send("Sorry I can't generate that")
        else:
            print("sleeping 2 seconds and trying again")
            time.sleep(2)
            await reply_with_image(message)


@client.event
async def on_message(message):
    print(message.content)
    if (message.content.find("!generate") == 0 and str(message.author.id) in keys.main_users):
        await reply_with_image(message)
    elif (message.content.find(keys.bot_discord_mention) > -1):
        await reply_to_message(message, "gpt-3.5-turbo")
    elif (isinstance(message.channel, discord.DMChannel) and str(message.author.id) in keys.main_users):
        await reply_to_message(message, "gpt-3.5-turbo")


@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')

client.run(keys.discord)
