from __future__ import annotations

from datetime import datetime
from sqlalchemy.orm import Session
from models.models import (
    User,
    Department,
    DefectCategory,
    Defect,
    Part,
    Quality,
    WorkCenter,
    WorkOrder,
    WorkOrderOp,
    Routing,
    RoutingStep,
    BOM,
    BOMItem,
    ActivityLog,
    Floor,
    FloorZone,
)
from strawberry.exceptions import GraphQLError
from app.schema import (
    UserInput,
    DepartmentInput,
    DefectCategoryInput,
    DefectInput,
    PartInput,
    QualityInput,
    WorkCenterInput,
    WorkOrderInput,
    WorkOrderOpInput,
    RoutingInput,
    RoutingStepInput,
    BOMInput,
    BOMItemInput,
    ActivityLogInput,
    FloorInput,
    FloorZoneInput,
)

# --- Pagination helper ---
DEFAULT_LIMIT = 50
MAX_LIMIT = 200


def _coerce_pagination(limit: int | None, offset: int | None) -> tuple[int, int]:
    """Clamp and sanitize limit/offset."""
    limit_ = DEFAULT_LIMIT if (limit is None or limit <= 0) else min(limit, MAX_LIMIT)
    offset_ = 0 if (offset is None or offset < 0) else offset
    return limit_, offset_


# --- Repository layer ---

class FloorRepo:
    def __init__(self, db: Session):
        self.db = db

    def list(self, limit: int | None = None, offset: int | None = None) -> list[Floor]:
        limit_, offset_ = _coerce_pagination(limit, offset)
        return self.db.query(Floor).offset(offset_).limit(limit_).all()

    def get(self, floor_id: int) -> Floor | None:
        return self.db.get(Floor, floor_id)

    def by_name(self, name: str) -> Floor | None:
        return self.db.query(Floor).filter(Floor.name == name).first()

    def create(self, floor: Floor) -> Floor:
        self.db.add(floor)
        self.db.commit()
        self.db.refresh(floor)
        return floor

    def delete(self, floor: Floor) -> None:
        self.db.delete(floor)
        self.db.commit()


class FloorZoneRepo:
    def __init__(self, db: Session):
        self.db = db

    def list(self, limit: int | None = None, offset: int | None = None) -> list[FloorZone]:
        limit_, offset_ = _coerce_pagination(limit, offset)
        return self.db.query(FloorZone).offset(offset_).limit(limit_).all()

    def list_by_floor(self, floor_id: int) -> list[FloorZone]:
        return self.db.query(FloorZone).filter(FloorZone.floor_id == floor_id).all()

    def get(self, zone_id: int) -> FloorZone | None:
        return self.db.get(FloorZone, zone_id)

    def create(self, zone: FloorZone) -> FloorZone:
        self.db.add(zone)
        self.db.commit()
        self.db.refresh(zone)
        return zone

    def delete(self, zone: FloorZone) -> None:
        self.db.delete(zone)
        self.db.commit()


class UserRepo:
    def __init__(self, db: Session):
        self.db = db

    def by_username(self, username: str) -> User | None:
        return self.db.query(User).filter(User.username == username).first()

    def list(self, limit: int | None = None, offset: int | None = None) -> list[User]:
        limit_, offset_ = _coerce_pagination(limit, offset)
        return self.db.query(User).offset(offset_).limit(limit_).all()

    def get(self, user_id: int) -> User | None:
        return self.db.get(User, user_id)

    def create(self, user: User) -> User:
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user

    def delete(self, user: User) -> None:
        self.db.delete(user)
        self.db.commit()


class DepartmentRepo:
    def __init__(self, db: Session):
        self.db = db

    def by_title(self, title: str) -> Department | None:
        return self.db.query(Department).filter(Department.title == title).first()

    def list(self, limit: int | None = None, offset: int | None = None) -> list[Department]:
        limit_, offset_ = _coerce_pagination(limit, offset)
        return self.db.query(Department).offset(offset_).limit(limit_).all()

    def get(self, department_id: int) -> Department | None:
        return self.db.get(Department, department_id)

    def create(self, department: Department) -> Department:
        self.db.add(department)
        self.db.commit()
        self.db.refresh(department)
        return department

    def delete(self, department: Department) -> None:
        self.db.delete(department)
        self.db.commit()


class PartRepo:
    def __init__(self, db: Session):
        self.db = db

    def list(self, limit: int | None = None, offset: int | None = None) -> list[Part]:
        limit_, offset_ = _coerce_pagination(limit, offset)
        return self.db.query(Part).offset(offset_).limit(limit_).all()

    def get(self, part_id: int) -> Part | None:
        return self.db.get(Part, part_id)

    def create(self, part: Part) -> Part:
        self.db.add(part)
        self.db.commit()
        self.db.refresh(part)
        return part

    def delete(self, part: Part) -> None:
        self.db.delete(part)
        self.db.commit()


class DefectCategoryRepo:
    def __init__(self, db: Session):
        self.db = db

    def by_title(self, title: str) -> DefectCategory | None:
        return self.db.query(DefectCategory).filter(DefectCategory.title == title).first()

    def list(self, limit: int | None = None, offset: int | None = None) -> list[DefectCategory]:
        limit_, offset_ = _coerce_pagination(limit, offset)
        return self.db.query(DefectCategory).offset(offset_).limit(limit_).all()

    def get(self, defect_category_id: int) -> DefectCategory | None:
        return self.db.get(DefectCategory, defect_category_id)

    def create(self, dc: DefectCategory) -> DefectCategory:
        self.db.add(dc)
        self.db.commit()
        self.db.refresh(dc)
        return dc

    def delete(self, dc: DefectCategory) -> None:
        self.db.delete(dc)
        self.db.commit()


