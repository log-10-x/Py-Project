from board import Board as B

class Main:
    def __init__(self):
        self.file = 'Ord2'
        self.board = B(self.file)
        self.camp = 'red'

    @staticmethod
    def pos_translate(pos):
        '''人为坐标转化为机器坐标'''

        pos = (pos[0]-1, pos[1]-1)
        return pos
    
    def camp_(self, camp):
        '''修改阵营'''

        if self.camp == 'black':
            self.file = 'Ord1'
            self.camp = 'black'
        else:
            self.file = 'Ord2'
            self.camp = 'red'

    def check_place(self, pos):
        '''检查位置是否有棋子'''

        if pos not in self.board.placed_posed():
            return True
        else:
            return False

    def move(self, piece, pos):
        self.board.change_board(piece, pos)

    def move(self, pos_1, pos_2, piece_1):
        self.board.change_board(pos_1, piece_1)
        self.board.change_board(pos_2, '0')
