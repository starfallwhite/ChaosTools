/**
 * 主页面组件
 *
 * 整合所有组件，实现完整工作流。
 * 根据 Prompt/6.frontend/prompt17.txt 规范实现。
 */

import { useState } from 'react'
import ModelSelector from '../components/ModelSelector'
import ParameterPanel from '../components/ParameterPanel'
import PlotView from '../components/PlotView'
import ChatPanel from '../components/ChatPanel'
import { callMCP } from '../api/client'

function MainPage() {
  const [selectedModel, setSelectedModel] = useState<string>('')
  const [paramSchema, setParamSchema] = useState<Record<string, any>>({})
  const [params, setParams] = useState<Record<string, any>>({})
  const [sessionId, setSessionId] = useState<string | null>(null)
  const [result, setResult] = useState<any>(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)

  // 模型选择回调
  const handleModelSelect = (model: string, schema: Record<string, any>) => {
    setSelectedModel(model)
    setParamSchema(schema)
    setResult(null)
    setError(null)
  }

  // 参数变化回调
  const handleParamsChange = (newParams: Record<string, any>) => {
    setParams(newParams)
  }

  // 运行仿真
  const handleRunSimulation = async () => {
    if (!selectedModel) {
      setError('Please select a model first')
      return
    }

    setLoading(true)
    setError(null)

    try {
      const response = await callMCP({
        tool: 'chaos_simulate',
        params: {
          model: selectedModel,
          model_params: params,
        },
        session_id: sessionId || undefined,
      })

      if (response.status === 'success') {
        setResult(response.data)
        setSessionId(response.session_id)
      } else {
        setError(response.data?.error || 'Simulation failed')
      }
    } catch (err) {
      setError(`Error: ${err}`)
    } finally {
      setLoading(false)
    }
  }

  // Chat 结果回调
  const handleChatResult = (data: any) => {
    setResult(data)
  }

  return (
    <div className="main-page">
      <header className="header">
        <h1>Chaos Simulation Platform</h1>
        <p>MCP-powered chaos analysis tools</p>
      </header>

      <div className="content">
        <div className="left-panel">
          <ModelSelector onModelSelect={handleModelSelect} />
          <ParameterPanel
            schema={paramSchema}
            onParamsChange={handleParamsChange}
          />
          <button
            className="run-button"
            onClick={handleRunSimulation}
            disabled={loading || !selectedModel}
          >
            {loading ? 'Running...' : 'Run Simulation'}
          </button>
          {error && <div className="error-message">{error}</div>}
        </div>

        <div className="right-panel">
          <PlotView data={result} />
          <ChatPanel sessionId={sessionId} onResult={handleChatResult} />
        </div>
      </div>

      {sessionId && (
        <footer className="footer">
          <small>Session: {sessionId}</small>
        </footer>
      )}
    </div>
  )
}

export default MainPage