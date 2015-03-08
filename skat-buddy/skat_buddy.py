from model.game import Game
from model.player import Player


game = Game([Player("Player1"), Player("Player2"), Player("Player3")])
game.start_new()

print("\nSkat:")
for card in game.skat:
    print(card)

print("\n" + game.players[0].name + ":")
for card in game.players[0].cards:
    print(card)

print("\n" + game.players[1].name + ":")
for card in game.players[1].cards:
    print(card)

print("\n" + game.players[2].name + ":")
for card in game.players[2].cards:
    print(card)

print("\nDealer=" + game.get_dealer().name)
print("First_Seat=" + game.get_first_seat().name)
print("Second_Seat=" + game.get_second_seat().name)
print("Third_Seat=" + game.get_third_seat().name)