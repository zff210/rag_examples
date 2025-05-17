import api from './index'

export const fetchMcpServers = async () => {
  const res = await api.get('/mcp/servers')
  return res.data
}

export const fetchServerTools = async (serverId) => {
  const res = await api.get('/mcp/tools', { params: { server_id: serverId } })
  return res.data
}

export const addServer = async (server) => {
  await api.post('/mcp/servers', server)
}

export const updateServer = async (serverId, server) => {
  await api.put(`/mcp/servers/${serverId}`, server)
}

export const deleteServer = async (serverId) => {
  await api.delete(`/mcp/servers/${serverId}`)
}

export const refreshTools = async (serverId) => {
  await api.post(`/mcp/servers/${serverId}/refresh-tools`)
} 