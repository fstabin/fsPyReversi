from reversi_status import TeamType
from reversi_status import ReversiStatus
import reversi_ai
import reversi_user
import copy

stoneInitList = [[3,3,TeamType.WHITE], [3,4,TeamType.BLACK], [4,3,TeamType.BLACK], [4,4,TeamType.WHITE]]

status = ReversiStatus()
status.FillStone(TeamType.NOTEAM)
for l in stoneInitList:
    status.setStone(l[0], l[1], l[2])

mPlayers = {    
    TeamType.BLACK: reversi_ai.ReversiAI(3),
    TeamType.WHITE: reversi_ai.ReversiAI(1)
    }

while not status.isFineshed():
    print(str(status))  #局面描画
    #置けるところを確かめるため、置けるところのリストを取得
    l = status.getPutableList()
    if len(l) == 0:
        status.passPlayer()
        continue
    cmd = mPlayers[status.getCurrentPlayer()].think(copy.deepcopy(status))
    if cmd[0] == 'quit':
        break
    elif cmd[0] == 'put':
        x = cmd[1]
        y = cmd[2]
        status.putStone(x,y)
    elif cmd[0] == 'do_over':
        if status.getChangeLogLen() >= 2:
            status.doOver()
            status.doOver()

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

input("Enterで終了>>")