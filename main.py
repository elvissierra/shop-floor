from fastapi import FastAPI


app = FastAPI()


@app.get("/")

def home():
    return {"message": "Startup"}


@app.post("/create")
async def create_user(username: str, department_id: int, job: str, time: int):
    user = User(username=username, department_id=department_id, job=job, time=time)
    session.add(user)
    session.commit()
    return {"instance create": user.text}


@app.get("/")
async def get_all_users():
    users_query = session.query(User).all()
    return users_query