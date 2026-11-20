"""
校园报修系统 · 后端入口（第 4 周骨架）

这周只要求它能跑起来。第 5 周会在这里逐步加上：数据库、提交报修、派单、处理……

启动（在 repair_system 文件夹里）：
    uvicorn app.main:app --reload
然后浏览器打开：
    http://127.0.0.1:8000/health   → 看到 {"status":"ok"} 就成功了
    http://127.0.0.1:8000/docs     → FastAPI 自动生成的接口文档，后面几周天天用
"""
from fastapi import FastAPI

app = FastAPI(title="校园报修系统", version="0.0.1")


@app.get("/health")
def health():
    """健康检查：部署后运维会用它判断服务是不是活着。"""
    return {"status": "ok"}


@app.get("/api/categories")
def categories():
    """报修类别。—— 这是你们小组的第一个"需求驱动"接口：
    类别从哪来？来自访谈记录里李师傅的那段话。需求定稿后，如果类别有调整，改这里。"""
    return ["水电", "门窗", "家具", "空调", "网络", "其他"]


# TODO（第 4 周作业 · 选做）：
#   参照上面的写法，加一个 GET /api/team 接口，返回你们小组的成员和分工，
#   例如 [{"name": "张三", "role": "后端负责人", "major": "计算机"}]
#   然后在 tests/test_health.py 里给它写一个测试。
