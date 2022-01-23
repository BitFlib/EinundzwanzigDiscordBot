import discord
from discord.ext import commands
import os
import random
import tips
import time
import ln
import price
import env
import qrcode
from PIL import Image

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
    
    if "!help" in message.content:
        await message.reply("""!send @User <betrag>
!deposit <betrag>
!withdraw <invoice> (Work in Progress)
!preis
!euroinsats <eur>
!satsineuro <sats>
!sats <eur/chf/usd> <betrag>
!eur/chf/usd <sats>
!moskauzeit""")
    
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
        
        amount = message.content.split(" ")[1]
        invoice = ln.get_invoice(amount)
        img = qrcode.make(invoice[0])
        img.save("qr.png")
        await message.reply("Bitte zahle die folgende Invoice innerhalb der nächsten 30 Sekunden " + invoice[0],file=discord.File('qr.png'), delete_after=30)
        time.sleep(30)
        if ln.check_invoice(invoice[1]) == True:
            tips.deposit(message.author.id, amount)
            await message.reply("Zahlung getätigt!")
        else:
            await message.reply("Zahlung nicht erhalten! Bitte nutze eine neue Invoice!")
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
        await message.reply("Dein Kontostand beträgt " + str(tips.get_balance(str(message.author.id))) + " Sats", delete_after=30)


    """
    Price related commands below
    """

    if message.content.startswith("!preis"):
        """
        Will return the current BTC price in USD, EUR, CHF
        parameters: none
        example: !preis
        """
        price_usd,price_eur,price_chf = price.get_prices()
        msg = "Aktueller Preis:\n\t" + str("{:,.2f}".format(price_usd)) + " USD/BTC\n\t" \
            + str("{:,.2f}".format(price_eur)) + " EUR/BTC\n\t" \
            + str("{:,.2f}".format(price_chf)) + " CHF/BTC"
        await message.reply(msg)

    if message.content.startswith("!sats"):
        """
        Will return the amount of sats for a given currency and currency amount
        parameters: [1]: currency, [2]: currency_amount
        example: !sats eur 420.69
        """
        try:
            currency = str(message.content.split(" ")[1])
            if(currency.upper() == "EUR") or (currency.upper() == "CHF") or (currency.upper() == "USD"):
                currency = currency.upper()
            else:
                raise ValueError()
            currency_amount = float(message.content.split(" ")[2])
        except:
            await message.reply("Fehlerhafte Eingabe")
            return
        msg = str("{:,.2f}".format(currency_amount)) + " " + str(currency) + " sind aktuell " \
            + str("{:,.0f}".format(price.get_sats_per_currency(currency,currency_amount))) + " sats."
        await message.reply(msg)
    
    if message.content.startswith('!eur') or message.content.startswith('!chf') or message.content.startswith('!usd'):
        """
        Will return the amount of given currency (dependend on command) for a given amount of sats
        parameters: [1]: sats_amount
        example: !usd 100000
        """
        try:
            currency = message.content[1:4].upper()
            sats_amount = int(message.content.split(" ")[1])
        except:
            await message.reply("Fehlerhafte Eingabe")
            return
        msg = str(sats_amount) + " sats sind aktuell " \
            + str("{:.2f}".format(price.get_currency_per_sats(currency, sats_amount))) + " " + currency + "."
        await message.reply(msg)

    if message.content.startswith("!moskauzeit") or message.content.startswith("!mz"):
        """
        Will return the current moscow time (and also coresponding eur/chf counterpart)
        parameters: none
        example: !mz
        """
        mt_usd, mt_eur, mt_chf = price.moscow_time()
        msg = "Moskau Zeit:\n\t" + str(mt_usd) + " sats/USD\n\t" \
                    + str(mt_eur) + " sats/EUR\n\t" \
                    + str(mt_chf) + " sats/CHF"
        await message.reply(msg)
    
bot.run(TOKEN)
