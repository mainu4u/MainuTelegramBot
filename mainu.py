# -*- coding: utf-8 -*-
import telebot
import logging
import requests
import utils.logger as log

ROOT = ''  # ${ROOT_PATH} for production mode

TOKEN = open(ROOT + 'sens_data/token', 'r').read()[:-1]

bot = telebot.TeleBot(TOKEN)

log.setup(ROOT)
logger = logging.getLogger(__name__)

#############################################
# Listener
#############################################


def listener(msgs):
    for m in msgs:
        if m.content_type == 'text':
            logger.info("%s (%d) ha dicho: %s" % (m.chat.first_name, m.chat.id,
                                                  m.text))
        else:
            logger.info("%s (%d) ha enviado algo que no es texto." %
                        (m.chat.first_name, m.chat.id))


bot.set_update_listener(listener)

#############################################
# MainU Telegram Bot
#############################################


@bot.message_handler(commands=['start', 'help'])
def welcome(m):
    logger.info("Devuelve el saludo")
    id = m.chat.id
    bot.send_message(id, "\U0001F44B ¡Hola! Soy el bot de MainU. Utilizo la "
                         "API pública de mainu.eus para ofrecerte servicios "
                         "relacionados con la cafetería de la Escuela de "
                         "Ingeniería de Bilbao. Estos son mis comandos:\n\n"
                         "/menu \U0001F449 Te diré qué tenemos de menú."
                         "/bocadillos \U0001F449 Te pasaré una lista de todos "
                         "los bocadillos con sus precios (prepárate, porque "
                         "es larga)")


@bot.message_handler(commands=['menu'])
def menu(m):
    logger.info("Devuelve el menú del día")
    id = m.chat.id
    r = requests.get("https://api.mainu.eus/menu")
    m = r.json()
    bot.send_message(id, "\U0001F35D *Primeros:*\n" +
                         "- %s\n" % (m['primeros'][0]['nombre']) +
                         "- %s\n" % (m['primeros'][1]['nombre']) +
                         "- %s\n\n" % (m['primeros'][2]['nombre']) +
                         "\U0001F357 *Segundos:*\n" +
                         "- %s\n" % (m['segundos'][0]['nombre']) +
                         "- %s\n" % (m['segundos'][1]['nombre']) +
                         "- %s\n\n" % (m['segundos'][2]['nombre']) +
                         "\U0001F370 *Postre:*\n" +
                         "- %s" % (m['postre'][0]['nombre']),
                         parse_mode="markdown")


@bot.message_handler(commands=['bocadillos'])
def bocadillos(m):
    logger.info("Devuelve una lista de bocadillos")
    id = m.chat.id
    r = requests.get("https://api.mainu.eus/bocadillos")
    bocs = r.json()
    bocadillos = ""
    for b in bocs:
        bocadillos = (bocadillos + '*' + b['nombre'] + '*: ' +
                      str(b['precio']) + ' €\n')
    bot.send_message(id, bocadillos[:-1], parse_mode="markdown")


@bot.message_handler(content_types=['text'])
def text(m):
    logger.info("Contesta a un texto sin comando")
    id = m.chat.id
    bot.send_message(id, "Si necesitas ayuda, escribe /help.")


bot.polling(True)
