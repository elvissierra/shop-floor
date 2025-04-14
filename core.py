import strawberry
from controller import CreateMutation
from schema import UserType, DefectCategoryType, DefectsType, DepartmentType, PartsType, QualityType

@strawberry.type
class Mutation:
    add_user: UserType = strawberry.mutation(resolver=CreateMutation.add_user)
    add_department: DepartmentType = strawberry.mutation(resolver=CreateMutation.add_department)
    add_part: PartsType = strawberry.mutation(resolver=CreateMutation.add_part)
    add_defect_category: DefectCategoryType = strawberry.mutation(resolver=CreateMutation.add_defect_category)
    add_defect: DefectsType = strawberry.mutation(resolver=CreateMutation.add_defect)
    add_quality: QualityType = strawberry.mutation(resolver=CreateMutation.add_quality)
