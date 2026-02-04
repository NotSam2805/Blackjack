import os
class Account:
    def __init__(self, new = False):
        self.username = input('Username: ')
        self.credit_file = self.username + '_credit.txt'
        self.log_file = self.username + '_log.txt'

        if new:
            self.credit = float(input('Add funds: '))
            self.save_credit()
            self.save_log(paid_in=self.credit)
        elif not os.path.isfile(self.credit_file):
            raise SystemError(f'No user \"{self.username}\" found')
        else:
            self.load_credit()
    
    def get_credit(self):
        self.credit = round(self.credit, 2)
        return self.credit

    def load_credit(self):
        credit = 0
        with open(self.credit_file,'r') as f:
            line = f.readlines()[-1]
            if line == '' or line == '\n':
                line = f.readlines()[-2]
            credit = float(line)
        self.credit = round(credit,2)
        return credit
    
    def save_credit(self):
        self.credit = round(self.credit,2)
        with open(self.credit_file, 'a') as f:
            f.write(f'{self.credit}\n')
    
    def save_log(self, paid_in = None, taken_out = None, won = None, bet = None):
        with open(self.log_file, 'a') as f:
            if paid_in != None:
                paid_in = round(paid_in,2)
                f.write(f'Paid in:{paid_in}\n')
            if taken_out != None:
                taken_out = round(taken_out,2)
                f.write(f'Paid out:{taken_out}\n')
            if won != None:
                if won >= 0:
                    won = round(won,2)
                    f.write(f'Won:{won}\n')
                else:
                    f.write(f'Lost:{-won}\n')
            if bet != None:
                bet = round(bet,2)
                f.write(f'Bet:{bet}\n')
            self.credit = round(self.credit,2)
            f.write(f'Credit:{self.credit}\n')

    def bet(self, amount):
        if amount > self.credit:
            print('Cannot bet more than current credit')
            print(f'Betting all credit: £{self.credit}')
            self.credit = 0
            self.save_log(bet = self.credit)
            return self.credit
        self.credit -= amount
        self.save_log(bet = amount)
        return amount

    def pay_in(self, amount):
        self.credit += amount
        self.save_log(paid_in=amount)

    def win(self, amount):
        self.credit += amount
        self.save_log(won=amount)
    
    def lost(self, amount):
        self.save_log(won=-amount)

    def cash_out(self, amount):
        if amount > self.credit:
            print(f'Cannot cash out more than credit')
            return
        self.credit -= amount
        self.save_log(taken_out=amount)
        self.save_credit()
    
    def print_report(self):
        lines = []
        with open(self.log_file,'r') as f:
            lines = f.readlines()
        
        total_in = 0
        total_out = 0
        won = 0
        bet = 0
        lost = 0
        games_played = 0
        peak_credit = 0
        for line in lines:
            split = line.split(':')
            if len(split) == 2:
                match split[0]:
                    case 'Paid in':
                        total_in += float(split[1])
                    case 'Paid out':
                        total_out += float(split[1])
                    case 'Bet':
                        games_played += 1
                        bet += float(split[1])
                    case 'Won':
                        won += float(split[1])
                    case 'Lost':
                        lost += float(split[1])
                    case 'Credit':
                        credit = float(split[1])
                        if credit > peak_credit:
                            peak_credit = credit
        
        print(f'Current credit: £{self.load_credit()}')
        print(f'Total paid in: £{total_in}')
        print(f'Total paid out: £{total_out}')
        print(f'Played {games_played} times')
        print(f'Peak credit: £{peak_credit}')
        if total_in > total_out:
            print(f'Total in: £{total_in - total_out}')
        total_won = round((total_out + self.credit) - total_in,2)
        if total_won >= 0:
            print(f'Total won: £{total_won}')
        else:
            print(f'Total lost: £{-total_won}')
