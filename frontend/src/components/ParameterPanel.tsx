/**
 * 参数面板组件
 *
 * 根据 param_schema 动态生成参数输入框。
 * 根据 Prompt/6.frontend/prompt12.txt 规范实现。
 */

import { useState, useEffect } from 'react'

interface ParamSchema {
  type: string
  description?: string
  default?: any
}

interface ParameterPanelProps {
  schema: Record<string, ParamSchema>
  onParamsChange: (params: Record<string, any>) => void
}

function ParameterPanel({ schema, onParamsChange }: ParameterPanelProps) {
  const [params, setParams] = useState<Record<string, any>>({})

  // 初始化默认参数
  useEffect(() => {
    const defaults: Record<string, any> = {}
    Object.entries(schema).forEach(([key, value]) => {
      defaults[key] = value.default
    })
    setParams(defaults)
    onParamsChange(defaults)
  }, [schema])

  // 参数变化处理
  const handleChange = (key: string, value: string) => {
    const schemaItem = schema[key]
    let parsedValue: any = value

    // 类型转换
    if (schemaItem.type === 'float' || schemaItem.type === 'number') {
      parsedValue = parseFloat(value) || 0
    } else if (schemaItem.type === 'int' || schemaItem.type === 'integer') {
      parsedValue = parseInt(value) || 0
    } else if (schemaItem.type === 'array') {
      // 数组输入：逗号分隔或 JSON 格式
      try {
        parsedValue = JSON.parse(value)
      } catch {
        parsedValue = value.split(',').map((v) => parseFloat(v.trim()) || v.trim())
      }
    }

    const newParams = { ...params, [key]: parsedValue }
    setParams(newParams)
    onParamsChange(newParams)
  }

  return (
    <div className="parameter-panel">
      <h3 className="section-title">Parameters</h3>
      {Object.entries(schema).map(([key, schemaItem]) => (
        <div key={key} className="param-group">
          <label className="param-label">
            {key}
            {schemaItem.description && (
              <span className="param-desc"> ({schemaItem.description})</span>
            )}
          </label>
          <input
            className="param-input"
            type={schemaItem.type === 'int' || schemaItem.type === 'float' ? 'number' : 'text'}
            value={params[key] ?? schemaItem.default ?? ''}
            onChange={(e) => handleChange(key, e.target.value)}
            placeholder={String(schemaItem.default ?? '')}
          />
        </div>
      ))}
    </div>
  )
}

export default ParameterPanel