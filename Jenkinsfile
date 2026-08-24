pipeline {
    agent any
    
    triggers {
        // 每 5 分钟检查一次 Git 仓库是否有新提交
        pollSCM('H/5 * * * *')
    }
    
    environment {
        DEPLOY_DIR = 'F:\\horse_ranch\\ci-cd-demo\\deploy'
        SERVER_PORT = '8000'
        VENV_DIR = '.venv'
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
                '''
            }
        }
        
        // ===================== 第二阶段：环境修复（自动建虚拟环境） =====================
        stage('环境修复') {
            steps {
                script {
                    // 2.1 创建 Python 虚拟环境
                    bat '''
                        echo ===============================================
                        echo 🔧 步骤 1/5：创建 Python 虚拟环境
                        echo ===============================================
                        
                        echo 删除旧虚拟环境...
                        if exist "%VENV_DIR%" rmdir /s /q "%VENV_DIR%"
                        
                        echo 正在创建新的虚拟环境到 .venv ...
                        python -m venv %VENV_DIR%
                        
                        if not exist "%VENV_DIR%\\\\Scripts\\\\python.exe" (
                            echo ❌ 虚拟环境创建失败！请确认 Python 已安装。
                            exit /b 1
                        )
                        
                        echo ---
                        echo ✅ 虚拟环境创建成功
                        "%VENV_DIR%\\\\Scripts\\\\python.exe" --version
                    '''
                    
                    // 2.2 升级 pip、setuptools、wheel
                    bat '''
                        echo ===============================================
                        echo 🔧 步骤 2/5：升级构建工具
                        echo ===============================================
                        
                        rem 升级 pip 和核心构建工具
                        "%VENV_DIR%\\\\Scripts\\\\python.exe" -m pip install --upgrade pip setuptools wheel
                        
                        echo ✅ pip/setuptools/wheel 已升级到最新版本
                    '''
                    
                    // 2.3 安装 requirements.txt 中的依赖
                    bat '''
                        echo ===============================================
                        echo 🔧 步骤 3/5：安装项目依赖
                        echo ===============================================
                        
                        echo 正在从 requirements.txt 安装依赖...
                        echo ---
                        "%VENV_DIR%\\\\Scripts\\\\python.exe" -m pip install -r requirements.txt
                        
                        echo ---
                        echo ✅ 所有依赖安装完成
                    '''
                    
                    // 2.4 验证依赖完整性
                    bat '''
                        echo ===============================================
                        echo 🔧 步骤 4/5：验证依赖包完整性
                        echo ===============================================
                        
                        echo 逐个验证 import...
                        "%VENV_DIR%\\\\Scripts\\\\python.exe" -c "import jinja2; print(f'✅ Jinja2 %%jinja2.__version%%')"
                        "%VENV_DIR%\\\\Scripts\\\\python.exe" -c "import faker; print(f'✅ Faker %%faker.__version%%')"
                        "%VENV_DIR%\\\\Scripts\\\\python.exe" -c "import emoji; print(f'✅ Emoji %%emoji.__version%%')"
                        
                        echo ---
                        echo 📦 虚拟环境中所有已安装包:
                        "%VENV_DIR%\\\\Scripts\\\\python.exe" -m pip list
                        
                        echo ================================
                        echo ✅ 依赖验证全部通过！
                    '''
                    
                    // 2.5 清理构建缓存
                    bat '''
                        echo ===============================================
                        echo 🔧 步骤 5/5：清理构建缓存
                        echo ===============================================
                        
                        rem 删除 __pycache__ 目录
                        for /d /r %%d in (__pycache__) do @if exist "%%d" rd /s /q "%%d" 2>nul
                        
                        rem 删除 egg-info 目录
                        for /d %%i in (*.egg-info) do rd /s /q "%%i" 2>nul
                        
                        echo ✅ 缓存已清理，将从零开始干净构建
                    '''
                }
            }
        }
        
        // ===================== 第三阶段：构建 =====================
        stage('构建') {
            steps {
                script {
                    bat '''
                        echo ===============================================
                        echo 🔨 第三阶段：使用虚拟环境的 Python 进行构建
                        echo ===============================================
                        
                        rem 明确使用虚拟环境中的 Python，确保隔离性
                        echo 🐍 使用的 Python: %VENV_DIR%\\\\Scripts\\\\python.exe
                        "%VENV_DIR%\\\\Scripts\\\\python.exe" --version
                        
                        echo ---
                        echo 📐 执行构建：build.py
                        
                        rem build.py 会读取模板 + 依赖包 → 生成 index.html
                        rem 这是一个标准的"源码 → 产物"转换过程
                        "%VENV_DIR%\\\\Scripts\\\\python.exe" build.py
                        
                        rem 验证构建产物是否存在且大小合理
                        if not exist index.html (
                            echo ❌ 构建失败：index.html 未生成
                            exit /b 1
                        )
                        
                        for %%F in (index.html) do (
                            echo ✅ 构建产物大小: %%~zF 字节
                            echo ✅ 构建产物已就绪
                        )
                        
                        echo ---
                        echo 📄 产物示例（前 50 行）:
                        echo ----------------------------------------------
                        type index.html | findstr /n "" | more +1 | more +48
                    '''
                }
            }
        }
        
        // ===================== 第四阶段：部署 =====================
        stage('部署') {
            steps {
                script {
                    bat """
                        echo ===============================================
                        echo 🚀 第四阶段：部署到目标目录
                        echo ===============================================
                        
                        echo ----------------------------------------------
                        echo 📦 步骤 1/2：准备部署目录
                        echo ----------------------------------------------
                        
                        rem 创建部署目录（如果不存在）
                        if not exist "%DEPLOY_DIR%" mkdir "%DEPLOY_DIR%"
                        
                        rem 备份当前线上版本（用于回滚）
                        if exist "%DEPLOY_DIR%\\\\\\\\index.html" (
                            echo 发现现有版本，正在备份...
                            copy /Y "%DEPLOY_DIR%\\\\\\\\index.html" "%%DEPLOY_DIR%%\\\\\\\\index.html.prev" >nul
                            echo ✅ 旧版本已备份到 index.html.prev
                        ) else (
                            echo 首次部署，无需备份
                        )
                        
                        echo ----------------------------------------------
                        echo 📦 步骤 2/2：发布构建产物
                        echo ----------------------------------------------
                        
                        rem 复制构建产物到部署目录
                        copy /Y index.html "%%DEPLOY_DIR%%%\\\\index.html"
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
                        
                        rem 对比新旧版本检测变更
                        if exist "%%DEPLOY_DIR%%\\\\\\\\index.html.prev" (
                            fc "%%DEPLOY_DIR%%\\\\\\\\index.html" "%%DEPLOY_DIR%%\\\\\\\\index.html.prev" >nul 2>&1
                            if errorlevel 1 (
                                echo 🔄 检测到内容变更！新版本已生效
                            ) else (
                                echo 内容与之前一致
                            )
                        )
                    """
                }
            }
        }
        
        // ===================== 第五阶段：启动服务 =====================
        stage('启动服务') {
            steps {
                script {
                    bat """
                        echo ===============================================
                        echo 🌐 第五阶段：启动 HTTP 服务
                        echo ===============================================
                        
                        rem 查找并终止占用端口的旧进程（安全重启）
                        echo 🔍 检查端口 %SERVER_PORT% 是否被占用...
                        
                        set PID_TO_KILL=
                        for /f "tokens=5" %%a in ('netstat -ano ^| findstr ":%%SERVER_PORT%%.*LISTENING"') do (
                            set PID_TO_KILL=%%a
                        )
                        
                        if defined PID_TO_KILL (
                            echo 发现旧进程 PID: %%PID_TO_KILL%%，正在停止...
                            taskkill /PID %%PID_TO_KILL%% /F >nul 2>&1
                            timeout /t 2 /nobreak >nul
                            echo ✅ 旧进程已终止
                        ) else (
                            echo ℹ️ 端口未被占用，无需清理
                        )
                        
                        rem 等待端口完全释放
                        timeout /t 1 /nobreak >nul
                        
                        rem 启动新的 HTTP 服务器（使用虚拟环境中的 Python）
                        echo ---
                        echo 启动 Python HTTP 服务器...
                        echo   目录: %DEPLOY_DIR%
                        echo   端口: %SERVER_PORT%
                        echo   Python: %VENV_DIR%\\\\Scripts\\\\python.exe
                        echo ---
                        
                        start "CI-CD Server (Port %SERVER_PORT%)" cmd /k "@echo off & cd /d \"%DEPLOY_DIR%\" & %VENV_DIR%\\\\Scripts\\\\python.exe -m http.server %SERVER_PORT%"
                        
                        echo ✅ 服务已启动！
                        echo 🌐 浏览器访问: http://localhost:%SERVER_PORT%
                    """
                }
            }
        }
        
        // ===================== 第六阶段：验证 =====================
        stage('验证') {
            steps {
                script {
                    bat """
                        echo ===============================================
                        echo ✅ 最终验证：确认一切就绪
                        echo ===============================================
                        
                        rem 1. 检查构建产物
                        if not exist "%DEPLOY_DIR%\\\\\\\\index.html" (
                            echo ❌ 验证失败：index.html 不存在
                            exit /b 1
                        )
                        echo ✅ 构建产物已部署
                        
                        rem 2. 检查源码副本
                        if not exist "%DEPLOY_DIR%\\\\\\\\build.py" (
                            echo ❌ 验证失败：build.py 未同步
                            exit /b 1
                        )
                        echo ✅ 源码已同步
                        
                        rem 3. 检查环境描述文件
                        if not exist "%DEPLOY_DIR%\\\\\\\\requirements.txt" (
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
                        
                        rem 5. 检查虚拟环境
                        if exist "%VENV_DIR%\\\\Scripts\\\\python.exe" (
                            echo ✅ 虚拟环境存在且可用
                            echo 📊 虚拟环境 Python 版本:
                            %VENV_DIR%\\\\Scripts\\\\python.exe --version
                        ) else (
                            echo ⚠️ 虚拟环境似乎丢失，下次构建将重新创建
                        )
                        
                        echo ===
                        echo ✅✅✅ 全部验证通过！
                    """
                }
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
║  📦 虚拟环境:                             ║
║     .venv/ (Python 隔离环境)               ║
║     • 不污染系统 Python                   ║
║     • 每次构建从零重建                    ║
║     • 依赖完全可重现                       ║
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
║     • 环境修复失败 → 缺 Python/venv      ║
║     • 构建失败 → 检查 build.py 报错      ║
║     • 部署失败 → 检查磁盘空间             ║
║     • 启动失败 → 端口被占用               ║
║                                          ║
║  2. 可以下载日志分析                       ║
║     Jenkins 任务页 → Console Output       ║
║                                          ║
╚══════════════════════════════════════════╝'''
        }
        always {
            echo '📊 Jenkins Pipeline 结束'
        }
    }
}
