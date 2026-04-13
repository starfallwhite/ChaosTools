/**
 * API 客户端
 *
 * 封装与后端 FastAPI 的通信。
 * 根据 Prompt/6.frontend/prompt14.txt 规范实现。
 */

// 使用 Vite 代理路径，开发时代理到 localhost:8000
const API_BASE = '/api'

/**
 * 调用 MCP 工具
 *
 * @param payload MCP 请求
 * @returns MCP 响应
 */
export async function callMCP(payload: {
  tool: string
  params?: Record<string, any>
  session_id?: string
}): Promise<{
  status: string
  data: any
  session_id: string
}> {
  const res = await fetch(`${API_BASE}/mcp`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(payload),
  })

  return res.json()
}

/**
 * 获取所有模型列表
 *
 * @returns 模型名称列表
 */
export async function getModels(): Promise<Record<string, any>> {
  const res = await fetch(`${API_BASE}/models`)
  return res.json()
}

/**
 * 获取模型详细信息
 *
 * @returns 模型信息列表
 */
export async function getModelsInfo(): Promise<any[]> {
  const res = await fetch(`${API_BASE}/models/info`)
  return res.json()
}

/**
 * 获取所有 MCP 工具
 *
 * @returns 工具 Schema 列表
 */
export async function getTools(): Promise<any[]> {
  const res = await fetch(`${API_BASE}/mcp/tools`)
  return res.json()
}

/**
 * 运行混沌仿真
 *
 * @param model 模型名称
 * @param params 模型参数
 * @returns 仿真结果
 */
export async function runSimulation(
  model: string,
  params: Record<string, any>
): Promise<any> {
  return callMCP({
    tool: 'chaos_simulate',
    params: {
      model,
      model_params: params,
    },
  })
}

/**
 * 执行 FFT 分析
 *
 * @param sessionId 会话 ID
 * @returns FFT 结果
 */
export async function runFFT(sessionId: string): Promise<any> {
  return callMCP({
    tool: 'fft_analysis',
    params: {},
    session_id: sessionId,
  })
}

/**
 * 计算 Lyapunov 指数
 *
 * @param sessionId 会话 ID
 * @returns Lyapunov 结果
 */
export async function runLyapunov(sessionId: string): Promise<any> {
  return callMCP({
    tool: 'lyapunov_calculate',
    params: {},
    session_id: sessionId,
  })
}

/**
 * 相空间重构
 *
 * @param sessionId 会话 ID
 * @param tau 延迟参数
 * @param dim 嵌入维度
 * @returns 相空间数据
 */
export async function runPhaseReconstruct(
  sessionId: string,
  tau: number = 10,
  dim: number = 2
): Promise<any> {
  return callMCP({
    tool: 'phase_reconstruct',
    params: { tau, dim },
    session_id: sessionId,
  })
}