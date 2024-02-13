import os
import sys
from io import StringIO

import pytest

from phonebook import Contact, PhoneBook
from schemas import Contact as ContactPydantic

TEST_FILE = "test_phonebook.txt"


@pytest.fixture
def phonebook():
    pb = PhoneBook(TEST_FILE)
    yield pb
    if os.path.exists(TEST_FILE):
        os.remove(TEST_FILE)


def test_add_contact(phonebook):
    contact = Contact(
        contact_id=0,
        last_name="Doe",
        first_name="John",
        middle_name="Foo",
        organization="ABC",
        work_phone="1111-2222",
        personal_phone="3333-4444",
    )
    phonebook._PhoneBook__add_contact(contact)
    assert len(phonebook.contacts) == 1
    assert phonebook.contacts[0].last_name == "Doe"


def test_edit_contact(phonebook):
    contact = Contact(
        contact_id=0,
        last_name="Doe",
        first_name="John",
        middle_name="Foo",
        organization="ABC",
        work_phone="1111-2222",
        personal_phone="3333-4444",
    )
    phonebook._PhoneBook__add_contact(contact)

    edited_contact = Contact(
        contact_id=0,
        last_name="Doe",
        first_name="Mike",
        middle_name="Foo",
        organization="ABC",
        work_phone="1111-2222",
        personal_phone="3333-4444",
    )
    phonebook._PhoneBook__edit_contact(0, edited_contact)
    assert len(phonebook.contacts) == 1
    assert phonebook.contacts[0].first_name == "Mike"


def test_search_contact_by_id(phonebook):
    output = StringIO()
    sys.stdout = output
    contact = Contact(
        contact_id=0,
        last_name="Doe",
        first_name="John",
        middle_name="Foo",
        organization="ABC",
        work_phone="1111-2222",
        personal_phone="3333-4444",
    )
    phonebook._PhoneBook__add_contact(contact)

    phonebook._PhoneBook__search_contact_by_id(0)

    sys.stdout = sys.__stdout__
    output_str = output.getvalue().strip()

    assert "ID: 0 | Doe John Foo | Organization: ABC | Work phone: 1111-2222 | Personal_phone: 3333-4444" in output_str


def test_search_contacts_by_attributes(phonebook):
    output = StringIO()
    sys.stdout = output
    contacts = [
        Contact(
            contact_id=i,
            last_name="Linder",
            first_name="Robert",
            middle_name="John",
            organization="Samurai",
            work_phone=f"4444{i}",
            personal_phone="5555",
        )
        for i in range(1)
    ]

    for contact in contacts:
        phonebook._PhoneBook__add_contact(contact)

    search_values = {"work_phone": "44440"}
    phonebook._PhoneBook__search_contacts_by_attributes(search_values)

    sys.stdout = sys.__stdout__
    output_str = output.getvalue().strip()

    assert "ID: 0 | Linder Robert John | Organization: Samurai | Work phone: 44440 | Personal_phone: 5555" in output_str


def test_contact_validation_error(phonebook):
    with pytest.raises(ValueError):
        contact = ContactPydantic(
            contact_id=0,
            last_name="Doe",
            first_name="John",
            middle_name="Foo",
            organization="ABC",
            work_phone="phone",
            personal_phone="3333-4444",
        )
