import tkinter as tk
import main as rs


root = tk.Tk()
root.title('Board GUI')
target = ''
choosing = True

class Piece:
    def __init__(self, name, pos:tuple, color, state='normal', cursor='hand2'):
        self.button = tk.Button(text    =name,
                                width   =3,
                                height  =1,
                                fg      =color,
                                command =self.click,
                                font    =('TkFixedFont', 20, 'bold'),
                                relief  ='raise',
                                cursor  =cursor,
                                state=state
                                )
        self.pos = rs.Main.pos_translate(pos)

#优化
    # def activate(self):
    #     def _raise(event):
    #         self.button.config(relief='raised')
    #     def _flat(event):
    #         self.button.config(relief='flat')
    #     global choosing
    #     if choosing:
    #         self.button.bind('<Enter>', _raise)
    #         self.button.bind('<Leave>', _flat)
    #         print('选择模式')
    #     else:
    #         self.button.bind('<Enter>', _flat)
    #         self.button.bind('<Leave>', _flat)
    #         print('非选择模式')

    def click(self):
        global target
        if target and target.button.cget('fg') != self.button.cget('fg'):
            target.button.grid_forget()
            target.button.grid(column = self.pos[0],
                               row    = self.pos[1])
            x = Piece(None, self.pos, None)
            x.set()
            self.button.destroy()
            target = ''
        elif target and target.button.cget('fg') == None:
            target = ''
        else:
            target = self
        print(target)

    def set(self,tup:tuple=''):
        if tup:
            return self.button.grid(column = tup[0],
                                    row    = tup[1])
        else:
            return self.button.grid(column = self.pos[0],
                                    row    = self.pos[1])
    
a = b = 0
for piece in rs.Main().board.read():
    b += 1
    for i in piece:
        a += 1
        if i in list(rs.Main().board.piece.keys())[:7]:
            x = Piece(rs.Main().board.piece[i],(a,b),'red')
            x.set()
            # x.activate()
        elif i in list(rs.Main().board.piece.keys())[7:]:
            x = Piece(rs.Main().board.piece[i],(a,b),'black')
            x.set()
            # x.activate()
        else:
            x = Piece(None,(a,b),None)
            x.set()
            # x.activate()

    a = 0

root.mainloop()
