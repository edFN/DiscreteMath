INF_MIN = float('-inf')
INF_MAX = float('+inf')

class Point:
    is_open: bool
    x: float

    def __init__(self, x: float, is_open: bool):
        self.x = x
        self.is_open = is_open

    def is_open(self) -> bool:
        return self.is_open is True

    def get_x(self) -> float:
        return self.x

    def __lt__(self, other):
        if not isinstance(other, (float, Point)):
            raise TypeError("Invalid operand")

        sc = other if isinstance(other, float) else other.x

        return self.x < sc

    def __le__(self, other):
        if not isinstance(other, (float, Point)):
            raise TypeError("Invalid operand")

        sc = other if isinstance(other, float) else other.x

        return self.x <= sc

    def __gt__(self, other):
        if not isinstance(other, (float, Point)):
            raise TypeError("Invalid operand")

        sc = other if isinstance(other, float) else other.x

        return self.x > sc
    def __str__(self):
        return "Lol"

    def __ge__(self, other):
        if not isinstance(other, (float, Point)):
            raise TypeError("Invalid operand")

        sc = other if isinstance(other, float) else other.x

        return self.x >= sc


class LineSegment:
    p1: Point
    p2: Point

    def __init__(self, p1: Point, p2: Point) -> None:
        if p1.x > p2.x:
            self.p1 = p2
            self.p2 = p1
        else:
            self.p1 = p1
            self.p2 = p2

    def __str__(self):
        ret = ""
        if self.p1.is_open:
            ret += f"({self.p1.x};"

            if self.p2.is_open:
                ret += f"{self.p2.x})"
            else:
                ret += f"{self.p2.x}]"
        else:
            ret += f"[{self.p1.x};"
            if self.p2.is_open:
                ret += f"{self.p2.x})"
            else:
                ret += f"{self.p2.x}]"
        return ret

    def get_p1(self) -> Point:
        return self.p1

    def get_p2(self) -> Point:
        return self.p2

#fix it
def is_subset(main: LineSegment, check: LineSegment) -> bool:
    if main.p1.x <= check.p1.x and main.p2.x >= check.p2.x:
        return True
    return False


def has_point(main: LineSegment, point: Point) -> bool:
    if main.p1.x == point.x:
        return not main.p1.is_open or main.p1.x == abs(INF_MAX)
    if point.x == main.p2.x:
        return not main.p2.is_open or main.p2.x == abs(INF_MAX)

    if main.p1.x < point.x < main.p2.x:
        return True

    return False


def intersect_line(line1:LineSegment,line2:LineSegment):
    l_s = None
    if line1.p1.x <= line2.p1.x:
        # if item.p2.x < item2.p2.x:
        #     continue
        if line1.p2.x >= line2.p1.x:
            if line1.p2.x >= line2.p2.x:
                l_s = LineSegment(line2.p1, line2.p2)

            else:
                l_s = LineSegment(line2.p1, line1.p2)
    else:
        if line1.p1.x > line2.p2.x:
            return None
        if line1.p2.x >= line2.p2.x:
            l_s = LineSegment(line1.p1, line2.p2)
        else:
            l_s = LineSegment(line1.p1, line1.p2)
    return l_s


class LineSegmentSet:
    line_segments: set

    def __init__(self) -> None:
        self.line_segments = set()

    def add(self, item: LineSegment):
        if item is not None:
            self.line_segments.add(item)
        else:
            raise ValueError('РћС‚СЂРµР·РѕРє РЅРµ РјРѕР¶РµС‚ Р±С‹С‚СЊ РїСѓСЃС‚С‹Рј')

    def __str__(self):
        ret = ""
        i = 1
        for item in self.line_segments:
            if i == len(self.line_segments):
                ret += str(item)
                break
            i += 1
            ret += str(item)+" U "
        return ret
