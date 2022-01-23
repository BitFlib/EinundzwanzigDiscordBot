from discord.ext import commands
import os
import random
import tips
import time
import ln
import price
import env

TOKEN = env.DISCORD_TOKEN

# Initialize Bot and Denote The Command Prefix
bot = commands.Bot(command_prefix="!")

# Runs when Bot Succesfully Connects
@bot.event
async def on_ready():
    print(f'{bot.user} succesfully logged in!')


@bot.event
async def on_message(message):
    if message.author == bot.user: 
        return
    

    if "Steuern" in message.content:
        await message.reply("Steuern sind Raub!")
    if "Ethereum" in message.content:
        msg= await message.reply("Sei kein Holger!")
    

    """
    Tip related commands below
    """
    
    if "!send" in message.content:
        try:
            zahlung = tips.send_user(str(message.author.id), str(message.mentions[0].id), int(message.content.split(" ")[2]))
            if zahlung == 1:
                await message.reply("Zahlung fehlgeschlagen! Hast du genug Geld?")
            else:
                await message.reply("Zahlung erfolgreich!")
        except:
            await message.reply('Fehlerhafte Eingabe')
    if "!deposit" in message.content:
        try:
            amount = message.content.split(" ")[1]
            invoice = ln.get_invoice(amount)
            await message.reply("Bitte zahle die folgende Invoice innerhalb der nächsten 30 Sekunden " + invoice[0])
            time.sleep(30)
            if ln.check_invoice(invoice[1]) == True:
                tips.deposit(amount)
                await message.reply("Zahlung getätigt!")
            else:
                await message.reply("Zahlung nicht erhalten! Bitte nutze eine neue Invoice!")
                await message.delete(message)
        except:
            await message.reply('Fehlerhafte Eingabe')
 
    if "!pay" in message.content:
        try:
            await message.reply("Funktion noch in Arbeit. Bitte schicke Ole eine Nachricht damit er dir das Auszahlen kann.")
            #invoice = message.content.split(" ")[1]
        
            #balance = tips.get_balance(message.author.id)
            #if int(ln.get_invoice_amount(invoice)) <= int(balance):
            #    ln.pay_invoice(invoice)
            #    await message.reply("Zahlung erfolgreich!")
        except:
            await message.reply("Auszahlung fehlgeschlagen")

    if "!balance" in message.content:
        await message.reply("Dein Kontostand beträgt " + str(tips.get_balance(str(message.author.id))) + " Sats" )


    """
    Price related commands below
    """
    if message.content.startswith('!preis'):
        await message.reply('Der aktuelle Preis beträgt: ' + str(price.get_price_euro()) + ' €/BTC')
    
    if message.content.startswith('!euroinsats'):
        try:
            euro_amount = int(message.content.split(" ")[1])
        except:
            await message.reply('Fehlerhafte Eingabe')
            return
        await message.reply(str(euro_amount) + '€ sind aktuell ' + str(price.get_sats_per_euro(euro_amount)) + ' sats.')
    
    if message.content.startswith('!satsineuro'):
        try:
            sats_amount = int(message.content.split(" ")[1])
        except:
            await message.reply('Fehlerhafte Eingabe')
            return
        await message.reply(str(sats_amount) + ' sats sind aktuell ' + str("{:.2f}".format(price.get_euro_per_sats(sats_amount))) + '€.')
    
bot.run(TOKEN)