from pydantic import BaseModel



class CreateConnectionSchema(BaseModel):
    person_id_a: int
    person_id_b: int
    via:str

class UpdateConnectionSchema(BaseModel):
    person_a_id: int | None = None
    person_b_id: int | None = None
    via: str | None = None

class ReadConnectionSchema(BaseModel):
    id:int
    person_a_id: int
    person_b_id: int
    via:str

    model_config = {
        "from_attributes": True
    }


