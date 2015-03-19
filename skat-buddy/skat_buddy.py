from game.game import Game
from game.game_state_machine import GameStateMachine
from game.game_variant import GameVariantGrand
from game.state.game_state_bid import BidCallAction, BidAcceptAction, BidPassAction, PickUpSkatAction, \
    PutDownSkatAction, \
    DeclareGameVariantAction
from game.state.game_state_start import GameStateStart, StartGameAction
from model.player import Player

player1 = Player("Alice")
player2 = Player("Bob")
player3 = Player("Carol")
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
state_machine.handle_action(BidCallAction(player3, 18))
# accept from bob
state_machine.handle_action(BidAcceptAction(player2, 18))
# call from carol
state_machine.handle_action(BidCallAction(player3, 20))
# pass from bob
state_machine.handle_action(BidPassAction(player2, 20))
# pass from alice
state_machine.handle_action(BidPassAction(player1, 20))

# carol is declarer
# carol pick up skat
state_machine.handle_action(PickUpSkatAction(player3))
print("\n" + player3.name + ": " + str(player3.cards))

# carol put down skat
state_machine.handle_action(PutDownSkatAction(player3, player3.cards[0:2]))
print("\nSkat: " + str(game.skat))

# carol declare game variant
state_machine.handle_action(DeclareGameVariantAction(player3, GameVariantGrand()))
print("\n" + player3.name + ": " + str(player3.cards))