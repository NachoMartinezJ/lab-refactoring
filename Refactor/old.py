import random
import sys

# We define the deck the players will use
face_cards = {'A':[11, 1], 'K': 10, 'Q': 10, 'J': 10}
useful_deck = ['A', 'K', 'Q', 'J', 10, 9, 8, 7, 6, 5, 4, 3, 2]

# First we ask the user to place the bet.
def place_bet():
    user_input = input('Please, introduce your bet: ')

    if (user_input.isdigit()):
        return int(user_input)
    else:
        print('You introduced a non valid character. Please introduce a number')

# Deal the first two cards.
def deal_first_hand():
    return [random.choice(useful_deck) for i in range(2)]

# Deal an additional card.
def deal_card():
    return random.choice(useful_deck)


# Choose value of Ace, we'll use it when asking the player which value does he want for the Ace.
def parse_ace_value(hand, value):
    for i in range(len(hand)):
        if (hand[i] == 'A'):
            hand[i] = value

# Check natural blackjack, we parse Ace to 11 automatically.
def natural_blackjack(hand):
    if(check_score(hand) == 21):
        parse_ace_value(hand, 11)
        parse_face_cards(hand)
    return sum(hand[:2]) == 21

# Check if player has two cards of the same denomination.
def check_denomination(hand):
    return hand[0] == hand[1]

# Check if player's cards sum 9, 10 or 11
def check_double_down(hand):
    result = sum(hand[:2])
    return result == 9 or result == 10 or result == 11

# Sum the value of the cards
def check_score(hand):
    if('A' in hand):
        p_input = int(input("Would you like your ace to be a 1 or an 11? "))
        parse_ace_value(hand, p_input)
    parse_face_cards(hand)
    return sum(hand)


# Compare the hand of the dealer and the player.
def compare_hands(p_hand, d_hand, player_wins, dealer_wins, tie):
    p_score = check_score(p_hand)
    d_score = check_score(d_hand)

    if (p_score > 21):
        print("You bust with %d points. Dealer wins" % p_score)
        dealer_wins = True
    if (d_score > 21):
        print("Dealer busts with %d points. Players wins" % d_score)
        player_wins = True
    if (p_score == d_score):
        print("There has been a tie. Player points: %d and hand: %s. Dealer points: %d and hand: %s" % (
            p_score, p_hand, d_score, d_hand))
        tie = True

    if (p_score > d_score):
        print("Player wins with %d points with the hand %s" % (p_score, p_hand))
        player_wins = True

    if (p_score < d_score):
        print("Dealer wins with %d points with the hand %s" % (d_score, d_hand))
        dealer_wins = True


# Check if the player has less than 21 points, to give him a new card.
def hit(hand):
    new_card = deal_card()

    if (check_score(hand) < 21):
        hand.append(new_card)
        return new_card

    else:
        print("You cannot ask for more cards")


# Change the value of the face cards, minus the ace, to its point value.
def parse_face_cards(hand):
    for i in range(len(hand)):
        if (hand[i] == 'K'):
            hand[i] = face_cards['K']

        if (hand[i] == 'Q'):
            hand[i] = face_cards['Q']

        if (hand[i] == 'J'):
            hand[i] = face_cards['J']

def dealer_play(hand):
    while(check_score(hand) <= 14):
        hit(hand)
    print("Dealer's hand: ", hand)
    return hand


def play():
    bet = place_bet()
    player_hand = []
    dealer_hand = [9, 'A']
    player_wins = False
    dealer_wins = False
    tie = False
    response = 'Y'
    double_down = False

    if (bet == None):
        print("Program ending")
    else:
        player_hand = deal_first_hand()
        print("Player's hand:", player_hand)
        # dealer_hand = deal_first_hand()
        print("Dealer's hand:", dealer_hand[0])

        if (natural_blackjack(player_hand)):
            print("Player wins with a natural blackjack!", player_hand)

        elif (natural_blackjack(dealer_hand)):
            print("Dealer wins with a natural blackjack!", dealer_hand)

        else:
            if (check_double_down(player_hand)):
                response = input("Would you like to double down? (Y/N):")

                if (response == 'Y'):
                    bet += bet
                    double_down = True
                    print("Your bet has doubled, now you're playing with: %d" % bet)

                elif (response == 'N'):
                    print("Your bet stays the same")

                else:
                    print("Invalid input, please introduce 'Y' or 'N' next time.")
                    sys.exit()

            response = 'Y'
            while (response == 'Y'):
                response = input("Would you like another card? (Y/N): ")

                if (response == 'Y' and check_score(player_hand) <= 21):
                    hit(player_hand)
                    print("Player's hand:", player_hand)
                    if (double_down):
                        break
                    if (check_score(player_hand) > 21):
                        print("You bust with %d points. Dealer wins" % check_score(player_hand))
                        break

                elif (response != 'Y' and response != 'N'):
                    print("Invalid input, please introduce 'Y' or 'N' next time.")

            dealer_play(dealer_hand)
            print("Player's hand: ", player_hand)
            p_score = check_score(player_hand)
            d_score = check_score(dealer_hand)

            if (p_score > 21):
                print("You bust with %d points. Dealer wins" % p_score)

            elif (d_score > 21):
                print("Dealer busts with %d points. Players wins" % d_score)

            elif (p_score == d_score):
                print("There has been a tie. Player points: %d and hand: %s. Dealer points: %d and hand: %s" % (
                    p_score, player_hand, d_score, dealer_hand))

            elif (p_score > d_score):
                print("Player wins with %d points with the hand %s" % (p_score, player_hand))

            elif (p_score < d_score):
                print("Dealer wins with %d points with the hand %s" % (d_score, dealer_hand))

play()



