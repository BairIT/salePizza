import telebot
from transitions import Machine
import config
import sale_pizza

bot = telebot.TeleBot(config.token)

sale_user = sale_pizza.sale_class()
machine = Machine(sale_user, states=sale_user.states, transitions=sale_user.transitions, initial='sale_pizza')


################################ begin ################################
@bot.message_handler(commands=['start'])
def start_message(message):
    first_name = message.from_user.first_name
    bot.send_message(message.chat.id, f'Привет, {first_name} , я бот, погнали')
    machine.set_state('sale_pizza')
    bot.send_message(message.chat.id, 'Какую вы хотите пиццу "большую" или "маленькую" ')
    print('sale_user.state - 1 : ', sale_user.state)


############################# sale_pizza ####################################
@bot.message_handler(func=lambda message: True)
def small_or_big(message):
    print('sale_user.state на функции проверки состояния sale_pizza: ', sale_user.state)
    answer = message.text.lower()
    print(answer)
    if sale_user.state == 'sale_pizza':
        sale_user.answers = []
        if answer =='нет':
            start_message(message)
        elif sale_user.smallorbig(answer):
            bot.send_message(message.chat.id, 'Выберите способ оплаты, введите: \"картой\" или \"наличкой\"')
        else:
            bot.send_message(message.chat.id, 'Попробуйте еще раз, "большую" или "маленькую" пиццу, '
                                              'для отмены - нет')
    else:
        cash_or_nocash(message)


################################  payment  #########################################
@bot.message_handler(func=lambda message: True)
def cash_or_nocash(message):
    print('sale_user.state  - на функции проверки состояния payment: ', sale_user.state)
    if sale_user.state == 'payment':
        answer2 = message.text.lower()
        print(answer2)
        if sale_user.cashnocash(answer2):
            bot.send_message(message.chat.id,
                         f'Вы хотите {sale_user.answers[0]} пиццу, оплата - {sale_user.answers[1]}? или "нет"')
        else:
            bot.send_message(message.chat.id, '"Большую" или "маленькую" пиццу, для отмены - нет')
            sale_user.to_sale_pizza()
    else:
        on_clarification(message)


########################  clarification ################################################
@bot.message_handler(func=lambda message: True)
def on_clarification(message):
    print('sale_user.state - на функции проверки состояния clarification: ', sale_user.state)
    if sale_user.state == 'clarification':
        answer3 = message.text.lower()
        print(answer3)
        if answer3 == 'да':
            sale_user.to_order()
            order(message)
            bot.send_message(message.chat.id, 'Cпасибо за заказ')
        elif answer3 == 'нет':
            bot.send_message(message.chat.id, 'тип оплаты: "картой" или "наличкой?", для отмены - нет')
            sale_user.to_payment()
        else:
            bot.send_message(message.chat.id, 'да или нет?')
    else:
        print('END')


@bot.message_handler(func=lambda message: True)
def order(message):
    print('sale_user.state - на функции проверки состояния order: ', sale_user.state)
    bot.send_message(message.chat.id, ' Удачи , для старта наберите /start')


bot.polling(none_stop=True, interval=0)