from datetime import datetime
import uuid
from ekbase.database.services.mcp_service import MCPService
from ekbase.database.models.mcp_server import MCPServer
from ekbase.database.models.mcp_tool import MCPTool
from typing import List
from fastmcp import Client
from fastmcp.client.transports import PythonStdioTransport, SSETransport
from ekbase.config import MCP
from ekbase.core.models.mcp_server_request import MCPServerRequest
import json


class MCPCoreService:
    def __init__(self):
        self.mcp_service = MCPService()


    async def fetch_mcp_tools(self, server_url: str, auth_type: str, auth_value: str) -> list:
        print(f'fetch_mcp_tools: {server_url}, {auth_type}, {auth_value}')
        try:
            # 根据协议类型选择不同的transport
            if server_url.startswith("stdio://"):
                transport = PythonStdioTransport(server_url.replace("stdio://", ""))
            else:
                transport = SSETransport(server_url, auth_type, auth_value)

            print(f'transport: {transport}')
                
            async with Client(transport, timeout=30) as client:   
                print(f'client: {client}')
                tools = await client.list_tools()
                print(f'tools: {tools}')
            # Ensure tools have required fields
            return [
                {
                    "id": str(uuid.uuid4()),
                    "name": tool.name,
                    "description": tool.description,
                    "input_schema": json.dumps(tool.inputSchema)
                }
                for tool in tools
            ]
        except Exception as e:
            print(f"Error fetching tools from {server_url}: {e}")
            return []
        
    async def create_server(self, server: MCPServerRequest) -> MCPServer:
        server_exist = self.mcp_service.select_by_name(server.name)
        if server_exist:
            raise Exception(f"server {server.name} already exists")
        mcp_server = MCPServer(
            id=str(uuid.uuid4()),
            name=server.name,
            url=server.url,
            description=server.description,
            auth_type=server.auth_type,
            auth_value=server.auth_value
        )
        self.mcp_service.create_server(mcp_server)
        await self.create_tools(mcp_server)
        return mcp_server
    
    async def create_tools(self, server: MCPServer):
        try:
            tools = await self.fetch_mcp_tools(server.url, server.auth_type, server.auth_value)
            mcp_tools = []
            for tool in tools:
                tool['server_id'] = server.id
                mcp_tool = MCPTool.from_dict(tool)
                mcp_tools.append(mcp_tool)
            self.mcp_service.batch_create_tool(mcp_tools)
        except Exception as e:
            raise e
    
    async def delete_server(self, server_id: str):
        self.mcp_service.delete_server(server_id)
        self.mcp_service.delete_tools_by_server_id(server_id)

    async def update_server(self, server_id: str, server: MCPServerRequest):
        mcp_server = MCPServer(
            id=server_id,
            name=server.name,
            url=server.url,
            description=server.description,
            auth_type=server.auth_type,
            auth_value=server.auth_value
        )
        self.mcp_service.update_server(mcp_server)
        self.mcp_service.delete_tools_by_server_id(server.id)
        await self.create_tools(server)

    async def refresh_tools(self, server_id: str):
        server = self.mcp_service.get_server(server_id)
        self.mcp_service.delete_tools_by_server_id(server.id)
        await self.create_tools(server)
    
    def get_server(self, server_id: str) -> MCPServer:
        return self.mcp_service.get_server(server_id)
    
    def get_all_tools(self) -> List[MCPTool]:
        return self.mcp_service.get_all_tools(MCP['limit'])
    
    def get_all_servers(self) -> List[MCPServer]:
        return self.mcp_service.get_all_servers()
    
    def get_tools_by_server_id(self, server_id: str) -> List[MCPTool]:
        return self.mcp_service.get_tools_by_server_id(server_id)