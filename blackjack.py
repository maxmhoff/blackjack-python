import time     # time is imported to make short delays between actions in the game and to save the date for highscores.
import random   # random is imported to shuffle the deck.
import json     # json is imported to handle highscores.

# Main variables of a deck of cards. Suits and ranks are defined as tupples since they are final.
suits = ('Clubs','Diamonds', 'Hearts', 'Spades')
ranks = ('Two', 'Three', 'Four', 'Five', 'Six', 'Seven', 'Eight', 'Nine', 'Ten', 'Jack', 'Queen', 'King', 'Ace')

# A dictionary that defines the values for each rank: 
values = {'Two': 2, 'Three': 3, 'Four': 4, 'Five': 5, 'Six': 6, 'Seven': 7, 'Eight': 8, 'Nine': 9, 'Ten': 10, 'Jack': 10, 'Queen': 10, 'King': 10, 'Ace': 11}

# A boolean to control whether the program should be running
running = True

# A boolean to control while loops and the flow of the game.
playing = True

# Some delay values are defined here. This will make it easier and faster to change the "feel" of the game. 
def short_delay():
    time.sleep(0.1)

def medium_delay():
    time.sleep(1)

def long_delay():
    time.sleep(2)

def very_long_delay():
    time.sleep(5)

# This is used to animate text prints.
def typewriter_print(line_of_text):
    print(line_of_text)
    short_delay()
        
class Card:

    # A card consists of two variables; a suit and a rank.
    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank

    # We override the __str__ to create a readable string presentation of the card.
    def __str__(self):
        return self.rank + ' of ' + self.suit

# A deck has 52 cards in it. The responsibility of creating each card for the game lies in this class. 
class Deck:
    def __init__(self):
        # Whenever we construct a deck we want it to contain the 52 cards. We make sure that the appropriate cards are added by doing a nested for-loop. 
        self.deck = []
        for suit in suits:
            for rank in ranks:
                self.deck.append(Card(suit, rank))

    # Once again we override the __str__ function, but this time around, it is mainly due to purpose of testing. First of all we are gonna make an empty string.
    # Then we will populate it with the card.__str__() function from each card in the deck:
    def __str__(self):
        deck_comp = ''
        for card in self.deck:
            deck_comp += '\n' + card.__str__()
        return 'Cards in the deck: ' + deck_comp

    # You could opt to use different shuffling algorithms, but in this case I would argue, that using the default random.shuffle function is more than sufficient.
    def shuffle(self):
        random.shuffle(self.deck)

    # Since the deck now is a list of cards we can simply use the .pop function to deal a card.
    def deal(self):
        single_card = self.deck.pop()
        return single_card

# A player class to keep track of each player's hand and current balance.
# In this class we will also determine whether an ace should count as 1 or 11.
# The starting_balance is the default money balance the player will start with.
class Player:
    def __init__(self, name, starting_balance):
        self.name = name
        self.hand = []
        self.hand_sum = 0
        self.aces = 0
        self.balance = starting_balance     
        self.bet = 0
    
    def add_card(self, deck):
        dealt_card = deck.deal()
        self.hand.append(dealt_card)
        self.hand_sum += values[dealt_card.rank]
        if dealt_card.rank == 'Ace':
            self.aces += 1
        while self.hand_sum > 21 and self.aces > 0:
            self.hand_sum -= 10
            self.aces -= 1


    def hit_or_stand(self, deck):
        global playing
    
        while True:
            x = input("Would you like to Hit or Stand? Enter 'H' or 'S'\n")
        
            if x[0].lower() == 'h':
                self.add_card(deck)
                print()

            elif x[0].lower() == 's':
                print()
                print(self.name + ' stands. ' + dealer.name + ' is playing:')
                playing = False
                print()

            else:
                print("Sorry, please try again.")
                continue
            break

    def reset_hand(self):
        self.hand = []
        self.hand_sum = 0
        self.aces = 0
    
    def take_bet(self):
        while True:
            medium_delay()
            try:
                self.bet = int(input('How much money do you want to place on the bet?\n'))
            except ValueError:
                print('Sorry, the bet must be a whole number (and thus it cannot contain decimals or other characters).\n')
            else:
                if self.bet > self.balance:
                    print('Sorry, your bet cannot exceed your current balance: ' + str(self.balance) + '$.\n')
                elif self.bet <= 0:
                    print('Sorry, you have to bet something in order to participate.\n')
                else:
                    print()
                    break
        
    def bet_won(self):    
        self.balance += self.bet
        medium_delay()
        print('You won ' + str(self.bet) + '$. Your current balance is: ' + str(self.balance) + '$.\n')
    
    def bet_lost(self):
        self.balance -= self.bet
        medium_delay()
        print('You lost ' + str(self.bet) + '$. Your current balance is: ' + str(self.balance) + '$.\n')
        
    def show_hand(self):
        print(self.name + '\'s hand (' + str(self.hand_sum) + '):')
        for card in self.hand:
            print(card)
        print()

    # This function is introduced to show the dealer's hand.
    def show_hand_hidden(self):
        print(self.name + '\'s hand:')
        print('<hidden card>')
        for card in self.hand[1:]:
            print(card)
        print()

