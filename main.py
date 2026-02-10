import Cards as C
import time
import Accounts as a
from enum import Enum

#Possible outcomes from blackjack, need to be able handle all of these
class result(Enum):
    player_natural_blackjack = 0
    dealer_natural_blackjack = 1
    both_natural_blackjack = 2
    player_bust = 3
    dealer_bust = 4
    dealer_wins = 5
    player_wins = 6
    stand_off = 7

def ask_question(question:str, valid_answers:list[str]): #Simple function to only accept valid inputs
    while True:
        inp = input(question)
        if inp in valid_answers:
            return inp

def deal_cards(deck:list[C.Card], hand:list[C.Card], n_cards:int): #Take n number of cards from deck and add them to the hand
    for i in range(n_cards):
        hand.append(deck.pop())
    return (deck, hand)

def hand_value(hand:list[C.Card]) -> int: #Calculate the value of the hand
    value = 0
    #Count the number of aces, need to handle when ace is 11 and when 1
    ace_count = 0
    for card in hand:
        if card.rank != C.Rank.ace:
            #If not ace, just add value
            value += card.value
        else:
            ace_count += 1
    
    #Initially set the value to all aces to 11
    for i in range(ace_count):
        value += 11

    #If over 21, need to count aces as 1, minus 10 for each ace until value is 21 or less
    while ace_count > 0 and value > 21:
        value -= 10
        ace_count -= 1
    return value

def hand_to_string(hand:list[C.Card]) -> str: #For printing a hand
    string = ''
    for card in hand:
        string += card.id + ', '
    return string[:-2]

def black_jack(deck = None, n_decks = 6):
    dealers_hand = []
    players_hand = []

    #If needed, generate and shuffle new deck
    if (deck == None) or len(deck) < ((52/n_decks) + 26):
        print('Shuffling the deck')
        print()
        deck = C.deck
        for i in range(1,n_decks):
            deck += C.deck
        deck = C.shuffle_deck(deck)
    
    #Player and dealer gets 2 cards
    deck, players_hand = deal_cards(deck, players_hand, 2)
    deck, dealers_hand = deal_cards(deck, dealers_hand, 2)

    #Find the value of the hands
    dealer_value = hand_value(dealers_hand)
    player_value = hand_value(players_hand)

    #Print the hands (Player can see their full hand, only first card in dealer's hand is shown)
    face_down_cards = 'X,' * (len(dealers_hand) - 1)
    face_down_cards = face_down_cards[:-1]
    print(f'Dealer: {dealers_hand[0].id}, {face_down_cards}')
    print(f'You: {hand_to_string(players_hand)} ({player_value})')
    time.sleep(1)
    print()

    #If player/dealer got a natural blackjack
    player_natural = player_value == 21
    dealer_natural = dealer_value == 21

    #Return if blackjack
    if player_natural and dealer_natural:
        print(f'Dealer: {hand_to_string(dealers_hand)}')
        print(f'Both have blackjack')
        return result.both_natural_blackjack, deck
    elif player_natural:
        print(f'Dealer: {hand_to_string(dealers_hand)} ({dealer_value})')
        print(f'Blackjack!')
        return result.player_natural_blackjack, deck
    elif dealer_natural:
        print(f'Dealer: {hand_to_string(dealers_hand)}')
        print(f'Dealer blackjack')
        return result.dealer_natural_blackjack, deck
    
    #Player's turn
    player_standing = False
    while (not player_standing) and (not player_natural):
        #Get hit or stand input
        h_or_s = ask_question('Hit(H) or stand(S)? ', ['H','h','s','S'])

        #If hit
        if (h_or_s == 'H') or (h_or_s == 'h'):
            #Deal card to player
            deck, players_hand = deal_cards(deck, players_hand, 1)
            #Calculate value of the hand
            player_value = hand_value(players_hand)
            print(f'You: {hand_to_string(players_hand)} ({player_value})')
            time.sleep(1)

            #If player bust, return
            if player_value > 21:
                print(f'You bust')
                print(f'Dealer: {hand_to_string(dealers_hand)} ({dealer_value})')
                return result.player_bust, deck
            #Automatically stand if the player hits 21
            elif player_value == 21:
                player_standing = True
        #Not hit = stand
        else:
            #Stand, end loop
            player_standing = True
    
    print()

    print(f'Dealer: {hand_to_string(dealers_hand)} ({dealer_value})')

    #Dealers turn
    dealer_standing = False
    while (not dealer_standing):
        if dealer_value <= 16:
            #Hit
            time.sleep(1)
            #Deal card to dealer
            deck, dealers_hand = deal_cards(deck, dealers_hand, 1)
            #Calculate dealers value
            dealer_value = hand_value(dealers_hand)
            print(f'Dealer: {hand_to_string(dealers_hand)} ({dealer_value})')

            if dealer_value > 21:
                print(f'Dealer bust!')
                return result.dealer_bust, deck
        else:
            #Stand, end loop
            dealer_standing = True
    
    #Return correct result
    if dealer_value == player_value:
        print(f'Stand off')
        return result.stand_off, deck
    
    if dealer_value > player_value:
        return result.dealer_wins, deck
    
    return result.player_wins, deck

winings = 0

total_bet = 0
initial_credit = 0

#User login (see Accounts.py)
user = None
if ask_question('New user? ', ['y','n']) == 'y':
    user = a.Account(True)
else:
    user = a.Account()
initial_credit = user.get_credit()

#Add any credit to user
add = float(input('Add credit: £'))
initial_credit += add
if add > 0:
    user.pay_in(add)

d = None
stand_off = False
bet = 0

done = False
while not done:
    if user.get_credit() <= 0.1:
        #User doesn't have enough credit
        print(f'£{user.get_credit()} credit')
        #Add credit
        add = float(input('Add credit: £'))
        if add > 0:
            user.pay_in(add)
    
    if not stand_off:
        #Player places bet
        print(f'£{user.get_credit()} credit')

        #Get bet amount
        bet = 0
        while bet < 0.1:
            bet = float(input('Bet (minimum £0.10): £'))
        bet = round(user.bet(bet),2)
        total_bet += bet
        total_bet = round(total_bet,2)

    #If stand off, use the same bet and play again
    else:
        print(f'Bet: £{bet}')
    print()

    #Play (r = game result, d = deck)
    r, d = black_jack(deck=d, n_decks=6)
    
    #Handle game result
    stand_off = False
    match r:
        case result.both_natural_blackjack:
            user.win(bet)
        case result.dealer_natural_blackjack | result.player_bust | result.dealer_wins:
            user.lost(bet)
            winings -= bet
        case result.player_natural_blackjack:
            user.win(2.5*bet)
            winings += 1.5 * bet
        case result.dealer_bust | result.player_wins:
            user.win(2 * bet)
            winings += bet
        case result.stand_off:
            stand_off = True
    winings = round(winings,2)
    
    #Save users credit
    user.save_credit()
    user.save_log()
    
    time.sleep(1)
    print()
    
    print(f'Total bet: £{total_bet}, winings: £{winings}, credit: £{user.get_credit()}')
    if not stand_off:
        if ask_question('Play again? ', ['y','n']) != 'y':
            done = True
    time.sleep(1)
    print('\n')

profit = user.get_credit() - initial_credit

if ask_question('Cash out? ', ['y','n']) == 'y':
    amount = float(input('Amount: £'))
    user.cash_out(amount)
    print(f'£{amount} Taken out')
print()

user.save_credit()
user.save_log()

if ask_question('Show account report? ', ['y', 'n']) == 'y':
    print()
    user.print_report()