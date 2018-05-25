from enum import Enum
class TeamType(Enum):
    BLACK = 1
    WHITE = -1

    def __neg__(self):
        if self == TeamType.BLACK:
            return TeamType.WHITE
        if self == TeamType.WHITE:
            return TeamType.BLACK

class ReversiStatus:
    """リバーシゲーム本体の状態すべてをコントロールするクラス"""
    __mStoneRowLen = 8
    __mStoneRowAmount = 8
    __mStoneBuffer = list([None] * __mStoneRowLen * __mStoneRowAmount) #リバーシ台
    __mCurrentTeamType = TeamType.BLACK
    __mBlackStoneAmount = 0
    __mWhiteStoneAmount = 0
    __mDidPassBefore = 0
      
    def __str__(self):
        outstr = "CurrentPlayer = " + str(self.__mCurrentTeamType) + "\n"
        outstr += "x01234567\n"
        for j in range(0, self.__mStoneRowAmount):
            outstr += str(j)
            for i in range(0, self.__mStoneRowLen):
                stone = self.getStone(i,j)
                if stone == TeamType.BLACK:
                    outstr += "○"
                elif stone == TeamType.WHITE:
                    outstr += "●"
                else:
                    outstr += "□"
            outstr += "\n"
        return outstr

    def __getStoneIndex(self, x, y):
        """
        x,y座標から、リバーシ台上の石の位置を特定する\n
        戻り値:
            int インデックス(失敗時None)\n
        入力:
            x,y: int型 座標\n
        \n
        例外:
            IndexError: x,yが台の範囲外の時\n
        """
        if((x <= -1) | (self.__mStoneRowLen <= x) | (y <= -1) | (self.__mStoneRowLen <= y)):
            return None
        return x + y * self.__mStoneRowLen
    
    #初期化関連関数群

    def __init__(self):
        for i in range(0, len(self.__mStoneBuffer)):
            self.__mStoneBuffer[i] = None
        return    
    
    
    def FillStone(self, aTeamType):
        for j in range(0, self.__mStoneRowAmount):
            for i in range(0, self.__mStoneRowLen):
                self.setStone(i,j, aTeamType)

    #メンバを直接操作する関数群

    def setStone(self, x, y, aTeamType):
        """
        リバーシ台上の石を強制的に変更する\n
        戻り値:\n
            void\n
        入力:\n
            x,y: int型 座標\n
            aTeamType: TeamType型 変更する後のチーム(石をなくすにはTeamType.NONE)を指定する\n
        例外:\n
            IndexError: x,yが台の範囲外の時\n
        """
        if self.getStone(x,y) == TeamType.WHITE:
            self.__mWhiteStoneAmount -= 1
        if aTeamType == TeamType.WHITE:
            self.__mWhiteStoneAmount += 1
        if self.getStone(x,y) == TeamType.BLACK:
            self.__mBlackStoneAmount -= 1
        if aTeamType == TeamType.BLACK:
            self.__mBlackStoneAmount += 1
        self.__mStoneBuffer[self.__getStoneIndex(x,y)]  = aTeamType
    
    def changePlayer(self, DidCurrentPlayerPass):
        self.__mCurrentTeamType = -self.__mCurrentTeamType
        if(DidCurrentPlayerPass):
            self.__mDidPassBefore += 1
        else:
            self.__mDidPassBefore = 0

    #操作関数群

    def checkPutable(self, x, y, aTeamType):
        """
        指定された座標に石が置けるか確認する\n
        戻り値:\n
            bool 石が置けるかどうか\n
        入力:\n
            x,y: int型 座標
            aTeamType: TeamType型 石を置くチーム
        """
        if self.getStone(x,y) != None:
            return False
        ofsX = [-1,0,1,-1,1,-1,0,1]
        ofsY = [-1,-1,-1,0,0,1,1,1]
        for i in range(0,8):
            bx = x
            by = y
            l = 0
            while True:
                bx = bx + ofsX[i]
                by = by + ofsY[i]
                stone = self.getStone(bx,by)
                if stone == None:
                    break
                elif stone == -aTeamType:
                    l += 1
                elif stone == aTeamType:
                    if l >= 1:
                        return True
        return False

    def getPutableList(self, aTeamType):
        """
        石のおけるすべての座標のリストを取得する\n
        戻り値:\n
            [[int, int], [int, int], ...]\n
        入力:\n
            x,y: int型 座標
            aTeamType: TeamType型 変更する後のチーム(石をなくすにはTeamType.NONE)を指定する
        """
        putableList = list()
        for j in range(0, self.__mStoneRowAmount):
            for i in range(0, self.__mStoneRowLen):
                if self.checkPutable(i,j,aTeamType):
                    putableList.append([i,j])
        return putableList

    def getStone(self, x, y):
        """
        リバーシ台上の石のチーム情報を取得する\n
        戻り値:\n
            TeamType\n
        入力:\n
            x,y: int型 座標\n
        例外:\n
            IndexError: x,yが台の範囲外の時\n
        """
        index = self.__getStoneIndex(x,y)
        if index == None:
            return None
        else:
            return  self.__mStoneBuffer[index]

    def putStone(self, x, y):
        """
        リバーシ台上にゲームルールにのっとり石を配置する\n
        その後石を置く側を交代する\n
        戻り値:\n
            石が置けたとき　変更した長さint[8]\n
            おけなかったとき None
        入力:\n
            x,y: int型 座標\n
            aTeamType: TeamType型 変更する後のチーム(石をなくすにはTeamType.NONE)を指定する\n
        例外:\n
            IndexError: x,yが台の範囲外の時\n
        """
        #すでに石が置かれているときキャンセル
        if self.getStone(x,y) != None:
            return None

        #石を何個反転させるか判定し
        #石を強制的に変更する
        noChange = True
        ofsX = [-1,0,1,-1,1,-1,0,1]
        ofsY = [-1,-1,-1,0,0,1,1,1]
        revl = [0,0,0,0,0,0,0,0]#反転させる石の数
        for i in range(0,8):
            bx = x
            by = y
            while True:
                bx = bx + ofsX[i]
                by = by + ofsY[i]
                stone = self.getStone(bx, by)
                if stone == -self.__mCurrentTeamType:
                    revl[i] += 1
                elif stone  == self.__mCurrentTeamType:
                    if(revl[i] >= 1):
                        for rev in range(1, revl[i] + 1):
                            self.setStone(x + ofsX[i] * rev,y + ofsY[i] * rev, self.__mCurrentTeamType)
                        noChange = False
                    break
                else:
                    revl[i] = 0
                    break
        if noChange:
            return None
        self.setStone(x, y, self.__mCurrentTeamType)
        self.changePlayer(False)
        return revl

    def getCurrentPlayer(self):
        return self.__mCurrentTeamType

    def getBlackStoneAmount(self):
        return self.__mBlackStoneAmount

    def getWhiteStoneAmount(self):
         return self.__mWhiteStoneAmount

    def isFineshed(self):
        return self.__mDidPassBefore >= 2

    def passPlayer(self):
        self.changePlayer(True)