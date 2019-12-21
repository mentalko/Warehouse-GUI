import sys, logging
import tkinter as tk
from tkinter import ttk, IntVar
from tkinter import messagebox
from child_window import AddingWindow, EditingWindow
from models import Product, Category, Warehouse, session


class Main(tk.Frame):
    def __init__(self, root):
        super().__init__(root)
        self.init_main()
        self.view_records()
        # print(session.query(Product.warehouse, Category.id, Category.name).all())

    def init_main(self):
        clmn_names = ( '№','Категория', 'Производитель', 'Продукт', 'Количество', 'Дата' )
        clmn_width = (10,150, 150, 150, 100, 100)

        toolbar = tk.Frame()
        toolbar.pack(side=tk.TOP, fill=tk.X)

        menu_add_dialog = tk.Button(toolbar, text='Добавить', bd=0)
        menu_add_dialog.bind('<Button>', lambda event: AddingWindow(root, app))
        menu_edit_dialog = tk.Button(toolbar, text=' Редактировать', bd=0)
        menu_edit_dialog.bind('<Button>', lambda event: EditingWindow(root,app))
        menu_delete_dialog = tk.Button(toolbar, text='Удалить', bd=0, command=self.delete)

        for c in (menu_add_dialog,menu_edit_dialog, menu_delete_dialog):
            c.pack(side=tk.LEFT)
        self.e_search = tk.Entry(toolbar, width=100)
        self.e_search.bind('<Key>', lambda event: self.search())
        self.e_search.pack(side=tk.LEFT)

        self.tree = ttk.Treeview(self, columns=clmn_names, height=50, show='headings')
        self.tree.column([0], width=15)
        for indx in range(len(clmn_names)):
            self.tree.heading(clmn_names[indx], text=clmn_names[indx])
        self.tree.pack(fill=tk.BOTH, expand=False)

    def view_records(self):
        try:
            self.all_products = \
                session.query(Warehouse.id, Category.name, Product.producer, Product.name, Warehouse.count, Warehouse.date)\
                .filter(Category.id == Product.category_id) \
                .filter(Product.id == Warehouse.product_id).all()

            for product in self.all_products:
                session.query(Warehouse.product_id, Warehouse.date).filter()
            print(self.all_products)
            [self.tree.delete(i) for i in self.tree.get_children()]
            [self.tree.insert('', 'end', values=row) for row in self.all_products ]
        except:
            logging.error('something wrong in view_records!!!')
        # self.cbox_all_spec['values'] = list(self.all_specialties.values())

    def search(self):

        search_result = \
            session.query(Warehouse.id, Category.name, Product.producer, Product.name, Warehouse.count, Warehouse.date) \
            .filter(Category.id == Product.category_id) \
            .filter(Product.id == Warehouse.product_id) \
            .filter(Product.name.contains(self.e_search.get())) \
            .all()
        print('<<< ',self.e_search.get())
        print('>>> ', search_result)

        [self.tree.delete(i) for i in self.tree.get_children()]
        [self.tree.insert('', 'end', values=row) for row in search_result]


    #https://ru.stackoverflow.com/questions/336931/%D0%98%D1%81%D0%BF%D0%BE%D0%BB%D1%8C%D0%B7%D0%BE%D0%B2%D0%B0%D0%BD%D0%B8%D0%B5-%D1%84%D1%83%D0%BD%D0%BA%D1%86%D0%B8%D0%B8-relationship-%D0%B2-sqlalchemy

    def delete(self):
        try:
            selected_id = self.tree.set(self.tree.selection()[0], '#1')
            wh = session.query(Warehouse).filter_by(id=selected_id).first()
            prod = session.query(Product).filter_by(id=wh.product_id).first()

            logging.info('>>> selected_id: {} ; wh.product_id: {}'.format(selected_id, wh.product_id))

            session.delete(wh)
            session.delete(prod)
            session.commit()
            self.view_records()
        except:
            logging.error('Error in delete!')


    # def delete_records(self):
    #     for selection_item in self.tree.selection():
    #         db.deliting([self.tree.set(selection_item, '#1')])
    #     self.view_records()
    #
    # def open_adding_dialog(self):
    #     AddingWindow(root, app)
    #
    # def open_editing_dialog(self):
    #     try:
    #         EditingWindow(root, app, self.tree.set(self.tree.selection()[0], '#1'))
    #     except:
    #         logging.exception('Item not selected')
    #
    # def open_add_spec_dialog(self):
    #     AddSpecWindow(root, app)

def create_record():
    moloko = Product(name='Молоко', category_id=1)
    moloko.products = [
        Warehouse(date='11/12/19', count=5),
        Warehouse(date='12/12/19', count=14),
    ]
    session.add(moloko)
    session.commit()


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s : %(levelname)s : %(message)s')
    # create_record()
    root = tk.Tk()
    app = Main(root)
    app.pack()
    root.title("Склад")
    root.geometry("1050x650+200+50")

    root.resizable(True, True)
    root.mainloop()
