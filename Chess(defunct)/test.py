# from board import Board as B
# from real_shit import RealShit as RS

# piece = {'1':'将', '2':'士', '3':'象', '4':'马', '5':'車', '6':'炮', '7':'卒',
#          'a':'帥', 'b':'仕', 'c':'相', 'd':'馬', 'e':'車', 'f':'砲', 'g':'兵'}
# b = B('Var')

# # print(b.read())
# # print(b.pos('7'))
# # print(list(piece.keys()))
# print(B('Var').change_board('7',(1,5)))
# print(RS().check_place((4,8)))
# print(B('Var').placed_posed())
# print(list(RS().board.piece.keys())[:7])


#并发测试
# import itertools
# import time
# from threading import Thread,Event

# def spin(msg)



#gui优化部分
    # def click(self):
    #     global group
    #     global choosing
    #     if group:
    #         print(group[0].button.cget('fg') == self.button.cget('fg'))
    #         if group[0].button.cget('fg') == self.button.cget('fg'):
    #             group[0] = self
    #         else:
    #             Piece(None,self.pos,None).set()
    #             self.set()
    #         choosing = True
    #     else:
    #         group.append(self)
    #         choosing = False
    #     self.activate()
    #     print(group)
    #     print(choosing)

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