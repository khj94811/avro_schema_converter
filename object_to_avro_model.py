from dataclasses import dataclass, make_dataclass
from dataclasses_avroschema import AvroModel, types

primitive = (int, str, bool, float, None, bytes)

class BaseClass(AvroModel):
    class Meta:
        namespace = "example"

class AClass:
    def __init__(self, aint, astr):
        self.aint = aint
        self.astr = astr

class BClass:
    def __init__(self, bint, bstr, aclass):
        self.bint = bint
        self.bstr = bstr
        self.aclass = aclass

def convert_obj_to_avro_model(obj):
    fields = []
    for k, v in obj.__dict__.items():
        if type(v) not in primitive:
            converted_class = convert_obj_to_avro_model(v)
            fields.append((k, converted_class))
        else:
            fields.append((k, type(v)))
    new_class = make_dataclass(cls_name=obj.__class__.__name__, bases=(BaseClass,), fields=fields)
    return new_class

def main():
    obj = BClass(1, "2", AClass(3, "4"))

    NewBClass = convert_obj_to_avro_model(obj)
    
    obj2 = NewBClass(1, "2", AClass(3, "4"))
    print(obj2.avro_schema())


if __name__ == "__main__":
    main()
