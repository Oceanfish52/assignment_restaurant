from dbsqlalchemy import db


class MenuModel(db.Model):
    __tablename__ = 'menu'
    name = db.Column(db.String(80), unique=True, nullable=False, primary_key=True)
    description = db.Column(db.Integer, nullable=False)
    image = db.Column(db.Text, nullable=False)
    price = db.Column(db.Integer, nullable=False)
    detail = db.Column(db.String(100), nullable=False)

    def __init__(self, name, description, image, price, detail):
        self.name = name
        self.description = description
        self.image = image
        self.price = price
        self.detail = detail

    def __repr__(self):
        return "<Name: {}>".format(self.name)

    @classmethod
    def search_all(cls):
        return cls.query.all()

    @classmethod
    def search_menu(cls, name):
        return cls.query.filter(cls.name == name).all()

    @classmethod
    def add(cls):
        initial_menu = [
            MenuModel(name='Hawaiian Pizza',
                      description="All-time favourite toppings, Hawaiian pizza in Tropical Hawaii style.",
                      image='https://s3-ap-sou theast-1.amazon aws.com/intervie w.ampostech.co m/backend/resta urant/menu1.jpg',
                      price=300,
                      detail="Italian Ham Pineapple"),
            MenuModel(name='Chicken Tom Yum Pizza',
                      description="Best marinated chicken with pineapple and mushroom on Spicy Lemon sauce."
                                  " Enjoy our tasty Thai style pizza.",
                      image='https://s3-ap-sou theast-1.amazon aws.com/intervie w.ampostech.co m/backend/resta urant/menu2.jpg',
                      price=350,
                      detail="Italian Thai Chicken Mushroom Hot"),
            MenuModel(name='Xiaolongbao',
                      description="Chinese steamed bun",
                      image='https://s3-ap-sou theast-1.amazon aws.com/intervie w.ampostech.co m/backend/resta urant/menu3.jpg',
                      price=200,
                      detail="Chinese Pork Recomme nded"),
            MenuModel(name='Kimchi',
                      description="Chinese steamed bun",
                      image='https://s3-ap-sou theast-1.amazon aws.com/intervie w.ampostech.co m/backend/resta urant/menu4.jpg',
                      price=50,
                      detail="Korean Radish Cabbage"),
            MenuModel(name='Oolong tea',
                      description="Partially fermented tea grown in the Alishan area",
                      image='https://s3-ap-sou theast-1.amazon aws.com/intervie w.ampostech.co m/backend/resta urant/menu5.jpg',
                      price=30,
                      detail="Hot Non-alcoh ol"),
            MenuModel(name='Beer',
                      description="Fantastic flavors and authentic regional appeal beer",
                      image='https://s3-ap-sou theast-1.amazon aws.com/intervie w.ampostech.co m/backend/resta urant/menu6.jpg',
                      price=60,
                      detail="Alcohol")]
        db.session.add_all(initial_menu)
        db.session.commit()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def rollback_from_db(self):
        db.session.rollback()
