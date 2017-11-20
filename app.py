# encoding: utf-8

import re
import os
import sys
import tkinter
from datetime import date
from readjson import JsonReader
from newdishdialog import NewDishDialog
from newentrydialog import NewEntryDialog
from newdishhtml import DishesHTMLReport
from tkinter.ttk import Frame, Label, Button, Entry, Scrollbar, Treeview, Style, Checkbutton
from tkinter import N, S, W, E, X, NO, RIGHT, CENTER, VERTICAL, END, messagebox, filedialog, PhotoImage, DISABLED, IntVar
from autoentry import AutocompleteEntry

DEFAULT_MINSIZE_WIDTH = 900
DEFAULT_MINSIZE_HEIGHT = 750

json_path = os.getcwd() + '\\files\\dishes.json'
logo_path = os.getcwd() + '\\images\\logo.png'

class Program(Frame):
    """Class to represent a main window"""
    def __init__(self, parent):
        # Some top-level settings.
        Frame.__init__(self, parent)
        self.content = Frame(self, padding=(5, 5, 5, 20))
        self.parent = parent
        self.parent.title('Restaurant manager')
        self.parent.minsize(DEFAULT_MINSIZE_WIDTH, DEFAULT_MINSIZE_HEIGHT)
        self.parent.protocol('WM_DELETE_WINDOW', self.onQuit)

        # Some variables.
        self.track_weight = IntVar()
        self.custom_entries = []
        self.jsonReader = JsonReader(json_path)
        self.frames = []
        self.entries = {}
        self.dishes = self.jsonReader.getDishesDict()
        self.dishes_names = self.jsonReader.getDishesNames()
        self.parent.iconphoto(
            True,
            PhotoImage(
                file=os.path.join(
                    sys.path[0], 
                    logo_path
                )
            )
        )

        # Initialize all widgets.
        self.initWidgets()

    def initWidgets(self):
        """
        Initialize all widgets in window here.
        Entries are saved in [self.entries] list.
        ----------------------------------------------------------
        5 frames are initialized and saved into [self.frames] list here:
        1) [About frame] - Frame to contain all non-food entries.
        2) [Separator frame] - Frame to contain a simple separator.
        3) [New order frame] - Frame to contain entries for adding orders to the main table.
        4) [Orders table frame] - Frame to contain table with list of added orders.
        5) [Save report frame] - Frame to contain buttons, which save a report.
        ----------------------------------------------------------
        """
        # Create 5 frames here.
        for i in range(5):
            self.frames.append(
                Frame(self.content)
            )
        # Set the weights of cols and rows in the grid.
        self.configureGrid()
        # Center a window.
        self.centerWindow()

        # Place 4 frames to the window.
        self.frames[0].grid(column=0, row=0, sticky=N+E+W, padx=5, pady=3)
        self.frames[1].grid(column=0, row=1, sticky=N+S+E+W, padx=5, pady=3)
        self.frames[2].grid(column=0, row=2, sticky=N+S+E+W, padx=5, pady=3)
        self.frames[3].grid(column=0, row=3, sticky=N+S+E+W, padx=5, pady=10)
        self.frames[4].grid(column=0, row=4, sticky=S+E+W, padx=5, pady=3)

        # About frame widgets.
        Label(self.frames[0], text='Заказчик').grid(row=0, column=0, sticky=E, pady=5)
        Label(self.frames[0], text='Менеджер').grid(row=0, column=2, sticky=E, pady=5)
        Label(self.frames[0], text='Вид мероприятия', justify=RIGHT, wraplength=90
              ).grid(row=0, column=4, sticky=E, pady=5)
        Label(self.frames[0], text='Дата').grid(row=1, column=0, sticky=E, pady=5)
        Label(self.frames[0], text='Время').grid(row=1, column=2, sticky=E, pady=5)
        Label(self.frames[0], text='Место проведения', justify=RIGHT, wraplength=90
              ).grid(row=1, column=4, sticky=E, pady=5)
        Label(self.frames[0], text='Количество персон', justify=RIGHT, wraplength=90
              ).grid(row=1, column=6, sticky=E, pady=5)

        self.entries['client'] = Entry(self.frames[0])
        self.entries['manager'] = Entry(self.frames[0])
        self.entries['type'] = Entry(self.frames[0], width=10)
        self.entries['date'] = Entry(self.frames[0])
        self.entries['time'] = Entry(self.frames[0])
        self.entries['location'] = Entry(self.frames[0], width=10)
        self.entries['persons'] = Entry(self.frames[0], width=10)

        self.entries['client'].focus_set()
        today = date.today().isoformat().split('-')[::-1]
        self.entries['date'].insert(0, '.'.join(today))

        self.entries['client'].grid(row=0, column=1, sticky=E+W, padx=(3, 13), pady=5)
        self.entries['manager'].grid(row=0, column=3, sticky=E+W, padx=(3, 13), pady=5)
        self.entries['type'].grid(row=0, column=5, columnspan=3, sticky=E+W, padx=(3, 13), pady=5)
        self.entries['date'].grid(row=1, column=1, sticky=E+W, padx=(3, 13), pady=5)
        self.entries['time'].grid(row=1, column=3, sticky=E+W, padx=(3, 13), pady=5)
        self.entries['location'].grid(row=1, column=5, sticky=E + W, padx=(3, 13), pady=5)
        self.entries['persons'].grid(row=1, column=7, sticky=E+W, padx=(3, 13), pady=5)

        # Add a separator between [about] and [new order] frames
        sep1 = Frame(self.frames[1], height=2, borderwidth=1, relief='sunken')
        sep1.pack(fill=X, padx=1, pady=10)

        # New Order frame widgets.
        Label(self.frames[2], text='Название', anchor=E).grid(row=0, column=0, sticky=E)
        Label(self.frames[2], text='Комментарий', anchor=E).grid(row=1, column=0, sticky=E)
        Label(self.frames[2], text='Количество', anchor=E).grid(row=2, column=0, sticky=E)
        self.sum_lbl = Label(self.frames[2], text='Текущая сумма заказа:\n 0 грн', anchor=E, justify=RIGHT)

        self.entries['name'] = AutocompleteEntry(self.frames[2])
        self.entries['comment'] = Entry(self.frames[2])
        self.entries['amount'] = Entry(self.frames[2])
        addOrder_btn = Button(self.frames[2], text='Добавить блюдо в отчет')

        self.entries['name'].set_completion_list(self.dishes_names)
        self.entries['amount'].insert(0, '1')
        addOrder_btn['command'] = lambda: self.addDish()

        self.entries['name'].grid(row=0, column=1, columnspan=5, sticky=W+E, pady=3, padx=(3, 15))
        self.entries['comment'].grid(row=1, column=1, columnspan=5, sticky=W+E, pady=3, padx=(3, 15))
        self.entries['amount'].grid(row=2, column=1, columnspan=2, sticky=W+E, pady=3, padx=(3, 15))
        addOrder_btn.grid(row=3, column=1, sticky=W, pady=3, padx=3)
        self.sum_lbl.grid(row=4, column=5, pady=0, padx=(190, 0))

        customEntry_btn = Button(self.frames[2], text='Добавить собственную строку в отчет')
        customEntry_btn['command'] = lambda: self.addCustomEntry()
        customEntry_btn.grid(row=4, column=1, sticky=W, pady=3, padx=3)

        # Orders Table frame widgets.
        self.orders_view = Treeview(self.frames[3])
        self.orders_view['columns'] = ('Weight', 'Amount', 'Comment', 'Price', 'Sum')
        self.orders_view.bind('<Delete>', lambda e: self.deleteEntry(e, self.orders_view))

        self.orders_view.heading('#0', text='Название')
        self.orders_view.column('#0', anchor='w', minwidth=307, width=307)
        self.orders_view.heading('Weight', text='Выход')
        self.orders_view.column('Weight', anchor=CENTER, minwidth=100, width=100, stretch=NO)
        self.orders_view.heading('Amount', text='Количество')
        self.orders_view.column('Amount', anchor=CENTER, minwidth=100, width=100, stretch=NO)
        self.orders_view.heading('Comment', text='Комментарий')
        self.orders_view.column('Comment', anchor='w', minwidth=130, width=130)
        self.orders_view.heading('Price', text='Цена, грн')
        self.orders_view.column('Price', anchor=CENTER, minwidth=110, width=110, stretch=NO)
        self.orders_view.heading('Sum', text='Сумма, грн')
        self.orders_view.column('Sum', anchor=CENTER, minwidth=108, width=108, stretch=NO)

        self.orders_view.grid(row=0, column=0, sticky=N+S+E+W, padx=3, pady=3)

        # NOTE: next [for] block is for testing purposes only.
        """
        for dish in self.dishes:
            self.orders_view.insert('', 'end',
                text=dish,
                values=[
                    self.dishes[dish]['weight'],
                    5,  # [amount] column
                    'wats up?',  # [comment] column
                    self.dishes[dish]['price'],
                    5 * float(self.dishes[dish]['price'])
                ]
            )
        """

        orders_scrlbar = Scrollbar(self.frames[3], orient=VERTICAL, command=self.orders_view.yview)
        self.orders_view['yscrollcommand'] = orders_scrlbar.set
        orders_scrlbar.grid(row=0, column=1, sticky=N+S)

        # Save Report frame widgets.
        saveWeb_btn = Button(self.frames[4], text='Сохранить отчет', width=20)
        trackweight_chkbox = Checkbutton(self.frames[4], text='Учитывать средний вес', variable=self.track_weight)

        saveWeb_btn['command'] = lambda: self.saveWeb()

        saveWeb_btn.pack(side='left', anchor=CENTER, padx=5, pady=3)
        trackweight_chkbox.pack(side='left', anchor=CENTER, pady=3, padx=3)

    def configureGrid(self):
        """Configure weights of grids columns and rows"""
        # Top-level configuration.
        self.grid(sticky=N+S+E+W)
        top = self.winfo_toplevel()
        top.rowconfigure(0, weight=1)
        top.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)

        # Configuration of main content frame.
        self.configureFrame(self.content, [1], [0, 0, 0, 3, 0])
        # Configuration of about frame.
        self.configureFrame(self.frames[0], [0, 1, 0, 1, 0, 0, 0, 0], [0, 0, 0])
        # Configuration of new order frame.
        self.configureFrame(self.frames[2], [0, 1, 1, 1, 1, 1], [0, 0, 0, 0])
        # Configuration of orders table frame.
        self.configureFrame(self.frames[3], [1, 0], [1])

    def centerWindow(self):
        """Place the main window in the center of screen"""
        window_w = DEFAULT_MINSIZE_WIDTH
        window_h = DEFAULT_MINSIZE_HEIGHT
        screen_w = self.winfo_screenwidth()
        screen_h = self.winfo_screenheight()
        x = (screen_w - window_w) / 2
        y = (screen_h - window_h) / 2
        self.parent.geometry('%dx%d+%d+%d' % (window_w, window_h, x, y))

    def onQuit(self):
        """Before the program exits, ask user, if he really wants it"""
        if messagebox.askyesno('Выход из программы', 'Вы действительно хотите выйти из программы?'):
            self.quit()

    @staticmethod
    def deleteEntry(e, tree):
        """Event to handle deletion in TreeView woth [Delete] button"""
        selected_item = tree.selection()[0]  # get selected item
        tree.delete(selected_item)

    @staticmethod
    def configureFrame(frame, columns_wght, rows_wght):
        """Function to organize frame configuration routine"""
        frame.grid(column=0, row=0, sticky=N + S + E + W)
        for i, weight in enumerate(columns_wght):
            frame.columnconfigure(i, weight=weight)
        for i, weight in enumerate(rows_wght):
            frame.rowconfigure(i, weight=weight)

    def saveWeb(self):
        """Save data from the TreeView to the html report"""
        # Validation: if there is no items in tree_view
        if not self.orders_view.get_children():
            messagebox.showerror(
                'Ошибка',
                'Ошибка создания отчета: нет блюд.'
            )
            return

        # Open file dialog to choose saving path.
        file = filedialog.asksaveasfile(
            mode='w',
            defaultextension='.html',
            filetypes=[('Веб страница', '.html'), ('Все файлы', '.*')]
        )
        # If user pressed [Cancel] or closed a file dialog.
        if file is None:
            return

        # Pack files to send to HTML saver module.
        # Dictionary looks like: { name:{weight,amount,comment,price,total}, name:... }
        packed_dishes = {
            'global': {
                'trackw': self.track_weight.get(),  # flag - is weight tracked
                'totalsum': self.sum_lbl['text'][21:-4],  # str - total sum of dishes
                'centries': self.custom_entries  # [5*str] - custom entries
            },
            'about': {
                'client': self.entries['client'].get(),
                'manager': self.entries['manager'].get(),
                'type': self.entries['type'].get(),
                'date': self.entries['date'].get(),
                'time': self.entries['time'].get(),
                'location': self.entries['location'].get(),
                'persons': self.entries['persons'].get()
            },
            'dishes': {}
        }
        for child in self.orders_view.get_children():
            child_content = self.orders_view.item(child)
            child_values = child_content['values']
            child_name = child_content['text']
            child_type = self.dishes[child_name]['type']
            # Pack data about a certain dish.
            packed_child = {
                child_name: {
                    'weight': child_values[0],
                    'amount': child_values[1],
                    'comment': child_values[2],
                    'price': child_values[3],
                    'total': child_values[4],
                    'type': child_type
                }
            }
            packed_dishes['dishes'].update(packed_child)
        # Save the HTML report
        html_writer = DishesHTMLReport(file, data=packed_dishes)
        html_writer.create_html()
        messagebox.showinfo(
            'Успешное сохранение',
            'Данные были успешно сохранены.'
        )

    def addCustomEntry(self):
        """This functions opens a window, which gives access for creating custom entries to report"""
        newentry_dialog = NewEntryDialog(self, title='Добавить собственную строку в отчет')
        if newentry_dialog.result:
            self.custom_entries.append(newentry_dialog.result)

    def addDish(self):
        """This function adds an entry to the order_view TreeView widget."""
        # Get packed_info as a dictionary.
        packed_info = self.packInfo()
        # If info packed successfully, add a new entry to orders TreeView.
        if not packed_info:
            return
        # Add a dish to the TreeView.
        self.orders_view.insert(
            '', 'end',
            text=packed_info['dish'],
            values=packed_info['values']
        )
        # Clear all entries.
        entries_toclear = ['name', 'comment', 'amount']
        for entry_key in entries_toclear:
            self.entries[entry_key].delete(0, END)
            self.entries[entry_key].insert(0, '')
        self.entries['amount'].insert(0, '1')
        # Change [sum] label.
        total_sum = float(self.sum_lbl['text'][21:-4]) + float(packed_info['values'][4])
        self.sum_lbl['text'] = 'Текущая сумма заказа:\n %.2f грн' % total_sum
        # Set focus to ['name'] entry.
        self.entries['name'].focus_set()

    def packInfo(self):
        """Pack values, that were inserted into Entries and Text, into dictionary"""
        msg = self.validateForm()
        if msg == 'OK':
            name = self.entries['name'].get()
            amount = self.entries['amount'].get()
            total_price = float(amount) * float(self.dishes[name]['price'])
            pack = {
                'dish': name,
                'values': [
                    self.dishes[name]['weight'],
                    str(amount),
                    self.entries['comment'].get(),
                    self.dishes[name]['price'],
                    '%.2f' % total_price
                ]
            }
            return pack
        elif msg == 'NEWDISH_CANCELED':
            return False
        else:
            messagebox.showerror(
                'Ошибка ввода',
                'При вводе случились ошибки: \n%s' % msg
            )
            return False

    def validateForm(self):
        """Validate all Entry and Text Widgets"""
        msg = ''
        index = 1
        translations = {
            'client': 'Клиент',
            'manager': 'Менеджер',
            'type': 'Вид мероприятия',
            'date': 'Дата',
            'time': 'Время',
            'location': 'Место проведения',
            'persons': 'Количество персон',
            'name': 'Название',
            'comment': 'Комментарий',
            'amount': 'Количество',
        }

        for k in self.entries:
            # Check if some entry is empty.
            if self.entries[k].get() == '':
                if k == 'comment':
                    continue
                msg += '%i) Поле [%s] пустое.\n' % (index, translations[k])
                index += 1

        # Persons entry should contain only digits.
        if not all(letter.isdigit() for letter in self.entries['persons'].get()):
            msg += '%i) Поле [Количество персон] должно содержать только цифры.\n' % index
            index += 1
        # Check date entry.
        match = re.search(r'(\d{2})[.](\d{2})[.](\d{4})$', self.entries['date'].get())
        if not match:
            msg += '%i) Неправильный формат даты.\nПравильный формат: дд.мм.гггг\n' % index
            index += 1
        # Check amount entry.
        check = all(letter.isdigit() or letter == '.' for letter in self.entries['amount'].get())
        if not check:
            msg += '%i) Поле [Количество] должно содержать только цифры, или точки.\n' % index
            index += 1

        # Ask about [name] entry only if there are no more errors left.
        if msg != '':
            return msg

        # Check name entry.
        if (self.entries['name'].get() not in self.dishes_names and self.entries['name'].get() != ''):
            if messagebox.askyesno('Добавление нового блюда', 'Блюда %s нет в списке. Добавить?' % self.entries['name'].get()):
                # Create a new window, which will contain a [result] dictionary {name,type,weight,price}
                newdish_dialog = NewDishDialog(self, self.entries['name'].get(), 'Добавить новое блюдо')
                if newdish_dialog.result:
                    dishToJSON = {
                        newdish_dialog.result['name']: {
                            'weight': newdish_dialog.result['weight'],
                            'price': newdish_dialog.result['price'],
                            'type': newdish_dialog.result['type']
                        }
                    }
                    self.jsonReader.writeDish(dishToJSON)
                    self.jsonReader.prepInformation()
                    self.dishes = self.jsonReader.getDishesDict()
                    self.dishes_names = self.jsonReader.getDishesNames()
                    self.entries['name'].set_completion_list(self.dishes_names)
                else:
                    # if [exit] was pressed
                    return 'NEWDISH_CANCELED'
            else:
                return 'NEWDISH_CANCELED'
        # Check if the same dish is in the orderslist.
        for child in self.orders_view.get_children():
            child_content = self.orders_view.item(child)
            if self.entries['name'].get() == child_content['text']:
                msg += '%i) Ошибка в поле [Название] - такое блюдо уже есть в списке.' % index
                index += 1

        # If all tests passed correctly, msg is 'OK'
        if msg == '':
            msg = 'OK'
        return msg


def main():
    root = tkinter.Tk()
    app = Program(root)
    root.mainloop()


if __name__ == '__main__':
    main()
