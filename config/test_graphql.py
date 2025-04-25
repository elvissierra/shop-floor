

def test_add_and_fetch_departments(client):
    add_mutation = """
    mutation {
      addDepartment(departmentData: {
        title: "HR",
        description: "Human Resources"
      }) {
        id
        title
        description
      }
    }
    """
    resp = client.post("/graphql", json={"query": add_mutation})
    assert resp.status_code == 200
    data = resp.json()["data"]["addDepartment"]
    assert data["title"] == "HR"
    assert data["description"] == "Human Resources"
    dept_id = data["id"]

    fetch_query = """
    query {
      departments {
        id
        title
        description
      }
    }
    """
    resp2 = client.post("/graphql", json={"query": fetch_query})
    assert resp2.status_code == 200
    depts = resp2.json()["data"]["departments"]
    assert any(d["id"] == dept_id and d["title"] == "HR" for d in depts)
