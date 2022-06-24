from main_logic import *

class SegmentSetReader:
    input: str
    def __init__(self,read):
        self.input = read

    def read(self) -> LineSegmentSet:
        set = LineSegmentSet()
        splitted = self.input.split("U")
        for item in splitted:
            cur = self.process(item)
            if cur is not None:
                set.add(cur)
            else:
                print("Error")
                return None
        return set

    @staticmethod
    def process(str) -> LineSegment:
        str = str.replace(" ","")
        is_open1 = False
        if str[0] == "[": is_open1 = False
        elif str[0] == "(": is_open1 = True
        else:
            return None

        numbers = str[1:len(str)-1].split(";")

        try:
            p1 = float(numbers[0])
            p2 = float(numbers[1])
        except:
            print("Error")
            return None

        is_open2 = False
        if str[-1] == "]": is_open2 = False
        elif str[-1] == ")": is_open2 = True
        else:
            return None

        return LineSegment(Point(p1,is_open1),Point(p2,is_open2))
