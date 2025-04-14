import strawberry

from typing import List, Optional


@strawberry.type
class DepartmentType:
    id: int
    title: str
    description: str

@strawberry.type
class DefectCategoryType:
    id: int
    title: str
    department_id: int

@strawberry.type
class PartsType:
    id: int
    name: str
    department_id: int

@strawberry.type
class UsersType:
    id: int
    username: str
    department_id: int
    job: str
    time: int

@strawberry.type
class DefectsType:
    id: int
    title: str
    description: str
    part_id: int
    defect_category_id: int

@strawberry.type
class QualityType:
    id: int
    pass_fail: str
    defect_count: int
    part_id: int

# input types
@strawberry.input
class DepartmentInput:
    id: int
    title: str
    description: str

@strawberry.input
class DefectCategoryInput:
    id: int
    title: str
    department_id: int

@strawberry.input
class PartsInput:
    id: int
    name: str
    department_id: int

@strawberry.input
class UserInput:
    id: int
    username: str
    department_id: int
    job: str
    time: int

@strawberry.input
class DefectInput:
    id: int
    title: str
    description: str
    part_id: int
    defect_category_id: int

@strawberry.input
class QualityInput:
    id: int
    pass_fail: str
    defect_count: int
    part_id: int