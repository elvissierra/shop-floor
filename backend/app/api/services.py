from sqlalchemy.orm import Session
from models.models import User, Department, DefectCategory, Defect, Part, Quality
from app.schema import (
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
    def __init__(self, db: Session): self.db = db
    def by_username(self, username: str) -> User | None:
        return self.db.query(User).filter(User.username == username).first()
    def list(self, limit: int | None = None, offset: int | None = None) -> list[User]:
        l, o = _coerce_pagination(limit, offset)
        return self.db.query(User).offset(o).limit(l).all()
    def get(self, user_id: int) -> User | None:
        return self.db.query(User).get(user_id)
    def create(self, user: User) -> User:
        self.db.add(user); self.db.commit(); self.db.refresh(user); return user
    def delete(self, user: User) -> None:
        self.db.delete(user); self.db.commit()

class DepartmentRepo:
    def __init__(self, db: Session): self.db = db
    def by_title(self, title: str) -> Department | None:
        return self.db.query(Department).filter(Department.title == title).first()
    def list(self, limit: int | None = None, offset: int | None = None) -> list[Department]:
        l, o = _coerce_pagination(limit, offset)
        return self.db.query(Department).offset(o).limit(l).all()
    def get(self, department_id: int) -> Department | None:
        return self.db.query(Department).get(department_id)
    def create(self, department: Department) -> Department:
        self.db.add(department); self.db.commit(); self.db.refresh(department); return department
    def delete(self, department: Department) -> None:
        self.db.delete(department); self.db.commit()

class PartRepo:
    def __init__(self, db: Session): self.db = db
    def list(self, limit: int | None = None, offset: int | None = None) -> list[Part]:
        l, o = _coerce_pagination(limit, offset)
        return self.db.query(Part).offset(o).limit(l).all()
    def get(self, part_id: int) -> Part | None:
        return self.db.query(Part).get(part_id)
    def create(self, part: Part) -> Part:
        self.db.add(part); self.db.commit(); self.db.refresh(part); return part

class DefectCategoryRepo:
    def __init__(self, db: Session): self.db = db
    def list(self, limit: int | None = None, offset: int | None = None) -> list[DefectCategory]:
        l, o = _coerce_pagination(limit, offset)
        return self.db.query(DefectCategory).offset(o).limit(l).all()
    def get(self, defect_category_id: int) -> DefectCategory | None:
        return self.db.query(DefectCategory).get(defect_category_id)
    def create(self, dc: DefectCategory) -> DefectCategory:
        self.db.add(dc); self.db.commit(); self.db.refresh(dc); return dc

class DefectRepo:
    def __init__(self, db: Session): self.db = db
    def list(self, limit: int | None = None, offset: int | None = None) -> list[Defect]:
        l, o = _coerce_pagination(limit, offset)
        return self.db.query(Defect).offset(o).limit(l).all()
    def get(self, defect_id: int) -> Defect | None:
        return self.db.query(Defect).get(defect_id)
    def first_by_part(self, part_id: int) -> Defect | None:
        return self.db.query(Defect).filter(Defect.part_id == part_id).first()
    def first_by_defect_category(self, defect_category_id: int) -> Defect | None:
        return self.db.query(Defect).filter(Defect.defect_category_id == defect_category_id).first()
    def first_by_part_and_defect_category(self, part_id: int, defect_category_id: int) -> Defect | None:
        return (self.db.query(Defect)
                .filter(Defect.part_id == part_id, Defect.defect_category_id == defect_category_id)
                .first())
    def first_by_part_and_department(self, part_id: int, department_id: int) -> Defect | None:
        return (self.db.query(Defect)
                .filter(Defect.part_id == part_id, Defect.department_id == department_id)
                .first())
    def create(self, defect: Defect) -> Defect:
        self.db.add(defect); self.db.commit(); self.db.refresh(defect); return defect

class QualityRepo:
    def __init__(self, db: Session): self.db = db
    def list(self, limit: int | None = None, offset: int | None = None) -> list[Quality]:
        l, o = _coerce_pagination(limit, offset)
        return self.db.query(Quality).offset(o).limit(l).all()
    def get(self, quality_id: int) -> Quality | None:
        return self.db.query(Quality).get(quality_id)
    def first_by_part(self, part_id: int) -> Quality | None:
        return self.db.query(Quality).filter(Quality.part_id == part_id).first()
    def create(self, quality: Quality) -> Quality:
        self.db.add(quality); self.db.commit(); self.db.refresh(quality); return quality


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

    # ---- User: update & delete ----
    def update_user(self, user_id: int, data: UserInput) -> User:
        user = self.db.query(User).get(user_id)
        if not user:
            raise Exception(f"User {user_id} not found")
        # Optional uniqueness check if username changed
        if data.username and data.username != user.username:
            exists = self.db.query(User).filter(User.username == data.username).first()
            if exists:
                raise Exception("User already exists; check username.")
            user.username = data.username
        user.department_id = data.department_id
        user.job = data.job
        user.time = data.time
        self.db.commit()
        self.db.refresh(user)
        return user
    
    def delete_user(self, user_id: int) -> bool:
        user = self.db.query(User).get(user_id)
        if not user:
            raise Exception(f"User {user_id} not found")
        self.db.delete(user)
        self.db.commit()
        return True
    
    # ---- Part: update & delete ----
    def update_part(self, part_id: int, data: PartInput) -> Part:
        part = self.db.query(Part).get(part_id)
        if not part:
            raise Exception(f"Part {part_id} not found")
        part.name = data.name
        part.department_id = data.department_id
        self.db.commit()
        self.db.refresh(part)
        return part
    
    def delete_part(self, part_id: int) -> bool:
        part = self.db.query(Part).get(part_id)
        if not part:
            raise Exception(f"Part {part_id} not found")
        self.db.delete(part)
        self.db.commit()
        return True
    
    # ---- DefectCategory: update & delete ----
    def update_defect_category(self, defect_category_id: int, data: DefectCategoryInput) -> DefectCategory:
        dc = self.db.query(DefectCategory).get(defect_category_id)
        if not dc:
            raise Exception(f"Defect category {defect_category_id} not found")
        # Optional uniqueness check if title changed
        if data.title and data.title != dc.title:
            exists = self.db.query(DefectCategory).filter(DefectCategory.title == data.title).first()
            if exists:
                raise Exception("Defect category already exists; check title.")
            dc.title = data.title
        dc.department_id = data.department_id
        self.db.commit()
        self.db.refresh(dc)
        return dc
    
    def delete_defect_category(self, defect_category_id: int) -> bool:
        dc = self.db.query(DefectCategory).get(defect_category_id)
        if not dc:
            raise Exception(f"Defect category {defect_category_id} not found")
        self.db.delete(dc)
        self.db.commit()
        return True
    
    # ---- Defect: update & delete ----
    def update_defect(self, defect_id: int, data: DefectInput) -> Defect:
        defect = self.db.query(Defect).get(defect_id)
        if not defect:
            raise Exception(f"Defect {defect_id} not found")
        defect.title = data.title
        defect.description = data.description
        defect.part_id = data.part_id
        defect.defect_category_id = data.defect_category_id
        self.db.commit()
        self.db.refresh(defect)
        return defect
    
    def delete_defect(self, defect_id: int) -> bool:
        defect = self.db.query(Defect).get(defect_id)
        if not defect:
            raise Exception(f"Defect {defect_id} not found")
        self.db.delete(defect)
        self.db.commit()
        return True
    
    # ---- Quality: update & delete ----
    def update_quality(self, quality_id: int, data: QualityInput) -> Quality:
        quality = self.db.query(Quality).get(quality_id)
        if not quality:
            raise Exception(f"Quality {quality_id} not found")
        quality.pass_fail = data.pass_fail
        quality.defect_count = data.defect_count
        quality.part_id = data.part_id
        self.db.commit()
        self.db.refresh(quality)
        return quality
    
    def delete_quality(self, quality_id: int) -> bool:
        quality = self.db.query(Quality).get(quality_id)
        if not quality:
            raise Exception(f"Quality {quality_id} not found")
        self.db.delete(quality)
        self.db.commit()
        return True

class QueryService:
    def __init__(self, db: Session):
        self.db = db
        self.users = UserRepo(db)
        self.departments = DepartmentRepo(db)
        self.parts = PartRepo(db)
        self.defect_categories = DefectCategoryRepo(db)
        self.defects = DefectRepo(db)
        self.qualities = QualityRepo(db)

    # ---- Users ----
    def get_all_users(self, limit: int | None = None, offset: int | None = None) -> list[User]:
        return self.users.list(limit=limit, offset=offset)

    def get_user(self, user_id: int) -> User:
        user = self.users.get(user_id)
        if not user:
            raise Exception(f"User {user_id} not found")
        return user

    # ---- Departments ----
    def get_all_departments(self, limit: int | None = None, offset: int | None = None) -> list[Department]:
        return self.departments.list(limit=limit, offset=offset)

    def get_department(self, department_id: int) -> Department:
        department = self.departments.get(department_id)
        if not department:
            raise Exception(f"Department {department_id} not found")
        return department

    def get_department_by_title(self, title: str) -> Department:
        department = self.departments.by_title(title)
        if not department:
            raise Exception(f"Department {title} not found")
        return department

    # ---- Parts ----
    def get_all_parts(self, limit: int | None = None, offset: int | None = None) -> list[Part]:
        return self.parts.list(limit=limit, offset=offset)

    def get_part(self, part_id: int) -> Part:
        part = self.parts.get(part_id)
        if not part:
            raise Exception(f"Part {part_id} not found")
        return part

    # ---- Defect Categories ----
    def get_all_defect_categories(self, limit: int | None = None, offset: int | None = None) -> list[DefectCategory]:
        return self.defect_categories.list(limit=limit, offset=offset)

    def get_defect_category(self, defect_category_id: int) -> DefectCategory:
        defect_category = self.defect_categories.get(defect_category_id)
        if not defect_category:
            raise Exception(f"Defect category {defect_category_id} not found")
        return defect_category

    # ---- Defects ----
    def get_all_defects(self, limit: int | None = None, offset: int | None = None) -> list[Defect]:
        return self.defects.list(limit=limit, offset=offset)

    def get_defect(self, defect_id: int) -> Defect:
        defect = self.defects.get(defect_id)
        if not defect:
            raise Exception(f"Defect {defect_id} not found")
        return defect

    def get_defect_by_part_id(self, part_id: int) -> Defect:
        defect = self.defects.first_by_part(part_id)
        if not defect:
            raise Exception(f"Defect for part {part_id} not found")
        return defect

    def get_defect_by_defect_category_id(self, defect_category_id: int) -> Defect:
        defect = self.defects.first_by_defect_category(defect_category_id)
        if not defect:
            raise Exception(f"Defect for defect category {defect_category_id} not found")
        return defect

    def get_defect_by_part_id_and_defect_category_id(self, part_id: int, defect_category_id: int) -> Defect:
        defect = self.defects.first_by_part_and_defect_category(part_id, defect_category_id)
        if not defect:
            raise Exception(f"Defect for part {part_id} and defect category {defect_category_id} not found")
        return defect

    def get_defect_by_part_id_and_department_id(self, part_id: int, department_id: int) -> Defect:
        defect = self.defects.first_by_part_and_department(part_id, department_id)
        if not defect:
            raise Exception(f"Defect for part {part_id} and department {department_id} not found")
        return defect

    # ---- Qualities ----
    def get_all_qualities(self, limit: int | None = None, offset: int | None = None) -> list[Quality]:
        return self.qualities.list(limit=limit, offset=offset)

    def get_quality(self, quality_id: int) -> Quality:
        quality = self.qualities.get(quality_id)
        if not quality:
            raise Exception(f"Quality {quality_id} not found")
        return quality

    def get_quality_by_part_id(self, part_id: int) -> Quality:
        quality = self.qualities.first_by_part(part_id)
        if not quality:
            raise Exception(f"Quality for part {part_id} not found")
        return quality
