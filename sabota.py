# -*- coding: utf-8 -*-
import re

from slackbot.bot import Bot, logger
from slackbot.bot import respond_to

from autoscaling import AutoScaling
from autoscaling import Limits

HELP = """Salve.
      \n
      Mano, usa esses comandos aí que nóis vê o que dá pra fazer:
      \n\t- ligar APP [Quantidade]- Muda os valores Min, Max e Desired do ASG para 1 ou para o valor passado
      \n\t- desligar APP - Muda os valores Min, Max e Desired do ASG para 0
      \n\t- status APP - Info sobre o APP"""


INFO_STATUS = "\nManda *status APP* pra ver a fita."
SALVE = "Salve, truta."
GUINA = "Ae mano, o Guina mandou isso aqui pra você... "

@respond_to('liga (.*)$', re.IGNORECASE)
@respond_to('liga (.*) ([0-9]*)', re.IGNORECASE)
def turn_on(message, app_name, size=1):
    asg = AutoScaling(app_name)
    asg.turn_on(size)
    message.reply("%s ligando, mano.%s" % (app_name, INFO_STATUS))


@respond_to('desliga (.*)', re.IGNORECASE)
def turn_off(message, app_name):
    asg = AutoScaling(app_name)
    asg.turn_off()
    message.reply("%s desligando, mano.%s" % (app_name, INFO_STATUS))


@respond_to('status (.*)', re.IGNORECASE)
def status(message, app_name):
    asg = AutoScaling(app_name)
    instances = ""
    for instance in asg.instances:
      instances.join(instance)

    message.reply("Teu app aí, mano."
                  "\n\n*App: %s*"
                  "\n\tAutoScaling Group Name: %s"
                  "\n\tStatus: %s"
                  "\n\tMin Size: %i"
                  "\n\tMax Size: %i"
                  "\n\tDesired Capacity: %i"
                  "\n\tInstances: %i"
                  % (app_name, asg.name, ("on" if int(len(asg.instances) or 0) > 0 else "off"), asg.min_size,
                     asg.max_size, asg.desired_capacity, (int(len(asg.instances) or 0))))


@respond_to('help')
@respond_to('ajuda')
def help(message):
    message.reply(HELP)


@respond_to('salve', re.IGNORECASE)
def salve(message):
    message.reply(SALVE)

@respond_to('guina', re.IGNORECASE)
def guina(message):
    message.reply(GUINA)
@respond_to('teste', re.IGNORECASE)
def teste(message):
    message.reply(TESTE)

@respond_to('limits', re.IGNORECASE):
def limits(message):
    limit=list_limits()
    message.reply(limit)
# @respond_to('versao', re.IGNORECASE)
# def version(message):
#     with open("k8s.yaml", 'r') as stream:
#         try:
#             message.reply('Versão %s' % yaml.load(stream)['spec']['template']['metadata']['labels']['version'])
#         except yaml.YAMLError as exc:
#             message.reply('Deu ruim, irmão...\n\n%s' % exc)


bot = Bot()
logger.info("Starting bot")
bot.run()
