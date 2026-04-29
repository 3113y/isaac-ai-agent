#!/bin/bash
# Isaac API Document Processor - Docker启动脚本

set -e

# 颜色输出
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${GREEN}🚀 Isaac API Document Processor${NC}\n"

# 检查 .env 文件
if [ ! -f ".env" ]; then
    echo -e "${YELLOW}⚠️  .env 文件不存在，创建默认配置...${NC}"
    cat > .env << 'EOF'
# 在这里填入你的 DeepSeek API Key (Anthropic 兼容接口)
ANTHROPIC_API_KEY=sk-your-api-key-here
ANTHROPIC_BASE_URL=https://api.deepseek.com/anthropic

# 日志级别 (INFO, DEBUG, WARNING, ERROR)
LOG_LEVEL=INFO
EOF
    echo -e "${YELLOW}📝 已创建 .env 文件，请编辑并填入 ANTHROPIC_API_KEY${NC}\n"
fi

# 检查 API Key
if grep -q "sk-your-api-key-here" .env || ! grep -Eq "^(ANTHROPIC_API_KEY|DEEPSEEK_API_KEY)=sk-" .env; then
    echo -e "${RED}❌ 请先在 .env 文件中设置 ANTHROPIC_API_KEY（或兼容 DEEPSEEK_API_KEY）${NC}"
    echo -e "${RED}   ANTHROPIC_API_KEY=sk-xxxxxxxxxxxx${NC}\n"
    exit 1
fi

# 检查 Docker
if ! command -v docker &> /dev/null; then
    echo -e "${RED}❌ Docker 未安装${NC}"
    exit 1
fi

echo -e "${GREEN}✅ 环境检查通过${NC}\n"

# 构建镜像
echo -e "${GREEN}📦 构建 Docker 镜像...${NC}"
docker compose build --quiet

# 创建输出目录
mkdir -p processed_docs

# 运行
echo -e "${GREEN}🔄 开始处理 Isaac API 文档...${NC}\n"
docker compose run --rm isaac-processor

echo -e "\n${GREEN}✅ 完成！${NC}"
echo -e "${GREEN}📁 结果已保存到 processed_docs/ 目录${NC}"
