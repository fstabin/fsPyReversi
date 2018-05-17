from reversi_status import TeamType
from reversi_status import ReversiStatus

stoneInitList = [[3,3,TeamType.WHITE], [3,4,TeamType.BLACK], [4,3,TeamType.BLACK], [4,4,TeamType.WHITE]]

status = ReversiStatus()
status.FillStone(None)
for l in stoneInitList:
    status.setStone(l[0], l[1], l[2])
passed = 0

while True:
    print(str(status))  #局面描画
    l = status.getPutableList(status.getCurrentPlayer())
    if len(l) == 0:
        if passed == 1:
            break
        else:
            passed += 1
            continue
    uin = input(str(status.getCurrentPlayer()) + "?>>")
    if uin == "quit":
        break
    elif uin == "put":
        print("where?")
        try:
            x = int(input("x?>>"))
            y = int(input("y?>>"))
        except ValueError:
            print("where?(please input int value)")
            x = int(input("x?>>"))
            y = int(input("y?>>"))
        status.putStone(x,y)

print("result")
b = status.getBlackStoneAmount()
w = status.getWhiteStoneAmount()
print(str(TeamType.BLACK) + " = " + str(b))
print(str(TeamType.WHITE) + " = " + str(w))
winner = ""
if b > w:
    winner = str(TeamType.BLACK)
elif b < w:
    winner = str(TeamType.WHITE)
else:
    winner = "Draw"
print("Winner = " + winner)