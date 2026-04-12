/**
 * 模型选择组件
 *
 * 从 /models 获取模型列表，提供下拉选择。
 * 根据 Prompt/6.frontend/prompt12.txt 规范实现。
 */

import { useState, useEffect } from 'react'
import { getModels } from '../api/client'

interface ModelSelectorProps {
  onModelSelect: (model: string, schema: Record<string, any>) => void
}

function ModelSelector({ onModelSelect }: ModelSelectorProps) {
  const [models, setModels] = useState<Record<string, any>>({})
  const [selectedModel, setSelectedModel] = useState<string>('')
  const [loading, setLoading] = useState(true)

  // 获取模型列表
  useEffect(() => {
    getModels()
      .then((data) => {
        setModels(data)
        setLoading(false)
        // 默认选择第一个模型
        const firstModel = Object.keys(data)[0]
        if (firstModel) {
          setSelectedModel(firstModel)
          onModelSelect(firstModel, data[firstModel])
        }
      })
      .catch((err) => {
        console.error('Failed to fetch models:', err)
        setLoading(false)
      })
  }, [])

  // 模型选择变化
  const handleChange = (e: React.ChangeEvent<HTMLSelectElement>) => {
    const model = e.target.value
    setSelectedModel(model)
    if (models[model]) {
      onModelSelect(model, models[model])
    }
  }

  if (loading) {
    return <div className="loading">Loading models...</div>
  }

  return (
    <div className="model-selector-container">
      <h3 className="section-title">Model Selection</h3>
      <select
        className="model-selector"
        value={selectedModel}
        onChange={handleChange}
      >
        {Object.keys(models).map((name) => (
          <option key={name} value={name}>
            {name}
          </option>
        ))}
      </select>
    </div>
  )
}

export default ModelSelector