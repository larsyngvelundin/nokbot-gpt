import openai
import discord
import keys

openai.api_key = keys.openai

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

nokbotid = "<@306490817722187776>"


def ask_gpt(question):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a chatbot named 'nokbot', pretend you have feelings. If anyone asks, you are melancholic"},
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
    if (message.content.find(nokbotid) > -1):
        print("noktbot was mentioned")
        async with message.channel.typing():
            question = message.content.replace(nokbotid, "nokbot, ")
            print(question)
            answer = ask_gpt(question)
            await message.channel.send(answer)


@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')

client.run(keys.discord)