# Highscore functions
def save_highscores(highscores):
    with open('highscores.json', 'w') as file:
        json.dump(highscores, file)

def load_highscores():
    try:
        with open('highscores.json', 'r') as file:
            highscores = json.load(file)
    except FileNotFoundError:
        return []
    return highscores

def check_for_highscore(player):
    new_highscore = False
    highscores = load_highscores()
    if len(highscores) == 3:
        for highscore in highscores:
            score = highscore[1]
            if player.balance > score:
                print('You made it to the highscore list!\n')
                highscores.append([player.name, player.balance, time.strftime("%d-%m-%y")])
                new_highscore = True
                medium_delay()
                break

    # If the list's length is less than three you are automatically on the highscore list since our highscore list has three slots. 
    else:
        print('You made it to the highscore list!\n')
        highscores.append([player.name, player.balance, time.strftime("%d-%m-%y")])
        new_highscore = True
        medium_delay()
    
    # Since the highscore list should be sorted by score, which is the second entry in json objects sort(key=lambda x: x[1]) is used.
    highscores.sort(key=lambda x: x[1])
    highscores.reverse()    
    while len(highscores) > 3:
        highscores.pop()
    save_highscores(highscores)
    if new_highscore == True:
        print_highscores()
        new_highscore == False

# This function is pretty self-explanatory
def print_highscores():
    i = 1
    typewriter_print('\t\t Highscores')
    typewriter_print('________________________________________________')
    typewriter_print('')
    if len(load_highscores()) != 0:
        for highscore in load_highscores():
                # Since the player name (highscore[0]) is most likely to have a different lengths, there is a lot of formatting to ensure that the shown length of the name is always 16 characters
            typewriter_print(str(i) + '.\t' + highscore[0].ljust(15, ' ')[0:15] + '\t' + str(highscore[1]) + '$\t\t' + highscore[2]) 
            if i < len(load_highscores()):
                typewriter_print('------------------------------------------------')
            else:
                typewriter_print('________________________________________________')
            i += 1
    else:
        typewriter_print('\tNo highscores have been added yet.\n')
    typewriter_print('')

