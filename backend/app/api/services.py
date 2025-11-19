from __future__ import annotations

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
class FloorRepo:
    def __init__(self, db: Session):
        self.db = db

    def list(self, limit: int | None = None, offset: int | None = None) -> list[Floor]:
        l, o = _coerce_pagination(limit, offset)
        return self.db.query(Floor).offset(o).limit(l).all()

    def get(self, floor_id: int) -> Floor | None:
        return self.db.get(Floor, floor_id)

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
        l, o = _coerce_pagination(limit, offset)
        return self.db.query(FloorZone).offset(o).limit(l).all()

    def list_by_floor(self, floor_id: int) -> list[FloorZone]:
        return (
            self.db.query(FloorZone)
            .filter(FloorZone.floor_id == floor_id)
            .all()
        )

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

# --- Pagination helper ---
DEFAULT_LIMIT = 50
MAX_LIMIT = 200


def _coerce_pagination(limit: int | None, offset: int | None) -> tuple[int, int]:
    """Clamp and sanitize limit/offset."""
    l = DEFAULT_LIMIT if (limit is None or limit <= 0) else min(limit, MAX_LIMIT)
    o = 0 if (offset is None or offset < 0) else offset
    return l, o


# --- Repository layer (low-level DB access; no business logic) ---
class UserRepo:
    def __init__(self, db: Session):
        self.db = db

    def by_username(self, username: str) -> User | None:
        return self.db.query(User).filter(User.username == username).first()

    def list(self, limit: int | None = None, offset: int | None = None) -> list[User]:
        l, o = _coerce_pagination(limit, offset)
        return self.db.query(User).offset(o).limit(l).all()

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

    def list(
        self, limit: int | None = None, offset: int | None = None
    ) -> list[Department]:
        l, o = _coerce_pagination(limit, offset)
        return self.db.query(Department).offset(o).limit(l).all()

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
        l, o = _coerce_pagination(limit, offset)
        return self.db.query(Part).offset(o).limit(l).all()

    def get(self, part_id: int) -> Part | None:
        return self.db.get(Part, part_id)

    def create(self, part: Part) -> Part:
        self.db.add(part)
        self.db.commit()
        self.db.refresh(part)
        return part


class DefectCategoryRepo:
    def __init__(self, db: Session):
        self.db = db

    def list(
        self, limit: int | None = None, offset: int | None = None
    ) -> list[DefectCategory]:
        l, o = _coerce_pagination(limit, offset)
        return self.db.query(DefectCategory).offset(o).limit(l).all()

    def get(self, defect_category_id: int) -> DefectCategory | None:
        return self.db.get(DefectCategory, defect_category_id)

    def create(self, dc: DefectCategory) -> DefectCategory:
        self.db.add(dc)
        self.db.commit()
        self.db.refresh(dc)
        return dc


class DefectRepo:
    def __init__(self, db: Session):
        self.db = db

    def list(self, limit: int | None = None, offset: int | None = None) -> list[Defect]:
        l, o = _coerce_pagination(limit, offset)
        return self.db.query(Defect).offset(o).limit(l).all()

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

    def first_by_part_and_department(self, part_id: int, department_id: int) -> Defect | None:
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


class QualityRepo:
    def __init__(self, db: Session):
        self.db = db

    def list(
        self, limit: int | None = None, offset: int | None = None
    ) -> list[Quality]:
        l, o = _coerce_pagination(limit, offset)
        return self.db.query(Quality).offset(o).limit(l).all()

    def get(self, quality_id: int) -> Quality | None:
        return self.db.get(Quality, quality_id)

    def first_by_part(self, part_id: int) -> Quality | None:
        return self.db.query(Quality).filter(Quality.part_id == part_id).first()

    def create(self, quality: Quality) -> Quality:
        self.db.add(quality)
        self.db.commit()
        self.db.refresh(quality)
        return quality


