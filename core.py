import strawberry
from controller import CreateMutation
from schema import DefectCategoryType, DefectsType, DepartmentType, PartsType, QualityType, UsersType

@strawberry.type
class Mutation:
    create_user = strawberry.mutation(resolver=CreateMutation.add_user)
    