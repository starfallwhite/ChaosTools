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
    const y = innerData.y || []

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
            {
              x: t,
              y: y,
              type: 'scatter',
              mode: 'lines',
              name: 'y(t)',
              line: { color: '#ff7f0e' },
            },
          ]}
          layout={{
            width: 600,
            height: 400,
            title: 'Time Series Plot',
            xaxis: { title: 'Time' },
            yaxis: { title: 'Value' },
          }}
        />
        {data.summary && (
          <div className="data-summary">
            <p>Length: {data.summary.length}</p>
            <p>x_mean: {data.summary.x_mean?.toFixed(4)}</p>
            <p>x_std: {data.summary.x_std?.toFixed(4)}</p>
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
    const points = data.data_preview || data.data?.points || []
    const pointsArray = Array.isArray(points) ? points : []

    return (
      <div className="plot-view">
        <h3 className="section-title">Phase Space</h3>
        <Plot
          data={[
            {
              x: pointsArray.map((p: number[]) => p[0]),
              y: pointsArray.map((p: number[]) => p[1] || 0),
              type: 'scatter',
              mode: 'markers',
              name: 'Phase',
              marker: { color: '#d62728', size: 3 },
            },
          ]}
          layout={{
            width: 600,
            height: 400,
            title: 'Phase Space Reconstruction',
            xaxis: { title: 'x(t)' },
            yaxis: { title: 'x(t+tau)' },
          }}
        />
        {data.summary && (
          <div className="data-summary">
            <p>Points: {data.summary.num_points}</p>
            <p>Dim: {data.summary.embedding_dim}</p>
            <p>Tau: {data.summary.delay_tau}</p>
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