class WorkCenterRepo:
    def __init__(self, db: Session):
        self.db = db

    def list(self, limit: int | None = None, offset: int | None = None) -> list[WorkCenter]:
        l, o = _coerce_pagination(limit, offset)
        return self.db.query(WorkCenter).offset(o).limit(l).all()

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

    def list(self, limit: int | None = None, offset: int | None = None) -> list[WorkOrder]:
        l, o = _coerce_pagination(limit, offset)
        return self.db.query(WorkOrder).offset(o).limit(l).all()

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
        l, o = _coerce_pagination(limit, offset)
        return self.db.query(WorkOrderOp).offset(o).limit(l).all()

    def list_by_work_order(self, work_order_id: int) -> list[WorkOrderOp]:
        return (
            self.db.query(WorkOrderOp)
            .filter(WorkOrderOp.work_order_id == work_order_id)
            .order_by(WorkOrderOp.sequence)
            .all()
        )

    def create(self, op: WorkOrderOp) -> WorkOrderOp:
        self.db.add(op)
        self.db.commit()
        self.db.refresh(op)
        return op


class RoutingRepo:
    def __init__(self, db: Session):
        self.db = db

    def list(self, limit: int | None = None, offset: int | None = None) -> list[Routing]:
        l, o = _coerce_pagination(limit, offset)
        return self.db.query(Routing).offset(o).limit(l).all()

    def get(self, routing_id: int) -> Routing | None:
        return self.db.get(Routing, routing_id)

    def create(self, routing: Routing) -> Routing:
        self.db.add(routing)
        self.db.commit()
        self.db.refresh(routing)
        return routing


class RoutingStepRepo:
    def __init__(self, db: Session):
        self.db = db

    def list(self, limit: int | None = None, offset: int | None = None) -> list[RoutingStep]:
        l, o = _coerce_pagination(limit, offset)
        return self.db.query(RoutingStep).offset(o).limit(l).all()

    def list_by_routing(self, routing_id: int) -> list[RoutingStep]:
        return (
            self.db.query(RoutingStep)
            .filter(RoutingStep.routing_id == routing_id)
            .order_by(RoutingStep.sequence)
            .all()
        )

    def create(self, step: RoutingStep) -> RoutingStep:
        self.db.add(step)
        self.db.commit()
        self.db.refresh(step)
        return step


class BOMRepo:
    def __init__(self, db: Session):
        self.db = db

    def list(self, limit: int | None = None, offset: int | None = None) -> list[BOM]:
        l, o = _coerce_pagination(limit, offset)
        return self.db.query(BOM).offset(o).limit(l).all()

    def get(self, bom_id: int) -> BOM | None:
        return self.db.get(BOM, bom_id)

    def create(self, bom: BOM) -> BOM:
        self.db.add(bom)
        self.db.commit()
        self.db.refresh(bom)
        return bom


class BOMItemRepo:
    def __init__(self, db: Session):
        self.db = db

    def list(self, limit: int | None = None, offset: int | None = None) -> list[BOMItem]:
        l, o = _coerce_pagination(limit, offset)
        return self.db.query(BOMItem).offset(o).limit(l).all()

    def list_by_bom(self, bom_id: int) -> list[BOMItem]:
        return self.db.query(BOMItem).filter(BOMItem.bom_id == bom_id).all()

    def create(self, item: BOMItem) -> BOMItem:
        self.db.add(item)
        self.db.commit()
        self.db.refresh(item)
        return item


class ActivityLogRepo:
    def __init__(self, db: Session):
        self.db = db

    def list(self, limit: int | None = None, offset: int | None = None) -> list[ActivityLog]:
        l, o = _coerce_pagination(limit, offset)
        return self.db.query(ActivityLog).offset(o).limit(l).all()

    def create(self, log: ActivityLog) -> ActivityLog:
        self.db.add(log)
        self.db.commit()
        self.db.refresh(log)
        return log


