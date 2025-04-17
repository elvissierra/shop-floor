from sqlalchemy.orm import Session
from models.models import User, Department, DefectCategory, Defect, Part, Quality
from schema import (
    UserInput,
    DepartmentInput,
    DepartmentType,
    DefectCategoryInput,
    DefectInput,
    PartInput,
    QualityInput,
)

class MutationService:
    def __init__(self, db: Session):
        self.db = db

    def add_user(self, user_data: UserInput) -> User:
        existing_user = self.db.query(User).filter(User.username == user_data.username).first()
        if existing_user:
            raise Exception("User already exists; check username.")

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
            raise Exception("Department already exists; check title.")

        department = Department(
            title=department_data.title,
            description=department_data.description,
        )
        self.db.add(department)
        self.db.commit()
        self.db.refresh(department)
        return department

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
        defect_category = DefectCategory(
            title=def_cat_data.title,
            department_id=def_cat_data.department_id,
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

class QueryService:
    def __init__(self, db: Session):
        self.db = db

    def get_all_departments(self) -> list[DepartmentType]:
        return self.db.query(Department).all()