from typing import List, Optional
import strawberry
from sqlalchemy.orm import Session
from app.schema import (
    UserType,
    DefectCategoryType,
    DefectType,
    DepartmentType,
    PartType,
    QualityType,
    UserInput,
    DepartmentInput,
    DefectCategoryInput,
    DefectInput,
    PartInput,
    QualityInput,
    WorkCenterType,
    WorkOrderType,
    WorkOrderOpType,
    RoutingType,
    RoutingStepType,
    BOMType,
    BOMItemType,
    ActivityLogType,
    WorkCenterInput,
    WorkOrderInput,
    WorkOrderOpInput,
    RoutingInput,
    RoutingStepInput,
    BOMInput,
    BOMItemInput,
    ActivityLogInput,
)
from app.api.services import MutationService, QueryService


@strawberry.type
class Mutation:
    @strawberry.mutation
    def add_user(self, user_data: UserInput, info) -> UserType:
        db = info.context.get("db")
        service = MutationService(db)
        user = service.add_user(user_data)
        return UserType(
            id=user.id,
            username=user.username,
            department_id=user.department_id,
            job=user.job,
            time=user.time,
        )

    @strawberry.mutation
    def add_department(self, department_data: DepartmentInput, info) -> DepartmentType:
        db = info.context.get("db")
        service = MutationService(db)
        department = service.add_department(department_data)
        return DepartmentType(
            id=department.id,
            title=department.title,
            description=department.description,
        )

    @strawberry.mutation
    def update_department(self, id: int, data: DepartmentInput, info) -> DepartmentType:
        db: Session = info.context["db"]
        d = MutationService(db).update_department(id, data)
        return DepartmentType(id=d.id, title=d.title, description=d.description)

    @strawberry.mutation
    def delete_department(self, id: int, info) -> bool:
        db: Session = info.context["db"]
        return MutationService(db).delete_department(id)

    @strawberry.mutation
    def add_part(self, part_data: PartInput, info) -> PartType:
        db = info.context.get("db")
        service = MutationService(db)
        part = service.add_part(part_data)
        return PartType(
            id=part.id,
            name=part.name,
            department_id=part.department_id,
        )

    @strawberry.mutation
    def add_defect_category(
        self, def_cat_data: DefectCategoryInput, info
    ) -> DefectCategoryType:
        db = info.context.get("db")
        service = MutationService(db)
        defect_category = service.add_defect_category(def_cat_data)
        return DefectCategoryType(
            id=defect_category.id,
            title=defect_category.title,
            department_id=defect_category.department_id,
        )

    @strawberry.mutation
    def add_defect(self, defect_data: DefectInput, info) -> DefectType:
        db = info.context.get("db")
        service = MutationService(db)
        defect = service.add_defect(defect_data)
        return DefectType(
            id=defect.id,
            title=defect.title,
            description=defect.description,
            part_id=defect.part_id,
            defect_category_id=defect.defect_category_id,
        )

    @strawberry.mutation
    def add_quality(self, quality_data: QualityInput, info) -> QualityType:
        db = info.context.get("db")
        service = MutationService(db)
        quality = service.add_quality(quality_data)
        return QualityType(
            id=quality.id,
            pass_fail=quality.pass_fail,
            defect_count=quality.defect_count,
            part_id=quality.part_id,
        )

        # ---- User CRUD ----

    @strawberry.mutation
    def update_user(self, id: int, data: UserInput, info) -> UserType:
        db: Session = info.context["db"]
        u = MutationService(db).update_user(id, data)
        return UserType(
            id=u.id,
            username=u.username,
            department_id=u.department_id,
            job=u.job,
            time=u.time,
        )

    @strawberry.mutation
    def delete_user(self, id: int, info) -> bool:
        db: Session = info.context["db"]
        return MutationService(db).delete_user(id)

    # ---- Part CRUD ----
    @strawberry.mutation
    def update_part(self, id: int, data: PartInput, info) -> PartType:
        db: Session = info.context["db"]
        p = MutationService(db).update_part(id, data)
        return PartType(id=p.id, name=p.name, department_id=p.department_id)

    @strawberry.mutation
    def delete_part(self, id: int, info) -> bool:
        db: Session = info.context["db"]
        return MutationService(db).delete_part(id)

    # ---- DefectCategory CRUD ----
    @strawberry.mutation
    def update_defect_category(
        self, id: int, data: DefectCategoryInput, info
    ) -> DefectCategoryType:
        db: Session = info.context["db"]
        dc = MutationService(db).update_defect_category(id, data)
        return DefectCategoryType(
            id=dc.id, title=dc.title, department_id=dc.department_id
        )

    @strawberry.mutation
    def delete_defect_category(self, id: int, info) -> bool:
        db: Session = info.context["db"]
        return MutationService(db).delete_defect_category(id)

    # ---- Defect CRUD ----
    @strawberry.mutation
    def update_defect(self, id: int, data: DefectInput, info) -> DefectType:
        db: Session = info.context["db"]
        d = MutationService(db).update_defect(id, data)
        return DefectType(
            id=d.id,
            title=d.title,
            description=d.description,
            part_id=d.part_id,
            defect_category_id=d.defect_category_id,
        )

    @strawberry.mutation
    def delete_defect(self, id: int, info) -> bool:
        db: Session = info.context["db"]
        return MutationService(db).delete_defect(id)

    # ---- Quality CRUD ----
    @strawberry.mutation
    def update_quality(self, id: int, data: QualityInput, info) -> QualityType:
        db: Session = info.context["db"]
        q = MutationService(db).update_quality(id, data)
        return QualityType(
            id=q.id,
            pass_fail=q.pass_fail,
            defect_count=q.defect_count,
            part_id=q.part_id,
        )

    @strawberry.mutation
    def delete_quality(self, id: int, info) -> bool:
        db: Session = info.context["db"]
        return MutationService(db).delete_quality(id)


    @strawberry.mutation
    def add_work_center(self, data: WorkCenterInput, info) -> WorkCenterType:
        db: Session = info.context["db"]
        wc = MutationService(db).add_work_center(data)
        return WorkCenterType(
            id=wc.id,
            name=wc.name,
            code=wc.code,
            department_id=wc.department_id,
        )

    @strawberry.mutation
    def add_work_order(self, data: WorkOrderInput, info) -> WorkOrderType:
        db: Session = info.context["db"]
        wo = MutationService(db).add_work_order(data)
        return WorkOrderType(
            id=wo.id,
            number=wo.number,
            status=wo.status,
            quantity=wo.quantity,
            part_id=wo.part_id,
            department_id=wo.department_id,
            work_center_id=wo.work_center_id,
        )

    @strawberry.mutation
    def add_work_order_op(self, data: WorkOrderOpInput, info) -> WorkOrderOpType:
        db: Session = info.context["db"]
        op = MutationService(db).add_work_order_op(data)
        return WorkOrderOpType(
            id=op.id,
            work_order_id=op.work_order_id,
            sequence=op.sequence,
            work_center_id=op.work_center_id,
            status=op.status,
        )

    @strawberry.mutation
    def add_routing(self, data: RoutingInput, info) -> RoutingType:
        db: Session = info.context["db"]
        r = MutationService(db).add_routing(data)
        return RoutingType(
            id=r.id,
            name=r.name,
            part_id=r.part_id,
            version=r.version,
        )

    @strawberry.mutation
    def add_routing_step(self, data: RoutingStepInput, info) -> RoutingStepType:
        db: Session = info.context["db"]
        s = MutationService(db).add_routing_step(data)
        return RoutingStepType(
            id=s.id,
            routing_id=s.routing_id,
            sequence=s.sequence,
            work_center_id=s.work_center_id,
            description=s.description,
            standard_minutes=s.standard_minutes,
        )

    @strawberry.mutation
    def add_bom(self, data: BOMInput, info) -> BOMType:
        db: Session = info.context["db"]
        b = MutationService(db).add_bom(data)
        return BOMType(
            id=b.id,
            part_id=b.part_id,
            revision=b.revision,
        )

    @strawberry.mutation
    def add_bom_item(self, data: BOMItemInput, info) -> BOMItemType:
        db: Session = info.context["db"]
        i = MutationService(db).add_bom_item(data)
        return BOMItemType(
            id=i.id,
            bom_id=i.bom_id,
            component_part_id=i.component_part_id,
            quantity=i.quantity,
        )

    @strawberry.mutation
    def add_activity_log(self, data: ActivityLogInput, info) -> ActivityLogType:
        db: Session = info.context["db"]
        log = MutationService(db).add_activity_log(data)
        return ActivityLogType(
            id=log.id,
            user_id=log.user_id,
            part_id=log.part_id,
            department_id=log.department_id,
            work_order_id=log.work_order_id,
            event_type=log.event_type,
            message=log.message,
            created_at=log.created_at.isoformat() if log.created_at else "",
        )


