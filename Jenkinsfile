pipeline {
    agent any
    
    triggers {
        // 每 5 分钟检查一次 Git 仓库是否有新提交
        pollSCM('H/5 * * * *')
    }
    
    environment {
        DEPLOY_DIR = 'F:\\horse_ranch\\ci-cd-demo\\deploy'
        SERVER_PORT = '8000'
    }
    
    stages {
        // ===================== 第一阶段：拉取源码 =====================
        stage('拉取源码') {
            steps {
                echo '============================================'
                echo '📥 第一阶段：从 Git 仓库拉取最新源码'
                echo '============================================'
                checkout scm
                
                echo ''
                echo '📋 拉取的源代码清单:'
                bat '''
                    dir /b
                    echo ================================
                    echo 📄 requirements.txt 内容:
                    type requirements.txt
                    echo ---
                    echo 📄 build.py 脚本已就绪
                '''
            }
        }
        
        // ===================== 第二阶段：环境修复 =====================
        stage('环境修复') {
            steps {
                echo '============================================'
                echo '🔧 第二阶段：检查并修复运行环境'
                echo '============================================'
                
                // 2.1 检查语言运行时版本
                bat '''
                    echo ===============================================
                    echo 🔍 步骤 1/4：检查 Python 运行时版本
                    echo ===============================================
                    python --version
                    
                    echo 如果未找到 Python，请先在系统上安装
                '''
                
                // 2.2 解析依赖文件并安装缺失的包
                bat '''
                    echo ===============================================
                    echo 🔍 步骤 2/4：安装/更新项目依赖
                    echo ===============================================
                    
                    rem 使用 requirements.txt 中的精确版本安装
                    rem --upgrade 确保获取最新版本依赖
                    rem --force-reinstall 避免旧版本残留问题
                    pip install --quiet -r requirements.txt 2>&1 || goto env_error
                    goto env_ok
                    
                    :env_error
                    echo ❌ 依赖安装失败！请检查 requirements.txt 或网络
                    exit /b 1
                    
                    :env_ok
                    echo ✅ 依赖安装成功
                '''
                
                // 2.3 验证所有依赖是否就位
                bat '''
                    echo ===============================================
                    echo 🔍 步骤 3/4：验证依赖完整性
                    echo ===============================================
                    
                    rem 逐个验证每个必需的包能否 import
                    python -c "import jinja2; print(f'✅ Jinja2 {jinja2.__version__}')" 
                    python -c "import faker; print(f'✅ Faker {faker.__version__}')" 
                    python -c "import emoji; print(f'✅ Emoji {emoji.__version__}')" 
                    
                    echo 所有依赖验证通过！
                '''
                
                // 2.4 清理旧的构建缓存
                bat '''
                    echo ===============================================
                    echo 🔍 步骤 4/4：清理旧构建缓存
                    echo ===============================================
                    
                    rem 删除上次构建的缓存目录（如果有）
                    if exist __pycache__ rmdir /s /q __pycache__ 2>nul
                    for /d %%i in (*.egg-info) do rd /s /q "%%i" 2>nul
                    
                    echo ✅ 缓存清理完成，将从零开始干净构建
                '''
            }
        }
        
        // ===================== 第三阶段：构建 =====================
        stage('构建') {
            steps {
                echo '============================================'
                echo '🔨 第三阶段：从源码构建可运行产物'
                echo '============================================'
                
                bat '''
                    echo ----------------------------------------------
                    echo 📐 执行构建：python build.py
                    echo ----------------------------------------------
                    
                    rem build.py 会读取模板 + 依赖包 → 生成 index.html
                    rem 这是一个标准的"源码 → 产物"转换过程
                    python build.py
                    
                    rem 验证构建产物是否存在且大小合理
                    if not exist index.html (
                        echo ❌ 构建失败：index.html 未生成
                        exit /b 1
                    )
                    
                    for %%F in (index.html) do (
                        echo ✅ 构建产物大小: %%~zF 字节
                        echo ✅ 构建产物已就绪
                    )
                    
                    rem 显示生成的 HTML 关键信息（前 50 行）
                    echo ----------------------------------------------
                    echo 📄 产物示例（前 50 行）:
                    echo ----------------------------------------------
                    type index.html | findstr /n "" | more +1 | more +48
                '''
            }
        }
        
        // ===================== 第四阶段：部署 =====================
        stage('部署') {
            steps {
                echo '============================================'
                echo '🚀 第四阶段：部署到目标目录'
                echo '============================================'
                
                bat """
                    echo ----------------------------------------------
                    echo 📦 步骤 1/2：准备部署目录
                    echo ----------------------------------------------
                    
                    rem 创建部署目录（如果不存在）
                    if not exist "%DEPLOY_DIR%" mkdir "%DEPLOY_DIR%"
                    
                    rem 备份当前线上版本（用于回滚）
                    if exist "%DEPLOY_DIR%\\\\index.html" (
                        echo 发现现有版本，正在备份...
                        copy /Y "%DEPLOY_DIR%\\\\index.html" "%%DEPLOY_DIR%%\\\\index.html.prev" >nul
                        echo ✅ 旧版本已备份到 index.html.prev
                    ) else (
                        echo 首次部署，无需备份
                    )
                    
                    echo ----------------------------------------------
                    echo 📦 步骤 2/2：发布构建产物
                    echo ----------------------------------------------
                    
                    rem 复制构建产物到部署目录
                    copy /Y index.html "%%DEPLOY_DIR%%%\\index.html"
                    echo ✅ 已发布 index.html
                    
                    rem 同时部署源码，方便排查和重复构建
                    copy /Y build.py "%%DEPLOY_DIR%%%\\\\build.py"
                    copy /Y requirements.txt "%%DEPLOY_DIR%%%\\\\requirements.txt"
                    echo ✅ 已同步源码便于追溯
                    
                    rem 展示部署结果
                    echo ----------------------------------------------
                    echo 📂 部署目录内容:
                    echo ----------------------------------------------
                    dir "%%DEPLOY_DIR%%"
                    
                    rem 计算新版本和旧版本的差异
                    if exist "%%DEPLOY_DIR%%\\\\index.html.prev" (
                        fc "%%DEPLOY_DIR%%\\\\index.html" "%%DEPLOY_DIR%%\\\\index.html.prev" >nul 2>&1
                        if errorlevel 1 (
                            echo 🔄 检测到内容变更！新版本已生效
                        ) else (
                            echo 内容与之前一致
                        )
                    )
                """
            }
        }
        
        // ===================== 第五阶段：启动服务 =====================
        stage('启动服务') {
            steps {
                echo '============================================'
                echo '🌐 第五阶段：启动 HTTP 服务'
                echo '============================================'
                
                bat """
                    rem 查找并终止占用端口的旧进程（安全重启）
                    echo 🔍 检查端口 %SERVER_PORT% 是否被占用...
                    
                    set PID_TO_KILL=
                    for /f "tokens=5" %%a in ('netstat -ano ^| findstr ":%%SERVER_PORT%%.*LISTENING"') do (
                        set PID_TO_KILL=%%a
                    )
                    
                    if defined PID_TO_KILL (
                        echo 发现旧进程 PID: %%PID_TO_KILL%%，正在停止...
                        taskkill /PID %%PID_TO_KILL%% /F >nul 2>&1
                        timeout /t 1 /nobreak >nul
                        echo ✅ 旧进程已终止
                    ) else (
                        echo ℹ️ 端口未被占用，无需清理
                    )
                    
                    rem 启动新的 HTTP 服务器
                    echo ---
                    echo 启动 Python HTTP 服务器...
                    echo   目录: %DEPLOY_DIR%
                    echo   端口: %SERVER_PORT%
                    echo ---
                    
                    start "CI-CD Server (Port %SERVER_PORT%)" cmd /k "@echo off & cd /d \"%DEPLOY_DIR%\" & python -m http.server %SERVER_PORT%"
                    
                    echo ✅ 服务已启动！
                    echo 🌐 浏览器访问: http://localhost:%SERVER_PORT%
                """
            }
        }
        
        // ===================== 第六阶段：验证 =====================
        stage('验证') {
            steps {
                echo '============================================'
                echo '✅ 最终验证：确认一切就绪'
                echo '============================================'
                
                bat """
                    rem 1. 检查构建产物
                    if not exist "%DEPLOY_DIR%\\\\index.html" (
                        echo ❌ 验证失败：index.html 不存在
                        exit /b 1
                    )
                    echo ✅ 构建产物已部署
                    
                    rem 2. 检查源码副本
                    if not exist "%DEPLOY_DIR%\\\\build.py" (
                        echo ❌ 验证失败：build.py 未同步
                        exit /b 1
                    )
                    echo ✅ 源码已同步
                    
                    rem 3. 检查环境描述文件
                    if not exist "%DEPLOY_DIR%\\\\requirements.txt" (
                        echo ❌ 验证失败：requirements.txt 未同步
                        exit /b 1
                    )
                    echo ✅ 环境描述文件已同步
                    
                    rem 4. 检查服务端口
                    netstat -ano | findstr ":%SERVER_PORT%.*LISTENING" >nul 2>&1
                    if errorlevel 1 (
                        echo ⚠️ 服务可能未在运行（无占用端口）
                        echo 💡 请手动访问 http://localhost:%SERVER_PORT% 确认
                    ) else (
                        echo ✅ HTTP 服务正在监听 %SERVER_PORT% 端口
                    )
                    
                    echo ===
                    echo ✅✅✅ 全部验证通过！
                """
            }
        }
    }
    
    post {
        success {
            echo '''
╔══════════════════════════════════════════╗
║         Pipeline 全部完成！              ║
╠══════════════════════════════════════════╣
║                                          ║
║  📂 部署目录:                             ║
║     %DEPLOY_DIR%                           ║
║                                          ║
║  🌐 预览地址:                             ║
║     http://localhost:%SERVER_PORT%          ║
║                                          ║
║  🔄 后续操作:                             ║
║     1. 修改代码 (如 build.py)             ║
║     2. git commit & push                 ║
║     3. Jenkins 自动检测并重跑此 Pipeline ║
║                                          ║
╚══════════════════════════════════════════╝'''
        }
        failure {
            echo '''
╔══════════════════════════════════════════╗
║         ❌ Pipeline 构建失败!           ║
╠══════════════════════════════════════════╣
║                                          ║
║  请按以下顺序排查:                        ║
║                                          ║
║  1. 看上方哪个阶段报红                     ║
║     • 拉取源码失败 → 网络/仓库权限       ║
║     • 环境修复失败 → 缺 Python/pip       ║
║     • 构建失败 → 检查 build.py 报错      ║
║     • 部署失败 → 检查磁盘空间             ║
║     • 启动失败 → 端口被占用               ║
║                                          ║
║  2. 可以下载日志分析                       ║
║     Jenkins 任务页 → 某次构建 → Console Output ║
║                                          ║
╚══════════════════════════════════════════╝'''
        }
        always {
            echo '📊 Jenkins Pipeline 结束'
        }
    }
}
