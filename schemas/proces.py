from pydantic import BaseModel, constr, conint, validator
from typing import List


class CreateProcess(BaseModel):
    material_type_id: int
    connection: str
    name: str
    step: int
    deadline: int

    # @validator('name')
    # def validate_name_uniqueness(cls, value, values):
    #     if 'processes' in values:
    #         names = [process.name for process in values['processes']]
    #         if value in names:
    #             raise ValueError('Name must be unique for each process')
    #     return value
    #
    # @validator('step')
    # def validate_step_gt_0(cls, value):
    #     if value <= 0:
    #         raise ValueError('Step must be greater than 0')
    #     return value
    #
    # @validator('step')
    # def validate_step_unique_for_material_type(cls, value, values):
    #     if 'processes' in values:
    #         same_material_type_processes = [process for process in values['processes']
    #         if process.material_type_id == values['material_type_id']]
    #         steps = [process.step for process in same_material_type_processes]
    #         if value in steps:
    #             raise ValueError('Step must be unique for each material_type_id')
    #     return value


class UpdateProcess(BaseModel):
    id: int
    material_type_id: int
    connection: str
    name: str
    step: int
    deadline: int

    # @validator('name')
    # def validate_name_uniqueness(cls, value, values):
    #     if 'processes' in values:
    #         names = [process.name for process in values['processes'] if process.id != values['id']]
    #         if value in names:
    #             raise ValueError('Name must be unique for each process')
    #     return value
    #
    # @validator('step')
    # def validate_step_gt_0(cls, value):
    #     if value <= 0:
    #         raise ValueError('Step must be greater than 0')
    #     return value
    #
    # @validator('step')
    # def validate_step_unique_for_material_type(cls, value, values):
    #     if 'processes' in values:
    #         same_material_type_processes = [process for process in values['processes']
    #         if process.material_type_id == values['material_type_id'] and process.id != values['id']]
    #         steps = [process.step for process in same_material_type_processes]
    #         if value in steps:
    #             raise ValueError('Step must be unique for each material_type_id')
    #     return value
