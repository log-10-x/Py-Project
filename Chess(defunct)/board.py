class Board:
    def __init__(self, file) -> None:
        self.file = file
        self.piece = {'1':'将', '2':'士', '3':'象', '4':'馬', '5':'車', '6':'砲', '7':'卒',
                      'a':'帥', 'b':'仕', 'c':'相', 'd':'傌', 'e':'俥', 'f':'炮', 'g':'兵'}

    def read(self) -> list:
        '''返回一个二维数组(列表):[[棋子]...,[棋子]...,...]'''

        with open(self.file, 'r', encoding='utf-8') as f:
            my_list = []
            big_list = []
            for r in f.readlines():
                for x in r:
                    if x != '\n':
                        my_list.append(x)
                    else:
                        big_list.append(my_list)
                        my_list = []
        return big_list

    def pos(self, piece):
        '''返回一个字典:{棋子:[(x,y),...]}'''

        a, b = 0, 0
        d = []
        for p in self.read():
            b += 1
            for q in p:
                a += 1
                if q == piece:
                    d.append((a,b))
            a = 0
        return d

    def get_row_column(self, piece) -> tuple:
        '''返回一个元组:(((x,y),...),((x,y),...))'''

        row, column = [], []
        for p in self.pos(piece)[piece]:
            x, y = p[0], p[1]
            for v in range(1, 11):
                column.append((v, y))
                if v < 10:
                    row.append((x, v))
        return tuple(set(row)), tuple(set(column))

    def change_board(self, piece, pos):
        '''修改文件Var,在pos位置放'''

        board = self.read()
        board[pos[1]-1][pos[0]-1] = piece
        with open(self.file, 'w', encoding='utf-8') as f:
            for p in board:
                for q in p:
                    f.write(q)
                f.write('\n')

    def placed_posed(self):
        '''记录棋盘上已占的位置'''

        d = {}
        little = []
        for p in list(self.piece.keys())[:7]:
            for t in self.pos(p):
                little.append(t)
        d['num'] = little
        little = []
        for p in list(self.piece.keys())[7:]:
            for t in self.pos(p):
                little.append(t)
        d['letter'] = little
        return d
