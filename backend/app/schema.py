import strawberry

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
class PartType:
    id: int
    name: str
    department_id: int


@strawberry.type
class UserType:
    id: int
    username: str
    department_id: int
    job: str
    time: int


@strawberry.type
class DefectType:
    id: int
    title: str
    description: str
    part_id: int
    defect_category_id: int


@strawberry.type
class QualityType:
    id: int
    pass_fail: bool
    defect_count: int
    part_id: int


@strawberry.input
class DepartmentInput:
    title: str
    description: str


@strawberry.input
class DefectCategoryInput:
    title: str
    department_id: int


@strawberry.input
class PartInput:
    name: str
    department_id: int


@strawberry.input
class UserInput:
    username: str
    department_id: int
    job: str
    time: int


@strawberry.input
class DefectInput:
    title: str
    description: str
    part_id: int
    defect_category_id: int


@strawberry.input
class QualityInput:
    pass_fail: bool
    defect_count: int
    part_id: int
