import pytest
def test():
    assert 3!=2


def test_is_instance():
    assert isinstance('This is a string',str)


class Student:
    def __init__(self,name: str, phone: str, age: int):
        self.name = name
        self.phone = phone
        self.age = age


def test_person():
    s1 = Student("Maruf Ahmed","01723123",25)
    assert s1.name == "Maruf Ahmed" , "First Name should be Maruf"
    assert s1.phone == "01723123"
    assert s1.age == 25




@pytest.fixture
def studentCreator():
    return Student("Maruf Ahmed","01723123",25)

def testFixture(studentCreator):

    assert studentCreator.phone == "01723123"
    assert studentCreator.age == 25
    assert studentCreator.name == 'Maaaaruf Ahmed', " Name should be Maruf"