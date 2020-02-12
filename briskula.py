import random
import time

SUITS = ["Bastoni", "Coppa", "Denari", "Spade"]
POWER_RANGE = range(1, 14)
MAX_HAND_SIZE = 3


class Card(object):

    def __init__(self, suit, power):
        self.suit = suit
        self.power = power
        self.value = self.set_value(self.power)
        self.heuristic_value = self.value

    def set_value(self, power):
        value = 0
        if power == 1:
            value = 11
        elif power == 3:
            value = 10
        elif power > 10:
            for char in str(power):
                value += int(char)
        else:
            value = 0
        return value

    def set_heuristic(self, adut_suit):
        if self.suit == adut_suit:
            self.heuristic_value += 5

    def isStronger(self, card):
        if self.value > card.value:
            return True
        elif self.value == card.value:
            if self.power > card.power:
                return True
        return False

    def beats(self, card, adut_suit, leading_suit):
        if card.suit == self.suit:
            if card.isStronger(self):
                return False
            else:
                return True
        if card.suit == adut_suit and self.suit != adut_suit:
            return False
        elif card.suit == leading_suit and self.suit != adut_suit and self.suit != leading_suit:
            return False
        elif card.suit != adut_suit and card.suit != leading_suit and self.suit != adut_suit and self.suit != leading_suit:
            return None

        return True


class Player(object):

    def __init__(self, name):
        self.name = name
        self.points = 0
        self.current_hand = []

    def human_card_play(self):
        for card in self.current_hand:
            print(card.suit, card.power, end=', ')
        while True:
            played_index = int(input())
            if played_index in range(1, len(self.current_hand)+1):
                break
            else:
                print("Invalid card index chosen!")
        return self.current_hand.pop(played_index - 1)

    def ai_card_play(self, turn, adut, battlefield, no_players, leading_suit=None):
        time.sleep(1.5)
        if turn == 1:
            lowest = self.find_lowest_heuristic()
            self.current_hand.remove(lowest)
            return lowest

        strongest = find_strongest(battlefield, adut, leading_suit)
        points = accumulate_points(battlefield)

        beaten = False
        for card in self.current_hand:
            if card.beats(strongest, adut, leading_suit):
                beaten = True
                break
        if not beaten:
            lowest = self.find_lowest_heuristic()
            self.current_hand.remove(lowest)
            return lowest

        if (no_players == 2 and turn == 2) or (no_players == 3 and turn == 3) or (no_players == 3 and turn == 2):
            if strongest.suit != adut:
                strongest_nonadut_in_hand = find_strongest_nonadut(self.current_hand, strongest.suit, adut)
                if strongest_nonadut_in_hand is not None and strongest_nonadut_in_hand.beats(strongest, adut, leading_suit):
                    self.current_hand.remove(strongest_nonadut_in_hand)
                    return strongest_nonadut_in_hand
                else:
                    weakest_adut = find_weakest_adut(self.current_hand, adut)
                    if points in range(1, 8):
                        if weakest_adut.heuristic_value <= 5:
                            self.current_hand.remove(weakest_adut)
                            return weakest_adut
                        else:
                            lowest = self.find_lowest_heuristic()
                            self.current_hand.remove(lowest)
                            return lowest
                    elif points > 8:
                        self.current_hand.remove(weakest_adut)
                        return weakest_adut
                    elif points == 0:
                        lowest = self.find_lowest_heuristic()
                        self.current_hand.remove(lowest)
                        return lowest
            else:
                if points >= 10:
                    ace = find_strongest_adut(self.current_hand, adut)
                    self.current_hand.remove(ace)
                    return ace

                lowest = self.find_lowest_heuristic()
                if lowest.value <= 4:
                    self.current_hand.remove(lowest)
                    return lowest

                for card in self.current_hand:
                    if card.beats(strongest, adut, leading_suit):
                        self.current_hand.remove(card)
                        return card



        return self.current_hand.pop(random.randint(0, len(self.current_hand) - 1))

    def draw(self, deck):
        self.current_hand.append(deck.pop(len(deck) - 1))

    def find_lowest_heuristic(self):
        lowest = self.current_hand[0]
        for card in self.current_hand:
            if card.heuristic_value < lowest.heuristic_value:
                lowest = card
            elif card.heuristic_value == lowest.heuristic_value:
                if card.power < lowest.power:
                    lowest = card
        return lowest


def accumulate_points(battlefield):
    points = 0
    for card in battlefield:
        points += card.value
    return points


def find_strongest(battlefield, adut_suit, leading_suit):
    strongest = battlefield[0]
    for card in battlefield:
        if card.beats(strongest, adut_suit, leading_suit):
            strongest = card

    return strongest


def find_strongest_nonadut(hand, suit, adut):
    strongest = None
    for card in hand:
        if card.suit == suit:
            if strongest is None:
                strongest = card
                continue
            if card.beats(strongest, adut, suit):
                strongest = card

    return strongest


def find_weakest_adut(hand, adut):
    weakest = None
    for card in hand:
        if card.suit == adut:
            if weakest is None:
                weakest = card
                continue
            if weakest.isStronger(card):
                weakest = card

    return weakest


def find_strongest_adut(hand, adut):
    strongest = None
    for card in hand:
        if card.suit == adut:
            if strongest is None:
                strongest = card
                continue
            if card.isStronger(strongest):
                strongest = card

    return strongest


def fight(battlefield, adut):
    for player, card in battlefield.items():
        leading_player = player
        strongest = card
        leading_suit = card.suit
        break
    for player, card in battlefield.items():
        if card.suit == adut and strongest.suit != adut:
            strongest = card
            leading_player = player
        elif card.suit == adut and strongest.suit == adut:
            if card.isStronger(strongest):
                strongest = card
                leading_player = player
        elif card.suit == leading_suit and strongest.suit != adut and card.isStronger(strongest):
            strongest = card
            leading_player = player

    points_in_a_round = 0
    for card in battlefield.values():
        leading_player.points += card.value
        points_in_a_round += card.value

    time.sleep(1.5)
    print("Player {0} wins this fight, accumulating {1} points!".format(leading_player.name, points_in_a_round))
    print()

    return leading_player


p1 = Player("1")
p2 = Player("2")
p3 = Player("3")
p4 = Player("4")

c1 = Card("Denari", 7)
c2 = Card("Denari", 4)
c3 = Card("Bastoni", 1)
c4 = Card("Coppa", 1)

battlecard1 = Card("Spade", 6)
battlecard2 = Card("Coppa", 12)

c1.set_heuristic("Bastoni")
c2.set_heuristic("Bastoni")
c3.set_heuristic("Bastoni")
c4.set_heuristic("Bastoni")

p1.current_hand.append(c1)
p1.current_hand.append(c2)
p1.current_hand.append(c3)
p1.current_hand.append(c4)

played = p1.ai_card_play(3, "Spade", [battlecard1, battlecard2], "Spade")

print(played.suit, played.power)


