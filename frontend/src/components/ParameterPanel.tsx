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

/**
 * 解析科学计数法输入
 * 支持: 1e-9, 10e-12, 1E6, 3e6 等格式
 */
function parseScientificNotation(value: string): number | null {
  // 匹配科学计数法格式: 数字 + e/E + 数字
  const sciMatch = value.match(/^([\d.]+)[eE]([+-]?\d+)$/i)
  if (sciMatch) {
    const base = parseFloat(sciMatch[1])
    const exp = parseInt(sciMatch[2])
    if (!isNaN(base) && !isNaN(exp)) {
      return base * Math.pow(10, exp)
    }
  }
  return null
}

/**
 * 智能解析数值输入
 * 支持: 普通数值、科学计数法、数学表达式(pi/4)
 */
function parseNumericValue(value: string): number | string {
  const trimmed = value.trim()

  // 先尝试科学计数法
  const sciValue = parseScientificNotation(trimmed)
  if (sciValue !== null) {
    return sciValue
  }

  // 尝试普通数值
  const numValue = parseFloat(trimmed)
  if (!isNaN(numValue)) {
    return numValue
  }

  // 尝试数学表达式 (简单支持 pi/4, pi 等)
  if (trimmed.toLowerCase().includes('pi')) {
    try {
      // 替换 pi 为数值
      const expr = trimmed.toLowerCase().replace(/pi/g, String(Math.PI))
      // 简单计算（仅支持除法）
      if (expr.includes('/')) {
        const parts = expr.split('/')
        if (parts.length === 2) {
          const a = parseFloat(parts[0])
          const b = parseFloat(parts[1])
          if (!isNaN(a) && !isNaN(b)) {
            return a / b
          }
        }
      } else {
        return parseFloat(expr)
      }
    } catch {
      return trimmed
    }
  }

  return trimmed
}

function ParameterPanel({ schema, onParamsChange }: ParameterPanelProps) {
  const [params, setParams] = useState<Record<string, any>>({})
  const [inputValues, setInputValues] = useState<Record<string, string>>({})

  // 初始化默认参数
  useEffect(() => {
    const defaults: Record<string, any> = {}
    const inputDefaults: Record<string, string> = {}
    Object.entries(schema).forEach(([key, value]) => {
      defaults[key] = value.default
      // 格式化显示值（科学计数法保持原样）
      inputDefaults[key] = formatDisplayValue(value.default, value.type)
    })
    setParams(defaults)
    setInputValues(inputDefaults)
    onParamsChange(defaults)
  }, [schema])

  // 格式化显示值
  function formatDisplayValue(val: any, _type: string): string {
    if (val === null || val === undefined) return ''

    // 数组类型
    if (Array.isArray(val)) {
      return JSON.stringify(val)
    }

    // 数值类型 - 保持科学计数法格式
    if (typeof val === 'number') {
      // 对于非常小或非常大的数，使用科学计数法显示
      if (Math.abs(val) < 1e-3 || Math.abs(val) > 1e6) {
        return val.toExponential(11).replace(/\.?0+e/, 'e')
      }
      // 检查是否是 pi/4
      if (Math.abs(val - Math.PI / 4) < 0.001) {
        return 'pi/4'
      }
      return String(val)
    }

    return String(val)
  }

  // 参数变化处理
  const handleChange = (key: string, value: string) => {
    const schemaItem = schema[key]

    // 更新输入显示
    setInputValues(prev => ({ ...prev, [key]: value }))

    let parsedValue: any = value

    // 类型转换
    if (schemaItem.type === 'float' || schemaItem.type === 'number') {
      parsedValue = parseNumericValue(value)
    } else if (schemaItem.type === 'int' || schemaItem.type === 'integer') {
      const sciValue = parseScientificNotation(value)
      if (sciValue !== null) {
        parsedValue = Math.round(sciValue)
      } else {
        parsedValue = parseInt(value) || 0
      }
    } else if (schemaItem.type === 'array') {
      // 数组输入：逗号分隔或 JSON 格式
      try {
        parsedValue = JSON.parse(value)
      } catch {
        parsedValue = value.split(',').map((v) => {
          const num = parseNumericValue(v.trim())
          return typeof num === 'number' ? num : v.trim()
        })
      }
    }

    const newParams = { ...params, [key]: parsedValue }
    setParams(newParams)
    onParamsChange(newParams)
  }

  return (
    <div className="parameter-panel">
      <h3 className="section-title">Parameters</h3>
      <div className="param-help">
        <small>支持科学计数法: 1e-9, 10e-12, 3e6 等</small>
      </div>
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
            type="text"
            value={inputValues[key] ?? ''}
            onChange={(e) => handleChange(key, e.target.value)}
            placeholder={formatDisplayValue(schemaItem.default, schemaItem.type)}
          />
        </div>
      ))}
    </div>
  )
}

export default ParameterPanel