# The help option with tips and tricks
def print_help():
    typewriter_print('________________________________________________________')
    typewriter_print('')
    typewriter_print('[1. General]')
    typewriter_print('')
    typewriter_print('1.1\tYour initial balance is always 100$. In other')
    typewriter_print('\twords: You should never bet less than 100$ on')
    typewriter_print('\tyour first bet.')
    typewriter_print('')
    typewriter_print('1.2\tWhenever your hand is shown, a number will appear')
    typewriter_print('\tright next to it. This number is meant to help')
    typewriter_print('\tyou. It shows the current total sum of your hand.')
    typewriter_print('\tOnce the dealer\'s cards are no longer hidden,')
    typewriter_print('\tthe number will appear next to their hand too.')
    typewriter_print('')
    typewriter_print('1.3\tAll good games contain a cheat code.')
    typewriter_print('\t...So does this.')
    typewriter_print('')
    typewriter_print('---------------------------------------------------------')
    typewriter_print('')
    typewriter_print('[2. Blackjack]')
    typewriter_print('')
    typewriter_print('2.1\tIn blackjack cards with ranks from 2-10 ')
    typewriter_print('\tis valued by their default rank, while jacks,')
    typewriter_print('\tqueens and kings count as ten. The ace can act as')
    typewriter_print('\tthe value of one or the value of eleven.')
    typewriter_print('')
    typewriter_print('2.2\tThe objective is to get a higher total hand sum')
    typewriter_print('\tthan the dealer without exceeding 21 points.')
    typewriter_print('')
    typewriter_print('2.3\tIn "Max\' Blackjack Casino" the dealer never hits')
    typewriter_print('\tif his hand has a total sum of 17 or higher, and')
    typewriter_print('\talways hits if it\'s lower.')
    typewriter_print('')
    typewriter_print('2.4\tA natural or a blackjack (21 in two cards) is')
    typewriter_print('\tvalued higher than 21 with three cards or more.')
    typewriter_print('')
    typewriter_print('---------------------------------------------------------')
    typewriter_print('')
    typewriter_print('[3. Highscores]')
    typewriter_print('')
    typewriter_print('3.1\tThe highscore list is limited to three entries.')
    typewriter_print('')
    typewriter_print('3.2\tLosing all your money is not really an')
    typewriter_print('\tachievement, therefore you have to cash out')
    typewriter_print('\tto save your highscore. This option is shown')
    typewriter_print('\tafter each game of Blackjack. Use it wisely!')
    typewriter_print('')
    typewriter_print('3.3\tIf for some reason your highscore list is corrupt')
    typewriter_print('\ttry deleting the highscores.json file. A new file')
    typewriter_print('\tshould automatically be created once your first')
    typewriter_print('\thighscore is saved.')
    typewriter_print('')
    typewriter_print('_________________________________________________________')
    typewriter_print('')

# The casino starts here:
typewriter_print('')
typewriter_print('//////////////////////////////////////////////////')
typewriter_print('')
typewriter_print('\tWelcome to Max\' Blackjack Casino!')
typewriter_print('')
typewriter_print('//////////////////////////////////////////////////')
typewriter_print('')

# We prompt the user to get a player name. This name will be used in the highscore list and through-out the game.
name = input('Enter your name: \n')
print()
player = Player(name, 100)
# The dealer is called 'Dealer' by default.
dealer = Player('Dealer', 0)

while True:
    medium_delay()
    print('[Choose an option]\t\tBalance: ' + str(player.balance) + '$')
    print('1. Play')
    print('2. See highscores')
    print('3. Help')
    print('4. Exit')
    chosen_option = input()
    print()
    if chosen_option == '1':
        break

    elif chosen_option == '2':
        print_highscores()

    elif chosen_option == '3':
        print_help()

    elif chosen_option == '4':
        running = False
        break
    
    elif chosen_option == '1.3':
        player.balance += 1000

    else:
        print('Please enter a number between 1-4 to choose an option.\n')


