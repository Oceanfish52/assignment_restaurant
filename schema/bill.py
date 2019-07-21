from marshmallow import Schema, fields, ValidationError


class MenuOrder(Schema):
    name = fields.String(required=True)
    quantities = fields.Integer(required=True)
    order_time = fields.String()


class BillSchema(Schema):
    bill_id = fields.String(required=True)
    total_price = fields.String(required=True)
    menu = fields.List(fields.Nested(MenuOrder))


class BillMenuSchema(Schema):
    bill_id = fields.String(required=True)
    name = fields.String(required=True)
    quantities = fields.Integer(required=True)
    order_time = fields.String()


class BillCheckSchema(Schema):
    bill_id = fields.String(required=True)


class BillDeleteSchema(Schema):
    bill_id = fields.String(required=True)
    order_time = fields.String(required=True)
