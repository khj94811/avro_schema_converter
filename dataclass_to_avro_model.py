from dataclasses import dataclass, make_dataclass
from dataclasses_avroschema import AvroModel, types

primitive = (int, str, bool, float, None, bytes)

class BaseClass(AvroModel):
    class Meta:
        namespace = "example"

@dataclass
class AClass:
    aint: int
    astr: str

@dataclass
class BClass:
    bint: int
    bstr: str
    aclass: AClass

def convert_dataclass_to_avro_model(thisClass):
    fields = []
    for k, v in thisClass.__annotations__.items():
        if v not in primitive:
            converted_class = convert_dataclass_to_avro_model(v)
            fields.append((k, converted_class))
        else:
            fields.append((k, v))
    new_class = make_dataclass(cls_name=thisClass.__name__, bases=(BaseClass,), fields=fields)
    return new_class

def main():
    NewBClass = convert_dataclass_to_avro_model(BClass)
    obj = NewBClass(1, "2", AClass(3, "4"))
    print(obj.avro_schema())


if __name__ == "__main__":
    main()