while running:
    # A new deck is created and shuffled.
    deck = Deck()
    deck.shuffle()

    # Then the player places a bet.
    player.take_bet()
    
    # Each player recieves two cards.
    player.add_card(deck)
    player.add_card(deck)

    dealer.add_card(deck)
    dealer.add_card(deck)

    # The player gets to see one of the dealer's cards.
    dealer.show_hand_hidden()
    
    medium_delay()

    while playing:
        player.show_hand()
        medium_delay()
        # Since a natural (a blackjack) is the best draw of the game, we simply assume that the player wants to stand. Hence the 'break'.
        if len(player.hand) == 2 and player.hand_sum == 21:
            print('Wow, that\'s a Blackjack!\n')
            break
        player.hit_or_stand(deck)
        
        # if the player busts:
        if player.hand_sum > 21:
            player.show_hand()
            medium_delay()
            print(player.name + ' busts!\n')
            long_delay()
            player.bet_lost()
            break

    # Once the player is done playing, then it's the dealer's turn. First of all his hand i revealed.
    if player.hand_sum <= 21:
        medium_delay()
        dealer.show_hand()
        medium_delay()

        if dealer.hand_sum != 21 and player.hand_sum == 21 and len(player.hand) == 2:
            print(player.name + ' wins with a blackjack!!!\n')
            player.bet_won()
        
        elif dealer.hand_sum == 21 and len(dealer.hand) == 2 and player.hand_sum == 21 and len(player.hand):
            print('Oh my... you don\'t get to see this every day! ' + dealer.name + ' and ' + player.name + ' tied with a blackjack each. It\'s a push!')
        
        # The dealer always hits untill he has a value of 17 or higher unless the player has a natural (a value of 21 in two cards).
        else:
            while dealer.hand_sum < 17:
                print(dealer.name + ' hits! \n')
                dealer.add_card(deck)
                medium_delay()
                dealer.show_hand()
                medium_delay()


            if dealer.hand_sum > 21:
                print(dealer.name + ' busts, ' + player.name + ' wins!\n')
                player.bet_won()

            elif dealer.hand_sum > player.hand_sum:
                print(dealer.name + ' wins!\n')
                player.bet_lost()

            elif dealer.hand_sum < player.hand_sum:
                print(dealer.name + ' stands.')
                print()
                medium_delay()
                print(player.name + ' wins!\n')
                player.bet_won()
            
            elif dealer.hand_sum == 21 and len(dealer.hand) == 2 and dealer.hand_sum == player.hand_sum:
                print('That\'s just bad luck, ' + dealer.name + ' has a blackjack and wins!\n')
                player.bet_lost()
                
            else:
                print(dealer.name + ' stands.')
                print()
                medium_delay()
                print(dealer.name + ' and ' + player.name + ' tie. It\'s a push!\n')
                medium_delay()
    
    # Ask to play again
    if(player.balance <= 0):
        medium_delay
        print('Oh no, you are broke...\n')
        long_delay()

        # Instead of forcing the player to restart the game each time he/she is broke.
        list_of_excuses_to_give_the_player_one_hundred_dollars = [
            'You are not in a position to get a small loan of a million dollars, but a very good friend of yours offered to donate you 100$!\n', 
            'But it looks like fortune smiles upon you, while exiting the casino you found 100$ on the floor!\n', 
            'No need to worry, your mom has agreed to loan you 100 bucks!\n', 
            'With a look of disgust on your face you reach down into your empty pockets... but hey, what was that? 100 dollars?! How did you forget?\n',
            'Outside of the casino you managed to sell your wrist watch for 100$. You are back in business!\n',
            'An incredibly generous person mistook you for a homeless beggar. He gave you 100$!\n',
            'You didn\'t really need that wedding ring, did you? Good thing you got rid of it. Now you\'ve got 100 dollars in your pocket, yeah baby!\n',
            'A pension account, hah! Who needs that? You withdrew 100 dollars from it, let\'s make them count!\n',
            'Your shoes weren\'t made for walking... that\'s why you sold them! With 100$ and the chance to win more, you can get a new pair in no time!\n',
            'In a fancy place like this, nobody will miss 100 dollars... that\'s what you said to yourself when you "borrowed" them from a bystander.\n'     
            ]
        # random.choice is used to ensure we get the variety
        print(random.choice(list_of_excuses_to_give_the_player_one_hundred_dollars))
        player.balance = 100
        very_long_delay()
        
    while True:
        print('[Choose an option]\t\tBalance: ' + str(player.balance) + '$')
        print('1. Play again')
        print('2. See highscores')
        print('3. Help')
        print('4. Cash out')
        chosen_option = input()
        print()
        if chosen_option == '1':
            playing = True
            player.reset_hand()
            dealer.reset_hand()
            break
        elif chosen_option == '2':
            print_highscores()
        elif chosen_option == '3':
            print_help()
        elif chosen_option == '4':
            check_for_highscore(player)
            running = False
            break
        else:
            print('Please enter a number between 1-4 to choose an option.\n')

# Goodbye message
medium_delay()
print('On behalf of the entire staff at Max\' Blackjack Casino I can safely say')
long_delay()
print('that we...')
medium_delay()
print('...erhm...')
medium_delay()
print('That I hope to see you again soon!')
long_delay()