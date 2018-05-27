from reversi_status import TeamType
from reversi_status import ReversiStatus
import sys

class ReversiUser:


    def think(self, status):
        """リバーシの打つ手を考えて出力する
        put x y
        pass
        quit
        """
        while True:
            uin = input(str(status.getCurrentPlayer()) + "?>>")
            if uin == "quit":
                return ['quit']
            elif uin == "do_over":
                return ['do_over']
            elif uin == "put":
                print("where?")
                try:
                    x = int(input("x?>>"))
                    y = int(input("y?>>"))
                except ValueError:
                    print("please input int value")
                    continue
                return ("put", x, y)
                