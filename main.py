
import tkinter as tk
from random import shuffle
from tkinter.messagebox import showinfo, showerror


colors = {
    1: 'blue',
    2: 'green',
    3: '#FFBD33',
    4: 'blue',
    5: '#FBCEB1',
    6: '#FF5733',
    7: '#33FFBD',
    8: '#7248AD',
}


class MyButton(tk.Button):

    def __init__(self, master, x, y, number=0, *args, **kwargs):
        super(MyButton, self).__init__(master, width=3, font='Calibri 15 bold', *args, **kwargs)
        self.x = x
        self.y = y
        self.number = number
        self.is_mine = False
        self.count_bomb = 0
        self.is_open = False

    def __repr__(self):
        return f'MyButton {self.x} {self.y} {self.number} {self.is_mine}'


class MineSweeper:
    window = tk.Tk()
    window.title("Игра сапер")
    window.geometry("350x350+700+200")
    window.minsize(100, 100)
    window.maxsize(700, 800)
    ROW = 4
    COLUMNS = 4
    MINES = 13
    IS_GAME_OVER = False

    def __init__(self):
        self.buttons = []

        for i in range(MineSweeper.ROW + 2):
            temp = []
            for j in range(MineSweeper.COLUMNS + 2):
                btn = MyButton(MineSweeper.window, x=i, y=j)
                btn.config(command=lambda button=btn: self.click(button))
                btn.bind('<Button-3>', self.right_click)
                temp.append(btn)

            self.buttons.append(temp)

    def right_click(self, event):
        if MineSweeper.IS_GAME_OVER:
            return
        cur_btn = event.widget
        if cur_btn['state'] == 'normal':
            cur_btn['state'] = 'disabled'
            cur_btn['text'] = '🚩'
        elif cur_btn['text'] == '🚩':
            cur_btn['text'] = ''
            cur_btn['state'] = 'normal'

    def __init__(self):
        self.buttons = []
        self.non_mine_buttons_opened = 0

        for i in range(MineSweeper.ROW + 2):
            temp = []
            for j in range(MineSweeper.COLUMNS + 2):
                btn = MyButton(MineSweeper.window, x=i, y=j)
                btn.config(command=lambda button=btn: self.click(button))
                btn.bind('<Button-3>', self.right_click)
                temp.append(btn)

            self.buttons.append(temp)

    def click(self, clicked_button: MyButton):
        if MineSweeper.IS_GAME_OVER:
            return

        for i in range(1, MineSweeper.ROW + 1):
            for j in range(1, MineSweeper.COLUMNS + 1):
                btn = self.buttons[i][j]
                count_bomb = 0
                if not btn.is_mine:
                    for row_dx in [-1, 0, 1]:
                        for col_dx in [-1, 0, 1]:
                            neighbour = self.buttons[i + row_dx][j + col_dx]
                            if neighbour.is_mine:
                                count_bomb += 1

        if clicked_button.is_mine:
            clicked_button.config(text='*', bg='red', disabledforeground='black')
            clicked_button.is_open = True
            MineSweeper.IS_GAME_OVER = True
            showinfo('Game over!', 'Вы проиграли!')
            for i in range(1, MineSweeper.ROW + 1):
                for j in range(1, MineSweeper.COLUMNS + 1):
                    btn = self.buttons[i][j]
                    if btn.is_mine:
                        btn['text'] = '*'
        else:
            color = colors.get(clicked_button.count_bomb)
            if clicked_button.count_bomb:
                clicked_button.config(text=clicked_button.count_bomb, disabledforeground=color)
                clicked_button.is_open = True
            else:
                self.breadth_first_search(clicked_button)
                clicked_button.is_open = True
            clicked_button.config(state='disabled')
            clicked_button.config(relief=tk.SUNKEN)

        opened_buttons = sum(1 for i in range(1, MineSweeper.ROW + 1) for j in range(1, MineSweeper.COLUMNS + 1)
                             if self.buttons[i][j].is_open)
        total_buttons = MineSweeper.ROW * MineSweeper.COLUMNS
        if total_buttons - opened_buttons == MineSweeper.MINES:
            MineSweeper.IS_GAME_OVER = True
            showinfo('Win!', 'Вы победили!')

    def breadth_first_search(self, btn: MyButton):
        queue = [btn]
        while queue:

            cur_btn = queue.pop()
            color = colors.get(cur_btn.count_bomb, 'black')
            if cur_btn.count_bomb:
                cur_btn.config(text=cur_btn.count_bomb, disabledforeground=color)
            else:
                cur_btn.config(text='', disabledforeground=color)
                cur_btn.is_open = True
                cur_btn.config(state='disabled')
                cur_btn.config(relief=tk.SUNKEN)

            if cur_btn.count_bomb == 0:
                x, y = cur_btn.x, cur_btn.y
                for dx in [-1, 0, 1]:
                    for dy in [-1, 0, 1]:
                        if not abs(dx - dy) == 1:
                            continue

                        next_button = self.buttons[x + dx][y + dy]
                        if not next_button.is_open and 1 <= next_button.x <= MineSweeper.ROW and 1 <= next_button.y <= MineSweeper.COLUMNS and next_button not in queue:
                            queue.append(next_button)

    def reload(self):
        self.window.winfo_children()[0].destroy()
        [child.destroy() for child in self.window.winfo_children()]
        self.__init__()
        self.create_widgets()
        self.insert_mines()
        self.count_mines()
        self.print_buttons()
        MineSweeper.IS_GAME_OVER = False

    def settings(self):
        win_settings = tk.Toplevel(self.window)
        win_settings.wm_title('Настройки')
        tk.Label(win_settings, text='Количество строк').grid(row=0, column=0, sticky='w')
        row_entry = tk.Entry(win_settings)
        row_entry.insert(0, MineSweeper.ROW)
        row_entry.grid(row=0, column=1, padx=20, pady=20)
        tk.Label(win_settings, text='Количество колонок').grid(row=1, column=0, sticky='w')
        column_entry = tk.Entry(win_settings)
        column_entry.insert(0, MineSweeper.COLUMNS)
        column_entry.grid(row=1, column=1, padx=20, pady=20)
        tk.Label(win_settings, text='Количество мин').grid(row=2, column=0, sticky='w')
        mines_entry = tk.Entry(win_settings)
        mines_entry.insert(0, MineSweeper.MINES)
        mines_entry.grid(row=2, column=1, padx=20, pady=20)

        tk.Button(win_settings, text='Применить',
                  command=lambda: self.apply_settings(row_entry, column_entry, mines_entry)).grid(row=3, columnspan=2,
                                                                                                  padx=20, pady=20)

    def apply_settings(self, row: tk.Entry, column: tk.Entry, mines: tk.Entry):
        try:
            int(row.get()), int(column.get()), int(mines.get())
        except ValueError:
            showerror('Ошибка', 'Вы ввели неправильное значение!')
            return

        MineSweeper.ROW = int(row.get())
        MineSweeper.COLUMNS = int(column.get())
        MineSweeper.MINES = int(mines.get())
        self.reload()

    def create_widgets(self):

        menubar = tk.Menu(self.window)  # Создали меню
        self.window.config(menu=menubar)

        settings_menu = tk.Menu(menubar, tearoff=0)  # Создали подменю
        settings_menu.add_command(label='Играть', command=self.reload)
        settings_menu.add_command(label='Настройки', command=self.settings)
        settings_menu.add_command(label='Выход', command=self.window.destroy)

        menubar.add_cascade(label='Файл', menu=settings_menu)  # Объединили в один cascade

        count = 1
        for i in range(1, MineSweeper.ROW + 1):
            for j in range(1, MineSweeper.COLUMNS + 1):
                btn = self.buttons[i][j]
                btn.number = count
                btn.grid(row=i, column=j, sticky='nwes')
                count += 1

        for i in range(1, MineSweeper.ROW + 1):
            MineSweeper.window.rowconfigure(i, weight=1)

        for j in range(1, MineSweeper.COLUMNS + 1):
            MineSweeper.window.columnconfigure(j, weight=1)

    def open_all_buttons(self):
        for i in range(MineSweeper.ROW + 2):
            for j in range(MineSweeper.COLUMNS + 2):
                btn = self.buttons[i][j]
                if btn.is_mine:
                    btn.config(text='*', bg='red', disabledforeground='black')
                elif btn.count_bomb in colors:
                    color = colors.get(btn.count_bomb, 'black')
                    btn.config(text=btn.count_bomb, foreground=color)

    def start(self):
        self.create_widgets()
        self.insert_mines()
        self.count_mines()
        self.print_buttons()
        # self.open_all_buttons()
        MineSweeper.window.mainloop()

    def print_buttons(self):
        for i in range(1, MineSweeper.ROW + 1):
            for j in range(1, MineSweeper.COLUMNS + 1):
                btn = self.buttons[i][j]
                if btn.is_mine:
                    print('B', end=' ')
                else:
                    print(btn.count_bomb, end=' ')
            print()

    def insert_mines(self):
        index_mines = self.get_mine_place()
        print(index_mines)
        count = 1
        for i in range(1, MineSweeper.ROW + 1):
            for j in range(1, MineSweeper.COLUMNS + 1):
                btn = self.buttons[i][j]
                btn.number = count
                if btn.number in index_mines:
                    btn.is_mine = True
                count += 1

    def count_mines(self):
        for i in range(1, MineSweeper.ROW + 1):
            for j in range(1, MineSweeper.COLUMNS + 1):
                btn = self.buttons[i][j]
                count_bomb = 0
                if not btn.is_mine:
                    for row_dx in [-1, 0, 1]:
                        for col_dx in [-1, 0, 1]:
                            neighbour = self.buttons[i + row_dx][j + col_dx]
                            if neighbour.is_mine:
                                count_bomb += 1

                btn.count_bomb = count_bomb

    @staticmethod
    def get_mine_place():
        indexes = list(range(1, MineSweeper.COLUMNS * MineSweeper.ROW + 1))
        shuffle(indexes)
        return indexes[:MineSweeper.MINES]


game = MineSweeper()
game.start()
