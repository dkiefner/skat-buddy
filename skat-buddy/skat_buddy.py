from game.game import Game
from game.game_state_machine import GameStateMachine
from game.game_variant import GameVariantGrand
from game.state.game_state_bid import BidCallAction, BidAcceptAction, BidPassAction, PickUpSkatAction, \
    PutDownSkatAction, \
    DeclareGameVariantAction
from game.state.game_state_start import GameStateStart, StartGameAction
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
