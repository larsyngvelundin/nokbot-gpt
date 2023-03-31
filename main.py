import openai
import discord
import keys

openai.api_key = keys.openai

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)


def ask_gpt(question):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": f"You are a chatbot named '{keys.bot_name}'"},
            {"role": "user", "content": question},
        ]
    )

    result = ''
    for choice in response.choices:
        result += choice.message.content

    return (result)


@client.event
async def on_message(message):
    print(message.content)
    if (message.content.find(keys.bot_discord_mention) > -1 or (isinstance(message.channel, discord.DMChannel) and str(message.author.id) == keys.main_user)):
        async with message.channel.typing():
            question = message.content.replace(keys.bot_discord_mention, "")
            answer = ask_gpt(question)
            await message.channel.send(answer)


@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')

client.run(keys.discord)
