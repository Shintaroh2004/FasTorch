from pydantic import BaseModel
import logging

logger = logging.getLogger(__name__)

class Person(BaseModel):
    name:str
    age:int

def test_serialize_json():
    json='{"name":"hoge","age":2}'
    person = Person.model_validate_json(json)
    logger.info(person)
    assert person.name == "hoge" and person.age==2

def test_deserialize_json():
    person=Person(name="hogege",age=2)
    json=person.model_dump_json()
    logger.info(json)
    assert type(json) == str