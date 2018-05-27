from reversi_status import TeamType
from reversi_status import ReversiStatus

class ReversiAI:
    __scoreMap = [
        [100,10,10,10,10,10,10,100],
        [10,-5,-5,-5,-5,-5,-5,10],
        [10,-5,-3,-3,-3,-3,-5,10],
        [10,-5,-3,5,5,-3,-5,10],
        [10,-5,-3,5,5,-3,-5,10],
        [10,-5,-3,-3,-3,-3,-5,10],
        [10,-5,-5,-5,-5,-5,-5,10],
        [100,10,10,10,10,10,10,100]
    ]
    def think(self, status):
        """リバーシの打つ手を考えて出力する"""
        ptype = status.getCurrentPlayer()
        sstack = [(status, status.getPutableList(status.getCurrentPlayer()) ,0, 0)]#状態,配置リスト,深度,得点 
        depth = 0

        while(len(sstack) > 0){
            
        }