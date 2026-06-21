@echo off
rem 快速部署到 GitHub - Windows 脚本

echo ========================================
echo   微信提醒 - GitHub 快速部署
echo ========================================
echo.

if not exist .git (
    echo [1/6] 初始化 git 仓库...
    git init
    echo.
)

echo [2/6] 添加文件...
git add .
echo.

echo [3/6] 提交更改...
git commit -m "Add wechat reminder skill" 2>nul || git commit -m "Update wechat reminder skill"
echo.

echo [4/6] 检查远程仓库...
git remote -v >nul 2>&1
if errorlevel 1 (
    echo.
    echo ========================================
    echo   下一步操作
    echo ========================================
    echo.
    echo 请先在 GitHub 创建一个仓库，然后运行：
    echo.
    echo   git remote add origin https://github.com/你的用户名/仓库名.git
    echo   git branch -M main
    echo   git push -u origin main
    echo.
    echo 然后在 GitHub 仓库中配置 Secrets：
    echo   - Settings ^> Secrets and variables ^> Actions
    echo   - 添加 SCT_KEY (或其他推送服务配置)
    echo.
    echo 详细文档: docs\GITHUB_DEPLOY.md
    echo.
) else (
    echo [5/6] 推送到 GitHub...
    git branch -M main
    git push -u origin main
    echo.
    echo [6/6] 完成！
    echo.
    echo ========================================
    echo   下一步
    echo ========================================
    echo.
    echo 1. 在 GitHub 仓库中配置 Secrets:
    echo    - Settings ^> Secrets and variables ^> Actions
    echo    - 添加 SCT_KEY (你的 Server酱 SENDKEY)
    echo.
    echo 2. 启用 GitHub Actions:
    echo    - Actions ^> 微信定时提醒 ^> Enable workflow
    echo.
    echo 3. 手动测试一次:
    echo    - Actions ^> 微信定时提醒 ^> Run workflow
    echo.
    echo 详细文档: docs\GITHUB_DEPLOY.md
    echo.
)
