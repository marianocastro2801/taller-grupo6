from marshmallow import Schema, fields, validate, ValidationError

# Validaciones

not_blank = validate.Length(min=1, error='Field cannot be blank')
max_lenght = validate.Length(max=50, error='Field must be less than 50 characters')

#Estructura a JSON request
class PersonaSchema(Schema):
    
    DNI = fields.Int()
    fecha_hora_nacimiento = fields.Str(required=True, validate=[not_blank, max_lenght])
    
    
persona_schema = PersonaSchema(many=False)


