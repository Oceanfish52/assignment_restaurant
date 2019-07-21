from marshmallow import Schema, fields, ValidationError


class MenuSchema(Schema):
    name = fields.String(required=True)
    description = fields.String(required=True)
    image = fields.String(required=True)
    price = fields.Integer(required=True)
    detail = fields.String(required=True)


