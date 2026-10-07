from pydantic import BaseModel, field_validator

class CreatePersonSchema(BaseModel):
    name: str
    note: str
    is_self: bool
    is_favourite: bool

class UpdatePersonSchema(BaseModel):
    name: str | None = None
    note: str | None = None
    is_self: bool | None = None
    is_favourite: bool | None = None

    @field_validator("name", "is_self", "is_favourite", mode="before")
    @classmethod
    def reject_null(cls, value):
        if value is None:
            raise ValueError("This field cannot be null")
        return value


class ReadPersonSchema(BaseModel):
    id: int
    name: str
    note: str | None
    is_self: bool
    is_favourite: bool

    model_config = {
        "from_attributes": True
    }

