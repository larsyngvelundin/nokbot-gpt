import openai
import discord
import keys
import time

openai.api_key = keys.openai

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)


async def ask_gpt(question, model, message):
    openai.api_key = keys.openai
    history = []
    async for msg in message.channel.history(limit=50):
        agent = "assistant"
        if (msg.author.id == message.author.id):
            agent = "user"
        history.append({"role": agent, "content": msg.content})
        if (msg.content.find("and") != 0 and msg.content.find("And") != 0):
            if (message.author.id == msg.author.id):
                break
    messages = [
        {"role": "system", "content": f"You are a chatbot named '{keys.bot_name}'"}]
    for i in range(len(history)-1, -1, -1):
        messages.append(history[i])

    response = openai.ChatCompletion.create(
        model=model,
        messages=messages
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
            answer = await ask_gpt(question, model, message)
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


@ client.event
async def on_message(message):
    if (message.content.find("!generate") == 0 and str(message.author.id) in keys.main_users):
        await reply_with_image(message)
    elif (message.content.find(keys.bot_discord_mention) > -1):
        await reply_to_message(message, "gpt-3.5-turbo")
    elif (isinstance(message.channel, discord.DMChannel) and str(message.author.id) in keys.main_users):
        await reply_to_message(message, "gpt-3.5-turbo")


@ client.event
async def on_ready():
    print(f'We have logged in as {client.user}')

client.run(keys.discord)
