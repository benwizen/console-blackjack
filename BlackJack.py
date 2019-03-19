import random

playing = True


class Card:
    rank_2_values = {'Two': 2, 'Three': 3, 'Four': 4,
                     'Five': 5, 'Six': 6, 'Seven': 7,
                     'Eight': 8, 'Nine': 9, 'Ten': 10,
                     'Jack': 10, 'Queen': 10, 'King': 10, 'Ace': 11}

    suits_2_symbols = {'Hearts': "\u2665", 'Diamonds': "\u2666",
                       'Spades': "\u2660", 'Clubs': "\u2663"}

    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank

    def get_value(self):
        return self.rank_2_values[self.rank]

    def __str__(self):
        return f"{self.suit} {self.rank} - {self.get_value()} {self.suits_2_symbols[self.suit]}"


class Deck:
    suits = ('Hearts', 'Diamonds', 'Spades', 'Clubs')
    ranks = ('Two', 'Three', 'Four',
             'Five', 'Six', 'Seven',
             'Eight', 'Nine', 'Ten',
             'Jack', 'Queen', 'King', 'Ace')

    def __init__(self):
        # self.cards = []
        # for suit in self.suits:
        #     for rank in self.ranks:
        #         card = Card(suit, rank)
        #         self.cards.append(card)
        self.cards = [Card(suit, rank) for rank in self.ranks for suit in self.suits]
        self.cards_count = 52

    def __str__(self):
        deck_str = ""
        for index, card in enumerate(self.cards):
            deck_str += f"{index + 1}: {card.__str__()}\n"
        return deck_str

    def shuffle(self):
        random.shuffle(self.cards)

    def deal(self):
        self.cards_count -= 1
        return self.cards.pop()


class Hand:
    def __init__(self):
        self.cards = []  # start with an empty list as we did in the Deck class
        self.value = 0  # start with zero value
        self.aces = 0  # add an attribute to keep track of aces

    def add_card(self, card):
        self.cards.append(card)
        self.value += card.get_value()
        if card.rank == 'Ace':
            self.aces += 1

    def adjust_for_ace(self):
        while self.value > 21 and self.aces > 0:
            self.value -= 10
            self.aces -= 1

    def __str__(self):
        hand_str = ""
        for index, card in enumerate(self.cards):
            hand_str += f"{index + 1}: {card.__str__()}\n"
        return hand_str


class Chips:

    def __init__(self, total=1000):
        self.total = total
        self.bet = 0

    def win_bet(self):
        self.total += self.bet * 2

    def lose_bet(self):
        self.total -= self.bet

    def __str__(self):
        return f"Total chips: {self.total}"


def take_bet(chips):
    while True:
        try:
            bet = int(input("Please insert your bet: "))
            chips.bet = bet
            if chips.total < bet:
                raise Exception("NotEnoughChipsException")
            break
        except ValueError:
            print("Not a number")
        except Exception as e:
            print(e.__str__())


def hit(deck, hand):
    hand.add_card(deck.deal())
    hand.adjust_for_ace()


def hit_or_stand(deck, hand):
    global playing  # to control an upcoming while loop

    while True:
        play = input("Hit or Stand? [h\s]: ")
        if play == 'h':
            hit(deck, hand)
        elif play == 's':
            playing = False
        else:
            print("Invalid input")
        break


def show_some(player, dealer):
    print("Players hand:")
    print(player)
    print("Dealers (partial) hand:")
    print(dealer.cards[1])
    print("")


def show_all(player, dealer):
    print("Players hand:")
    print(player)
    print("Dealers (Full) hand:")
    print(dealer)
    print("")


def player_busts(chips):
    print("Player busts!")
    chips.lose_bet()


def player_wins(chips):
    print("Player Wins!")
    chips.win_bet()


def dealer_busts(chips):
    print("Player Wins! Dealer busted")
    chips.win_bet()


def dealer_wins(chips):
    print("Dealer wins!")
    chips.lose_bet()


def push():
    print("A tie")


# Set up the Player's chips
players_chips = Chips()

while True:
    # Print an opening statement
    print("Welcome to our BlackJack game!")

    # Create & shuffle the deck, deal two cards to each player
    deck = Deck()
    deck.shuffle()

    player = Hand()
    dealer = Hand()

    for card in range(1, 3):
        player.add_card(deck.deal())
        dealer.add_card(deck.deal())

    # Prompt the Player for their bet
    take_bet(players_chips)

    # Show cards (but keep one dealer card hidden)
    show_some(player, dealer)
    print(f"Sum of cards: {player.value}")

    player_busted = False
    while playing:

        # Prompt for Player to Hit or Stand
        hit_or_stand(deck, player)

        # Show cards (but keep one dealer card hidden)
        show_some(player, dealer)
        print(f"Sum of cards: {player.value}")
        # If player's hand exceeds 21, run player_busts() and break out of loop
        if player.value > 21:
            player_busts(players_chips)
            player_busted = True
            break

    # If Player hasn't busted, play Dealer's hand until Dealer reaches 17
    if player_busted is False:
        while dealer.value < 17:
            hit(deck, dealer)
            # Show all cards
            show_all(player, dealer)

        show_all(player, dealer)

        # Different winning scenarios
        if dealer.value > 21:
            player_wins(players_chips)
        elif dealer.value == player.value:
            push()
        elif dealer.value > player.value:
            dealer_wins(players_chips)
        elif player.value > dealer.value:
            player_wins(players_chips)

    # Inform Player of their chips total
    print(players_chips)

    # Ask to play again
    again = input("Do you want to play another round? [y\\n] ")
    if again != 'y':
        break
    playing = True
