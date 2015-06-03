from game.game import Game
from game.game_state_machine import GameStateMachine
from game.game_variant import GameVariantGrand
from game.state.game_state_bid import BidCallAction, BidAcceptAction, BidPassAction, PickUpSkatAction, \
    PutDownSkatAction, \
    DeclareGameVariantAction
from game.state.game_state_play import PlayCardAction
from game.state.game_state_start import GameStateStart, StartGameAction
from model.card import Card
from model.player import Player

player1 = Player(1, "Alice")
player2 = Player(2, "Bob")
player3 = Player(3, "Carol")
game = Game([player1, player2, player3])
state_machine = GameStateMachine(GameStateStart(game))

# ------------------------------------------------------------
# Simulate a game
# ------------------------------------------------------------
print("Start game")
state_machine.handle_action(StartGameAction())

print("\nDealer=" + game.get_dealer().name)
print("First_Seat=" + game.get_first_seat().name + " " + str(game.get_first_seat().cards))
print("Second_Seat=" + game.get_second_seat().name + " " + str(game.get_second_seat().cards))
print("Third_Seat=" + game.get_third_seat().name + " " + str(game.get_third_seat().cards))
print("Skat=" + str(game.skat))

# call from carol
print("\n" + player3.name + " bids 18")
state_machine.handle_action(BidCallAction(player3, 18))
# accept from bob
print(player2.name + " accepts 18")
state_machine.handle_action(BidAcceptAction(player2, 18))
# call from carol
print(player3.name + " bids 20")
state_machine.handle_action(BidCallAction(player3, 20))
# pass from bob
print(player2.name + " pass on 20")
state_machine.handle_action(BidPassAction(player2, 20))
# pass from alice
print(player1.name + " pass on 20")
state_machine.handle_action(BidPassAction(player1, 20))

# carol is player3
# carol pick up skat
print(player3.name + " is player3")
print(player3.name + " picked up skat")
state_machine.handle_action(PickUpSkatAction(player3))
print("\n" + player3.name + ": " + str(player3.cards))

# carol put down skat
print(player3.name + " puts skat down")
state_machine.handle_action(PutDownSkatAction(player3, player3.cards[0:2]))
print("\nSkat: " + str(game.skat))

# carol declare game variant
print(player3.name + " declares game variant grand")
state_machine.handle_action(DeclareGameVariantAction(player3, GameVariantGrand()))
print("\n" + player3.name + ": " + str(player3.cards))

game.dealer = 1
game.trick.leader = player3
game.skat = [Card(Card.Suit.CLUB, Card.Face.EIGHT), Card(Card.Suit.CLUB, Card.Face.NINE)]
player3.cards = [Card(Card.Suit.SPADE, Card.Face.JACK), Card(Card.Suit.CLUB, Card.Face.TEN), Card(Card.Suit.DIAMOND, Card.Face.ACE), Card(Card.Suit.HEARTS, Card.Face.JACK), Card(Card.Suit.SPADE, Card.Face.ACE), Card(Card.Suit.HEARTS, Card.Face.ACE), Card(Card.Suit.HEARTS, Card.Face.TEN), Card(Card.Suit.SPADE, Card.Face.TEN), Card(Card.Suit.DIAMOND, Card.Face.KING), Card(Card.Suit.DIAMOND, Card.Face.EIGHT)]
player1.cards = [Card(Card.Suit.CLUB, Card.Face.JACK), Card(Card.Suit.CLUB, Card.Face.KING), Card(Card.Suit.DIAMOND, Card.Face.SEVEN), Card(Card.Suit.SPADE, Card.Face.SEVEN), Card(Card.Suit.SPADE, Card.Face.EIGHT), Card(Card.Suit.HEARTS, Card.Face.EIGHT), Card(Card.Suit.HEARTS, Card.Face.KING), Card(Card.Suit.SPADE, Card.Face.KING), Card(Card.Suit.CLUB, Card.Face.SEVEN), Card(Card.Suit.CLUB, Card.Face.QUEEN)]
player2.cards = [Card(Card.Suit.DIAMOND, Card.Face.JACK), Card(Card.Suit.CLUB, Card.Face.ACE), Card(Card.Suit.DIAMOND, Card.Face.TEN), Card(Card.Suit.HEARTS, Card.Face.SEVEN), Card(Card.Suit.SPADE, Card.Face.QUEEN), Card(Card.Suit.HEARTS, Card.Face.NINE), Card(Card.Suit.HEARTS, Card.Face.QUEEN), Card(Card.Suit.SPADE, Card.Face.NINE), Card(Card.Suit.DIAMOND, Card.Face.QUEEN), Card(Card.Suit.DIAMOND, Card.Face.NINE)]

