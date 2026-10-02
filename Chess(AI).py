import tkinter as tk
from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True)
class Piece:
    """保存棋子的阵营、规则类型和棋盘上显示的汉字。"""

    color: str
    kind: str
    symbol: str


class XiangqiBoard:
    """管理象棋棋盘状态、合法走法以及对局胜负。"""

    def __init__(self):
        """创建棋盘对象并载入标准开局。"""
        self.reset()

    def reset(self):
        """清空棋盘后摆放双方棋子，并将红方设为先行方。"""
        self.squares: list[list[Optional[Piece]]] = [
            [None for _ in range(9)] for _ in range(10)
        ]
        # 定义底线棋子顺序，并分别按双方规则摆放棋子。
        back_rank = (
            ("rook", "車"), ("horse", "馬"), ("elephant", "象"),
            ("advisor", "士"), ("general", "将"), ("advisor", "士"),
            ("elephant", "象"), ("horse", "馬"), ("rook", "車"),
        )
        for color, row, cannon, pawn in (
            ("black", 0, 2, 3),
            ("red", 9, 7, 6),
        ):
            for column, (kind, symbol) in enumerate(back_rank):
                if color == "red":
                    # 红方使用与黑方对应的传统棋子字样。
                    symbol = {
                        "rook": "俥", "horse": "傌", "elephant": "相",
                        "advisor": "仕", "general": "帥",
                    }[kind]
                self.squares[row][column] = Piece(color, kind, symbol)
            cannon_symbol = "炮" if color == "red" else "砲"
            self.squares[cannon][1] = Piece(color, "cannon", cannon_symbol)
            self.squares[cannon][7] = Piece(color, "cannon", cannon_symbol)
            pawn_symbol = "兵" if color == "red" else "卒"
            for column in (0, 2, 4, 6, 8):
                self.squares[pawn][column] = Piece(color, "pawn", pawn_symbol)
        # 重置当前行棋方和胜负状态。
        self.turn = "red"
        self.winner: Optional[str] = None

    def piece_at(self, position):
        """返回指定坐标上的棋子；坐标越界或为空时返回 None。"""
        x, y = position
        if 0 <= x < 9 and 0 <= y < 10:
            return self.squares[y][x]
        return None

    def legal_moves(self, start):
        """筛出指定棋子所有不会使己方将帅被将军的合法着法。"""
        piece = self.piece_at(start)
        if piece is None or piece.color != self.turn or self.winner:
            return []
        moves = []
        # 临时模拟每一步，过滤掉走后己方仍处于被将状态的着法。
        for destination in self._pseudo_moves(start, piece):
            captured = self.piece_at(destination)
            self.squares[start[1]][start[0]] = None
            self.squares[destination[1]][destination[0]] = piece
            safe = not self.is_in_check(piece.color)
            self.squares[start[1]][start[0]] = piece
            self.squares[destination[1]][destination[0]] = captured
            if safe:
                moves.append(destination)
        return moves

    def _pseudo_moves(self, start, piece):
        """根据棋子类型生成尚未排除将军状态的候选着法。"""
        x, y = start
        color, kind = piece.color, piece.kind

        def available(nx, ny):
            """判断目标坐标在棋盘内且没有己方棋子占据。"""
            if not (0 <= nx < 9 and 0 <= ny < 10):
                return False
            target = self.squares[ny][nx]
            return target is None or target.color != color

        moves = []
        if kind == "general":
            # 将帅只能在九宫内走一步，且可以沿无遮挡直线照面吃将。
            palace_rows = range(0, 3) if color == "black" else range(7, 10)
            for nx, ny in ((x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)):
                if nx in range(3, 6) and ny in palace_rows and available(nx, ny):
                    moves.append((nx, ny))
            for step in (-1, 1):
                ny = y + step
                while 0 <= ny < 10:
                    target = self.squares[ny][x]
                    if target is not None:
                        if target.color != color and target.kind == "general":
                            moves.append((x, ny))
                        break
                    ny += step
        elif kind == "advisor":
            # 士只能在九宫内沿斜线走一步。
            palace_rows = range(0, 3) if color == "black" else range(7, 10)
            for nx, ny in ((x + 1, y + 1), (x - 1, y + 1),
                           (x + 1, y - 1), (x - 1, y - 1)):
                if nx in range(3, 6) and ny in palace_rows and available(nx, ny):
                    moves.append((nx, ny))
        elif kind == "elephant":
            # 象走田字，检查象眼，并限制在己方半场活动。
            for dx, dy in ((2, 2), (2, -2), (-2, 2), (-2, -2)):
                nx, ny = x + dx, y + dy
                eye = (x + dx // 2, y + dy // 2)
                stays_home = ny <= 4 if color == "black" else ny >= 5
                if (0 <= nx < 9 and 0 <= ny < 10 and stays_home
                        and self.piece_at(eye) is None and available(nx, ny)):
                    moves.append((nx, ny))
        elif kind == "horse":
            # 马走日字；起点与落点之间的马腿被挡时不能移动。
            for dx, dy, leg in (
                (1, 2, (0, 1)), (-1, 2, (0, 1)),
                (1, -2, (0, -1)), (-1, -2, (0, -1)),
                (2, 1, (1, 0)), (2, -1, (1, 0)),
                (-2, 1, (-1, 0)), (-2, -1, (-1, 0)),
            ):
                nx, ny = x + dx, y + dy
                if (self.piece_at((x + leg[0], y + leg[1])) is None
                        and available(nx, ny)):
                    moves.append((nx, ny))
        elif kind == "rook":
            # 车沿横竖方向移动，遇到第一枚棋子时停止并可吃敌子。
            for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                nx, ny = x + dx, y + dy
                while 0 <= nx < 9 and 0 <= ny < 10:
                    target = self.squares[ny][nx]
                    if target is None:
                        moves.append((nx, ny))
                    else:
                        if target.color != color:
                            moves.append((nx, ny))
                        break
                    nx += dx
                    ny += dy
        elif kind == "cannon":
            # 炮不隔子时可走空位，隔且仅隔一子时才可吃目标棋子。
            for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                nx, ny = x + dx, y + dy
                screen_found = False
                while 0 <= nx < 9 and 0 <= ny < 10:
                    target = self.squares[ny][nx]
                    if not screen_found:
                        if target is None:
                            moves.append((nx, ny))
                        else:
                            screen_found = True
                    elif target is not None:
                        if target.color != color:
                            moves.append((nx, ny))
                        break
                    nx += dx
                    ny += dy
        elif kind == "pawn":
            # 兵卒始终向前；过河后额外获得横向移动能力。
            forward = 1 if color == "black" else -1
            if available(x, y + forward):
                moves.append((x, y + forward))
            crossed_river = y >= 5 if color == "black" else y <= 4
            if crossed_river:
                for nx in (x - 1, x + 1):
                    if available(nx, y):
                        moves.append((nx, y))
        return moves

    def is_in_check(self, color):
        """判断指定阵营的将帅是否正受到对方棋子攻击。"""
        king_position = None
        for y, row in enumerate(self.squares):
            for x, piece in enumerate(row):
                if piece and piece.color == color and piece.kind == "general":
                    king_position = (x, y)
                    break
            if king_position is not None:
                break
        if king_position is None:
            return True
        # 检查对方所有棋子的攻击范围是否覆盖将帅位置。
        enemy = "black" if color == "red" else "red"
        for y, row in enumerate(self.squares):
            for x, piece in enumerate(row):
                if piece and piece.color == enemy:
                    if king_position in self._pseudo_moves((x, y), piece):
                        return True
        return False

    def make_move(self, start, destination):
        """执行合法走棋、切换行棋方，并在吃将或无棋可走时结束对局。"""
        if destination not in self.legal_moves(start):
            return False
        piece = self.piece_at(start)
        if piece is None:
            return False
        captured = self.piece_at(destination)
        # 将棋子移至目标点，并清空原位置。
        self.squares[destination[1]][destination[0]] = piece
        self.squares[start[1]][start[0]] = None
        if captured and captured.kind == "general":
            self.winner = piece.color
            return True
        self.turn = "black" if self.turn == "red" else "red"
        # 轮到的一方若没有任何合法着法，则当前走棋方获胜。
        if not any(
            candidate and candidate.color == self.turn
            and self.legal_moves((x, y))
            for y, row in enumerate(self.squares)
            for x, candidate in enumerate(row)
        ):
            self.winner = piece.color
        return True


class XiangqiGUI(tk.Tk):
    """使用 Tkinter 绘制棋盘并处理鼠标交互。"""

    # 棋盘尺寸由交叉点间距和外侧留白共同决定。
    CELL_SIZE = 64
    MARGIN = 48
    BOARD_WIDTH = MARGIN * 2 + CELL_SIZE * 8
    BOARD_HEIGHT = MARGIN * 2 + CELL_SIZE * 9

    def __init__(self):
        """创建窗口、状态栏、重新开始按钮和棋盘画布。"""
        super().__init__()
        self.title("中国象棋")
        self.resizable(False, False)
        self.configure(bg="#f4ead5")
        self.game = XiangqiBoard()
        self.selected = None
        self.destinations = []

        # 顶部工具栏显示行棋提示，并提供重新开始功能。
        toolbar = tk.Frame(self, bg="#f4ead5", padx=14, pady=10)
        toolbar.pack(fill="x")
        self.status = tk.Label(
            toolbar, text="", font=("Microsoft YaHei UI", 12, "bold"),
            bg="#f4ead5", fg="#333333", anchor="w",
        )
        self.status.pack(side="left", fill="x", expand=True)
        tk.Button(
            toolbar, text="重新开始", command=self.restart,
            font=("Microsoft YaHei UI", 10), padx=10,
        ).pack(side="right")

        # 棋盘画布负责绘制棋盘并接收玩家的鼠标点击。
        self.canvas = tk.Canvas(
            self, width=self.BOARD_WIDTH, height=self.BOARD_HEIGHT,
            bg="#e8bd75", highlightthickness=0,
        )
        self.canvas.pack(padx=14, pady=(0, 14))
        self.canvas.bind("<Button-1>", self.on_click)
        self.draw()

    def point(self, position):
        """将棋盘列、行坐标换算成画布像素坐标。"""
        x, y = position
        return self.MARGIN + x * self.CELL_SIZE, self.MARGIN + y * self.CELL_SIZE

    def draw(self):
        """重绘棋盘线、楚河汉界、合法落点、选中状态和所有棋子。"""
        canvas = self.canvas
        canvas.delete("all")
        # 绘制棋盘边框、横线与分段纵线。
        left, top = self.MARGIN, self.MARGIN
        right = left + self.CELL_SIZE * 8
        bottom = top + self.CELL_SIZE * 9
        canvas.create_rectangle(
            left - 2, top - 2, right + 2, bottom + 2,
            outline="#4c2814", width=3,
        )
        for row in range(10):
            y = top + row * self.CELL_SIZE
            canvas.create_line(left, y, right, y, fill="#4c2814", width=2)
        for column in range(9):
            x = left + column * self.CELL_SIZE
            if column in (0, 8):
                canvas.create_line(x, top, x, bottom, fill="#4c2814", width=2)
            else:
                canvas.create_line(x, top, x, top + self.CELL_SIZE * 4,
                                  fill="#4c2814", width=2)
                canvas.create_line(x, top + self.CELL_SIZE * 5, x, bottom,
                                  fill="#4c2814", width=2)
        # 绘制双方九宫斜线及楚河汉界背景和文字。
        for y in (top, bottom - self.CELL_SIZE * 2):
            canvas.create_line(
                left + self.CELL_SIZE * 3, y,
                left + self.CELL_SIZE * 5, y + self.CELL_SIZE * 2,
                fill="#4c2814", width=2,
            )
            canvas.create_line(
                left + self.CELL_SIZE * 5, y,
                left + self.CELL_SIZE * 3, y + self.CELL_SIZE * 2,
                fill="#4c2814", width=2,
            )
        canvas.create_rectangle(
            left + 1, top + self.CELL_SIZE * 4 + 1,
            right - 1, top + self.CELL_SIZE * 5 - 1,
            fill="#e8bd75", outline="",
        )
        canvas.create_text(
            left + self.CELL_SIZE * 2, top + self.CELL_SIZE * 4.5,
            text="楚 河", font=("KaiTi", 22), fill="#704522",
        )
        canvas.create_text(
            left + self.CELL_SIZE * 6, top + self.CELL_SIZE * 4.5,
            text="漢 界", font=("KaiTi", 22), fill="#704522",
        )

        # 用绿点标记合法落点，用蓝圈标记当前选中的棋子。
        for position in self.destinations:
            cx, cy = self.point(position)
            canvas.create_oval(cx - 6, cy - 6, cx + 6, cy + 6,
                               fill="#5b8c45", outline="#ffffff", width=1)
        if self.selected is not None:
            cx, cy = self.point(self.selected)
            canvas.create_oval(cx - 29, cy - 29, cx + 29, cy + 29,
                               outline="#3686c7", width=3)

        # 根据棋盘数据绘制全部棋子。
        for y, row in enumerate(self.game.squares):
            for x, piece in enumerate(row):
                if piece:
                    self.draw_piece((x, y), piece)

        # 更新顶部状态提示，显示当前行棋方、将军或胜负结果。
        if self.game.winner:
            name = "红方" if self.game.winner == "red" else "黑方"
            self.status.config(text=f"{name}胜利！点击“重新开始”再来一局。")
        else:
            name = "红方" if self.game.turn == "red" else "黑方"
            checked = "（被将军）" if self.game.is_in_check(self.game.turn) else ""
            self.status.config(text=f"{name}走棋{checked}　点击棋子后选择绿点移动")

    def draw_piece(self, position, piece):
        """在指定交叉点绘制带有阵营颜色的圆形棋子和汉字。"""
        cx, cy = self.point(position)
        radius = 25
        color = "#b4231c" if piece.color == "red" else "#222222"
        self.canvas.create_oval(
            cx - radius, cy - radius, cx + radius, cy + radius,
            fill="#f8e7bd", outline=color, width=2,
        )
        self.canvas.create_text(
            cx, cy, text=piece.symbol, fill=color,
            font=("KaiTi", 23, "bold"),
        )

    def on_click(self, event):
        """处理鼠标点击：选中己方棋子、走棋或取消当前选择。"""
        x = round((event.x - self.MARGIN) / self.CELL_SIZE)
        y = round((event.y - self.MARGIN) / self.CELL_SIZE)
        if not (0 <= x < 9 and 0 <= y < 10) or self.game.winner:
            return
        position = (x, y)
        if self.selected is not None and position in self.destinations:
            # 点击合法落点后提交走棋，并清除选中状态。
            self.game.make_move(self.selected, position)
            self.selected = None
            self.destinations = []
        else:
            # 点击己方棋子显示合法着法，点击其他位置则取消选择。
            piece = self.game.piece_at(position)
            if piece and piece.color == self.game.turn:
                self.selected = position
                self.destinations = self.game.legal_moves(position)
            else:
                self.selected = None
                self.destinations = []
        self.draw()

    def restart(self):
        """恢复标准开局并清除选中棋子和可走位置提示。"""
        self.game.reset()
        self.selected = None
        self.destinations = []
        self.draw()


if __name__ == "__main__":
    # 直接运行本文件时启动 Tkinter 象棋窗口的事件循环。
    XiangqiGUI().mainloop()
