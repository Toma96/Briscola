from briskula import *
import random
import collections

deck = []

for suit in SUITS:
    for power in POWER_RANGE:
        if power not in range(8, 11):
            deck.append(Card(suit, power))


print("Welcome to Briskula, classic Italian card game. When it's your turn, play a card from your hand by index (1/2/3)")
while True:
    no_players = int(input("Select number of players (2/3/4): "))
    if no_players in range(2, 5):
        break
    else:
        print("Invalid number of players!")

players = collections.OrderedDict()             # a dictionary with player names for keys and Player objects for values
counter = 0
while counter < no_players:
    name = input("Player {0}'s name: ".format(counter + 1))
    if name not in players.keys():
        players[name] = Player(name)
        counter += 1
    else:
        print("There's already a player with the given name!")

players_list = players.values()
print("Select human player: ", end='')
for player in players.keys():
    print(player, end=', ')
print()

humans = []
while True:
    human = input()
    if human == '':
        break
    elif human in players.keys() and human not in humans:
        humans.append(human)
        print("Select another human player, if not, press enter.")
        continue
    else:
        print("Invalid player name input!")

for name in players.keys():
    if name in humans:
        human_player = players[name]

random.shuffle(deck)

if no_players == 3:
    for card in deck:
        if card.power == 2:
            deck.remove(card)
            print("3 players: A card needs to be removed from the deck")
            print("Removed card is {0} {1}".format(card.suit, card.power))
            break

adut_card = deck.pop(len(deck) - 1)
print("The last card in the deck is {0} {1}".format(adut_card.suit, adut_card.power))
print("The strongest suit (adut) is {0}".format(adut_card.suit.upper()))
deck.insert(0, adut_card)

for card in deck:
    card.set_heuristic(adut_card.suit)

for player in players.values():
    for i in range(3):
        player.draw(deck)


"""     GAME       """
while len(deck) > 0 or len(human_player.current_hand) > 0:

    battlefield = collections.OrderedDict()
    field = []

    turn = 1
    for name, player in players.items():
        if name in humans:
            print("{0}'s turn: ".format(name))
            battlefield[player] = player.human_card_play()
            print("{0} played {1} {2}".format(name, battlefield[player].suit, battlefield[player].power))
        else:
            if turn == 1:
                battlefield[player] = player.ai_card_play(turn, adut_card.suit, field, no_players)
            else:
                battlefield[player] = player.ai_card_play(turn, adut_card.suit, field, no_players, leading_suit)
            print("Player {0} played {1} {2}".format(player.name, battlefield[player].suit, battlefield[player].power))
        if turn == 1:
            leading_suit = battlefield[player].suit
        field.append(battlefield[player])
        print()
        turn += 1

    leading_player = fight(battlefield, adut_card.suit)
    players = collections.OrderedDict()
    players[leading_player.name] = leading_player
    found_leading = False
    while len(players.values()) != no_players:
        for player in players_list:
            if found_leading:
                players[player.name] = player
            if player == leading_player:
                found_leading = True

    if len(deck) >= no_players:
        for player in players.values():
            player.draw(deck)


print()
print("GAME OVER!")
for name, player in players.items():
    print('Player {0} has {1} points.'.format(name, player.points))




