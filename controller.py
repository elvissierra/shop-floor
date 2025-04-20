from sqlalchemy.orm import Session
from models.models import User, Department, DefectCategory, Defect, Part, Quality
from schema import (
    UserInput,
    UserType,
    DepartmentInput,
    DepartmentType,
    DefectCategoryInput,
    DefectCategoryType,
    DefectInput,
    DefectType,
    PartInput,
    PartType,
    QualityInput,
    QualityType,
)


class MutationService:
    def __init__(self, db: Session):
        self.db = db

    def add_user(self, user_data: UserInput) -> User:
        existing_user = (
            self.db.query(User).filter(User.username == user_data.username).first()
        )
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

    def update_department(
        self, department_id: int, data: DepartmentInput
    ) -> Department:
        department = self.db.query(Department).get(department_id)
        if not department:
            raise Exception(f"Department {department_id} not found")
        department.title = data.title
        department.description = data.description
        self.db.commit()
        self.db.refresh(department)
        return department

    def delete_department(self, department_id: int) -> bool:
        department = self.db.query(Department).get(department_id)
        if not department:
            raise Exception(f"Department {department_id} not found")
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

    def get_all_users(self) -> list[UserType]:
        return self.db.query(User).all()

    def get_user(self, user_id: int) -> User:
        user = self.db.query(User).get(user_id)
        if not user:
            raise Exception("User {user_id} not found")
        return user

    def get_all_departments(self) -> list[DepartmentType]:
        return self.db.query(Department).all()

    def get_department(self, department_id: int) -> Department:
        department = self.db.query(Department).get(department_id)
        if not department:
            raise Exception("Department {department_id} not found")
        return department

    def get_department_by_title(self, title: str) -> Department:
        department = self.db.query(Department).filter(Department.title == title).first()
        if not department:
            raise Exception("Department {title} not found")
        return department

    def get_all_parts(self) -> list[PartType]:
        return self.db.query(Part).all()

    def get_part(self, part_id: int) -> Part:
        part = self.db.query(Part).get(part_id)
        if not part:
            raise Exception("Part {part_id} not found")
        return part

    def get_all_defect_categories(self) -> list[DefectCategoryType]:
        return self.db.query(DefectCategory).all()

    def get_defect_category(self, defect_category_id: int) -> DefectCategory:
        defect_category = self.db.query(DefectCategory).get(defect_category_id)
        if not defect_category:
            raise Exception("Defect category {defect_category_id} not found")
        return defect_category

    def get_all_defects(self) -> list[DefectType]:
        return self.db.query(Defect).all()

    def get_defect(self, defect_id: int) -> Defect:
        defect = self.db.query(Defect).get(defect_id)
        if not defect:
            raise Exception("Defect {defect_id} not found")
        return defect

    def get_all_qualities(self) -> list[QualityType]:
        return self.db.query(Quality).all()

    def get_quality(self, quality_id: int) -> Quality:
        quality = self.db.query(Quality).get(quality_id)
        if not quality:
            raise Exception("Quality {quality_id} not found")
        return quality

    def get_quality_by_part_id(self, part_id: int) -> Quality:
        quality = self.db.query(Quality).filter(Quality.part_id == part_id).first()
        if not quality:
            raise Exception("Quality for part {part_id} not found")
        return quality

    def get_defect_by_part_id(self, part_id: int) -> Defect:
        defect = self.db.query(Defect).filter(Defect.part_id == part_id).first()
        if not defect:
            raise Exception("Defect for part {part_id} not found")
        return defect

    def get_defect_by_defect_category_id(self, defect_category_id: int) -> Defect:
        defect = (
            self.db.query(Defect)
            .filter(Defect.defect_category_id == defect_category_id)
            .first()
        )
        if not defect:
            raise Exception("Defect for defect category {defect_category_id} not found")
        return defect

    def get_defect_by_department_id(self, department_id: int) -> Defect:
        defect = (
            self.db.query(Defect).filter(Defect.department_id == department_id).first()
        )
        if not defect:
            raise Exception("Defect for department {department_id} not found")
        return defect

    def get_defect_by_part_id_and_defect_category_id(
        self, part_id: int, defect_category_id: int
    ) -> Defect:
        defect = (
            self.db.query(Defect)
            .filter(
                Defect.part_id == part_id,
                Defect.defect_category_id == defect_category_id,
            )
            .first()
        )
        if not defect:
            raise Exception(
                "Defect for part {part_id} and defect category {defect_category_id} not found"
            )
        return defect

    def get_defect_by_part_id_and_department_id(
        self, part_id: int, department_id: int
    ) -> Defect:
        defect = (
            self.db.query(Defect)
            .filter(Defect.part_id == part_id, Defect.department_id == department_id)
            .first()
        )
        if not defect:
            raise Exception(
                "Defect for part {part_id} and department {department_id} not found"
            )
        return defect
