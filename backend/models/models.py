from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, DateTime, func
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    username = Column(String(50), unique=True, nullable=False)
    department_id = Column(Integer, ForeignKey("departments.id"))
    job = Column(String(50))
    time = Column(Integer)

    department = relationship("Department", back_populates="users")


class Department(Base):
    __tablename__ = "departments"

    id = Column(Integer, primary_key=True)
    title = Column(String(50), unique=True, nullable=False)
    description = Column(String(255))

    defect_categories = relationship("DefectCategory", back_populates="department")
    users = relationship("User", back_populates="department")
    parts = relationship("Part", back_populates="department")
    work_centers = relationship("WorkCenter", back_populates="department")
    floor_zones = relationship("FloorZone", back_populates="department")


class Part(Base):
    __tablename__ = "parts"

    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)
    department_id = Column(Integer, ForeignKey("departments.id"), index=True)

    defects = relationship("Defect", back_populates="part")
    department = relationship("Department", back_populates="parts")
    quality_records = relationship("Quality", back_populates="part")
    work_orders = relationship("WorkOrder", back_populates="part")
    routings = relationship("Routing", back_populates="part")
    boms = relationship("BOM", back_populates="part")
    activity_logs = relationship("ActivityLog", back_populates="part")


class DefectCategory(Base):
    __tablename__ = "defect_categories"

    id = Column(Integer, primary_key=True)
    title = Column(String(50), unique=True, nullable=False)
    department_id = Column(Integer, ForeignKey("departments.id"))

    department = relationship("Department", back_populates="defect_categories")


class Defect(Base):
    __tablename__ = "defects"

    id = Column(Integer, primary_key=True)
    title = Column(String(50), nullable=False)
    description = Column(String(255))
    part_id = Column(Integer, ForeignKey("parts.id"))
    defect_category_id = Column(Integer, ForeignKey("defect_categories.id"))

    part = relationship("Part", back_populates="defects")
    defect_category = relationship("DefectCategory")


class Quality(Base):
    __tablename__ = "quality"

    id = Column(Integer, primary_key=True)
    pass_fail = Column(Boolean, nullable=False)
    defect_count = Column(Integer, default=0)
    part_id = Column(Integer, ForeignKey("parts.id"))

    part = relationship("Part", back_populates="quality_records")


class WorkCenter(Base):
    __tablename__ = "work_centers"

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    code = Column(String(50), unique=True, nullable=True)
    department_id = Column(Integer, ForeignKey("departments.id"), nullable=True)

    department = relationship("Department", back_populates="work_centers")
    work_orders = relationship("WorkOrder", back_populates="work_center")
    operations = relationship("WorkOrderOp", back_populates="work_center")
    routing_steps = relationship("RoutingStep", back_populates="work_center")
    floor_zones = relationship("FloorZone", back_populates="work_center")


class WorkOrder(Base):
    __tablename__ = "work_orders"

    id = Column(Integer, primary_key=True)
    number = Column(String(50), unique=True, nullable=False)
    status = Column(String(30), nullable=False, default="open")
    quantity = Column(Integer, nullable=False, default=1)
    part_id = Column(Integer, ForeignKey("parts.id"), index=True, nullable=False)
    department_id = Column(Integer, ForeignKey("departments.id"), nullable=True)
    work_center_id = Column(Integer, ForeignKey("work_centers.id"), nullable=True)

    part = relationship("Part", back_populates="work_orders")
    department = relationship("Department")
    work_center = relationship("WorkCenter", back_populates="work_orders")
    operations = relationship("WorkOrderOp", back_populates="work_order")
    activity_logs = relationship("ActivityLog", back_populates="work_order")


class WorkOrderOp(Base):
    __tablename__ = "work_order_ops"

    id = Column(Integer, primary_key=True)
    work_order_id = Column(Integer, ForeignKey("work_orders.id"), nullable=False)
    sequence = Column(Integer, nullable=False)
    work_center_id = Column(Integer, ForeignKey("work_centers.id"), nullable=True)
    status = Column(String(30), nullable=False, default="pending")
    started_at = Column(DateTime, nullable=True)
    completed_at = Column(DateTime, nullable=True)

    work_order = relationship("WorkOrder", back_populates="operations")
    work_center = relationship("WorkCenter", back_populates="operations")


class Routing(Base):
    __tablename__ = "routings"

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    part_id = Column(Integer, ForeignKey("parts.id"), index=True, nullable=False)
    version = Column(String(20), nullable=True)

    part = relationship("Part", back_populates="routings")
    steps = relationship("RoutingStep", back_populates="routing")


class RoutingStep(Base):
    __tablename__ = "routing_steps"

    id = Column(Integer, primary_key=True)
    routing_id = Column(Integer, ForeignKey("routings.id"), nullable=False)
    sequence = Column(Integer, nullable=False)
    work_center_id = Column(Integer, ForeignKey("work_centers.id"), nullable=True)
    description = Column(String(255))
    standard_minutes = Column(Integer, nullable=True)

    routing = relationship("Routing", back_populates="steps")
    work_center = relationship("WorkCenter", back_populates="routing_steps")


class BOM(Base):
    __tablename__ = "boms"

    id = Column(Integer, primary_key=True)
    part_id = Column(Integer, ForeignKey("parts.id"), nullable=False)  # parent/assembly
    revision = Column(String(20), nullable=True)

    part = relationship("Part", back_populates="boms")
    items = relationship("BOMItem", back_populates="bom")


class BOMItem(Base):
    __tablename__ = "bom_items"

    id = Column(Integer, primary_key=True)
    bom_id = Column(Integer, ForeignKey("boms.id"), nullable=False)
    component_part_id = Column(Integer, ForeignKey("parts.id"), nullable=False)
    quantity = Column(Integer, nullable=False, default=1)

    bom = relationship("BOM", back_populates="items")
    component_part = relationship("Part", foreign_keys=[component_part_id])


class ActivityLog(Base):
    __tablename__ = "activity_logs"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    part_id = Column(Integer, ForeignKey("parts.id"), nullable=True)
    department_id = Column(Integer, ForeignKey("departments.id"), nullable=True)
    work_order_id = Column(Integer, ForeignKey("work_orders.id"), nullable=True)
    event_type = Column(String(50), nullable=False)
    message = Column(String(255))
    created_at = Column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )

    user = relationship("User")
    part = relationship("Part", back_populates="activity_logs")
    department = relationship("Department")
    work_order = relationship("WorkOrder", back_populates="activity_logs")


# ---- Floor and FloorZone models ----
class Floor(Base):
    __tablename__ = "floors"

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    description = Column(String(255))

    zones = relationship(
        "FloorZone", back_populates="floor", cascade="all, delete-orphan"
    )


class FloorZone(Base):
    __tablename__ = "floor_zones"

    id = Column(Integer, primary_key=True)
    floor_id = Column(Integer, ForeignKey("floors.id"), nullable=False)
    name = Column(String(100), nullable=False)
    # Semantic type of the zone, e.g. 'department', 'work_center', 'storage'
    zone_type = Column(String(50), nullable=True)
    department_id = Column(Integer, ForeignKey("departments.id"), nullable=True)
    work_center_id = Column(Integer, ForeignKey("work_centers.id"), nullable=True)
    # Simple, DB-agnostic encoding of the polygon: "x1,y1 x2,y2 ..."
    polygon = Column(String(2000), nullable=False)

    floor = relationship("Floor", back_populates="zones")
    department = relationship("Department", back_populates="floor_zones")
    work_center = relationship("WorkCenter", back_populates="floor_zones")