class DefectRepo:
    def __init__(self, db: Session):
        self.db = db

    def list(self, limit: int | None = None, offset: int | None = None) -> list[Defect]:
        limit_, offset_ = _coerce_pagination(limit, offset)
        return self.db.query(Defect).offset(offset_).limit(limit_).all()

    def get(self, defect_id: int) -> Defect | None:
        return self.db.get(Defect, defect_id)

    def first_by_part(self, part_id: int) -> Defect | None:
        return self.db.query(Defect).filter(Defect.part_id == part_id).first()

    def first_by_defect_category(self, defect_category_id: int) -> Defect | None:
        return (
            self.db.query(Defect)
            .filter(Defect.defect_category_id == defect_category_id)
            .first()
        )

    def first_by_part_and_defect_category(
        self, part_id: int, defect_category_id: int
    ) -> Defect | None:
        return (
            self.db.query(Defect)
            .filter(
                Defect.part_id == part_id,
                Defect.defect_category_id == defect_category_id,
            )
            .first()
        )

    def first_by_part_and_department(
        self, part_id: int, department_id: int
    ) -> Defect | None:
        return (
            self.db.query(Defect)
            .join(Defect.part)
            .filter(Defect.part_id == part_id, Part.department_id == department_id)
            .first()
        )

    def create(self, defect: Defect) -> Defect:
        self.db.add(defect)
        self.db.commit()
        self.db.refresh(defect)
        return defect

    def delete(self, defect: Defect) -> None:
        self.db.delete(defect)
        self.db.commit()


class QualityRepo:
    def __init__(self, db: Session):
        self.db = db

    def list(self, limit: int | None = None, offset: int | None = None) -> list[Quality]:
        limit_, offset_ = _coerce_pagination(limit, offset)
        return self.db.query(Quality).offset(offset_).limit(limit_).all()

    def get(self, quality_id: int) -> Quality | None:
        return self.db.get(Quality, quality_id)

    def first_by_part(self, part_id: int) -> Quality | None:
        return self.db.query(Quality).filter(Quality.part_id == part_id).first()

    def create(self, quality: Quality) -> Quality:
        self.db.add(quality)
        self.db.commit()
        self.db.refresh(quality)
        return quality

    def delete(self, quality: Quality) -> None:
        self.db.delete(quality)
        self.db.commit()


class WorkCenterRepo:
    def __init__(self, db: Session):
        self.db = db

    def by_code(self, code: str) -> WorkCenter | None:
        return self.db.query(WorkCenter).filter(WorkCenter.code == code).first()

    def list(self, limit: int | None = None, offset: int | None = None) -> list[WorkCenter]:
        limit_, offset_ = _coerce_pagination(limit, offset)
        return self.db.query(WorkCenter).offset(offset_).limit(limit_).all()

    def get(self, work_center_id: int) -> WorkCenter | None:
        return self.db.get(WorkCenter, work_center_id)

    def create(self, wc: WorkCenter) -> WorkCenter:
        self.db.add(wc)
        self.db.commit()
        self.db.refresh(wc)
        return wc

    def delete(self, wc: WorkCenter) -> None:
        self.db.delete(wc)
        self.db.commit()


class WorkOrderRepo:
    def __init__(self, db: Session):
        self.db = db

    def by_number(self, number: str) -> WorkOrder | None:
        return self.db.query(WorkOrder).filter(WorkOrder.number == number).first()

    def list(self, limit: int | None = None, offset: int | None = None) -> list[WorkOrder]:
        limit_, offset_ = _coerce_pagination(limit, offset)
        return self.db.query(WorkOrder).offset(offset_).limit(limit_).all()

    def get(self, work_order_id: int) -> WorkOrder | None:
        return self.db.get(WorkOrder, work_order_id)

    def create(self, wo: WorkOrder) -> WorkOrder:
        self.db.add(wo)
        self.db.commit()
        self.db.refresh(wo)
        return wo

    def delete(self, wo: WorkOrder) -> None:
        self.db.delete(wo)
        self.db.commit()


class WorkOrderOpRepo:
    def __init__(self, db: Session):
        self.db = db

    def list(self, limit: int | None = None, offset: int | None = None) -> list[WorkOrderOp]:
        limit_, offset_ = _coerce_pagination(limit, offset)
        return self.db.query(WorkOrderOp).offset(offset_).limit(limit_).all()

    def list_by_work_order(self, work_order_id: int) -> list[WorkOrderOp]:
        return (
            self.db.query(WorkOrderOp)
            .filter(WorkOrderOp.work_order_id == work_order_id)
            .order_by(WorkOrderOp.sequence)
            .all()
        )

    def get(self, op_id: int) -> WorkOrderOp | None:
        return self.db.get(WorkOrderOp, op_id)

    def create(self, op: WorkOrderOp) -> WorkOrderOp:
        self.db.add(op)
        self.db.commit()
        self.db.refresh(op)
        return op

    def delete(self, op: WorkOrderOp) -> None:
        self.db.delete(op)
        self.db.commit()


class RoutingRepo:
    def __init__(self, db: Session):
        self.db = db

    def list(self, limit: int | None = None, offset: int | None = None) -> list[Routing]:
        limit_, offset_ = _coerce_pagination(limit, offset)
        return self.db.query(Routing).offset(offset_).limit(limit_).all()

    def get(self, routing_id: int) -> Routing | None:
        return self.db.get(Routing, routing_id)

    def create(self, routing: Routing) -> Routing:
        self.db.add(routing)
        self.db.commit()
        self.db.refresh(routing)
        return routing

    def delete(self, routing: Routing) -> None:
        self.db.delete(routing)
        self.db.commit()


class RoutingStepRepo:
    def __init__(self, db: Session):
        self.db = db

    def list(self, limit: int | None = None, offset: int | None = None) -> list[RoutingStep]:
        limit_, offset_ = _coerce_pagination(limit, offset)
        return self.db.query(RoutingStep).offset(offset_).limit(limit_).all()

    def list_by_routing(self, routing_id: int) -> list[RoutingStep]:
        return (
            self.db.query(RoutingStep)
            .filter(RoutingStep.routing_id == routing_id)
            .order_by(RoutingStep.sequence)
            .all()
        )

    def get(self, step_id: int) -> RoutingStep | None:
        return self.db.get(RoutingStep, step_id)

    def create(self, step: RoutingStep) -> RoutingStep:
        self.db.add(step)
        self.db.commit()
        self.db.refresh(step)
        return step

    def delete(self, step: RoutingStep) -> None:
        self.db.delete(step)
        self.db.commit()


