@echo off
REM Isaac API Document Processor - Docker启动脚本 (Windows)
setlocal enabledelayedexpansion

cls
echo.
echo ========================================
echo   Isaac API Document Processor
echo ========================================
echo.

REM 检查 .env 文件
if not exist ".env" (
    echo 创建默认 .env 文件...
    (
        echo # 在这里填入你的 DeepSeek API Key ^(Anthropic 兼容接口^)
        echo ANTHROPIC_API_KEY=sk-your-api-key-here
        echo ANTHROPIC_BASE_URL=https://api.deepseek.com/anthropic
        echo.
        echo # 日志级别 [INFO, DEBUG, WARNING, ERROR]
        echo LOG_LEVEL=INFO
    ) > .env
    echo.
    echo 已创建 .env 文件，请编辑并填入 ANTHROPIC_API_KEY
    echo.
    pause
)

REM 检查 API Key
findstr /M "sk-your-api-key-here" .env > nul
if !errorlevel! equ 0 (
    echo.
    echo 错误: 请先在 .env 文件中设置 ANTHROPIC_API_KEY
    echo 示例: ANTHROPIC_API_KEY=sk-xxxxxxxxxxxx
    echo.
    pause
    exit /b 1
)

set HAS_API_KEY=0
findstr /R /C:"^ANTHROPIC_API_KEY=sk-" .env > nul
if !errorlevel! equ 0 set HAS_API_KEY=1
findstr /R /C:"^DEEPSEEK_API_KEY=sk-" .env > nul
if !errorlevel! equ 0 set HAS_API_KEY=1

if !HAS_API_KEY! equ 0 (
    echo.
    echo 错误: 未检测到有效 API Key，请设置 ANTHROPIC_API_KEY（或兼容 DEEPSEEK_API_KEY）
    echo 示例: ANTHROPIC_API_KEY=sk-xxxxxxxxxxxx
    echo.
    pause
    exit /b 1
)

REM 检查 Docker
docker --version >nul 2>&1
if !errorlevel! neq 0 (
    echo.
    echo 错误: Docker 未安装或不在系统路径中
    echo.
    pause
    exit /b 1
)

echo 环境检查通过
echo.
echo 构建 Docker 镜像...
docker compose build --quiet
if !errorlevel! neq 0 (
    echo.
    echo 错误: Docker 镜像构建失败
    echo.
    pause
    exit /b 1
)

echo.
echo 创建输出目录...
if not exist "processed_docs" mkdir processed_docs

echo.
echo 开始处理 Isaac API 文档...
echo.
docker compose run --rm isaac-processor

echo.
echo ========================================
echo   完成！
echo   结果已保存到 processed_docs/ 目录
echo ========================================
echo.
pause
