# ChaosTools - 混沌系统仿真平台

> MCP Server for Chaos Analysis - 供大模型调用的混沌分析工具服务

## 项目简介

ChaosTools 是一个基于 MCP (Model Context Protocol) 的混沌系统仿真与分析平台。用户可以通过与大模型对话，由大模型调用 MCP 工具执行混沌分析，也可以通过 Web 前端进行交互式操作。

### 核心特性

- **MCP Server**: 提供标准 LLM 工具接口，支持 Claude 等大模型调用
- **DDE 求解器**: RK4 算法求解延迟微分方程，基于 MATLAB chaos.m 转换
- **Numba 加速**: 支持 N > 1e6 大规模仿真
- **分析工具**: FFT 频谱分析、Lyapunov 指数计算、相空间重构
- **Web 前端**: React + TypeScript + Plotly 可视化界面

---

## 环境要求

### 后端
- Python 3.10+
- NumPy
- MCP SDK
- Numba (可选，用于大规模仿真加速)
- FastAPI + Uvicorn (用于 HTTP API)

### 前端
- Node.js 18+
- npm 或 yarn

---

## 快速开始

### 1. 克隆项目

```bash
git clone https://github.com/starfallwhite/ChaosTools.git
cd ChaosTools
```

### 2. 后端安装

```bash
# 创建虚拟环境 (推荐)
conda create -n chaos-tools python=3.10 -y
conda activate chaos-tools

# 或使用 venv
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

# 安装依赖
pip install -r requirements.txt
```

### 3. 前端安装

```bash
cd frontend
npm install
cd ..
```

---

## 运行项目

### 方式一：完整启动（前后端）

**步骤 1：启动后端 API 服务**

```bash
# 从项目根目录运行
python -m uvicorn backend.api.routes:app --host 0.0.0.0 --port 8000 --reload
```

后端服务将在 `http://localhost:8000` 启动。

**步骤 2：启动前端开发服务器**

```bash
cd frontend
npm run dev
```

前端服务将在 `http://localhost:3000` 启动。

**步骤 3：访问 Web 界面**

打开浏览器访问: `http://localhost:3000`

---

### 方式二：仅后端（用于 MCP 调用）

```bash
# 启动后端服务
python -m uvicorn backend.api.routes:app --host 0.0.0.0 --port 8000

# 或运行测试 Demo
python backend/main.py
```

---

## 使用说明

### Web 前端操作

1. **选择模型**: 在左侧面板下拉选择混沌模型（如 `electrooptic_feedback`）
2. **设置参数**: 根据参数面板调整仿真参数
3. **运行仿真**: 点击 "Run Simulation" 按钮
4. **查看结果**: PlotView 组件显示时序图
5. **后续分析**: 在 ChatPanel 输入命令执行 FFT、Lyapunov 分析等

### ChatPanel 支持的命令

| 命令 | 说明 |
|------|------|
| `FFT` / `频谱` | 执行 FFT 频谱分析 |
| `Lyapunov` / `李雅普诺夫` | 计算 Lyapunov 指数 |
| `Phase space` / `相空间` | 相空间重构（可指定 tau 和 dim） |
| `Model` / `模型` | 列出可用模型 |

示例：
- `Phase space tau=10 dim=3` - 指定延迟和维度

### API 接口调用

**获取模型列表：**
```bash
curl http://localhost:8000/models
```

**运行仿真：**
```bash
curl -X POST http://localhost:8000/mcp \
  -H "Content-Type: application/json" \
  -d '{"tool": "chaos_simulate", "params": {"model": "electrooptic_feedback", "model_params": {"N": 1000}}}'
```

**FFT 分析：**
```bash
curl -X POST http://localhost:8000/mcp \
  -H "Content-Type: application/json" \
  -d '{"tool": "fft_analysis", "params": {}, "session_id": "<从仿真获取的session_id>"}'
```

---

## 项目结构