class BOMRepo:
    def __init__(self, db: Session):
        self.db = db

    def list(self, limit: int | None = None, offset: int | None = None) -> list[BOM]:
        limit_, offset_ = _coerce_pagination(limit, offset)
        return self.db.query(BOM).offset(offset_).limit(limit_).all()

    def get(self, bom_id: int) -> BOM | None:
        return self.db.get(BOM, bom_id)

    def create(self, bom: BOM) -> BOM:
        self.db.add(bom)
        self.db.commit()
        self.db.refresh(bom)
        return bom

    def delete(self, bom: BOM) -> None:
        self.db.delete(bom)
        self.db.commit()


class BOMItemRepo:
    def __init__(self, db: Session):
        self.db = db

    def list(self, limit: int | None = None, offset: int | None = None) -> list[BOMItem]:
        limit_, offset_ = _coerce_pagination(limit, offset)
        return self.db.query(BOMItem).offset(offset_).limit(limit_).all()

    def list_by_bom(self, bom_id: int) -> list[BOMItem]:
        return self.db.query(BOMItem).filter(BOMItem.bom_id == bom_id).all()

    def get(self, item_id: int) -> BOMItem | None:
        return self.db.get(BOMItem, item_id)

    def create(self, item: BOMItem) -> BOMItem:
        self.db.add(item)
        self.db.commit()
        self.db.refresh(item)
        return item

    def delete(self, item: BOMItem) -> None:
        self.db.delete(item)
        self.db.commit()


class ActivityLogRepo:
    def __init__(self, db: Session):
        self.db = db

    def list(self, limit: int | None = None, offset: int | None = None) -> list[ActivityLog]:
        limit_, offset_ = _coerce_pagination(limit, offset)
        return self.db.query(ActivityLog).offset(offset_).limit(limit_).all()

    def get(self, log_id: int) -> ActivityLog | None:
        return self.db.get(ActivityLog, log_id)

    def list_by_work_order(self, work_order_id: int) -> list[ActivityLog]:
        return (
            self.db.query(ActivityLog)
            .filter(ActivityLog.work_order_id == work_order_id)
            .all()
        )

    def create(self, log: ActivityLog) -> ActivityLog:
        self.db.add(log)
        self.db.commit()
        self.db.refresh(log)
        return log


