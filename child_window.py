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


    # def add_records(self):
    #     session.query()
    #     self.view.view_records()
    #     self.destroy()
    #
    # def update_records(self):
    #     db.update_after_editing(self.selected_id, self.fields_values())
    #     self.view.view_records()
    #     self.destroy()
    #
    # def get_current_specialty(self, match_str):
    #     self.all_specialties = dict(db.c.execute('select  id, SpecName from specialty').fetchall())
    #     #print(self.all_specialties)
    #     print(match_str)
    #     try:
    #         return self.cbox_spec['values'].index(self.all_specialties.get(match_str))
    #     except:
    #         self.rb_onbase_value.set(11)
    #         self.click_radiobtn()
    #         return self.cbox_spec['values'].index(self.all_specialties.get(match_str))
    #
    # def get_spec_id_from_cbox(self, selected_str):
    #     for k, v in db.return_rb_dictionary(self.rb_onbase_value.get()).items():
    #         if v == selected_str:
    #             return k
    #
    # # endregion


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
        # self.cbox_gender.current(list_of_genders.index(self.dataset[12])) #?

    def update(self):
        wh = session.query(Warehouse).filter_by(id=self.selected_id).first()
        prod = session.query(Product).filter_by(id=wh.product_id).first()

        session.delete(wh)
        session.delete(prod)
        AddingWindow.add(self)






"""
        # self.b_add_or_edit = tk.Button(self, text='''Добавить''')
        # self.b_add_or_edit.place(relx=0.365, rely=0.911, height=24, width=63)
        # self.b_cancel = tk.Button(self, text='''Дать пинка!''')
        # self.b_cancel.place(relx=0.501, rely=0.911, height=24, width=75)

        # def __init__(self, root):
    #     self.title_value = StringVar()
    #     self.title_value.set("Добавление товара")
    #     super().__init__(root)
    #     self.init_child()
    #
    # def init_child(self):
    #     self.title(self.title_value.get())
    #     self.geometry("739x450+339+86")
    #     self.resizable(False, False)

        # self.date_of_registration = DateEntry(self, date_pattern='DD.MM.YYYY', width=12)
        # self.date_of_registration.place(relx=0.162, rely=0.022, relheight=0.047, relwidth=0.217)
        # # self.e_SI = tk.Entry(self)
        # # self.e_SI.place(relx=0.145, rely=0.24, height=20, relwidth=0.238)

      # self.date_of_birth = DateEntry(self.tkTab_1, date_pattern='DD.MM.YYYY', width=12, foreground='black')
        # self.date_of_birth.place(relx=0.667, rely=0.25, height=20, relwidth=0.248)
        # self.date_of_birth.configure(background="green")
"""