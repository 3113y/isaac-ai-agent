# Docker 使用指南

本项目使用 Docker 容器化，确保在任何系统上都能以完全相同的方式运行，无需配置 Python 环境。

## 前置要求

| 系统 | 要求 |
|------|------|
| Windows | Docker Desktop 4.0+ |
| Mac | Docker Desktop 4.0+ |
| Linux | Docker 20.10+, Docker Compose 2.0+ |

## 三步启动

### 1. 获取代码

```bash
git clone <repository-url>
cd AgentTheIsaac
```

### 2. 配置 API Key

编辑 `.env` 文件：

```env
DEEPSEEK_API_KEY=sk-your-key-here
```

从 https://platform.deepseek.com 免费获取。

### 3. 运行

**Windows:**
```powershell
.\run.bat
```

**Mac/Linux:**
```bash
./run.sh
```

处理完成后，结果在 `processed_docs/` 目录中。

---

## 输出文件

```
processed_docs/
├── processed_apis.json      # 提取的 API 数据
├── rag_knowledge_base.json  # RAG 系统知识库
└── report.json              # 处理统计报告
```

### `processed_apis.json`

```json
[
  {
    "filename": "EntityPlayer.md",
    "title": "EntityPlayer",
    "methods_count": 42,
    "methods": [
      {
        "name": "GetMovementDirection",
        "signature": "() -> Vector",
        "description": "..."
      }
    ]
  }
]
```

### `rag_knowledge_base.json`

```json
[
  {
    "class": "EntityPlayer",
    "function": "GetMovementDirection",
    "signature": "() -> Vector",
    "description": "...",
    "enhancement": {
      "summary": "...",
      "use_cases": ["..."],
      "key_methods": ["..."]
    }
  }
]
```

### `report.json`

```json
{
  "total_classes": 70,
  "total_methods": 1250,
  "total_api_entries": 1250,
  "stats": {
    "total_files": 70,
    "processed_files": 70,
    "errors": 0
  }
}
```

---

## 配置说明

### 必需配置

**DEEPSEEK_API_KEY** — 从 https://platform.deepseek.com 获取，填入 `.env` 文件。

### 可选配置

```env
LOG_LEVEL=INFO              # INFO | DEBUG | WARNING | ERROR
```

---

## 常用命令

```bash
# 查看镜像
docker images | grep isaac

# 运行处理器
docker compose run --rm isaac-processor

# 进入容器
docker compose run --rm isaac-processor bash

# 查看日志
docker compose logs isaac-processor

# 重新运行（覆盖之前的结果）
docker compose run --rm isaac-processor

# 停止并清理容器
docker compose down

# 删除镜像
docker rmi isaac-api-processor:latest

# 清理所有未使用资源
docker system prune -a
```

---

## 国内网络配置

如果 Docker 构建时网络缓慢或超时，配置国内镜像源。

### Docker Desktop (Windows/Mac)

打开 Docker Desktop → Settings → Docker Engine，添加：

```json
{
  "registry-mirrors": [
    "https://hub-mirror.c.163.com",
    "https://mirror.baidubce.com"
  ]
}
```

### Linux

编辑 `/etc/docker/daemon.json`，添加同上内容，然后：

```bash
sudo systemctl restart docker
```

---

## 离线构建（无需网络）

```bash
# 1. 生成依赖列表
pip freeze > requirements.txt

# 2. 下载依赖到本地
pip download -r requirements.txt -d ./wheels
```

然后修改 Dockerfile 使用本地 wheels 安装。

---

## 故障排除

| 问题 | 解决方案 |
|------|---------|
| Docker 未安装 | 下载 Docker Desktop: https://docker.com |
| API Key 缺失 | 编辑 .env 文件，填入 DEEPSEEK_API_KEY |
| 构建超时 | 配置 Docker 国内镜像源（见上方） |
| 权限错误 (Mac/Linux) | 运行 `chmod +x run.sh` |
| `Error: No such file or directory` | 确认 docs 目录在项目根目录 |
| `Permission denied` | 运行 `docker compose down` 后重试 |

---

## 本地运行（备选）

如果不想使用 Docker，参见 [QUICKSTART.md](QUICKSTART.md)。