@strawberry.type
class Query:

    @strawberry.field
    def users(
        self, info, limit: int | None = None, offset: int | None = None
    ) -> List[UserType]:
        db: Session = info.context.get("db")
        users = QueryService(db).get_all_users(limit=limit, offset=offset)
        return [
            UserType(
                id=user.id,
                username=user.username,
                department_id=user.department_id,
                job=user.job,
                time=user.time,
            )
            for user in users
        ]

    @strawberry.field
    def user(self, info, id: int) -> UserType:
        db: Session = info.context["db"]
        user = QueryService(db).get_user(id)
        return UserType(
            id=user.id,
            username=user.username,
            department_id=user.department_id,
            job=user.job,
            time=user.time,
        )

    @strawberry.field
    def departments(
        self, info, limit: int | None = None, offset: int | None = None
    ) -> List[DepartmentType]:
        db: Session = info.context.get("db")
        service = QueryService(db)
        departments = service.get_all_departments(limit=limit, offset=offset)
        return [
            DepartmentType(
                id=department.id,
                title=department.title,
                description=department.description,
            )
            for department in departments
        ]

    @strawberry.field
    def department(self, info, id: int) -> DepartmentType:
        db: Session = info.context["db"]
        department = QueryService(db).get_department(id)
        return DepartmentType(
            id=department.id, title=department.title, description=department.description
        )

    @strawberry.field
    def department_by_title(self, info, title: str) -> DepartmentType:
        db: Session = info.context["db"]
        department = QueryService(db).get_department_by_title(title)
        return DepartmentType(
            id=department.id, title=department.title, description=department.description
        )

    @strawberry.field
    def parts(
        self, info, limit: int | None = None, offset: int | None = None
    ) -> List[PartType]:
        db: Session = info.context.get("db")
        service = QueryService(db)
        parts = service.get_all_parts(limit=limit, offset=offset)
        return [
            PartType(
                id=part.id,
                name=part.name,
                department_id=part.department_id,
            )
            for part in parts
        ]

    @strawberry.field
    def part(self, info, id: int) -> PartType:
        db: Session = info.context["db"]
        part = QueryService(db).get_part(id)
        return PartType(id=part.id, name=part.name, department_id=part.department_id)

    @strawberry.field
    def defect_categories(
        self, info, limit: int | None = None, offset: int | None = None
    ) -> List[DefectCategoryType]:
        db: Session = info.context.get("db")
        service = QueryService(db)
        defect_categories = service.get_all_defect_categories(
            limit=limit, offset=offset
        )
        return [
            DefectCategoryType(
                id=defect_category.id,
                title=defect_category.title,
                department_id=defect_category.department_id,
            )
            for defect_category in defect_categories
        ]

    @strawberry.field
    def defect_category(self, info, id: int) -> DefectCategoryType:
        db: Session = info.context["db"]
        defect_category = QueryService(db).get_defect_category(id)
        return DefectCategoryType(
            id=defect_category.id,
            title=defect_category.title,
            department_id=defect_category.department_id,
        )

    @strawberry.field
    def defects(
        self, info, limit: int | None = None, offset: int | None = None
    ) -> List[DefectType]:
        db: Session = info.context.get("db")
        service = QueryService(db)
        defects = service.get_all_defects(limit=limit, offset=offset)
        return [
            DefectType(
                id=defect.id,
                title=defect.title,
                description=defect.description,
                part_id=defect.part_id,
                defect_category_id=defect.defect_category_id,
            )
            for defect in defects
        ]

    @strawberry.field
    def defect(self, info, id: int) -> DefectType:
        db: Session = info.context["db"]
        defect = QueryService(db).get_defect(id)
        return DefectType(
            id=defect.id,
            title=defect.title,
            description=defect.description,
            part_id=defect.part_id,
            defect_category_id=defect.defect_category_id,
        )

    @strawberry.field
    def qualities(
        self, info, limit: int | None = None, offset: int | None = None
    ) -> List[QualityType]:
        db: Session = info.context.get("db")
        service = QueryService(db)
        qualities = service.get_all_qualities(limit=limit, offset=offset)
        return [
            QualityType(
                id=quality.id,
                pass_fail=quality.pass_fail,
                defect_count=quality.defect_count,
                part_id=quality.part_id,
            )
            for quality in qualities
        ]

    @strawberry.field
    def quality(self, info, id: int) -> QualityType:
        db: Session = info.context["db"]
        quality = QueryService(db).get_quality(id)
        return QualityType(
            id=quality.id,
            pass_fail=quality.pass_fail,
            defect_count=quality.defect_count,
            part_id=quality.part_id,
        )


    @strawberry.field
    def work_centers(
        self, info, limit: int | None = None, offset: int | None = None
    ) -> List[WorkCenterType]:
        db: Session = info.context.get("db")
        service = QueryService(db)
        centers = service.get_all_work_centers(limit=limit, offset=offset)
        return [
            WorkCenterType(
                id=wc.id,
                name=wc.name,
                code=wc.code,
                department_id=wc.department_id,
            )
            for wc in centers
        ]

    @strawberry.field
    def work_orders(
        self, info, limit: int | None = None, offset: int | None = None
    ) -> List[WorkOrderType]:
        db: Session = info.context.get("db")
        service = QueryService(db)
        orders = service.get_all_work_orders(limit=limit, offset=offset)
        return [
            WorkOrderType(
                id=wo.id,
                number=wo.number,
                status=wo.status,
                quantity=wo.quantity,
                part_id=wo.part_id,
                department_id=wo.department_id,
                work_center_id=wo.work_center_id,
            )
            for wo in orders
        ]

    @strawberry.field
    def work_order_ops(
        self, info, limit: int | None = None, offset: int | None = None
    ) -> List[WorkOrderOpType]:
        db: Session = info.context.get("db")
        service = QueryService(db)
        ops = service.get_all_work_order_ops(limit=limit, offset=offset)
        return [
            WorkOrderOpType(
                id=op.id,
                work_order_id=op.work_order_id,
                sequence=op.sequence,
                work_center_id=op.work_center_id,
                status=op.status,
            )
            for op in ops
        ]

    @strawberry.field
    def routings(
        self, info, limit: int | None = None, offset: int | None = None
    ) -> List[RoutingType]:
        db: Session = info.context.get("db")
        service = QueryService(db)
        routings = service.get_all_routings(limit=limit, offset=offset)
        return [
            RoutingType(
                id=r.id,
                name=r.name,
                part_id=r.part_id,
                version=r.version,
            )
            for r in routings
        ]

    @strawberry.field
    def routing_steps(
        self, info, limit: int | None = None, offset: int | None = None
    ) -> List[RoutingStepType]:
        db: Session = info.context.get("db")
        service = QueryService(db)
        steps = service.get_all_routing_steps(limit=limit, offset=offset)
        return [
            RoutingStepType(
                id=s.id,
                routing_id=s.routing_id,
                sequence=s.sequence,
                work_center_id=s.work_center_id,
                description=s.description,
                standard_minutes=s.standard_minutes,
            )
            for s in steps
        ]

    @strawberry.field
    def boms(
        self, info, limit: int | None = None, offset: int | None = None
    ) -> List[BOMType]:
        db: Session = info.context.get("db")
        service = QueryService(db)
        boms = service.get_all_boms(limit=limit, offset=offset)
        return [
            BOMType(
                id=b.id,
                part_id=b.part_id,
                revision=b.revision,
            )
            for b in boms
        ]

    @strawberry.field
    def bom_items(
        self, info, limit: int | None = None, offset: int | None = None
    ) -> List[BOMItemType]:
        db: Session = info.context.get("db")
        service = QueryService(db)
        items = service.get_all_bom_items(limit=limit, offset=offset)
        return [
            BOMItemType(
                id=i.id,
                bom_id=i.bom_id,
                component_part_id=i.component_part_id,
                quantity=i.quantity,
            )
            for i in items
        ]

    @strawberry.field
    def activity_logs(
        self, info, limit: int | None = None, offset: int | None = None
    ) -> List[ActivityLogType]:
        db: Session = info.context.get("db")
        service = QueryService(db)
        logs = service.get_all_activity_logs(limit=limit, offset=offset)
        return [
            ActivityLogType(
                id=log.id,
                user_id=log.user_id,
                part_id=log.part_id,
                department_id=log.department_id,
                work_order_id=log.work_order_id,
                event_type=log.event_type,
                message=log.message,
                created_at=log.created_at.isoformat() if log.created_at else "",
            )
            for log in logs
        ]