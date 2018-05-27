from enum import IntEnum
import copy

class TeamType(IntEnum):
    BLACK = 1
    WHITE = -1
    NOTEAM = 0

    def __neg__(self):
        if self == TeamType.BLACK:
            return TeamType.WHITE
        if self == TeamType.WHITE:
            return TeamType.BLACK

offsX = [-1,0,1,-1,1,-1,0,1]
offsY = [-1,-1,-1,0,0,1,1,1]

class ReversiStatus:
    """リバーシゲーム本体の状態すべてをコントロールするクラス"""

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
        self.__mStoneRowLen = 8
        self.__mStoneRowAmount = 8
        self.__mStoneBuffer = list([TeamType.NOTEAM] * self.__mStoneRowLen * self.__mStoneRowAmount) #リバーシ台
        self.__mCurrentTeamType = TeamType.BLACK
        self.__mBlackStoneAmount = 0
        self.__mWhiteStoneAmount = 0
        self.__mChangeLog = []#[(int x,int y,list cahgeList[8]),...]
    
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
            aTeamType: TeamType型 変更する後のチーム(石をなくすにはTeamType.NOTEAM)を指定する\n
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
    
    def __changePlayer(self, changeInfo=None):
        """
        現在のプレイヤーの操作を記録しプレイヤーを交代する\n
        戻り値:
            なし\n
        入力:
            changeInfo: tuple(int x, int y, int changeList[8])\n
        \n
        例外:
            IndexError: x,yが台の範囲外の時\n
        """
        self.__mCurrentTeamType = -self.__mCurrentTeamType
        self.__mChangeLog.append(changeInfo)

    def __reverseStone(self, x,y, reverseList):
        for i in range(0,8):
            for rev in range(1, reverseList[i] + 1):
                self.setStone(x + offsX[i] * rev,y + offsY[i] * rev, self.__mCurrentTeamType)

    #ゲームを進行するクエリ関数群

    def putStone(self, x, y):
        """
        リバーシ台上にゲームルールにのっとり石を配置する\n
        その後石を置く側を交代する\n
        戻り値:\n
            石が置けたとき　変更した長さint[8]\n
            おけなかったとき None
        入力:\n
            x,y: int型 座標\n
            aTeamType: TeamType型 変更する後のチーム(石をなくすにはTeamType.NOTEAM)を指定する\n
        例外:\n
            IndexError: x,yが台の範囲外の時\n
        """
        #すでに石が置かれているときキャンセル
        if self.getStone(x,y) != TeamType.NOTEAM:
            return None

        #石を何個反転させるか判定し
        #石を強制的に変更する
        noChange = True
        reverseList = [0,0,0,0,0,0,0,0]#反転させる石の数
        for i in range(0,8):
            bx = x
            by = y
            while True:
                bx = bx + offsX[i]
                by = by + offsY[i]
                stone = self.getStone(bx, by)
                if stone == -self.__mCurrentTeamType:
                    reverseList[i] += 1
                elif stone  == self.__mCurrentTeamType:
                    if reverseList[i] >= 1:
                        noChange = False
                    break
                else:
                    reverseList[i] = 0
                    break
        if noChange:
            return None
        self.__reverseStone(x, y, reverseList)
        self.setStone(x, y, self.__mCurrentTeamType)
        self.__changePlayer((x, y, reverseList))
        return reverseList
    
    def passPlayer(self):
        self.__changePlayer()
    
    def doOver(self):
        changeInfo = self.__mChangeLog[len(self.__mChangeLog) - 1]
        self.__mChangeLog.pop()
        
        if(changeInfo != None):

            x = changeInfo[0]
            y = changeInfo[1]
            reverseList = changeInfo[2]#反転させる石の数
            self.__reverseStone(x, y, reverseList)
            self.setStone(x,y, TeamType.NOTEAM)

        self.__mCurrentTeamType = -self.__mCurrentTeamType

        return

    #ゲームの状態を取得する関数群
    
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

    def checkPutable(self, x, y, aTeamType):
        """
        指定された座標に石が置けるか確認する\n
        戻り値:\n
            bool 石が置けるかどうか\n
        入力:\n
            x,y: int型 座標
            aTeamType: TeamType型 石を置くチーム
        """
        if self.getStone(x,y) != TeamType.NOTEAM:
            return False
        for i in range(0,8):
            bx = x
            by = y
            l = 0
            while True:
                bx += offsX[i]
                by += offsY[i]
                stone = self.getStone(bx,by)
                if stone == -aTeamType:
                    l += 1
                elif stone == aTeamType:
                    if l >= 1:
                        return True
                    break
                else:
                    break
        return False

    def getPutableList(self):
        """
        石のおけるすべての座標のリストを取得する\n
        戻り値:\n
            [[int, int], [int, int], ...]\n
        入力:\n
            x,y: int型 座標
        """
        putableList = list()
        for j in range(0, self.__mStoneRowAmount):
            for i in range(0, self.__mStoneRowLen):
                if self.checkPutable(i,j,self.getCurrentPlayer()):
                    putableList.append([i,j])
        return putableList

    def getCurrentPlayer(self):
        return self.__mCurrentTeamType
    
    def getBlackStoneAmount(self):
        return self.__mBlackStoneAmount

    def getWhiteStoneAmount(self):
         return self.__mWhiteStoneAmount

    def isFineshed(self):
        """
        ゲームの終了条件(2連続でパスorすべての面が埋まっている)を満たしているか確認する関数\n
        戻り値:\n
            終了時　True
            それ以外 False
        入力:\n
            なし
        """
        finishedFlag = False
        clen = len(self.__mChangeLog)
        if clen >= 2:
            if (self.__mChangeLog[clen - 1] == self.__mChangeLog[clen - 2]) & (self.__mChangeLog[clen - 2] == None):
                finishedFlag = True
        if self.getBlackStoneAmount() + self.getWhiteStoneAmount() == 64:
             finishedFlag = True
        return finishedFlag

    def getWinner(self):
        """
        現段階で最も多い石のチームを返す関数\n
        戻り値:\n
            TeamType のうち石が多いほう
            ただし、あいこの時は NOTEAM が戻る
        入力:\n
            なし
        """
        if self.getBlackStoneAmount() > self.getWhiteStoneAmount():
            return TeamType.BLACK
        elif self.getBlackStoneAmount() < self.getWhiteStoneAmount():
            return TeamType.WHITE
        else:
            return TeamType.NOTEAM

    def getChangeLogLen(self):
        return len(self.__mChangeLog)

