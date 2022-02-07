class sale_class():

    def __init__(self):
        self.states = ['sale_pizza', 'payment', 'clarification', 'order']
        self.answers = []
        self.transitions = [
        {'trigger': 'choose', 'source': 'sale_pizza', 'dest': 'payment', 'conditions': 'smallorbig'},
        {'trigger': 'pay', 'source': 'payment', 'dest': 'clarification', 'conditions': 'cashnocash'},
        {'trigger': 'accept', 'source': 'clarification', 'dest': 'order'},
        ]

    def smallorbig(self, answer):
        if answer == 'большую' or answer == 'маленькую':
            self.to_payment()
            print('answers on bigsmall', self.answers)
            self.answers.append(answer)
            return True
        elif answer == 'нет':
            self.to_sale_pizza()
            self.answers = []
            answer = ''
            print('answer', answer)
        print('некорректный ввод : "большую или маленькую"')
        return False

    def cashnocash(self, answer2):

        if answer2 == 'наличкой' or answer2 == 'картой':
            # input('STOP КАРТА ИЛИ НАЛИЧКА')
            print('answers : ', self.answers)
            self.to_clarification()
            if len(self.answers) < 2:
                self.answers.append(answer2)
            else:
                self.answers[1] = answer2
            print('answers : ', self.answers)
            return True
        elif answer2 == 'нет':
            self.to_sale_pizza()
            self.answers = []
            answer2 = ''
            print('answer2', answer2)
        else:
            return False