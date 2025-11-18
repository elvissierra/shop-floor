import strawberry
from typing import Optional


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


@strawberry.type
class WorkCenterType:
    id: int
    name: str
    code: Optional[str]
    department_id: Optional[int]


@strawberry.type
class WorkOrderType:
    id: int
    number: str
    status: str
    quantity: int
    part_id: int
    department_id: Optional[int]
    work_center_id: Optional[int]


@strawberry.type
class WorkOrderOpType:
    id: int
    work_order_id: int
    sequence: int
    work_center_id: Optional[int]
    status: str


@strawberry.type
class RoutingType:
    id: int
    name: str
    part_id: int
    version: Optional[str]


@strawberry.type
class RoutingStepType:
    id: int
    routing_id: int
    sequence: int
    work_center_id: Optional[int]
    description: Optional[str]
    standard_minutes: Optional[int]


@strawberry.type
class BOMType:
    id: int
    part_id: int
    revision: Optional[str]


@strawberry.type
class BOMItemType:
    id: int
    bom_id: int
    component_part_id: int
    quantity: int


@strawberry.type
class ActivityLogType:
    id: int
    user_id: Optional[int]
    part_id: Optional[int]
    department_id: Optional[int]
    work_order_id: Optional[int]
    event_type: str
    message: Optional[str]
    created_at: str


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


@strawberry.input
class WorkCenterInput:
    name: str
    code: Optional[str] = None
    department_id: Optional[int] = None


@strawberry.input
class WorkOrderInput:
    number: str
    status: str
    quantity: int
    part_id: int
    department_id: Optional[int] = None
    work_center_id: Optional[int] = None


@strawberry.input
class WorkOrderOpInput:
    work_order_id: int
    sequence: int
    work_center_id: Optional[int] = None
    status: str = "pending"


@strawberry.input
class RoutingInput:
    name: str
    part_id: int
    version: Optional[str] = None


@strawberry.input
class RoutingStepInput:
    routing_id: int
    sequence: int
    work_center_id: Optional[int] = None
    description: Optional[str] = None
    standard_minutes: Optional[int] = None


@strawberry.input
class BOMInput:
    part_id: int
    revision: Optional[str] = None


@strawberry.input
class BOMItemInput:
    bom_id: int
    component_part_id: int
    quantity: int


@strawberry.input
class ActivityLogInput:
    user_id: Optional[int] = None
    part_id: Optional[int] = None
    department_id: Optional[int] = None
    work_order_id: Optional[int] = None
    event_type: str
    message: Optional[str] = None