```
ChaosTools/
├── backend/                   # 后端核心模块
│   ├── core/                  # 统一数据协议
│   │   └── data_protocol.py   # timeseries, spectrum, lyapunov, phase_space
│   │
│   ├── compute_engine/        # 数值求解引擎
│   │   ├── base_solver.py     # 抽象求解器基类
│   │   ├── dde_solver.py      # DDE 求解器 (RK4)
│   │   ├── dde_solver_numba.py # Numba 加速版
│   │   ├── dde_solver_interpolated.py # 线性插值版
│   │   └── utils.py           # delay 处理工具
│   │
│   ├── models/                # 混沌模型层
│   │   ├── base.py            # ChaosModel 抽象基类
│   │   ├── electrooptic.py    # 光电反馈模型
│   │   ├── registry.py        # 模型注册表
│   │   └── api.py             # 模型 API 接口
│   │
│   ├── skills/                # 分析技能层
│   │   ├── chaos_simulate.py  # MCP 工具: 混沌仿真
│   │   ├── fft_analysis.py    # MCP 工具: FFT 分析
│   │   ├── lyapunov.py        # MCP 工具: Lyapunov 计算
│   │   ├── phase_space.py     # MCP 工具: 相空间重构
│   │   └── list_models.py     # MCP 工具: 模型列表
│   │
│   ├── mcp/                   # MCP Server (LLM Tool Interface)
│   │   ├── types.py           # ToolRequest/ToolResponse
│   │   ├── registry.py        # 工具注册表
│   │   ├── session.py         # Session 管理
│   │   ├── executor.py        # 执行逻辑
│   │   ├── schema.py          # Tool Schema
│   │   └── server.py          # MCP Server 入口
│   │
│   ├── api/                   # HTTP API 层
│   │   └── routes.py          # FastAPI 路由
│   │
│   └── main.py                # 测试 + Demo 入口
│
├── frontend/                  # React 前端
│   ├── src/
│   │   ├── api/
│   │   │   └── client.ts      # API 客户端
│   │   ├── components/
│   │   │   ├── ModelSelector.tsx   # 模型选择
│   │   │   ├── ParameterPanel.tsx  # 参数面板
│   │   │   ├── PlotView.tsx        # Plotly 可视化
│   │   │   └── ChatPanel.tsx       # 自然语言命令
│   │   ├── pages/
│   │   │   └── MainPage.tsx        # 主页面
│   │   ├── App.tsx
│   │   └── main.tsx
│   ├── package.json
│   └── vite.config.ts
│
├── Prompt/                    # 开发提示词规范
│   ├── baseprompt.txt         # 总体架构规范
│   ├── 1.compute_engine/      # 求解器开发规范
│   ├── 4.mcp/                 # MCP Server 开发规范
│   └── 6.frontend/            # 前端开发规范
│
├── chaos.m                    # MATLAB 参考：RK4 算法
├── chaos_mes.m                # MATLAB 参考：信息耦合
├── requirements.txt           # Python 依赖
├── DEVLOG.md                  # 开发日志
└── Readme.md                  # 本文档
```

---

## MCP 工具列表

| 工具名称 | 功能 | 输入参数 | 输出类型 |
|----------|------|----------|----------|
| `chaos_simulate` | 运行混沌仿真 | model, model_params | timeseries |
| `fft_analysis` | FFT 频谱分析 | session_id | spectrum |
| `lyapunov_calculate` | Lyapunov 指数 | session_id | lyapunov |
| `phase_reconstruct` | 相空间重构 | tau, dim, session_id | phase_space |
| `list_models` | 列出模型 | detailed | model_list |
| `get_model_params` | 获取模型参数 | model | model_params |

---

## API 端点

| 端点 | 方法 | 说明 |
|------|------|------|
| `/` | GET | 健康检查 |
| `/health` | GET | 健康状态 |
| `/models` | GET | 获取所有模型 schema |
| `/models/info` | GET | 获取模型详细信息 |
| `/mcp` | POST | MCP 工具调用 |
| `/mcp/tools` | GET | 获取可用工具列表 |

---

## 模型参数

### electrooptic_feedback (光电反馈模型)

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| xin | array | [0.1, 0.1] | 初始状态 [x0, y0] |
| h | float | 1e-9 | 步长 (秒) |
| N | int | 10000 | 仿真步数 |
| T1 | float | 1e-6 | 延迟时间 (秒) |
| beta | float | 2.0 | 反馈强度 |
| phi | float | 0.5 | 相位偏移 (rad) |
| tau | float | 2.5e-11 | 时间常数 tou (秒) |
| xita | float | 5e-6 | 时间常数 xita (秒) |

### electrooptic_feedback_mes (带信息耦合)

额外参数：
| mes_bits | array | [1,0,1,1,0] | 信息比特序列 |
| mes_rate | float | 1e6 | 比特率 (bps) |

---

## 开发相关

### 运行测试

```bash
# 模块导入测试
python backend/main.py
```

### 前端构建

```bash
cd frontend
npm run build    # 生产构建
npm run preview  # 预览构建结果
```

---

## 已知问题

详见 [DEVLOG.md](DEVLOG.md) 的待解决问题部分：

1. **求解器数值溢出** - 默认参数可能导致数值不稳定，需要调整参数配置
2. **性能基准测试** - 待进行 Python vs MATLAB 性能对比
3. **Lyapunov 精确算法** - 当前使用工程近似方法

---

## 技术架构

```
用户/LLM --> HTTP API --> MCP Server --> Skills --> Compute Engine/Models
    |                                      |
    v                                      v
前端 React <-- API Client <-- JSON Response <-- Data Protocol
```

**核心设计决策：**

- **MCP = LLM Tool Interface Layer** (非 Workflow Engine)
- **Session 管理** - 解决 LLM 无状态问题
- **LLM友好数据格式** - summary + preview + full_data_ref，避免返回大数据

---

## 参考资料

- [MCP (Model Context Protocol)](https://modelcontextprotocol.io/)
- [FastAPI 文档](https://fastapi.tiangolo.com/)
- [React + Plotly](https://plotly.com/javascript/)
- MATLAB chaos.m - RK4 算法原始实现

---

## License

MIT License

---

*最后更新: 2026-04-13*