class MutationService:
    def __init__(self, db: Session):
        self.db = db
        self.users = UserRepo(db)
        self.departments = DepartmentRepo(db)
        self.parts = PartRepo(db)
        self.defect_categories = DefectCategoryRepo(db)
        self.defects = DefectRepo(db)
        self.qualities = QualityRepo(db)
        self.work_centers = WorkCenterRepo(db)
        self.work_orders = WorkOrderRepo(db)
        self.work_order_ops = WorkOrderOpRepo(db)
        self.routings = RoutingRepo(db)
        self.routing_steps = RoutingStepRepo(db)
        self.boms = BOMRepo(db)
        self.bom_items = BOMItemRepo(db)
        self.activity_logs = ActivityLogRepo(db)
        self.floors = FloorRepo(db)
        self.floor_zones = FloorZoneRepo(db)

    # ---- Floor CRUD ----
    def add_floor(self, data: FloorInput) -> Floor:
        if self.floors.by_name(data.name):
            raise GraphQLError(
                "Floor already exists; check name.",
                extensions={"code": "CONFLICT"},
            )
        return self.floors.create(Floor(name=data.name, description=data.description))

    def update_floor(self, floor_id: int, data: FloorInput) -> Floor:
        floor = self.floors.get(floor_id)
        if not floor:
            raise GraphQLError(
                f"Floor {floor_id} not found", extensions={"code": "NOT_FOUND"}
            )
        if data.name and data.name != floor.name and self.floors.by_name(data.name):
            raise GraphQLError(
                "Floor already exists; check name.", extensions={"code": "CONFLICT"}
            )
        floor.name = data.name
        floor.description = data.description
        self.db.commit()
        self.db.refresh(floor)
        return floor

    def delete_floor(self, floor_id: int) -> bool:
        floor = self.floors.get(floor_id)
        if not floor:
            raise GraphQLError(
                f"Floor {floor_id} not found", extensions={"code": "NOT_FOUND"}
            )
        self.floors.delete(floor)
        return True

    # ---- FloorZone CRUD ----
    def add_floor_zone(self, data: FloorZoneInput) -> FloorZone:
        if not self.floors.get(data.floor_id):
            raise GraphQLError(
                f"Floor {data.floor_id} not found", extensions={"code": "NOT_FOUND"}
            )
        if data.department_id is not None and not self.departments.get(data.department_id):
            raise GraphQLError(
                f"Department {data.department_id} not found",
                extensions={"code": "NOT_FOUND"},
            )
        if data.work_center_id is not None and not self.work_centers.get(data.work_center_id):
            raise GraphQLError(
                f"Work center {data.work_center_id} not found",
                extensions={"code": "NOT_FOUND"},
            )
        return self.floor_zones.create(
            FloorZone(
                floor_id=data.floor_id,
                name=data.name,
                zone_type=data.zone_type,
                department_id=data.department_id,
                work_center_id=data.work_center_id,
                polygon=data.polygon,
            )
        )

    def update_floor_zone(self, zone_id: int, data: FloorZoneInput) -> FloorZone:
        zone = self.floor_zones.get(zone_id)
        if not zone:
            raise GraphQLError(
                f"Floor zone {zone_id} not found", extensions={"code": "NOT_FOUND"}
            )
        if data.floor_id != zone.floor_id and not self.floors.get(data.floor_id):
            raise GraphQLError(
                f"Floor {data.floor_id} not found", extensions={"code": "NOT_FOUND"}
            )
        if data.department_id is not None and not self.departments.get(data.department_id):
            raise GraphQLError(
                f"Department {data.department_id} not found",
                extensions={"code": "NOT_FOUND"},
            )
        if data.work_center_id is not None and not self.work_centers.get(data.work_center_id):
            raise GraphQLError(
                f"Work center {data.work_center_id} not found",
                extensions={"code": "NOT_FOUND"},
            )
        zone.floor_id = data.floor_id
        zone.name = data.name
        zone.zone_type = data.zone_type
        zone.department_id = data.department_id
        zone.work_center_id = data.work_center_id
        zone.polygon = data.polygon
        self.db.commit()
        self.db.refresh(zone)
        return zone

    def delete_floor_zone(self, zone_id: int) -> bool:
        zone = self.floor_zones.get(zone_id)
        if not zone:
            raise GraphQLError(
                f"Floor zone {zone_id} not found", extensions={"code": "NOT_FOUND"}
            )
        self.floor_zones.delete(zone)
        return True

    # ---- User CRUD ----
    def add_user(self, user_data: UserInput) -> User:
        if self.users.by_username(user_data.username):
            raise GraphQLError(
                "User already exists; check username.", extensions={"code": "CONFLICT"}
            )
        return self.users.create(
            User(
                username=user_data.username,
                department_id=user_data.department_id,
                job=user_data.job,
                time=user_data.time,
            )
        )

    def update_user(self, user_id: int, data: UserInput) -> User:
        user = self.users.get(user_id)
        if not user:
            raise GraphQLError(
                f"User {user_id} not found", extensions={"code": "NOT_FOUND"}
            )
        if data.username and data.username != user.username and self.users.by_username(data.username):
            raise GraphQLError(
                "User already exists; check username.", extensions={"code": "CONFLICT"}
            )
        user.username = data.username
        user.department_id = data.department_id
        user.job = data.job
        user.time = data.time
        self.db.commit()
        self.db.refresh(user)
        return user

    def delete_user(self, user_id: int) -> bool:
        user = self.users.get(user_id)
        if not user:
            raise GraphQLError(
                f"User {user_id} not found", extensions={"code": "NOT_FOUND"}
            )
        self.users.delete(user)
        return True

    # ---- Department CRUD ----
    def add_department(self, department_data: DepartmentInput) -> Department:
        if self.departments.by_title(department_data.title):
            raise GraphQLError(
                "Department already exists; check title.",
                extensions={"code": "CONFLICT"},
            )
        return self.departments.create(
            Department(
                title=department_data.title,
                description=department_data.description,
            )
        )

    def update_department(self, department_id: int, data: DepartmentInput) -> Department:
        department = self.departments.get(department_id)
        if not department:
            raise GraphQLError(
                f"Department {department_id} not found",
                extensions={"code": "NOT_FOUND"},
            )
        department.title = data.title
        department.description = data.description
        self.db.commit()
        self.db.refresh(department)
        return department

    def delete_department(self, department_id: int) -> bool:
        department = self.departments.get(department_id)
        if not department:
            raise GraphQLError(
                f"Department {department_id} not found",
                extensions={"code": "NOT_FOUND"},
            )
        self.departments.delete(department)
        return True

    # ---- Part CRUD ----
    def add_part(self, part_data: PartInput) -> Part:
        return self.parts.create(
            Part(name=part_data.name, department_id=part_data.department_id)
        )

    def update_part(self, part_id: int, data: PartInput) -> Part:
        part = self.parts.get(part_id)
        if not part:
            raise GraphQLError(
                f"Part {part_id} not found", extensions={"code": "NOT_FOUND"}
            )
        part.name = data.name
        part.department_id = data.department_id
        self.db.commit()
        self.db.refresh(part)
        return part

    def delete_part(self, part_id: int) -> bool:
        part = self.parts.get(part_id)
        if not part:
            raise GraphQLError(
                f"Part {part_id} not found", extensions={"code": "NOT_FOUND"}
            )
        self.parts.delete(part)
        return True

    # ---- DefectCategory CRUD ----
    def add_defect_category(self, def_cat_data: DefectCategoryInput) -> DefectCategory:
        if def_cat_data.department_id is not None and not self.departments.get(
            def_cat_data.department_id
        ):
            raise GraphQLError(
                f"Department {def_cat_data.department_id} not found",
                extensions={"code": "NOT_FOUND"},
            )
        return self.defect_categories.create(
            DefectCategory(
                title=def_cat_data.title,
                department_id=def_cat_data.department_id,
            )
        )

    def update_defect_category(
        self, defect_category_id: int, data: DefectCategoryInput
    ) -> DefectCategory:
        dc = self.defect_categories.get(defect_category_id)
        if not dc:
            raise GraphQLError(
                f"Defect category {defect_category_id} not found",
                extensions={"code": "NOT_FOUND"},
            )
        if (
            data.title
            and data.title != dc.title
            and self.defect_categories.by_title(data.title)
        ):
            raise GraphQLError(
                "Defect category already exists; check title.",
                extensions={"code": "CONFLICT"},
            )
        dc.title = data.title
        dc.department_id = data.department_id
        self.db.commit()
        self.db.refresh(dc)
        return dc

    def delete_defect_category(self, defect_category_id: int) -> bool:
        dc = self.defect_categories.get(defect_category_id)
        if not dc:
            raise GraphQLError(
                f"Defect category {defect_category_id} not found",
                extensions={"code": "NOT_FOUND"},
            )
        self.defect_categories.delete(dc)
        return True

    # ---- Defect CRUD ----
    def add_defect(self, defect_data: DefectInput) -> Defect:
        return self.defects.create(
            Defect(
                title=defect_data.title,
                description=defect_data.description,
                part_id=defect_data.part_id,
                defect_category_id=defect_data.defect_category_id,
            )
        )

    def update_defect(self, defect_id: int, data: DefectInput) -> Defect:
        defect = self.defects.get(defect_id)
        if not defect:
            raise GraphQLError(
                f"Defect {defect_id} not found", extensions={"code": "NOT_FOUND"}
            )
        defect.title = data.title
        defect.description = data.description
        defect.part_id = data.part_id
        defect.defect_category_id = data.defect_category_id
        self.db.commit()
        self.db.refresh(defect)
        return defect

    def delete_defect(self, defect_id: int) -> bool:
        defect = self.defects.get(defect_id)
        if not defect:
            raise GraphQLError(
                f"Defect {defect_id} not found", extensions={"code": "NOT_FOUND"}
            )
        self.defects.delete(defect)
        return True

    # ---- Quality CRUD ----
    def add_quality(self, quality_data: QualityInput) -> Quality:
        return self.qualities.create(
            Quality(
                pass_fail=quality_data.pass_fail,
                defect_count=quality_data.defect_count,
                part_id=quality_data.part_id,
            )
        )

    def update_quality(self, quality_id: int, data: QualityInput) -> Quality:
        quality = self.qualities.get(quality_id)
        if not quality:
            raise GraphQLError(
                f"Quality {quality_id} not found", extensions={"code": "NOT_FOUND"}
            )
        quality.pass_fail = data.pass_fail
        quality.defect_count = data.defect_count
        quality.part_id = data.part_id
        self.db.commit()
        self.db.refresh(quality)
        return quality

    def delete_quality(self, quality_id: int) -> bool:
        quality = self.qualities.get(quality_id)
        if not quality:
            raise GraphQLError(
                f"Quality {quality_id} not found", extensions={"code": "NOT_FOUND"}
            )
        self.qualities.delete(quality)
        return True

    # ---- WorkCenter CRUD ----
    def add_work_center(self, data: WorkCenterInput) -> WorkCenter:
        if data.code and self.work_centers.by_code(data.code):
            raise GraphQLError(
                "Work center code already exists; check code.",
                extensions={"code": "CONFLICT"},
            )
        if data.department_id is not None and not self.departments.get(data.department_id):
            raise GraphQLError(
                f"Department {data.department_id} not found",
                extensions={"code": "NOT_FOUND"},
            )
        return self.work_centers.create(
            WorkCenter(name=data.name, code=data.code, department_id=data.department_id)
        )

    def update_work_center(self, work_center_id: int, data: WorkCenterInput) -> WorkCenter:
        wc = self.work_centers.get(work_center_id)
        if not wc:
            raise GraphQLError(
                f"Work center {work_center_id} not found",
                extensions={"code": "NOT_FOUND"},
            )
        if data.code and data.code != wc.code and self.work_centers.by_code(data.code):
            raise GraphQLError(
                "Work center code already exists; check code.",
                extensions={"code": "CONFLICT"},
            )
        if data.department_id is not None and not self.departments.get(data.department_id):
            raise GraphQLError(
                f"Department {data.department_id} not found",
                extensions={"code": "NOT_FOUND"},
            )
        wc.name = data.name
        wc.code = data.code
        wc.department_id = data.department_id
        self.db.commit()
        self.db.refresh(wc)
        return wc

    def delete_work_center(self, work_center_id: int) -> bool:
        wc = self.work_centers.get(work_center_id)
        if not wc:
            raise GraphQLError(
                f"Work center {work_center_id} not found",
                extensions={"code": "NOT_FOUND"},
            )
        self.work_centers.delete(wc)
        return True

    # ---- WorkOrder CRUD ----
    def add_work_order(self, data: WorkOrderInput) -> WorkOrder:
        if self.work_orders.by_number(data.number):
            raise GraphQLError(
                "Work order already exists; check number.",
                extensions={"code": "CONFLICT"},
            )
        part = self.parts.get(data.part_id)
        if not part:
            raise GraphQLError(
                f"Part {data.part_id} not found", extensions={"code": "NOT_FOUND"}
            )
        if data.work_center_id is not None and not self.work_centers.get(data.work_center_id):
            raise GraphQLError(
                f"Work center {data.work_center_id} not found",
                extensions={"code": "NOT_FOUND"},
            )
        department_id = (
            data.department_id if data.department_id is not None else part.department_id
        )
        return self.work_orders.create(
            WorkOrder(
                number=data.number,
                status=data.status,
                quantity=data.quantity,
                part_id=data.part_id,
                department_id=department_id,
                work_center_id=data.work_center_id,
            )
        )

    def update_work_order(self, work_order_id: int, data: WorkOrderInput) -> WorkOrder:
        wo = self.work_orders.get(work_order_id)
        if not wo:
            raise GraphQLError(
                f"Work order {work_order_id} not found",
                extensions={"code": "NOT_FOUND"},
            )
        if data.number and data.number != wo.number and self.work_orders.by_number(data.number):
            raise GraphQLError(
                "Work order already exists; check number.",
                extensions={"code": "CONFLICT"},
            )
        part = self.parts.get(data.part_id)
        if not part:
            raise GraphQLError(
                f"Part {data.part_id} not found", extensions={"code": "NOT_FOUND"}
            )
        if data.work_center_id is not None and not self.work_centers.get(data.work_center_id):
            raise GraphQLError(
                f"Work center {data.work_center_id} not found",
                extensions={"code": "NOT_FOUND"},
            )
        wo.number = data.number
        wo.status = data.status
        wo.quantity = data.quantity
        wo.part_id = data.part_id
        wo.department_id = (
            data.department_id if data.department_id is not None else part.department_id
        )
        wo.work_center_id = data.work_center_id
        self.db.commit()
        self.db.refresh(wo)
        return wo

    def delete_work_order(self, work_order_id: int) -> bool:
        wo = self.work_orders.get(work_order_id)
        if not wo:
            raise GraphQLError(
                f"Work order {work_order_id} not found",
                extensions={"code": "NOT_FOUND"},
            )
        self.work_orders.delete(wo)
        return True

    # ---- WorkOrderOp CRUD ----
    def add_work_order_op(self, data: WorkOrderOpInput) -> WorkOrderOp:
        if not self.work_orders.get(data.work_order_id):
            raise GraphQLError(
                f"Work order {data.work_order_id} not found",
                extensions={"code": "NOT_FOUND"},
            )
        if data.work_center_id is not None and not self.work_centers.get(data.work_center_id):
            raise GraphQLError(
                f"Work center {data.work_center_id} not found",
                extensions={"code": "NOT_FOUND"},
            )
        try:
            started_at = datetime.fromisoformat(data.started_at) if data.started_at else None
            completed_at = datetime.fromisoformat(data.completed_at) if data.completed_at else None
        except ValueError as e:
            raise GraphQLError(
                f"Invalid datetime format: {e}", extensions={"code": "BAD_USER_INPUT"}
            )
        return self.work_order_ops.create(
            WorkOrderOp(
                work_order_id=data.work_order_id,
                sequence=data.sequence,
                work_center_id=data.work_center_id,
                status=data.status,
                started_at=started_at,
                completed_at=completed_at,
            )
        )

    def update_work_order_op(self, op_id: int, data: WorkOrderOpInput) -> WorkOrderOp:
        op = self.work_order_ops.get(op_id)
        if not op:
            raise GraphQLError(
                f"Work order op {op_id} not found", extensions={"code": "NOT_FOUND"}
            )
        if data.work_center_id is not None and not self.work_centers.get(data.work_center_id):
            raise GraphQLError(
                f"Work center {data.work_center_id} not found",
                extensions={"code": "NOT_FOUND"},
            )
        try:
            started_at = datetime.fromisoformat(data.started_at) if data.started_at else None
            completed_at = datetime.fromisoformat(data.completed_at) if data.completed_at else None
        except ValueError as e:
            raise GraphQLError(
                f"Invalid datetime format: {e}", extensions={"code": "BAD_USER_INPUT"}
            )
        op.sequence = data.sequence
        op.work_center_id = data.work_center_id
        op.status = data.status
        op.started_at = started_at
        op.completed_at = completed_at
        self.db.commit()
        self.db.refresh(op)
        return op

    def delete_work_order_op(self, op_id: int) -> bool:
        op = self.work_order_ops.get(op_id)
        if not op:
            raise GraphQLError(
                f"Work order op {op_id} not found", extensions={"code": "NOT_FOUND"}
            )
        self.work_order_ops.delete(op)
        return True

    # ---- Routing CRUD ----
    def add_routing(self, data: RoutingInput) -> Routing:
        if not self.parts.get(data.part_id):
            raise GraphQLError(
                f"Part {data.part_id} not found", extensions={"code": "NOT_FOUND"}
            )
        return self.routings.create(
            Routing(name=data.name, part_id=data.part_id, version=data.version)
        )

    def update_routing(self, routing_id: int, data: RoutingInput) -> Routing:
        routing = self.routings.get(routing_id)
        if not routing:
            raise GraphQLError(
                f"Routing {routing_id} not found", extensions={"code": "NOT_FOUND"}
            )
        if not self.parts.get(data.part_id):
            raise GraphQLError(
                f"Part {data.part_id} not found", extensions={"code": "NOT_FOUND"}
            )
        routing.name = data.name
        routing.part_id = data.part_id
        routing.version = data.version
        self.db.commit()
        self.db.refresh(routing)
        return routing

    def delete_routing(self, routing_id: int) -> bool:
        routing = self.routings.get(routing_id)
        if not routing:
            raise GraphQLError(
                f"Routing {routing_id} not found", extensions={"code": "NOT_FOUND"}
            )
        self.routings.delete(routing)
        return True

    # ---- RoutingStep CRUD ----
    def add_routing_step(self, data: RoutingStepInput) -> RoutingStep:
        if not self.routings.get(data.routing_id):
            raise GraphQLError(
                f"Routing {data.routing_id} not found", extensions={"code": "NOT_FOUND"}
            )
        if data.work_center_id is not None and not self.work_centers.get(data.work_center_id):
            raise GraphQLError(
                f"Work center {data.work_center_id} not found",
                extensions={"code": "NOT_FOUND"},
            )
        return self.routing_steps.create(
            RoutingStep(
                routing_id=data.routing_id,
                sequence=data.sequence,
                work_center_id=data.work_center_id,
                description=data.description,
                standard_minutes=data.standard_minutes,
            )
        )

    def update_routing_step(self, step_id: int, data: RoutingStepInput) -> RoutingStep:
        step = self.routing_steps.get(step_id)
        if not step:
            raise GraphQLError(
                f"Routing step {step_id} not found", extensions={"code": "NOT_FOUND"}
            )
        if data.work_center_id is not None and not self.work_centers.get(data.work_center_id):
            raise GraphQLError(
                f"Work center {data.work_center_id} not found",
                extensions={"code": "NOT_FOUND"},
            )
        step.sequence = data.sequence
        step.work_center_id = data.work_center_id
        step.description = data.description
        step.standard_minutes = data.standard_minutes
        self.db.commit()
        self.db.refresh(step)
        return step

    def delete_routing_step(self, step_id: int) -> bool:
        step = self.routing_steps.get(step_id)
        if not step:
            raise GraphQLError(
                f"Routing step {step_id} not found", extensions={"code": "NOT_FOUND"}
            )
        self.routing_steps.delete(step)
        return True

    # ---- BOM CRUD ----
    def add_bom(self, data: BOMInput) -> BOM:
        if not self.parts.get(data.part_id):
            raise GraphQLError(
                f"Part {data.part_id} not found", extensions={"code": "NOT_FOUND"}
            )
        return self.boms.create(BOM(part_id=data.part_id, revision=data.revision))

    def update_bom(self, bom_id: int, data: BOMInput) -> BOM:
        bom = self.boms.get(bom_id)
        if not bom:
            raise GraphQLError(
                f"BOM {bom_id} not found", extensions={"code": "NOT_FOUND"}
            )
        if not self.parts.get(data.part_id):
            raise GraphQLError(
                f"Part {data.part_id} not found", extensions={"code": "NOT_FOUND"}
            )
        bom.part_id = data.part_id
        bom.revision = data.revision
        self.db.commit()
        self.db.refresh(bom)
        return bom

    def delete_bom(self, bom_id: int) -> bool:
        bom = self.boms.get(bom_id)
        if not bom:
            raise GraphQLError(
                f"BOM {bom_id} not found", extensions={"code": "NOT_FOUND"}
            )
        self.boms.delete(bom)
        return True

    # ---- BOMItem CRUD ----
    def add_bom_item(self, data: BOMItemInput) -> BOMItem:
        if not self.boms.get(data.bom_id):
            raise GraphQLError(
                f"BOM {data.bom_id} not found", extensions={"code": "NOT_FOUND"}
            )
        if not self.parts.get(data.component_part_id):
            raise GraphQLError(
                f"Part {data.component_part_id} not found",
                extensions={"code": "NOT_FOUND"},
            )
        return self.bom_items.create(
            BOMItem(
                bom_id=data.bom_id,
                component_part_id=data.component_part_id,
                quantity=data.quantity,
            )
        )

    def update_bom_item(self, item_id: int, data: BOMItemInput) -> BOMItem:
        item = self.bom_items.get(item_id)
        if not item:
            raise GraphQLError(
                f"BOM item {item_id} not found", extensions={"code": "NOT_FOUND"}
            )
        if not self.parts.get(data.component_part_id):
            raise GraphQLError(
                f"Part {data.component_part_id} not found",
                extensions={"code": "NOT_FOUND"},
            )
        item.component_part_id = data.component_part_id
        item.quantity = data.quantity
        self.db.commit()
        self.db.refresh(item)
        return item

    def delete_bom_item(self, item_id: int) -> bool:
        item = self.bom_items.get(item_id)
        if not item:
            raise GraphQLError(
                f"BOM item {item_id} not found", extensions={"code": "NOT_FOUND"}
            )
        self.bom_items.delete(item)
        return True

    # ---- ActivityLog (append-only) ----
    def add_activity_log(self, data: ActivityLogInput) -> ActivityLog:
        return self.activity_logs.create(
            ActivityLog(
                user_id=data.user_id,
                part_id=data.part_id,
                department_id=data.department_id,
                work_order_id=data.work_order_id,
                event_type=data.event_type,
                message=data.message,
            )
        )


