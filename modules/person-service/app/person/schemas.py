from marshmallow import Schema, fields


class PersonSchema(Schema):
    class Meta:
        fields = ("id", "first_name", "last_name", "company_name")

    id = fields.Int()
    first_name = fields.Str(required=True)
    last_name = fields.Str(required=True)
    company_name = fields.Str(required=True)