class MutationService:

    # ---- Floor: CRUD for shop-floor layouts ----
    def add_floor(self, data: FloorInput) -> Floor:
        existing = (
            self.db.query(Floor)
            .filter(Floor.name == data.name)
            .first()
        )
        if existing:
            raise GraphQLError(
                "Floor already exists; check name.",
                extensions={"code": "CONFLICT"},
            )

        floor = Floor(
            name=data.name,
            description=data.description,
        )
        self.db.add(floor)
        self.db.commit()
        self.db.refresh(floor)
        return floor

    def update_floor(self, floor_id: int, data: FloorInput) -> Floor:
        floor = self.db.get(Floor, floor_id)
        if not floor:
            raise GraphQLError(
                f"Floor {floor_id} not found",
                extensions={"code": "NOT_FOUND"},
            )

        if data.name and data.name != floor.name:
            exists = (
                self.db.query(Floor)
                .filter(Floor.name == data.name)
                .first()
            )
            if exists:
                raise GraphQLError(
                    "Floor already exists; check name.",
                    extensions={"code": "CONFLICT"},
                )

        floor.name = data.name
        floor.description = data.description
        self.db.commit()
        self.db.refresh(floor)
        return floor

    def delete_floor(self, floor_id: int) -> bool:
        floor = self.db.get(Floor, floor_id)
        if not floor:
            raise GraphQLError(
                f"Floor {floor_id} not found",
                extensions={"code": "NOT_FOUND"},
            )
        self.db.delete(floor)
        self.db.commit()
        return True

    # ---- Floor Zones: CRUD for interactive SVG regions ----
    def add_floor_zone(self, data: FloorZoneInput) -> FloorZone:
        floor = self.db.get(Floor, data.floor_id)
        if not floor:
            raise GraphQLError(
                f"Floor {data.floor_id} not found",
                extensions={"code": "NOT_FOUND"},
            )

        if data.department_id is not None:
            dept = self.db.get(Department, data.department_id)
            if not dept:
                raise GraphQLError(
                    f"Department {data.department_id} not found",
                    extensions={"code": "NOT_FOUND"},
                )

        if data.work_center_id is not None:
            wc = self.db.get(WorkCenter, data.work_center_id)
            if not wc:
                raise GraphQLError(
                    f"Work center {data.work_center_id} not found",
                    extensions={"code": "NOT_FOUND"},
                )

        zone = FloorZone(
            floor_id=data.floor_id,
            name=data.name,
            zone_type=data.zone_type,
            department_id=data.department_id,
            work_center_id=data.work_center_id,
            polygon=data.polygon,
        )
        self.db.add(zone)
        self.db.commit()
        self.db.refresh(zone)
        return zone

    def update_floor_zone(self, zone_id: int, data: FloorZoneInput) -> FloorZone:
        zone = self.db.get(FloorZone, zone_id)
        if not zone:
            raise GraphQLError(
                f"Floor zone {zone_id} not found",
                extensions={"code": "NOT_FOUND"},
            )

        if data.floor_id != zone.floor_id:
            floor = self.db.get(Floor, data.floor_id)
            if not floor:
                raise GraphQLError(
                    f"Floor {data.floor_id} not found",
                    extensions={"code": "NOT_FOUND"},
                )
            zone.floor_id = data.floor_id

        if data.department_id is not None:
            dept = self.db.get(Department, data.department_id)
            if not dept:
                raise GraphQLError(
                    f"Department {data.department_id} not found",
                    extensions={"code": "NOT_FOUND"},
                )
            zone.department_id = data.department_id
        else:
            zone.department_id = None

        if data.work_center_id is not None:
            wc = self.db.get(WorkCenter, data.work_center_id)
            if not wc:
                raise GraphQLError(
                    f"Work center {data.work_center_id} not found",
                    extensions={"code": "NOT_FOUND"},
                )
            zone.work_center_id = data.work_center_id
        else:
            zone.work_center_id = None

        zone.name = data.name
        zone.zone_type = data.zone_type
        zone.polygon = data.polygon
        self.db.commit()
        self.db.refresh(zone)
        return zone

    def delete_floor_zone(self, zone_id: int) -> bool:
        zone = self.db.get(FloorZone, zone_id)
        if not zone:
            raise GraphQLError(
                f"Floor zone {zone_id} not found",
                extensions={"code": "NOT_FOUND"},
            )
        self.db.delete(zone)
        self.db.commit()
        return True
    def __init__(self, db: Session):
        self.db = db

    def add_user(self, user_data: UserInput) -> User:
        existing_user = (
            self.db.query(User).filter(User.username == user_data.username).first()
        )
        if existing_user:
            raise GraphQLError("User already exists; check username.", extensions={"code": "CONFLICT"})

        user = User(
            username=user_data.username,
            department_id=user_data.department_id,
            job=user_data.job,
            time=user_data.time,
        )
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user

    def add_department(self, department_data: DepartmentInput) -> Department:
        existing_department = (
            self.db.query(Department)
            .filter(Department.title == department_data.title)
            .first()
        )
        if existing_department:
            raise GraphQLError("Department already exists; check title.", extensions={"code": "CONFLICT"})

        department = Department(
            title=department_data.title,
            description=department_data.description,
        )
        self.db.add(department)
        self.db.commit()
        self.db.refresh(department)
        return department

    def update_department(
        self, department_id: int, data: DepartmentInput
    ) -> Department:
        department = self.db.get(Department, department_id)
        if not department:
            raise GraphQLError(f"Department {department_id} not found", extensions={"code": "NOT_FOUND"})
        department.title = data.title
        department.description = data.description
        self.db.commit()
        self.db.refresh(department)
        return department

    def delete_department(self, department_id: int) -> bool:
        department = self.db.get(Department, department_id)
        if not department:
            raise GraphQLError(f"Department {department_id} not found", extensions={"code": "NOT_FOUND"})
        self.db.delete(department)
        self.db.commit()
        return True

    def add_part(self, part_data: PartInput) -> Part:
        part = Part(
            name=part_data.name,
            department_id=part_data.department_id,
        )
        self.db.add(part)
        self.db.commit()
        self.db.refresh(part)
        return part

    def add_defect_category(self, def_cat_data: DefectCategoryInput) -> DefectCategory:
        # Validate department exists to avoid raw FK errors
        department_id = def_cat_data.department_id
        if department_id is not None:
            dept = self.db.get(Department, department_id)
            if not dept:
                raise GraphQLError(
                    f"Department {department_id} not found",
                    extensions={"code": "NOT_FOUND"},
                )

        defect_category = DefectCategory(
            title=def_cat_data.title,
            department_id=department_id,
        )
        self.db.add(defect_category)
        self.db.commit()
        self.db.refresh(defect_category)
        return defect_category

    def add_defect(self, defect_data: DefectInput) -> Defect:
        defect = Defect(
            title=defect_data.title,
            description=defect_data.description,
            part_id=defect_data.part_id,
            defect_category_id=defect_data.defect_category_id,
        )
        self.db.add(defect)
        self.db.commit()
        self.db.refresh(defect)
        return defect

    def add_quality(self, quality_data: QualityInput) -> Quality:
        quality = Quality(
            pass_fail=quality_data.pass_fail,
            defect_count=quality_data.defect_count,
            part_id=quality_data.part_id,
        )
        self.db.add(quality)
        self.db.commit()
        self.db.refresh(quality)
        return quality

    # ---- User: update & delete ----
    def update_user(self, user_id: int, data: UserInput) -> User:
        user = self.db.get(User, user_id)
        if not user:
            raise GraphQLError(f"User {user_id} not found", extensions={"code": "NOT_FOUND"})
        # Optional uniqueness check if username changed
        if data.username and data.username != user.username:
            exists = self.db.query(User).filter(User.username == data.username).first()
            if exists:
                raise GraphQLError("User already exists; check username.", extensions={"code": "CONFLICT"})
            user.username = data.username
        user.department_id = data.department_id
        user.job = data.job
        user.time = data.time
        self.db.commit()
        self.db.refresh(user)
        return user

    def delete_user(self, user_id: int) -> bool:
        user = self.db.get(User, user_id)
        if not user:
            raise GraphQLError(f"User {user_id} not found", extensions={"code": "NOT_FOUND"})
        self.db.delete(user)
        self.db.commit()
        return True

    # ---- Part: update & delete ----
    def update_part(self, part_id: int, data: PartInput) -> Part:
        part = self.db.get(Part, part_id)
        if not part:
            raise GraphQLError(f"Part {part_id} not found", extensions={"code": "NOT_FOUND"})
        part.name = data.name
        part.department_id = data.department_id
        self.db.commit()
        self.db.refresh(part)
        return part

    def delete_part(self, part_id: int) -> bool:
        part = self.db.get(Part, part_id)
        if not part:
            raise GraphQLError(f"Part {part_id} not found", extensions={"code": "NOT_FOUND"})
        self.db.delete(part)
        self.db.commit()
        return True

    # ---- DefectCategory: update & delete ----
    def update_defect_category(
        self, defect_category_id: int, data: DefectCategoryInput
    ) -> DefectCategory:
        dc = self.db.get(DefectCategory, defect_category_id)
        if not dc:
            raise GraphQLError(f"Defect category {defect_category_id} not found", extensions={"code": "NOT_FOUND"})
        # Optional uniqueness check if title changed
        if data.title and data.title != dc.title:
            exists = (
                self.db.query(DefectCategory)
                .filter(DefectCategory.title == data.title)
                .first()
            )
            if exists:
                raise GraphQLError("Defect category already exists; check title.", extensions={"code": "CONFLICT"})
            dc.title = data.title
        dc.department_id = data.department_id
        self.db.commit()
        self.db.refresh(dc)
        return dc

    def delete_defect_category(self, defect_category_id: int) -> bool:
        dc = self.db.get(DefectCategory, defect_category_id)
        if not dc:
            raise GraphQLError(f"Defect category {defect_category_id} not found", extensions={"code": "NOT_FOUND"})
        self.db.delete(dc)
        self.db.commit()
        return True

    # ---- Defect: update & delete ----
    def update_defect(self, defect_id: int, data: DefectInput) -> Defect:
        defect = self.db.get(Defect, defect_id)
        if not defect:
            raise GraphQLError(f"Defect {defect_id} not found", extensions={"code": "NOT_FOUND"})
        defect.title = data.title
        defect.description = data.description
        defect.part_id = data.part_id
        defect.defect_category_id = data.defect_category_id
        self.db.commit()
        self.db.refresh(defect)
        return defect

    def delete_defect(self, defect_id: int) -> bool:
        defect = self.db.get(Defect, defect_id)
        if not defect:
            raise GraphQLError(f"Defect {defect_id} not found", extensions={"code": "NOT_FOUND"})
        self.db.delete(defect)
        self.db.commit()
        return True

    # ---- Quality: update & delete ----
    def update_quality(self, quality_id: int, data: QualityInput) -> Quality:
        quality = self.db.get(Quality, quality_id)
        if not quality:
            raise GraphQLError(f"Quality {quality_id} not found", extensions={"code": "NOT_FOUND"})
        quality.pass_fail = data.pass_fail
        quality.defect_count = data.defect_count
        quality.part_id = data.part_id
        self.db.commit()
        self.db.refresh(quality)
        return quality

    def delete_quality(self, quality_id: int) -> bool:
        quality = self.db.get(Quality, quality_id)
        if not quality:
            raise GraphQLError(f"Quality {quality_id} not found", extensions={"code": "NOT_FOUND"})
        self.db.delete(quality)
        self.db.commit()
        return True
    
    def add_work_center(self, data: WorkCenterInput) -> WorkCenter:
        # Optional uniqueness check on code to avoid DB integrity errors
        if data.code:
            existing = (
                self.db.query(WorkCenter)
                .filter(WorkCenter.code == data.code)
                .first()
            )
            if existing:
                raise GraphQLError(
                    "Work center code already exists; check code.",
                    extensions={"code": "CONFLICT"},
                )

        # Validate department if provided to avoid raw FK errors
        department_id = data.department_id
        if department_id is not None:
            dept = self.db.get(Department, department_id)
            if not dept:
                raise GraphQLError(
                    f"Department {department_id} not found",
                    extensions={"code": "NOT_FOUND"},
                )

        wc = WorkCenter(
            name=data.name,
            code=data.code,
            department_id=department_id,
        )
        self.db.add(wc)
        self.db.commit()
        self.db.refresh(wc)
        return wc

    def add_work_order(self, data: WorkOrderInput) -> WorkOrder:
        # Enforce unique work order number at the service layer
        existing = (
            self.db.query(WorkOrder)
            .filter(WorkOrder.number == data.number)
            .first()
        )
        if existing:
            raise GraphQLError(
                "Work order already exists; check number.",
                extensions={"code": "CONFLICT"},
            )

        part = self.db.get(Part, data.part_id)
        if not part:
            raise GraphQLError(
                f"Part {data.part_id} not found",
                extensions={"code": "NOT_FOUND"},
            )

        # Default department to the part's department if not explicitly provided
        department_id = (
            data.department_id
            if data.department_id is not None
            else part.department_id
        )

        work_center_id = data.work_center_id
        if work_center_id is not None:
            wc = self.db.get(WorkCenter, work_center_id)
            if not wc:
                raise GraphQLError(
                    f"Work center {work_center_id} not found",
                    extensions={"code": "NOT_FOUND"},
                )

        wo = WorkOrder(
            number=data.number,
            status=data.status,
            quantity=data.quantity,
            part_id=data.part_id,
            department_id=department_id,
            work_center_id=work_center_id,
        )
        self.db.add(wo)
        self.db.commit()
        self.db.refresh(wo)
        return wo

    def add_work_order_op(self, data: WorkOrderOpInput) -> WorkOrderOp:
        wo = self.db.get(WorkOrder, data.work_order_id)
        if not wo:
            raise GraphQLError(
                f"Work order {data.work_order_id} not found",
                extensions={"code": "NOT_FOUND"},
            )

        work_center_id = data.work_center_id
        if work_center_id is not None:
            wc = self.db.get(WorkCenter, work_center_id)
            if not wc:
                raise GraphQLError(
                    f"Work center {work_center_id} not found",
                    extensions={"code": "NOT_FOUND"},
                )

        op = WorkOrderOp(
            work_order_id=data.work_order_id,
            sequence=data.sequence,
            work_center_id=work_center_id,
            status=data.status,
        )
        self.db.add(op)
        self.db.commit()
        self.db.refresh(op)
        return op

    def add_routing(self, data: RoutingInput) -> Routing:
        part = self.db.get(Part, data.part_id)
        if not part:
            raise GraphQLError(
                f"Part {data.part_id} not found",
                extensions={"code": "NOT_FOUND"},
            )

        routing = Routing(
            name=data.name,
            part_id=data.part_id,
            version=data.version,
        )
        self.db.add(routing)
        self.db.commit()
        self.db.refresh(routing)
        return routing

    def add_routing_step(self, data: RoutingStepInput) -> RoutingStep:
        routing = self.db.get(Routing, data.routing_id)
        if not routing:
            raise GraphQLError(
                f"Routing {data.routing_id} not found",
                extensions={"code": "NOT_FOUND"},
            )

        work_center_id = data.work_center_id
        if work_center_id is not None:
            wc = self.db.get(WorkCenter, work_center_id)
            if not wc:
                raise GraphQLError(
                    f"Work center {work_center_id} not found",
                    extensions={"code": "NOT_FOUND"},
                )

        step = RoutingStep(
            routing_id=data.routing_id,
            sequence=data.sequence,
            work_center_id=work_center_id,
            description=data.description,
            standard_minutes=data.standard_minutes,
        )
        self.db.add(step)
        self.db.commit()
        self.db.refresh(step)
        return step

    def add_bom(self, data: BOMInput) -> BOM:
        part = self.db.get(Part, data.part_id)
        if not part:
            raise GraphQLError(
                f"Part {data.part_id} not found",
                extensions={"code": "NOT_FOUND"},
            )

        bom = BOM(
            part_id=data.part_id,
            revision=data.revision,
        )
        self.db.add(bom)
        self.db.commit()
        self.db.refresh(bom)
        return bom

    def add_bom_item(self, data: BOMItemInput) -> BOMItem:
        bom = self.db.get(BOM, data.bom_id)
        if not bom:
            raise GraphQLError(
                f"BOM {data.bom_id} not found",
                extensions={"code": "NOT_FOUND"},
            )

        component_part = self.db.get(Part, data.component_part_id)
        if not component_part:
            raise GraphQLError(
                f"Part {data.component_part_id} not found",
                extensions={"code": "NOT_FOUND"},
            )

        item = BOMItem(
            bom_id=data.bom_id,
            component_part_id=data.component_part_id,
            quantity=data.quantity,
        )
        self.db.add(item)
        self.db.commit()
        self.db.refresh(item)
        return item

    def add_activity_log(self, data: ActivityLogInput) -> ActivityLog:
        log = ActivityLog(
            user_id=data.user_id,
            part_id=data.part_id,
            department_id=data.department_id,
            work_order_id=data.work_order_id,
            event_type=data.event_type,
            message=data.message,
        )
        self.db.add(log)
        self.db.commit()
        self.db.refresh(log)
        return log



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
            raise GraphQLError(f"User {user_id} not found", extensions={"code": "NOT_FOUND"})
        return user

    # ---- Departments ----
    def get_all_departments(
        self, limit: int | None = None, offset: int | None = None
    ) -> list[Department]:
        return self.departments.list(limit=limit, offset=offset)

    def get_department(self, department_id: int) -> Department:
        department = self.departments.get(department_id)
        if not department:
            raise GraphQLError(f"Department {department_id} not found", extensions={"code": "NOT_FOUND"})
        return department

    def get_department_by_title(self, title: str) -> Department:
        department = self.departments.by_title(title)
        if not department:
            raise GraphQLError(f"Department {title} not found", extensions={"code": "NOT_FOUND"})
        return department

    # ---- Parts ----
    def get_all_parts(
        self, limit: int | None = None, offset: int | None = None
    ) -> list[Part]:
        return self.parts.list(limit=limit, offset=offset)

    def get_part(self, part_id: int) -> Part:
        part = self.parts.get(part_id)
        if not part:
            raise GraphQLError(f"Part {part_id} not found", extensions={"code": "NOT_FOUND"})
        return part

    # ---- Defect Categories ----
    def get_all_defect_categories(
        self, limit: int | None = None, offset: int | None = None
    ) -> list[DefectCategory]:
        return self.defect_categories.list(limit=limit, offset=offset)

    def get_defect_category(self, defect_category_id: int) -> DefectCategory:
        defect_category = self.defect_categories.get(defect_category_id)
        if not defect_category:
            raise GraphQLError(f"Defect category {defect_category_id} not found", extensions={"code": "NOT_FOUND"})
        return defect_category

    # ---- Defects ----
    def get_all_defects(
        self, limit: int | None = None, offset: int | None = None
    ) -> list[Defect]:
        return self.defects.list(limit=limit, offset=offset)

    def get_defect(self, defect_id: int) -> Defect:
        defect = self.defects.get(defect_id)
        if not defect:
            raise GraphQLError(f"Defect {defect_id} not found", extensions={"code": "NOT_FOUND"})
        return defect

    def get_defect_by_part_id(self, part_id: int) -> Defect:
        defect = self.defects.first_by_part(part_id)
        if not defect:
            raise GraphQLError(f"Defect for part {part_id} not found", extensions={"code": "NOT_FOUND"})
        return defect

    def get_defect_by_defect_category_id(self, defect_category_id: int) -> Defect:
        defect = self.defects.first_by_defect_category(defect_category_id)
        if not defect:
            raise GraphQLError(f"Defect for defect category {defect_category_id} not found", extensions={"code": "NOT_FOUND"})
        return defect

    def get_defect_by_part_id_and_defect_category_id(
        self, part_id: int, defect_category_id: int
    ) -> Defect:
        defect = self.defects.first_by_part_and_defect_category(
            part_id, defect_category_id
        )
        if not defect:
            raise GraphQLError(f"Defect for part {part_id} and defect category {defect_category_id} not found", extensions={"code": "NOT_FOUND"})
        return defect

    def get_defect_by_part_id_and_department_id(
        self, part_id: int, department_id: int
    ) -> Defect:
        defect = self.defects.first_by_part_and_department(part_id, department_id)
        if not defect:
            raise GraphQLError(f"Defect for part {part_id} and department {department_id} not found", extensions={"code": "NOT_FOUND"})
        return defect

    # ---- Qualities ----
    def get_all_qualities(
        self, limit: int | None = None, offset: int | None = None
    ) -> list[Quality]:
        return self.qualities.list(limit=limit, offset=offset)

    def get_quality(self, quality_id: int) -> Quality:
        quality = self.qualities.get(quality_id)
        if not quality:
            raise GraphQLError(f"Quality {quality_id} not found", extensions={"code": "NOT_FOUND"})
        return quality

    def get_quality_by_part_id(self, part_id: int) -> Quality:
        quality = self.qualities.first_by_part(part_id)
        if not quality:
            raise GraphQLError(f"Quality for part {part_id} not found", extensions={"code": "NOT_FOUND"})
        return quality

        # ---- Work Centers ----
    def get_all_work_centers(self, limit: int | None = None, offset: int | None = None) -> list[WorkCenter]:
        return self.work_centers.list(limit=limit, offset=offset)

    def get_work_center(self, work_center_id: int) -> WorkCenter:
        wc = self.work_centers.get(work_center_id)
        if not wc:
            raise GraphQLError(f"Work center {work_center_id} not found", extensions={"code": "NOT_FOUND"})
        return wc

    # ---- Work Orders ----
    def get_all_work_orders(self, limit: int | None = None, offset: int | None = None) -> list[WorkOrder]:
        return self.work_orders.list(limit=limit, offset=offset)

    def get_work_order(self, work_order_id: int) -> WorkOrder:
        wo = self.work_orders.get(work_order_id)
        if not wo:
            raise GraphQLError(f"Work order {work_order_id} not found", extensions={"code": "NOT_FOUND"})
        return wo

    # ---- Work Order Ops ----
    def get_all_work_order_ops(self, limit: int | None = None, offset: int | None = None) -> list[WorkOrderOp]:
        return self.work_order_ops.list(limit=limit, offset=offset)

    def get_work_order_ops_by_work_order(self, work_order_id: int) -> list[WorkOrderOp]:
        return self.work_order_ops.list_by_work_order(work_order_id)

    # ---- Routings ----
    def get_all_routings(self, limit: int | None = None, offset: int | None = None) -> list[Routing]:
        return self.routings.list(limit=limit, offset=offset)

    def get_routing(self, routing_id: int) -> Routing:
        r = self.routings.get(routing_id)
        if not r:
            raise GraphQLError(f"Routing {routing_id} not found", extensions={"code": "NOT_FOUND"})
        return r

    # ---- Routing Steps ----
    def get_all_routing_steps(self, limit: int | None = None, offset: int | None = None) -> list[RoutingStep]:
        return self.routing_steps.list(limit=limit, offset=offset)

    def get_routing_steps_by_routing(self, routing_id: int) -> list[RoutingStep]:
        return self.routing_steps.list_by_routing(routing_id)

    # ---- BOMs ----
    def get_all_boms(self, limit: int | None = None, offset: int | None = None) -> list[BOM]:
        return self.boms.list(limit=limit, offset=offset)

    def get_bom(self, bom_id: int) -> BOM:
        b = self.boms.get(bom_id)
        if not b:
            raise GraphQLError(f"BOM {bom_id} not found", extensions={"code": "NOT_FOUND"})
        return b

    # ---- BOM Items ----
    def get_all_bom_items(self, limit: int | None = None, offset: int | None = None) -> list[BOMItem]:
        return self.bom_items.list(limit=limit, offset=offset)

    def get_bom_items_by_bom(self, bom_id: int) -> list[BOMItem]:
        return self.bom_items.list_by_bom(bom_id)

    # ---- Activity Logs ----
    def get_all_activity_logs(self, limit: int | None = None, offset: int | None = None) -> list[ActivityLog]:
        return self.activity_logs.list(limit=limit, offset=offset)
    
    def get_activity_logs_for_work_order(
        self, work_order_id: int
    ) -> list[ActivityLog]:
        logs = self.activity_logs.list(limit=None, offset=None)
        return [log for log in logs if log.work_order_id == work_order_id]

    # ---- Floors & Floor Zones (shop-floor layouts) ----
    def get_all_floors(
        self, limit: int | None = None, offset: int | None = None
    ) -> list[Floor]:
        return self.floors.list(limit=limit, offset=offset)

    def get_floor(self, floor_id: int) -> Floor:
        floor = self.floors.get(floor_id)
        if not floor:
            raise GraphQLError(
                f"Floor {floor_id} not found",
                extensions={"code": "NOT_FOUND"},
            )
        return floor

    def get_all_floor_zones(
        self, limit: int | None = None, offset: int | None = None
    ) -> list[FloorZone]:
        return self.floor_zones.list(limit=limit, offset=offset)

    def get_floor_zones_by_floor(self, floor_id: int) -> list[FloorZone]:
        return self.floor_zones.list_by_floor(floor_id)