"""Sample FastAPI backend for Sharingan demo.

Contains intentional Bug #3: POST /api/v1/items does not validate
the request body, causing a 500 error on empty/malformed requests.
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI(title="Sharingan Sample API", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# In-memory store
users_db: dict[str, dict] = {}
items_db: list[dict] = []


class SignupRequest(BaseModel):
    email: str
    password: str


class LoginRequest(BaseModel):
    email: str
    password: str


@app.get("/api/v1/health")
def health_check():
    """Health check endpoint."""
    return {"status": "ok", "version": "0.1.0"}


@app.post("/api/v1/auth/signup")
def signup(request: SignupRequest):
    """Register a new user."""
    if request.email in users_db:
        raise HTTPException(status_code=400, detail="Email already registered")

    users_db[request.email] = {
        "email": request.email,
        "password": request.password,  # NOTE: plaintext for demo only
    }
    return {"message": "User created", "email": request.email}


@app.post("/api/v1/auth/login")
def login(request: LoginRequest):
    """Authenticate a user."""
    user = users_db.get(request.email)
    if not user or user["password"] != request.password:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    return {"token": f"fake-token-{request.email}", "email": request.email}


@app.get("/api/v1/items")
def list_items():
    """List all items."""
    return {"items": items_db}


@app.post("/api/v1/items")
def create_item(body: dict):
    """Create a new item.

    BUG #3: This endpoint accepts a raw dict instead of a Pydantic model.
    It does NOT validate that 'name' exists in the body, causing a KeyError
    (500 Internal Server Error) when the body is empty or missing 'name'.

    Should use a proper Pydantic model:
        class CreateItemRequest(BaseModel):
            name: str
            description: str = ""
    """
    # BUG: No validation — accessing body["name"] on empty dict causes KeyError → 500
    item = {
        "id": len(items_db) + 1,
        "name": body["name"],  # KeyError if body is empty!
        "description": body.get("description", ""),
    }
    items_db.append(item)
    return item


@app.get("/api/v1/items/{item_id}")
def get_item(item_id: int):
    """Get a specific item by ID."""
    for item in items_db:
        if item["id"] == item_id:
            return item
    raise HTTPException(status_code=404, detail="Item not found")


@app.delete("/api/v1/items/{item_id}")
def delete_item(item_id: int):
    """Delete an item by ID."""
    for i, item in enumerate(items_db):
        if item["id"] == item_id:
            items_db.pop(i)
            return {"message": "Item deleted"}
    raise HTTPException(status_code=404, detail="Item not found")