# trick 1
print("\nTrick " + str(game.round) + ":")
state_machine.handle_action(PlayCardAction(player3, Card(Card.Suit.SPADE, Card.Face.JACK)))
state_machine.handle_action(PlayCardAction(player1, Card(Card.Suit.CLUB, Card.Face.JACK)))
state_machine.handle_action(PlayCardAction(player2, Card(Card.Suit.DIAMOND, Card.Face.JACK)))

# trick 2
print("\nTrick " + str(game.round) + ":")
state_machine.handle_action(PlayCardAction(player1, Card(Card.Suit.CLUB, Card.Face.KING)))
state_machine.handle_action(PlayCardAction(player2, Card(Card.Suit.CLUB, Card.Face.ACE)))
state_machine.handle_action(PlayCardAction(player3, Card(Card.Suit.CLUB, Card.Face.TEN)))

# trick 3
print("\nTrick " + str(game.round) + ":")
state_machine.handle_action(PlayCardAction(player2, Card(Card.Suit.DIAMOND, Card.Face.TEN)))
state_machine.handle_action(PlayCardAction(player3, Card(Card.Suit.DIAMOND, Card.Face.ACE)))
state_machine.handle_action(PlayCardAction(player1, Card(Card.Suit.DIAMOND, Card.Face.SEVEN)))

# trick 4
print("\nTrick " + str(game.round) + ":")
state_machine.handle_action(PlayCardAction(player3, Card(Card.Suit.HEARTS, Card.Face.JACK)))
state_machine.handle_action(PlayCardAction(player1, Card(Card.Suit.SPADE, Card.Face.SEVEN)))
state_machine.handle_action(PlayCardAction(player2, Card(Card.Suit.HEARTS, Card.Face.SEVEN)))

# trick 5
print("\nTrick " + str(game.round) + ":")
state_machine.handle_action(PlayCardAction(player3, Card(Card.Suit.SPADE, Card.Face.ACE)))
state_machine.handle_action(PlayCardAction(player1, Card(Card.Suit.SPADE, Card.Face.EIGHT)))
state_machine.handle_action(PlayCardAction(player2, Card(Card.Suit.SPADE, Card.Face.QUEEN)))

# trick 6
print("\nTrick " + str(game.round) + ":")
state_machine.handle_action(PlayCardAction(player3, Card(Card.Suit.HEARTS, Card.Face.ACE)))
state_machine.handle_action(PlayCardAction(player1, Card(Card.Suit.HEARTS, Card.Face.EIGHT)))
state_machine.handle_action(PlayCardAction(player2, Card(Card.Suit.HEARTS, Card.Face.NINE)))

# trick 7
print("\nTrick " + str(game.round) + ":")
state_machine.handle_action(PlayCardAction(player3, Card(Card.Suit.HEARTS, Card.Face.TEN)))
state_machine.handle_action(PlayCardAction(player1, Card(Card.Suit.HEARTS, Card.Face.KING)))
state_machine.handle_action(PlayCardAction(player2, Card(Card.Suit.HEARTS, Card.Face.QUEEN)))

# trick 8
print("\nTrick " + str(game.round) + ":")
state_machine.handle_action(PlayCardAction(player3, Card(Card.Suit.SPADE, Card.Face.TEN)))
state_machine.handle_action(PlayCardAction(player1, Card(Card.Suit.SPADE, Card.Face.KING)))
state_machine.handle_action(PlayCardAction(player2, Card(Card.Suit.SPADE, Card.Face.NINE)))

# trick 9
print("\nTrick " + str(game.round) + ":")
state_machine.handle_action(PlayCardAction(player3, Card(Card.Suit.DIAMOND, Card.Face.KING)))
state_machine.handle_action(PlayCardAction(player1, Card(Card.Suit.CLUB, Card.Face.SEVEN)))
state_machine.handle_action(PlayCardAction(player2, Card(Card.Suit.DIAMOND, Card.Face.QUEEN)))

# trick 10
print("\nTrick " + str(game.round) + ":")
state_machine.handle_action(PlayCardAction(player3, Card(Card.Suit.DIAMOND, Card.Face.EIGHT)))
state_machine.handle_action(PlayCardAction(player1, Card(Card.Suit.CLUB, Card.Face.QUEEN)))
state_machine.handle_action(PlayCardAction(player2, Card(Card.Suit.DIAMOND, Card.Face.NINE)))

print("\nGame Over")
print("Declarer points: " + str(player3.sum_trick_values()))
print("Defender points: " + str(120 - player3.sum_trick_values()))
print("Winner is: " + player3.name)
