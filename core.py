from typing import List, Optional
import strawberry
from sqlalchemy.orm import Session
from schema import (
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
)
from controller import MutationService, QueryService

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


@strawberry.type
class Query:
    @strawberry.field
    def departments(self, info) -> List[DepartmentType]:
        db: Session = info.context.get("db")
        service = QueryService(db)
        departments = service.get_all_departments()
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
        d = QueryService(db).get_department(id)
        return DepartmentType(id=d.id, title=d.title, description=d.description)
    
    @strawberry.field
    def department_by_title(self, info, title: str) -> DepartmentType:
        db: Session = info.context["db"]
        d = QueryService(db).get_department_by_title(title)
        return DepartmentType(id=d.id, title=d.title, description=d.description)
    
    @strawberry.field
    def users(self, info) -> List[UserType]:
        db: Session = info.context.get("db")
        users = QueryService(db).get_all_users()
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