import os
from flask import Flask
from flask_restful import Api

from resource.menu import MenuResource, MenuItem, MenuListing, MenuKeywordMatching
from resource.bill import BillResource, BillOrderManagement, BillChecking, BillUpdateQuantity

name_db = "restaurant.db"
sqlite = "sqlite:///:{}".format(name_db)

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = sqlite
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
api = Api(app)

api.add_resource(MenuResource, '/menu/')
api.add_resource(MenuItem, '/menu/item/')
api.add_resource(MenuListing, '/menu/listing/')
api.add_resource(MenuKeywordMatching, '/menu/search/<string:keyword>')

api.add_resource(BillResource, '/bill/')
api.add_resource(BillChecking, '/bill/id/')
api.add_resource(BillOrderManagement, '/bill/manage/')
api.add_resource(BillUpdateQuantity, '/bill/manage/quantities/')


@app.before_first_request
def create_tables():
    from model.bill import BillModel, BillMenu
    from model.menu import MenuModel
    db.drop_all()
    db.create_all()
    # to initialize data
    MenuModel.add()
    BillModel.add()
    BillMenu.add()


if __name__ == "__main__":
    from dbsqlalchemy import db

    db.init_app(app)
    app.run(host='0.0.0.0',
            port=5002,
            debug=True)
