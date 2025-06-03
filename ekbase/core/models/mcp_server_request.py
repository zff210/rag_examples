from pydantic import BaseModel

class MCPServerRequest(BaseModel):
    name: str
    url: str
    description: str
    auth_type: str
    auth_value: str