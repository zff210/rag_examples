from ekbase.core.models.mcp_server_request import MCPServerRequest
from fastapi import APIRouter
from ekbase.core.services.mcp_core_service import MCPCoreService

router = APIRouter(prefix="/mcp", tags=["mcp"])

@router.post("/servers")
async def create_servers(request: MCPServerRequest):
    mcp_core_service = MCPCoreService()
    await mcp_core_service.create_server(request)

@router.get("/servers")
async def get_servers():
    mcp_core_service = MCPCoreService()
    return mcp_core_service.get_all_servers()

@router.get("/servers/{server_id}")
async def get_server(server_id: str):
    mcp_core_service = MCPCoreService()
    return mcp_core_service.get_server(server_id)

@router.put("/servers/{server_id}")
async def update_server(server_id: str, request: MCPServerRequest):
    mcp_core_service = MCPCoreService()
    await mcp_core_service.update_server(server_id, request)

@router.delete("/servers/{server_id}")
async def delete_server(server_id: str):
    mcp_core_service = MCPCoreService()
    return mcp_core_service.delete_server(server_id)

@router.post("/servers/{server_id}/refresh-tools")
async def refresh_tools(server_id: str):
    mcp_core_service = MCPCoreService()
    return await mcp_core_service.refresh_tools(server_id)

@router.get("/tools")
async def get_tools_by_server_id(server_id: str):
    mcp_core_service = MCPCoreService()
    return mcp_core_service.get_tools_by_server_id(server_id)