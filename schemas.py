from pydantic import BaseModel, NonNegativeInt, constr, field_validator


class Contact(BaseModel):
    contact_id: NonNegativeInt
    last_name: constr(min_length=1, max_length=20)
    first_name: constr(min_length=1, max_length=20)
    middle_name: constr(min_length=1, max_length=20)
    organization: constr(min_length=1, max_length=60)
    work_phone: constr(min_length=4, max_length=20)
    personal_phone: constr(min_length=4, max_length=20)

    @field_validator("last_name", "first_name", "middle_name")
    def name_must_contain_only_letters(cls, value):
        if not value.isalpha():
            raise ValueError("Only letters are allowed for name fields")
        return value

    @field_validator("work_phone", "personal_phone")
    def phone_must_contain_only_digits(cls, value):
        allowed_chars = set("0123456789+-")
        if not set(value).issubset(allowed_chars):
            raise ValueError("Only digits, +, and - are allowed for phone fields")
        return value
