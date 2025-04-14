from models.models import User
from schema import UserInput


class CreateMutation:

    def add_user(self, user_data: UserInput):
        user = User.where("username", user_data.username).get()
        if user:
            raise Exception("User already exists, cheack username")

        user = User()

        user.id = user_data.id
        user.username = user_data.username
        user.department_id = user_data.department_id
        user.job = user_data.job
        user.time = user_data.time

        user.save()

        return user