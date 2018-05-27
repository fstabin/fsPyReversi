from reversi_status import TeamType
from reversi_status import ReversiStatus
import sys

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
    __mWinBonus = 100000

    def __init__(self, mxDepth = 4):
        self.__mMxDepth = mxDepth

    def calcStatusScore(self,status):
        score = 0
        for y in range(0,8):
            for x in range(0,8):
                score += self.__scoreMap[y][x] * status.getStone(x,y)
        score *= status.getCurrentPlayer()
        if status.isFineshed():
            score += self.__mWinBonus * status.getWinner() * status.getCurrentPlayer()
        return score

    def mini_max(self, status, depth):
        if depth >= self.__mMxDepth:
            return self.calcStatusScore(status)
        if status.isFineshed():
            return self.calcStatusScore(status)
        score = -1000000
        
        pl = status.getPutableList()
        if len(pl) > 0:
            for i in pl:
                status.putStone(i[0],i[1])
                score = max(-self.mini_max(status, depth + 1), score)
                status.doOver()
        else:
            status.passPlayer()
            score = max(-self.mini_max(status, depth + 1),score)
            status.doOver()
            
        return score

    def alpha_beta(self, status, depth, a, b):
        if depth >= self.__mMxDepth:
            return self.calcStatusScore(status)
        if status.isFineshed():
            return self.calcStatusScore(status)
        score = -1000000
        
        pl = status.getPutableList()
        if len(pl) > 0:
            for i in pl:
                status.putStone(i[0],i[1])
                score = max(-self.alpha_beta(status, depth + 1, -b, -score), score)
                status.doOver()
                if score < a:
                    return a
        else:
            status.passPlayer()
            score = max(-self.alpha_beta(status, depth + 1, -b, -score),score)
            status.doOver()
            
        return score

    def think(self, status):
        """リバーシの打つ手を考えて出力する
        put x y
        pass
        quit
        """
        pl = status.getPutableList()
        if len(pl) > 0:
            score = -1000000
            x = 0
            y = 0
            for i in pl:
                status.putStone(i[0],i[1])
                tmpScore = -self.alpha_beta(status, 1, -1000000, 1000000)
                status.doOver()
                if tmpScore > score:
                    score = tmpScore
                    x = i[0]
                    y = i[1]
            print('put ',str(x) , " ", str(y))
            return ("put", x, y)
        else:
            return ['pass']
                