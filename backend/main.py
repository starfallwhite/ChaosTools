"""
混沌系统仿真平台 - MCP Server 入口

运行此文件启动 MCP Server：
    python -m backend.main

测试模块：
    python -m backend.main test

演示调用：
    python -m backend.main demo
"""

import sys


def test_modules():
    """测试模块导入"""
    print("\n========== Module Import Test ==========\n")

    errors = []

    # 测试 core
    try:
        from backend.core import data_protocol
        print("[OK] backend.core.data_protocol")
    except Exception as e:
        print(f"[FAIL] backend.core: {e}")
        errors.append(("core", str(e)))

    # 测试 compute_engine
    try:
        from backend.compute_engine import DDESolver
        solver = DDESolver()
        print("[OK] backend.compute_engine (DDESolver)")
    except Exception as e:
        print(f"[FAIL] backend.compute_engine: {e}")
        errors.append(("compute_engine", str(e)))

    # 测试 models
    try:
        from backend.models import list_models, MODEL_REGISTRY
        models = list_models()
        print(f"[OK] backend.models (available: {models})")
    except Exception as e:
        print(f"[FAIL] backend.models: {e}")
        errors.append(("models", str(e)))

    # 测试 skills
    try:
        from backend.skills import list_skills
        skills = list_skills()
        print(f"[OK] backend.skills (Skill classes: {skills})")
    except Exception as e:
        print(f"[FAIL] backend.skills: {e}")
        errors.append(("skills", str(e)))

    # 测试 MCP 模块
    print("\n---------- MCP Module Test ----------\n")

    try:
        from backend.mcp.types import ToolRequest, ToolResponse
        req = ToolRequest("test", {}, "sid")
        resp = ToolResponse("success", {}, "sid")
        print("[OK] backend.mcp.types (ToolRequest/ToolResponse)")
    except Exception as e:
        print(f"[FAIL] backend.mcp.types: {e}")
        errors.append(("mcp.types", str(e)))

    try:
        from backend.mcp.registry import tool_registry
        print(f"[OK] backend.mcp.registry (tools: {tool_registry.list()})")
    except Exception as e:
        print(f"[FAIL] backend.mcp.registry: {e}")
        errors.append(("mcp.registry", str(e)))

    try:
        from backend.mcp.session import session_manager
        sid = session_manager.create_session()
        print(f"[OK] backend.mcp.session (session: {sid[:8]}...)")
    except Exception as e:
        print(f"[FAIL] backend.mcp.session: {e}")
        errors.append(("mcp.session", str(e)))

    try:
        from backend.mcp.schema import get_all_schemas
        schemas = get_all_schemas()
        print(f"[OK] backend.mcp.schema (schemas: {len(schemas)})")
        for s in schemas:
            print(f"    - {s['name']}")
    except Exception as e:
        print(f"[FAIL] backend.mcp.schema: {e}")
        errors.append(("mcp.schema", str(e)))

    try:
        from backend.mcp.server import mcp_server, call_tool
        tools = mcp_server.get_tools()
        print(f"[OK] backend.mcp.server (tools: {len(tools)})")
    except Exception as e:
        print(f"[FAIL] backend.mcp.server: {e}")
        errors.append(("mcp.server", str(e)))

    # 测试 MCP 工具函数
    print("\n---------- MCP Tools Test ----------\n")

    try:
        # 导入工具模块（自动注册）
        import backend.skills.chaos_simulate
        import backend.skills.fft_analysis
        import backend.skills.lyapunov
        import backend.skills.phase_space

        registered = tool_registry.list()
        print(f"[OK] MCP tools registered: {registered}")
    except Exception as e:
        print(f"[FAIL] MCP tools: {e}")
        errors.append(("tools", str(e)))

    # 总结
    print("\n========== Test Summary ==========\n")

    if errors:
        print(f"Found {len(errors)} errors:")
        for module, err in errors:
            print(f"  - {module}: {err}")
        return False
    else:
        print("All module tests passed!")
        return True


def demo_mcp_call():
    """演示 MCP 工具调用（完整链式调用）"""
    print("\n========== MCP Call Demo ==========\n")

    from backend.mcp import call_tool

    session_id = None

    # 0. list_models（新增）
    print("0. list_models...")
    result0 = call_tool("list_models", {"detailed": False})

    if result0.get("status") == "success":
        models = result0.get("data", {}).get("data", {}).get("models", [])
        print(f"   [OK] models: {models}")
    else:
        print(f"   [FAIL] {result0.get('data', {}).get('error')}")

    # 1. chaos_simulate
    print("1. chaos_simulate...")
    result1 = call_tool("chaos_simulate", {
        "model": "electrooptic_feedback",
        "model_params": {
            "h": 0.001,
            "N": 1000,
            "T1": 0.1,
            "beta": 3.0,
            "phi": 0.5,
            "tau": 1.0,
            "xita": 0.1
        }
    })

    if result1.get("status") == "success":
        data = result1.get("data", {})
        summary = data.get("summary", {})
        print(f"   [OK] length={summary.get('length')}")
        session_id = result1.get("session_id")
        print(f"   session: {session_id[:8]}...")
    else:
        print(f"   [FAIL] {result1.get('data', {}).get('error')}")
        return

    # 2. fft_analysis
    print("\n2. fft_analysis...")
    result2 = call_tool("fft_analysis", {}, session_id=session_id)

    if result2.get("status") == "success":
        data = result2.get("data", {})
        summary = data.get("summary", {})
        print(f"   [OK] dominant_freq={summary.get('dominant_freq')}")
    else:
        print(f"   [FAIL] {result2.get('data', {}).get('error')}")

    # 3. lyapunov_calculate
    print("\n3. lyapunov_calculate...")
    result3 = call_tool("lyapunov_calculate", {}, session_id=session_id)

    if result3.get("status") == "success":
        data = result3.get("data", {})
        # 兼容两种格式
        lambda_max = data.get("lambda_max") or data.get("data", {}).get("lambda_max")
        interp = data.get("interpretation", "")
        if lambda_max is not None:
            print(f"   [OK] lambda_max={lambda_max:.4f}")
        else:
            print(f"   [OK] result={data}")
        if interp:
            print(f"   interpretation: {interp}")
    else:
        print(f"   [FAIL] {result3.get('data', {}).get('error')}")

    # 4. phase_reconstruct
    print("\n4. phase_reconstruct...")
    result4 = call_tool("phase_reconstruct", {
        "tau": 10,
        "dim": 2
    }, session_id=session_id)

    if result4.get("status") == "success":
        data = result4.get("data", {})
        summary = data.get("summary", {})
        print(f"   [OK] points={summary.get('num_points')}, dim={summary.get('embedding_dim')}")
    else:
        print(f"   [FAIL] {result4.get('data', {}).get('error')}")

    print("\nDemo completed!")


if __name__ == "__main__":
    if len(sys.argv) > 1:
        arg = sys.argv[1]

        if arg == "test":
            success = test_modules()
            sys.exit(0 if success else 1)

        elif arg == "demo":
            if test_modules():
                demo_mcp_call()
            sys.exit(0)

        else:
            print(f"Usage: python -m backend.main [test|demo]")
            sys.exit(1)

    else:
        test_modules()