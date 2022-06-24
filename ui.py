import tkinter
from tkinter import Tk, Canvas, Frame, BOTH, RIGHT
from tkinter import Button
import SegmentReader

from main_logic import *

class PointGraphics:
    fill:bool

    name:float
    def __init__(self,fill,name):

        self.fill = fill
        self.name = name

        self.y = 95

    def convert_from_segment_point(self,point:Point):
        self.name = point.x
        self.fill = point.is_open
    def draw(self,x,canva: tkinter.Canvas):
        if not self.fill:
            canva.create_oval(x, self.y, x + 16, self.y-15, fill="black")
        else:
            canva.create_oval(x, self.y, x + 16, self.y - 15,fill="white")

        canva.create_text(x+5, self.y+10, text=str(self.name))






class MainForm(Frame):


    def __init__(self):
        super().__init__(bg="red")

        self.line_width = 450
        self.screen_width = self.line_width + 50
        self.line_point_h = int(self.line_width)/4
        self.point_dictionary = {}
        self.initUi()
    def init_canva(self):
        line_padding_y = 90
        self.canva.create_line(30, line_padding_y, 1200 - 50, line_padding_y, width=2)
        self.canva.create_line(1200 - 50, line_padding_y, 1200 - 70, line_padding_y - 10, width=2)
        self.canva.create_line(1200 - 50, line_padding_y, 1200 - 70, line_padding_y + 10, width=2)
        self.canva.create_text(1200 - 37, line_padding_y, text="X", font="Courier 14")
        self.canva.create_text(25, 60, text="-∞", font='Courier 23')
        self.canva.create_text(1200 - 60, 60, text="∞", font='Courier 23')
    def initUi(self):
        self.master.title("Draw lines")

        self.pack(fill=BOTH,expand=1,side=tkinter.LEFT)

        frame1_canva = Frame(self)

        line_padding_y = 90
        self.canva = Canvas(frame1_canva,width=1200)
        self.start = 30
        self.end = 1200-70
        self.canva.create_line(30,line_padding_y,1200-50,line_padding_y,width=2)
        self.canva.create_line(1200-50,line_padding_y,1200-70,line_padding_y-10,width=2)
        self.canva.create_line(1200 - 50, line_padding_y, 1200 - 70, line_padding_y+10, width=2)
        self.canva.create_text(1200-37,line_padding_y,text="X",font="Courier 14")
        self.canva.create_text(25,60,text="-∞",font='Courier 23')
        self.canva.create_text(1200-60, 60, text="∞", font='Courier 23')
        lbl = tkinter.Label(frame1_canva,text="Числовая прямая",borderwidth=1,
                            font='Courier 20')

        self.canva.grid(column=0,row=2)
        lbl.grid(column=0,row=1)

        frame1_canva.grid(row=0,column=0,rowspan=2,sticky='nswe')

        frame2_main = Frame(self)

        A = tkinter.Label(frame2_main,text="A = ",font = 'Courier 14')
        A.grid(column=0,row=0)
        B = tkinter.Label(frame2_main,text="B = ",font = 'Courier 14')
        B.grid(column=0,row=2)
        btn = Button(frame2_main,text="OK",borderwidth=10,width=25,command=self.process)
        btn.grid(row=0,column=2,columnspan=3,sticky='nswe')
        btn1 = Button(frame2_main, text="CLEAR", borderwidth=10,width=25,command=self.func)

        btn1.grid(row=2, column=2,columnspan=3)

        self.entry = tkinter.Entry(frame2_main,width=82,font = 'Courier 14',borderwidth=4)
        self.entry.grid(rowspan=2,columnspan=1,row=0,column=1,sticky='nswe',pady=10)
        self.entry1 = tkinter.Entry(frame2_main, width=82, font='Courier 14',borderwidth=4)
        self.entry1.grid(rowspan=2, columnspan=1, row=2, column=1, sticky='nswe', pady=15)

        frame2_main.grid(row=3,column=0,columnspan=5,sticky='nswe')

        lbl_frame = Frame(self)
        self.lbl_intersect = tkinter.Label(lbl_frame,text="",font = 'Courier 12')
        self.lbl_sum = tkinter.Label(lbl_frame,text="",font = 'Courier 12')
        self.lbl_sub = tkinter.Label(lbl_frame,text="",font = 'Courier 12')

        self.lbl_intersect.grid(column=1,row=0,pady=15)
        self.lbl_sum.grid(column=1,row=1,pady=15)
        self.lbl_sub.grid(column=1,row=2,pady=15)

        lbl_frame.grid(row=5,rowspan=2,sticky='nswe')



    def func(self):
        self.entry.delete(0,'end')
        self.entry1.delete(0,'end')

    def process(self) -> LineSegmentSet:
        set = LineSegmentSet()
        if self.entry.get() == "" or self.entry1.get() == "":
            print("Error")
            return

        first_set = self.entry.get()
        second_set = self.entry1.get()
        #make a parsing
        first_set1 =SegmentReader.SegmentSetReader(first_set).read()
        if(first_set1 is None):
            print("Error")
            return None
        second_set1 = SegmentReader.SegmentSetReader(second_set).read()
        if (second_set1 is None):
            print("Error")
            return None


        self.canva.delete("all")
        self.init_canva()
        self.make_point(first_set1,second_set1)

        inter = segment_intersect(first_set1,second_set1)
        if(len(inter.line_segments) != 0):
            self.lbl_intersect.config(text=f"A&B = {str(inter)}")
        else:
            self.lbl_intersect.config(text=f"A&B = 0 (пустое множество)")

        sum = segment_plus(first_set1,second_set1)
        self.lbl_sum.config(text = f"A|B = {str(sum)}")
        sub = segment_sub(first_set1,second_set1)
        self.lbl_sub.config(text=f"A\B = {str(sub)}")

        for item in inter.line_segments:
            self.make_crosses(item.p1.x,item.p2.x)







    def make_crosses(self,x1,x2):
        first_pos = self.point_dictionary[x1]
        second_pos = self.point_dictionary[x2]
        distance = abs(second_pos-first_pos) / 5

        x = first_pos
        print("distance: "+str(distance))

        for i in range(5):
            self.canva.create_line(x, 110 , x+distance+5, 95, width=2)
            x+=distance




    def make_point(self,segment:LineSegmentSet,another: LineSegmentSet):
        distance = (self.line_width-35-70) / ((len(segment.line_segments)+len(another.line_segments))*2) + 15


        x = self.start+distance

        arr = segment.sorted_points(another)

        for item in arr:
            if item.x == INF_MIN:
                PointGraphics(item.is_open, item.x).draw(12,self.canva)
                self.point_dictionary[item.x] = 12
            elif item.x == INF_MAX:
                PointGraphics(item.is_open,item.x).draw(self.end+12,self.canva)
                self.point_dictionary[item.x] = self.end +12
            else:
                PointGraphics(item.is_open, item.x).draw(x,self.canva)
                self.point_dictionary[item.x] = x
                x += distance

        #connecting
        y = 0
        for item in segment.line_segments:
            self.connect_points_from_dict(item.p1.x,item.p2.x,y)
            y += 4
        for item in another.line_segments:
            self.connect_points_from_dict(item.p1.x,item.p2.x,y)
            y += 4

    def connect_points_from_dict(self,x1,x2,up_y = 0):

        HEIGHT_UP = 55

        first_pos = self.point_dictionary[x1]
        second_pos = self.point_dictionary[x2]
        self.canva.create_line(first_pos+5,55-up_y,second_pos+5,55-up_y,width=2)
        self.canva.create_line(first_pos+7,85-up_y,first_pos+5,55-up_y,width=2)
        self.canva.create_line(second_pos+7,85-up_y,second_pos+5,55-up_y,width=2)


        # canva = Canvas(self,height=int(self.screen_width/2))
        #
        # canva.create_line(10,20,10+self.line_width,30)
        #
        # canva.pack(fill=BOTH,expand=1)
        # btn = Button(self,text="Process")
        #
        #
        # entry = tkinter.Entry(self,borderwidth=5)
        # entry.pack(side=tkinter.LEFT,padx=100)
        #
        # btn.pack(expand=1,side=tkinter.RIGHT)












