/**
 * 绘图视图组件
 *
 * 使用 Plotly 展示时序数据、频谱、相空间。
 * 根据 Prompt/6.frontend/prompt15.txt 规范实现。
 */

// @ts-ignore - react-plotly.js doesn't have TypeScript types
import Plot from 'react-plotly.js'

interface PlotViewProps {
  data: {
    type: string
    data?: any
    summary?: any
    data_preview?: any
    interpretation?: string
  } | null
}

function PlotView({ data }: PlotViewProps) {
  if (!data) {
    return (
      <div className="plot-empty">
        <h3 className="section-title">Plot View</h3>
        <p>No data to display. Run simulation first.</p>
      </div>
    )
  }

  const dataType = data.type

  // 时序数据绘图
  if (dataType === 'timeseries') {
    const innerData = data.data_preview || data.data || {}
    const t = innerData.t || []
    const x = innerData.x || []

    return (
      <div className="plot-view">
        <h3 className="section-title">Time Series</h3>
        <Plot
          data={[
            {
              x: t,
              y: x,
              type: 'scatter',
              mode: 'lines',
              name: 'x(t)',
              line: { color: '#1f77b4' },
            },
          ]}
          layout={{
            width: 600,
            height: 400,
            title: 'Time Series Plot',
            xaxis: { title: 'Time' },
            yaxis: { title: 'x' },
          }}
        />
        {data.summary && (
          <div className="data-summary">
            <p>Length: {data.summary.length}</p>
            <p>x_mean: {data.summary.x_mean?.toFixed(4)}</p>
            <p>x_std: {data.summary.x_std?.toFixed(4)}</p>
            <p>x_max: {data.summary.x_max?.toFixed(4)}</p>
            <p>x_min: {data.summary.x_min?.toFixed(4)}</p>
          </div>
        )}
      </div>
    )
  }

  // 频谱数据绘图
  if (dataType === 'spectrum') {
    const innerData = data.data_preview || data.data || {}
    const f = innerData.f || []
    const Pxx = innerData.Pxx || []

    return (
      <div className="plot-view">
        <h3 className="section-title">FFT Spectrum</h3>
        <Plot
          data={[
            {
              x: f,
              y: Pxx,
              type: 'scatter',
              mode: 'lines',
              name: 'Pxx',
              line: { color: '#2ca02c' },
            },
          ]}
          layout={{
            width: 600,
            height: 400,
            title: 'Frequency Spectrum',
            xaxis: { title: 'Frequency' },
            yaxis: { title: 'Power' },
          }}
        />
        {data.summary && (
          <div className="data-summary">
            <p>Dominant freq: {data.summary.dominant_freq?.toFixed(2)}</p>
            <p>Max power: {data.summary.max_power?.toFixed(4)}</p>
          </div>
        )}
      </div>
    )
  }

  // 相空间绘图
  if (dataType === 'phase_space') {
    const innerData = data.data_preview || data.data || {}
    const xDelay = innerData.x_delay || []
    const xCurrent = innerData.x_current || []

    // 确保 x_delay 和 x_current 是数组
    const xDelayArray = Array.isArray(xDelay) ? xDelay : []
    const xCurrentArray = Array.isArray(xCurrent) ? xCurrent : []

    return (
      <div className="plot-view">
        <h3 className="section-title">Phase Space</h3>
        <Plot
          data={[
            {
              x: xDelayArray,
              y: xCurrentArray,
              type: 'scatter',
              mode: 'markers',
              name: 'Phase',
              marker: { color: '#d62728', size: 2 },
            },
          ]}
          layout={{
            width: 600,
            height: 400,
            title: 'Phase Space (x(t-T1) vs x(t))',
            xaxis: { title: 'x(t-T1)' },
            yaxis: { title: 'x(t)' },
          }}
        />
        {data.summary && (
          <div className="data-summary">
            <p>Points: {data.summary.num_points}</p>
            <p>Delay points (n): {data.summary.n_delay}</p>
            <p>T1: {data.summary.T1_ns?.toFixed(2)} ns</p>
          </div>
        )}
      </div>
    )
  }

  // Lyapunov 指数显示
  if (dataType === 'lyapunov') {
    const lambdaMax = data.data?.lambda_max

    return (
      <div className="plot-view">
        <h3 className="section-title">Lyapunov Exponent</h3>
        <div className="lyapunov-result">
          <p>
            <strong>λ_max:</strong> {lambdaMax?.toFixed(4)}
          </p>
          {data.interpretation && (
            <p className="interpretation">{data.interpretation}</p>
          )}
        </div>
      </div>
    )
  }

  // 模型列表
  if (dataType === 'model_list') {
    const models = data.data?.models || []

    return (
      <div className="plot-view">
        <h3 className="section-title">Available Models</h3>
        <ul>
          {models.map((m: string) => (
            <li key={m}>{m}</li>
          ))}
        </ul>
      </div>
    )
  }

  return (
    <div className="plot-view">
      <h3 className="section-title">Unknown Data Type</h3>
      <p>Type: {dataType}</p>
      <pre>{JSON.stringify(data, null, 2)}</pre>
    </div>
  )
}

export default PlotView