class QueryService:
    def __init__(self, db: Session):
        self.db = db
        self.users = UserRepo(db)
        self.departments = DepartmentRepo(db)
        self.parts = PartRepo(db)
        self.defect_categories = DefectCategoryRepo(db)
        self.defects = DefectRepo(db)
        self.qualities = QualityRepo(db)
        self.work_centers = WorkCenterRepo(db)
        self.work_orders = WorkOrderRepo(db)
        self.work_order_ops = WorkOrderOpRepo(db)
        self.routings = RoutingRepo(db)
        self.routing_steps = RoutingStepRepo(db)
        self.boms = BOMRepo(db)
        self.bom_items = BOMItemRepo(db)
        self.activity_logs = ActivityLogRepo(db)
        self.floors = FloorRepo(db)
        self.floor_zones = FloorZoneRepo(db)

    # ---- Users ----
    def get_all_users(
        self, limit: int | None = None, offset: int | None = None
    ) -> list[User]:
        return self.users.list(limit=limit, offset=offset)

    def get_user(self, user_id: int) -> User:
        user = self.users.get(user_id)
        if not user:
            raise GraphQLError(
                f"User {user_id} not found", extensions={"code": "NOT_FOUND"}
            )
        return user

    # ---- Departments ----
    def get_all_departments(
        self, limit: int | None = None, offset: int | None = None
    ) -> list[Department]:
        return self.departments.list(limit=limit, offset=offset)

    def get_department(self, department_id: int) -> Department:
        department = self.departments.get(department_id)
        if not department:
            raise GraphQLError(
                f"Department {department_id} not found",
                extensions={"code": "NOT_FOUND"},
            )
        return department

    def get_department_by_title(self, title: str) -> Department:
        department = self.departments.by_title(title)
        if not department:
            raise GraphQLError(
                f"Department {title} not found", extensions={"code": "NOT_FOUND"}
            )
        return department

    # ---- Parts ----
    def get_all_parts(
        self, limit: int | None = None, offset: int | None = None
    ) -> list[Part]:
        return self.parts.list(limit=limit, offset=offset)

    def get_part(self, part_id: int) -> Part:
        part = self.parts.get(part_id)
        if not part:
            raise GraphQLError(
                f"Part {part_id} not found", extensions={"code": "NOT_FOUND"}
            )
        return part

    # ---- DefectCategories ----
    def get_all_defect_categories(
        self, limit: int | None = None, offset: int | None = None
    ) -> list[DefectCategory]:
        return self.defect_categories.list(limit=limit, offset=offset)

    def get_defect_category(self, defect_category_id: int) -> DefectCategory:
        dc = self.defect_categories.get(defect_category_id)
        if not dc:
            raise GraphQLError(
                f"Defect category {defect_category_id} not found",
                extensions={"code": "NOT_FOUND"},
            )
        return dc

    # ---- Defects ----
    def get_all_defects(
        self, limit: int | None = None, offset: int | None = None
    ) -> list[Defect]:
        return self.defects.list(limit=limit, offset=offset)

    def get_defect(self, defect_id: int) -> Defect:
        defect = self.defects.get(defect_id)
        if not defect:
            raise GraphQLError(
                f"Defect {defect_id} not found", extensions={"code": "NOT_FOUND"}
            )
        return defect

    def get_defect_by_part_id(self, part_id: int) -> Defect:
        defect = self.defects.first_by_part(part_id)
        if not defect:
            raise GraphQLError(
                f"Defect for part {part_id} not found",
                extensions={"code": "NOT_FOUND"},
            )
        return defect

    def get_defect_by_defect_category_id(self, defect_category_id: int) -> Defect:
        defect = self.defects.first_by_defect_category(defect_category_id)
        if not defect:
            raise GraphQLError(
                f"Defect for defect category {defect_category_id} not found",
                extensions={"code": "NOT_FOUND"},
            )
        return defect

    def get_defect_by_part_id_and_defect_category_id(
        self, part_id: int, defect_category_id: int
    ) -> Defect:
        defect = self.defects.first_by_part_and_defect_category(part_id, defect_category_id)
        if not defect:
            raise GraphQLError(
                f"Defect for part {part_id} and defect category {defect_category_id} not found",
                extensions={"code": "NOT_FOUND"},
            )
        return defect

    def get_defect_by_part_id_and_department_id(
        self, part_id: int, department_id: int
    ) -> Defect:
        defect = self.defects.first_by_part_and_department(part_id, department_id)
        if not defect:
            raise GraphQLError(
                f"Defect for part {part_id} and department {department_id} not found",
                extensions={"code": "NOT_FOUND"},
            )
        return defect

    # ---- Qualities ----
    def get_all_qualities(
        self, limit: int | None = None, offset: int | None = None
    ) -> list[Quality]:
        return self.qualities.list(limit=limit, offset=offset)

    def get_quality(self, quality_id: int) -> Quality:
        quality = self.qualities.get(quality_id)
        if not quality:
            raise GraphQLError(
                f"Quality {quality_id} not found", extensions={"code": "NOT_FOUND"}
            )
        return quality

    def get_quality_by_part_id(self, part_id: int) -> Quality:
        quality = self.qualities.first_by_part(part_id)
        if not quality:
            raise GraphQLError(
                f"Quality for part {part_id} not found",
                extensions={"code": "NOT_FOUND"},
            )
        return quality

    # ---- WorkCenters ----
    def get_all_work_centers(
        self, limit: int | None = None, offset: int | None = None
    ) -> list[WorkCenter]:
        return self.work_centers.list(limit=limit, offset=offset)

    def get_work_center(self, work_center_id: int) -> WorkCenter:
        wc = self.work_centers.get(work_center_id)
        if not wc:
            raise GraphQLError(
                f"Work center {work_center_id} not found",
                extensions={"code": "NOT_FOUND"},
            )
        return wc

    # ---- WorkOrders ----
    def get_all_work_orders(
        self, limit: int | None = None, offset: int | None = None
    ) -> list[WorkOrder]:
        return self.work_orders.list(limit=limit, offset=offset)

    def get_work_order(self, work_order_id: int) -> WorkOrder:
        wo = self.work_orders.get(work_order_id)
        if not wo:
            raise GraphQLError(
                f"Work order {work_order_id} not found",
                extensions={"code": "NOT_FOUND"},
            )
        return wo

    # ---- WorkOrderOps ----
    def get_all_work_order_ops(
        self, limit: int | None = None, offset: int | None = None
    ) -> list[WorkOrderOp]:
        return self.work_order_ops.list(limit=limit, offset=offset)

    def get_work_order_op(self, op_id: int) -> WorkOrderOp:
        op = self.work_order_ops.get(op_id)
        if not op:
            raise GraphQLError(
                f"Work order op {op_id} not found", extensions={"code": "NOT_FOUND"}
            )
        return op

    def get_work_order_ops_by_work_order(self, work_order_id: int) -> list[WorkOrderOp]:
        return self.work_order_ops.list_by_work_order(work_order_id)

    # ---- Routings ----
    def get_all_routings(
        self, limit: int | None = None, offset: int | None = None
    ) -> list[Routing]:
        return self.routings.list(limit=limit, offset=offset)

    def get_routing(self, routing_id: int) -> Routing:
        r = self.routings.get(routing_id)
        if not r:
            raise GraphQLError(
                f"Routing {routing_id} not found", extensions={"code": "NOT_FOUND"}
            )
        return r

    # ---- RoutingSteps ----
    def get_all_routing_steps(
        self, limit: int | None = None, offset: int | None = None
    ) -> list[RoutingStep]:
        return self.routing_steps.list(limit=limit, offset=offset)

    def get_routing_step(self, step_id: int) -> RoutingStep:
        step = self.routing_steps.get(step_id)
        if not step:
            raise GraphQLError(
                f"Routing step {step_id} not found", extensions={"code": "NOT_FOUND"}
            )
        return step

    def get_routing_steps_by_routing(self, routing_id: int) -> list[RoutingStep]:
        return self.routing_steps.list_by_routing(routing_id)

    # ---- BOMs ----
    def get_all_boms(
        self, limit: int | None = None, offset: int | None = None
    ) -> list[BOM]:
        return self.boms.list(limit=limit, offset=offset)

    def get_bom(self, bom_id: int) -> BOM:
        b = self.boms.get(bom_id)
        if not b:
            raise GraphQLError(
                f"BOM {bom_id} not found", extensions={"code": "NOT_FOUND"}
            )
        return b

    # ---- BOMItems ----
    def get_all_bom_items(
        self, limit: int | None = None, offset: int | None = None
    ) -> list[BOMItem]:
        return self.bom_items.list(limit=limit, offset=offset)

    def get_bom_item(self, item_id: int) -> BOMItem:
        item = self.bom_items.get(item_id)
        if not item:
            raise GraphQLError(
                f"BOM item {item_id} not found", extensions={"code": "NOT_FOUND"}
            )
        return item

    def get_bom_items_by_bom(self, bom_id: int) -> list[BOMItem]:
        return self.bom_items.list_by_bom(bom_id)

    # ---- ActivityLogs ----
    def get_all_activity_logs(
        self, limit: int | None = None, offset: int | None = None
    ) -> list[ActivityLog]:
        return self.activity_logs.list(limit=limit, offset=offset)

    def get_activity_logs_for_work_order(self, work_order_id: int) -> list[ActivityLog]:
        return self.activity_logs.list_by_work_order(work_order_id)

    # ---- Floors ----
    def get_all_floors(
        self, limit: int | None = None, offset: int | None = None
    ) -> list[Floor]:
        return self.floors.list(limit=limit, offset=offset)

    def get_floor(self, floor_id: int) -> Floor:
        floor = self.floors.get(floor_id)
        if not floor:
            raise GraphQLError(
                f"Floor {floor_id} not found", extensions={"code": "NOT_FOUND"}
            )
        return floor

    # ---- FloorZones ----
    def get_all_floor_zones(
        self, limit: int | None = None, offset: int | None = None
    ) -> list[FloorZone]:
        return self.floor_zones.list(limit=limit, offset=offset)

    def get_floor_zones_by_floor(self, floor_id: int) -> list[FloorZone]:
        return self.floor_zones.list_by_floor(floor_id)
