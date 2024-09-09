from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from github_push import push_to_github
from yaml_generator import generate

app = FastAPI()

class GenerateYaml(BaseModel):
    user_input: str
    model: str
    api_key: str

class GithubPush(BaseModel):
    yaml_content: str
    Repository_list: str
    access_token: str
@app.post("/generate_yaml")
async def generate_yaml(request: GenerateYaml):
    try:
        yaml_content = generate(request.user_input, request.model, request.api_key)
        return {"message": "Success", "status": 200, "data": yaml_content}
    except Exception as e:
        return {"message": f"Error generating YAML: {str(e)}", "status": 500}

@app.post("/github_push")
async def github_push(request: GithubPush):
    try:
        result = push_to_github(request.access_token, request.yaml_content, request.Repository_list)
        if result is None:
            return {"message": "Successfully pushed YAML", "status": 200}
        else:
            return {"message": f"Failed to push YAML: {result}", "status": 500}
    except Exception as e:
        return {"message": f"Error during GitHub push: {str(e)}", "status": 500}
