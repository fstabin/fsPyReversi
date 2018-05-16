from enum import Enum
class TeamType(Enum):
    BLACK = 1
    WHITE = -1
    NONE = 0

class ReversiStatus:
    """リバーシゲーム本体の状態すべてをコントロールするクラス"""
    __stoneRowLen = 8
    __stoneRowAmount = 8
    __stoneBuffer = list(__stoneRowLen * __stoneRowAmount) #リバーシ台
    __currentTeamType = TeamType.BLACK

    def __init__(self):
        for i in range(0, len(list)):
            self.__stoneBuffer[i] = TeamType.NONE
        return

    def __getStoneRef(self, x, y):
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
        if((x <= -1) | (self.__stoneRowLen <= x) | (y <= -1) | (self.__stoneRowLen <= y)):
            return IndexError
        return ref(self.__stoneBuffer[x + y * self.__stoneRowLen])

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
        ref = self.__getStoneRef(x, y)
        ref = aTeamType
 
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
        return self.__getStoneRef(x, y)

    def putStone(delf, x, y):
        """
        リバーシ台上の石を強制的に変更する\n
        戻り値:\n
            bool\n
        入力:\n
            x,y: int型 座標\n
            aTeamType: TeamType型 変更する後のチーム(石をなくすにはTeamType.NONE)を指定する\n
        例外:\n
            IndexError: x,yが台の範囲外の時\n
        """
        (self.__getStoneRef(x, y)) = self.__currentTeamType

        return True


