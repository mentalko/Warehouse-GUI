import sys
import tkinter as tk
from tkinter import ttk, IntVar, StringVar
from tkcalendar import DateEntry

from models import Product, Category, Warehouse, session

class AddingWindow(tk.Toplevel):

    def __init__(self, root, app):
        super().__init__(root)
        self.init_child()
        self.fields_values()
        self.app = app
    def init_child(self):
        self.title('Добавление продукта')
        self.geometry('450x450')
        self.resizable(False, False)

        self.l_category = tk.Label(self, text='Категория:')
        self.l_category.place(relx=.05, rely=.05)
        self.categories = session.query(Category.name).all()
        self.cbox_category = ttk.Combobox(self, values=sum(self.categories, ()))
        self.cbox_category.place(relx=.2, rely=.05, width=300)

        self.l_name = tk.Label(self, text='Название:')
        self.l_name.place(relx=0.05, rely=0.15)
        self.e_name = tk.Entry(self)
        self.e_name.place(relx=0.2, rely=0.15, width=300)

        self.l_producer = tk.Label(self, text='Производитель:')
        self.l_producer.place(relx=.05, rely=.25)
        self.e_producer = tk.Entry(self)
        self.e_producer.place(relx=.3, rely=.25, width=250)

        self.l_count = tk.Label(self, text='Количество:')
        self.l_count.place(relx=.05, rely=.35)
        self.e_count = tk.Entry(self)
        self.e_count.place(relx=.3, rely=.35)

        self.l_date = tk.Label(self, text='Дата прихода:')
        self.l_date.place(relx=.05, rely=.45)
        self.d_date = DateEntry(self, datepattern='DD.MM.YYYY')
        self.d_date.place(relx=.3, rely=.45)

        self.b_add_or_edit = tk.Button(self, text='Добавить', command=self.add)
        self.b_add_or_edit.place(relx=.2, rely=.8)
        self.b_cancel = tk.Button(self, text='Отмена', command= self.destroy)
        self.b_cancel.place(relx=.4, rely=.8)


    def fields_values(self):
        return [self.cbox_category.get(),
                self.e_name.get(),
                self.e_producer.get(),
                self.e_count.get(),
                self.d_date.get(),
                ]

    def add(self):
        ('<<<',self.fields_values())

        prod = Product(name=self.e_name.get(),
                       producer=self.e_producer.get(),
                       category_id=session.query(Category.id)
                       .filter(Category.name==self.cbox_category.get()).scalar()
                       )
        prod.products = [
            Warehouse(date=self.d_date.get(), count=self.e_count.get())
        ]

        session.add(prod)
        session.commit()
        self.destroy()
        self.app.view_records()

class EditingWindow(AddingWindow):
    def __init__(self, root, app):
        super().__init__(root, app )
        self.selected_id = app.tree.set(app.tree.selection()[0], '#1')
        self.init_edit(app)
        self.paste_data()

    def init_edit(self, app):
        self.title('Редактировать данные')
        self.b_add_or_edit['text'] = 'Обновить'
        self.b_add_or_edit['command'] = self.update

    def paste_data(self):
        self.dataset = session\
            .query(Warehouse.id, Product.category_id, Product.name,  Product.producer,
                   Warehouse.count, Warehouse.date)\
            .filter(Category.id == Product.category_id) \
            .filter(Product.id == Warehouse.product_id) \
            .filter_by(id = self.selected_id).first()
        
        print('dataset', self.dataset)

        self.cbox_category.current(self.dataset[1]-1)
        self.e_name.insert(0, self.dataset[2])
        self.e_producer.insert(0, self.dataset[3])
        self.e_count.insert(0, self.dataset[4])
        self.d_date.set_date(self.dataset[5])
        self.d_date.config(date_pattern='DD.MM.YYYY')

    def update(self):
        wh = session.query(Warehouse).filter_by(id=self.selected_id).first()
        prod = session.query(Product).filter_by(id=wh.product_id).first()

        session.delete(wh)
        session.delete(prod)
        AddingWindow.add(self)