#fix it
    def sorted_points(self):
        points = []
        for item in self.line_segments:
            points += [item.p1]
            points += [item.p2]

        points.sort()
        points = self.delete_dupl(points)
        for i in points:
            print(i.x)
        return points
    def sorted_points(self,another):
        points = []
        for item in self.line_segments:
            points += [item.p1]
            points += [item.p2]
        for item in another.line_segments:
            points += [item.p1]
            points += [item.p2]


        points.sort()
        points = self.delete_dupl(points)
        for i in points:
            print(i.x)
        return points
    def delete_dupl(self,arr): #so bad
        new_arr = []
        ret_arr = []
        if(len(arr) < 2):
            return arr
        for i in range(len(arr)):
            if arr[i].x not in new_arr:
                new_arr.append(arr[i].x)
                ret_arr.append(arr[i])
        return ret_arr


def segment_intersect(set1: LineSegmentSet, set2: LineSegmentSet) -> LineSegmentSet:
    intersect = LineSegmentSet()
    for item in set1.line_segments:
        for item2 in set2.line_segments:
            if item.p1.x <= item2.p1.x:
                # if item.p2.x < item2.p2.x:
                #     continue
                if item.p2.x >= item2.p1.x:
                    if item.p2.x >= item2.p2.x:
                        l_s = LineSegment(item2.p1, item2.p2)
                        intersect.add(l_s)
                    else:
                        l_s = LineSegment(item2.p1, item.p2)
                        intersect.add(l_s)
            else:
                if item.p1.x > item2.p2.x:
                    continue

                if item.p2.x >= item2.p2.x:
                    l_s = LineSegment(item.p1, item2.p2)
                    intersect.add(l_s)
                else:
                    l_s = LineSegment(item.p1, item.p2)
                    intersect.add(l_s)
    return intersect


def segment_plus(set1: LineSegmentSet, set2: LineSegmentSet) -> LineSegmentSet:
    plus = LineSegmentSet()

    intersected = segment_intersect(set1, set2)

    if len(intersected.line_segments) == 0:
        for item in set1.line_segments:
            plus.add(item)
        for item in set2.line_segments:
            plus.add(item)
    else:
        for item in set1.line_segments:
            connected = []
            for item2 in set2.line_segments:
                if is_subset(item, item2):
                    connected.append(item)
                elif is_subset(item2, item):
                    connected.append(item2)
                elif has_point(item, item2.p1):
                    connected.append(LineSegment(item.p1, item2.p2))
                elif has_point(item, item2.p2):
                    connected.append(LineSegment(item2.p1, item.p2))
                else:
                    plus.add(item2)
            if(len(connected) > 0):
                init = False
                min_a = None
                max_a = None
                for con in connected:
                    if not init:
                        min_a = con.p1
                        max_a = con.p2
                        init = True
                    else:
                        if min_a > con.p1:
                            min_a = con.p1
                        if max_a < con.p2:
                            max_a = con.p2

                plus.add(LineSegment(min_a, max_a))

    arr = list(plus.line_segments)
    item = arr[0]
    for i in range(len(arr)):
        for j in range(len(arr)):
            if i==j: continue
            if(is_subset(arr[i],arr[j])):
                arr[j] = arr[i]
            elif(is_subset(arr[j],arr[i])):
                arr[i] = arr[j]
    plus.line_segments = set(arr)
    return plus


def segment_sub(set1: LineSegmentSet, set2: LineSegmentSet):
    sub = LineSegmentSet()

    for item in set1.line_segments:
        g = True
        temp = []
        for item2 in set2.line_segments:
            if is_subset(item, item2):
                temp.append(LineSegment(item.p1, Point(item2.p1.x, True)))
                temp.append(LineSegment(Point(item2.p2.x, True), item.p2))
                g = False
            elif is_subset(item2,item):
                temp = []
                g = False
                break
            elif has_point(item, item2.p1):
                temp.append(LineSegment(item.p1, Point(item2.p1.x, True)))
                g = False
            elif has_point(item, item2.p2):
                temp.append(LineSegment(Point(item2.p2.x, True), item.p2))
                g = False

        if g:
            sub.add(item)
        else:
            if(len(temp) == 0): continue
            x = temp[0]
            for i in range(1, len(temp)):
                if intersect_line(x, temp[i]) is not None:
                    x = intersect_line(x, temp[i])
                else:
                    sub.add(temp[i])
            sub.add(x)
    return sub

