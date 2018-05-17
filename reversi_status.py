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
    __mStoneBuffer = list(__mStoneRowLen * __mStoneRowAmount) #リバーシ台
    __mCurrentTeamType = TeamType.BLACK

    __mStoneBufferChangeLog = list()#[x, y, list[8]]

    def __init__(self):
        for i in range(0, len(list)):
            self.__mStoneBuffer[i] = TeamType.NONE
        return

    def __getStoneIndex(self, x, y):
        """
        x,y座標から、リバーシ台上の石の位置を特定する\n
        戻り値:
            int インデックス(失敗時-1)\n
        入力:
            x,y: int型 座標\n
        \n
        例外:
            IndexError: x,yが台の範囲外の時\n
        """
        if((x <= -1) | (self.__mStoneRowLen <= x) | (y <= -1) | (self.__mStoneRowLen <= y)):
            return None
        return x + y * self.__mStoneRowLen

    def checkPutable(self, x, y, aTeamType):
        if self.getStone(x,y) != TeamType.NONE:
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
                stone = self.getStone(x,y)
                if stone == None:
                    return
                elif stone == -aTeamType:
                    l += 1
                    break 
                elif stone == aTeamType:
                    if l >= 1:
                        return True
        return False

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
        self.__mStoneBuffer[self.__getStoneIndex(x,y)]  = aTeamType
 
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
        return  self.__mStoneBuffer[self.__getStoneIndex(x,y)]

    def putStone(self, x, y):
        """
        リバーシ台上の石を強制的に変更する\n
        戻り値:\n
            変更した長さint[8]\n
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
        self.__mStoneBufferChangeLog.append(self.__mStoneBuffer)
        return revl


