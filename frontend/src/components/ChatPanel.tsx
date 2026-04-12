/**
 * 聊天面板组件
 *
 * 提供自然语言输入，调用 MCP 工具。
 * 简化版本：直接解析命令，不连接真实 LLM。
 * 根据 Prompt/6.frontend/prompt16.txt 规范实现。
 */

import { useState } from 'react'
import { callMCP } from '../api/client'

interface ChatMessage {
  type: 'user' | 'system'
  content: string
  status?: 'ok' | 'error'
}

interface ChatPanelProps {
  sessionId: string | null
  onResult: (data: any) => void
}

function ChatPanel({ sessionId, onResult }: ChatPanelProps) {
  const [input, setInput] = useState('')
  const [messages, setMessages] = useState<ChatMessage[]>([])

  // 解析用户命令
  const parseCommand = (text: string): { tool: string; params: any } | null => {
    const lower = text.toLowerCase()

    if (lower.includes('fft') || lower.includes('频谱')) {
      return { tool: 'fft_analysis', params: {} }
    }
    if (lower.includes('lyapunov') || lower.includes('李雅普诺夫')) {
      return { tool: 'lyapunov_calculate', params: {} }
    }
    if (lower.includes('phase') || lower.includes('相空间')) {
      // 解析 tau 和 dim
      const tauMatch = text.match(/tau\s*[=:]\s*(\d+)/i)
      const dimMatch = text.match(/dim\s*[=:]\s*(\d+)/i)
      return {
        tool: 'phase_reconstruct',
        params: {
          tau: tauMatch ? parseInt(tauMatch[1]) : 10,
          dim: dimMatch ? parseInt(dimMatch[1]) : 2,
        },
      }
    }
    if (lower.includes('model') || lower.includes('模型')) {
      return { tool: 'list_models', params: {} }
    }

    return null
  }

  // 发送命令
  const handleSend = async () => {
    if (!input.trim()) return

    // 添加用户消息
    const userMsg: ChatMessage = { type: 'user', content: input }
    setMessages((prev) => [...prev, userMsg])

    // 解析命令
    const command = parseCommand(input)

    if (!command) {
      const errorMsg: ChatMessage = {
        type: 'system',
        content: 'Unknown command. Try: "FFT", "Lyapunov", "Phase space"',
        status: 'error',
      }
      setMessages((prev) => [...prev, errorMsg])
      setInput('')
      return
    }

    // 调用 MCP
    try {
      const result = await callMCP({
        tool: command.tool,
        params: command.params,
        session_id: sessionId || undefined,
      })

      if (result.status === 'success') {
        const successMsg: ChatMessage = {
          type: 'system',
          content: `${command.tool} completed successfully`,
          status: 'ok',
        }
        setMessages((prev) => [...prev, successMsg])
        onResult(result.data)
      } else {
        const errorMsg: ChatMessage = {
          type: 'system',
          content: `Error: ${result.data?.error || 'Unknown error'}`,
          status: 'error',
        }
        setMessages((prev) => [...prev, errorMsg])
      }
    } catch (err) {
      const errorMsg: ChatMessage = {
        type: 'system',
        content: `Error: ${err}`,
        status: 'error',
      }
      setMessages((prev) => [...prev, errorMsg])
    }

    setInput('')
  }

  return (
    <div className="chat-panel">
      <h3 className="section-title">Chat Panel</h3>
      <div className="chat-messages">
        {messages.map((msg, i) => (
          <div key={i} className={`chat-message ${msg.status || ''}`}>
            <strong>{msg.type === 'user' ? 'You: ' : 'System: '}</strong>
            {msg.content}
          </div>
        ))}
      </div>
      <input
        className="chat-input"
        type="text"
        value={input}
        onChange={(e) => setInput(e.target.value)}
        placeholder="Try: 'FFT', 'Lyapunov', 'Phase space'"
        onKeyDown={(e) => e.key === 'Enter' && handleSend()}
      />
      <button className="run-button" onClick={handleSend}>
        Send
      </button>
    </div>
  )
}

export default ChatPanel