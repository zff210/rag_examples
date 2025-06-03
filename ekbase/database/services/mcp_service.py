from typing import List
from ekbase.database.models.mcp_server import MCPServer
from ekbase.database.models.mcp_tool import MCPTool
from ekbase.database.utils import Database

class MCPService:
    def __init__(self):
        self.db = Database()

    def create_server(self, server: MCPServer) -> MCPServer:
        query = """
        INSERT INTO mcp_servers (id, name, url, description, auth_type, auth_value)
        VALUES (?, ?, ?, ?, ?, ?)
        """
        self.db.execute(query, (
            server.id,
            server.name,
            server.url,
            server.description,
            server.auth_type,
            server.auth_value
        ))
        self.db.commit()
        return server
    
    def batch_create_tool(self, tools: List[MCPTool]):
        query = """
        INSERT INTO mcp_tools (id, server_id, name, description, input_schema)
        VALUES (?, ?, ?, ?, ?)
        """
        values = [(tool.id, tool.server_id, tool.name, tool.description, tool.input_schema) for tool in tools]
        self.db.executemany(query, values)
        self.db.commit()

    def select_by_name(self, name: str) -> MCPServer:
        query = """
        SELECT id, name, url, description, auth_type, auth_value, created_at, updated_at
        FROM mcp_servers
        WHERE name = ?
        """
        cursor = self.db.execute(query, (name,))
        row = cursor.fetchone()
        if row:
            return MCPServer.from_dict(dict(row))
        return None
    
    def get_server(self, server_id: str) -> MCPServer:
        query = """
        SELECT id, name, url, description, auth_type, auth_value, created_at, updated_at
        FROM mcp_servers
        WHERE id = ?
        """
        cursor = self.db.execute(query, (server_id,))
        row = cursor.fetchone()
        if row:
            return MCPServer.from_dict(dict(row))
        return None
    
    def list_servers(self) -> List[MCPServer]:
        query = """
        SELECT id, name, url, description, auth_type, auth_value, created_at, updated_at
        FROM mcp_servers
        """
        cursor = self.db.execute(query)
        return [MCPServer.from_dict(dict(row)) for row in cursor]
    
    def update_server(self, server: MCPServer):
        query = """
        UPDATE mcp_servers SET name = ?, url = ?, description = ?, auth_type = ?, auth_value = ?, updated_at = ?
        WHERE id = ?
        """
        self.db.execute(query, (server.name, server.url, server.description, server.auth_type, server.auth_value, server.updated_at, server.id))
        self.db.commit()
    
    def delete_server(self, server_id: str):
        query = """
        DELETE FROM mcp_servers WHERE id = ?
        """
        self.db.execute(query, (server_id,))
        self.db.commit()

    def create_tool(self, tool: MCPTool) -> MCPTool:
        query = """
        INSERT INTO mcp_tools (id, server_id, name, description, input_schema)
        VALUES (?, ?, ?, ?, ?)
        """
        self.db.execute(query, (
            tool.id, 
            tool.server_id, 
            tool.name, 
            tool.description, 
            tool.input_schema
        ))
        self.db.commit()
        return tool
    
    def get_tools_by_server_id(self, server_id: str) -> List[MCPTool]:
        """
        获取指定服务器下的所有工具
        """
        query = """
        SELECT id, server_id, name, description, input_schema, created_at, updated_at
        FROM mcp_tools
        WHERE server_id = ?
        """
        cursor = self.db.execute(query, (server_id,))
        return [MCPTool.from_dict(dict(row)) for row in cursor]
    
    def get_all_servers(self) -> List[MCPServer]:
        query = """
        SELECT id, name, url, description, auth_type, auth_value, created_at, updated_at
        FROM mcp_servers
        """
        cursor = self.db.execute(query)
        return [MCPServer.from_dict(dict(row)) for row in cursor]
    
    def get_all_tools(self, limit: int = 50) -> List[MCPTool]:
        query = """
        SELECT id, server_id, name, description, input_schema, created_at, updated_at
        FROM mcp_tools
        ORDER BY created_at DESC
        LIMIT ?
        """
        cursor = self.db.execute(query, (limit,))
        return [MCPTool.from_dict(dict(row)) for row in cursor]
    
    def delete_tools_by_server_id(self, server_id: str):
        query = """
        DELETE FROM mcp_tools WHERE server_id = ?
        """
        self.db.execute(query, (server_id,))
        self.db.commit()       