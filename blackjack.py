import random as random
import sys


def starterDeck(shoe = 1):
    """sets up the cards, depending on how many shoes there are"""
    deck = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "A"] * 4 * shoe
    random.shuffle(deck)
    return deck

def draw(decks):
    """allowing players to draw and modify the deck"""
    card = decks[0]
    decks.remove(deck[0])
    return card, decks

def score(card):
    """calculates the score of an individual card"""
    try:
        score_ = int(card)
        return score_
    except ValueError:
        if card == "A":
            score_ = 1
            return score_
        else:
            score_ = 10
            return score_


def gameStart(deck):
    """sets up the game till the very first turn the player has any action"""
    playerHand1, newDeck = draw(deck)
    dealerHand1, newDeck = draw(newDeck)
    playerHand2, newDeck = draw(newDeck)
    dealerHand2, newDeck = draw(newDeck)
    playerHand = [playerHand1, playerHand2]
    dealerHand = [dealerHand1, dealerHand2]
    return playerHand, dealerHand, newDeck


def scoreCalc(playerHand):
    """Calculate the 'soft' and 'hard' score of player's hand (if they have an Ace in their hand)"""
    playerScore = 0
    for card in playerHand:
        playerScore += score(card)

    if "A" in playerHand:
        hard = playerScore
        soft = playerScore + 10
        if soft > 21:
            return hard
        else:
            return hard, soft
    else:
        return playerScore


def hit(hand, deck):
    """first player action, allows the player to hit (draw) one card, and add it to their hand"""
    newCard, newDeck = draw(deck)
    playerHand = hand[:]
    playerHand.append(newCard)
    return playerHand, newDeck

def dealerAction(dealerHand, deck):
    """This part details on what the dealer does (if the player doesn't bust on their turn), this strategy assumes that the dealer treats an Ace as an 1, unless they're at a 21"""
    print("Dealer's second card is:", dealerHand[1])
    print(dealerHand)
    dealerScore = scoreCalc(dealerHand)
    try:
        while True:
            if dealerScore[-1] == 21:
                print("Dealer wins!")
                print(dealerHand)
                return True
            else:
                    if dealerScore[-1] > 17:
                        dealerHand, newDeck = hit(dealerHand, deck)
                        dealerScore = scoreCalc(dealerHand)
                        if dealerScore[-1] == 21:
                            print(dealerHand)
                            print("Dealer wins!")

                            break
                        elif dealerScore[0] >= 17:
                            return(dealerHand)
                            break
                        elif dealerScore[0] and dealerScore[1] >= 21:
                            dealerScore = -1
                            return(dealerScore)
                            break
                    else:
                        return dealerHand

    except TypeError:
                    while True:
                        dealerHand, newDeck = hit(dealerHand, deck)
                        print("dealer hits!")
                        for i in dealerHand:
                            dealerScore = score(i) + dealerScore
                            if dealerScore >= 17:
                                if dealerScore == 21:
                                    print("Dealer wins!")
                                    print(dealerHand)
                                    print(dealerScore)
                                    return (dealerHand, dealerScore, newDeck)
                                elif dealerScore > 21:
                                    return(dealerHand, dealerScore, newDeck)
                        if dealerScore >= 17:
                            return(dealerHand, dealerScore, newDeck)
                            break


def playerAction(hand, deck):
    """player has more agencies, they can hit, stand, double, or split, while true, player turn can end two ways:"""
    """when player signals stand or when player busts"""
    """use nexted list to model player hands (and splitting)"""
    try:
        if hand[2]:
            choice = input("You can hit, stand or double")
    except IndexError:
        if hand[0] == hand[1]:
            choice = input("You can hit, stand, double, or split")
        else:
            choice = input("You can hit, stand or double")
    if choice == "hit":
        playerHand, newDeck = hit(hand, deck)
        return [playerHand], newDeck
    elif choice == "stand":
        return [hand], deck
    elif choice == "double":
        playerHand, newDeck = hit(hand, deck)
        return [playerHand], newDeck


def playerTurn(hand, deck):
    """we want player turn to: check for 21, check for busting, run on an infinite loop till player either hits, wins, or busts return True if player wins or """
    print("Your current hand is ", hand)
    playerHand, newDeck = playerAction(hand, deck)
    print(playerHand)


def handState(hand, deck):
    """takes in a set, returns a set"""

    handHolder = {
        "hands": [],  # store player hands (list of cards)
        "score": []  # store corresponding scores
    }
    handHolder["hands"].append(hand)

    score = 0
    i = 0

    while True:
        print("Your current hand is ", hand)
        playerHand, newDeck = playerAction(hand, deck)
        try:
            handHolder["hands"].append(playerHand[1])
        except IndexError:
            pass


        print(playerHand[0])
        score = scoreCalc(playerHand[0])
        if playerHand[0] == hand:
            print(hand)
            handHolder["score"].append(score)
            break

        if type(score) == int:
            if score > 21:
                print("You've busted!")
                handHolder["score"].append(score)
                break
            elif score == 21:
                print("You've won!")
                handHolder["score"].append(score)
                break

        elif type(score) == tuple:
            if score[0] == 21 or score[1] == 21:
                print("You won!")
                if score[0] == 21:
                    handHolder["score"].append(score[0])
                    break
                elif score[1] == 21:
                    handHolder["score"].append(score[1])
                    break

            elif score[0] > 21:
                print("You've busted!")
                handHolder["score"].append(score[0])
                break
            else:
                pass
        hand = playerHand[0]
        handHolder["hands"] = playerHand[0]

    return handHolder, newDeck







"""TODO chip system"""



def main():
    deck = starterDeck()
    playerHand, dealerHand, newDeck = gameStart(deck)
    playerHand, newDeck = handState(playerHand, newDeck)
    playerScore = (playerHand["score"][0])
    if playerScore > 21:
        print("Game Over!")
    else:
        dealerHand, dealerScore, newDeck =dealerAction(dealerHand, newDeck)
        if dealerScore > 21:
            print("Dealer busts! Dealer cards are ", dealerHand)
        elif dealerScore > playerScore:
            print("Dealer wins!")
        elif dealerScore == playerScore:
            print("Draw!")
        else:
            print("Player wins!")

if __name__ == "__main__":
    main()
