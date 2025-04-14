from models.models import User, Department, DefectCategory, Defect, Part, Quality
from schema import UserInput, DepartmentInput, DefectCategoryInput, DefectInput, PartsInput, QualityInput


class CreateMutation:

    def add_user(self, user_data: UserInput):
        user = User.where("username", user_data.username).get()
        if user:
            raise Exception("User already exists, check username")

        user = User()

        user.id = user_data.id
        user.username = user_data.username
        user.department_id = user_data.department_id
        user.job = user_data.job
        user.time = user_data.time

        user.save()

        return user
    
    def add_department(self, department_data: DepartmentInput):
        department = Department.where("title", department.title).get()
        
        if department:
            raise Exception("Department already exists, check title")

        department = Department()

        department.id = department_data.id
        department.title = department_data.title
        department.description = department_data.description

        department.save()

        return department
    
    def add_part(self, part_data: PartsInput):
        part = Part()
        part.id = part_data.id
        part.name = part_data.name
        part.department_id = part_data.department_id

        part.save()

        return part
    
    def add_defect_category(self, def_cat_data: DefectCategoryInput):
        defect_category = DefectCategory()

        defect_category.id = def_cat_data.id
        defect_category.title = def_cat_data.title
        defect_category.department_id = def_cat_data.department_id

        defect_category.save()

        return defect_category
    
    def add_defect(self, defect_data: DefectInput):
        defect = Defect()

        defect.id = defect_data.id
        defect.title = defect_data.title
        defect.description = defect_data.department_id
        defect.part = defect_data.job
        defect.defect_category_id = defect_data.time

        defect.save()

        return defect
    
    def add_quality(self, quality_data: QualityInput):
        quality = Quality()

        quality.id = quality_data.id
        quality.pass_fail = quality_data.pass_fail
        quality.defect_count = quality_data.defect_count
        quality.part_id = quality_data.id

        quality.save()

        return quality