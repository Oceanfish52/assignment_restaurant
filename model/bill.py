from dbsqlalchemy import db
from sqlalchemy import and_
from model.menu import MenuModel


class BillModel(db.Model):
    __tablename__ = 'bill'
    bill_id = db.Column(db.String(80), primary_key=True, nullable=False)
    total_price = db.Column(db.Integer, nullable=False)

    def __init__(self, bill_id, total_price):
        self.bill_id = bill_id
        self.total_price = total_price

    def __repr__(self):
        return "<#Bill: {} with {}>".format(self.bill_id, self.total_price)

    @classmethod
    def add(cls):
        initial_bill = BillModel(bill_id='101', total_price="300")
        db.session.add(initial_bill)
        db.session.commit()

    @classmethod
    def search_bill(cls, bill_id):
        return cls.query.filter(cls.bill_id == bill_id).first()

    @classmethod
    def search_bill_order(cls, bill_id):
        return db.session.query(cls.bill_id, BillMenu) \
            .join(BillMenu, cls.bill_id == BillMenu.bill_id).filter(cls.bill_id == bill_id).all()

    @classmethod
    def search_all(cls):
        return cls.query.all()

    def update_to_db(self):
        db.session.commit()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def rollback_from_db(self):
        db.session.rollback()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()


class BillMenu(db.Model):
    __tablename__ = 'order'
    bill_id = db.Column(db.String(80), db.ForeignKey('bill.bill_id'), primary_key=True, nullable=False)
    name = db.Column(db.String(80), db.ForeignKey('menu.name'), primary_key=True, nullable=False)
    order_time = db.Column(db.String(100), primary_key=True, nullable=False)
    quantities = db.Column(db.Integer, nullable=False)

    def __init__(self, bill_id, name, order_time, quantities):
        self.bill_id = bill_id
        self.name = name
        self.order_time = order_time
        self.quantities = quantities

    def __repr__(self):
        return "<#Bill with Menu: {} {} {} {}>".format(self.bill_id, self.order_time,
                                                       self.name, self.quantities)

    @classmethod
    def add(cls):
        initial_order = BillMenu(bill_id='101',
                                 name='Xiaolongbao',
                                 order_time='2019-07-21 12:00:00',
                                 quantities='1')
        db.session.add(initial_order)
        db.session.commit()

    @classmethod
    def search_billmenu(cls, billid):
        return cls.query.filter(cls.bill_id == billid).first()

    @classmethod
    def search_billname(cls, billid, name, ordertime):
        return cls.query.filter(and_(cls.bill_id == billid, cls.name == name, cls.order_time == ordertime)).first()

    @classmethod
    def search_billoreder(cls, billid, ordertime):
        return cls.query.filter(and_(cls.bill_id == billid,
                                     cls.order_time == ordertime)).first()

    @classmethod
    def search_price(cls, name):
        return db.session.query(cls.name, MenuModel.price) \
            .join(MenuModel, cls.name == MenuModel.name).filter(cls.name == name).first()

    def update_to_db(self):
        db.session.commit()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def rollback_from_db(self):
        db.session.rollback()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
