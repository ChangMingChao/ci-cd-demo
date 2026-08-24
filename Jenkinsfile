pipeline {
    agent any
    
    triggers {
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
                
                bat '''
                    dir /b
                    echo ================================
                    echo 📄 requirements.txt 内容:
                    type requirements.txt
                '''
            }
        }
        
        // ===================== 第二阶段：环境修复 =====================
        stage('环境修复') {
            steps {
                // 2.1 复用已有虚拟环境，不存在才创建
                bat '''
                    echo ===============================================
                    echo 🔧 步骤 1/5：检查/创建 Python 虚拟环境
                    echo ===============================================
                    
                    if exist "%VENV_DIR%\\Scripts\\python.exe" (
                        echo ✅ 发现已有虚拟环境，直接复用（增量修复模式）
                        echo 📊 当前 Python 版本:
                        "%VENV_DIR%\\Scripts\\python.exe" --version
                        echo ---
                        echo 📦 当前已安装的包:
                        "%VENV_DIR%\\Scripts\\python.exe" -m pip list --format=columns
                    ) else (
                        echo 🔨 未找到虚拟环境，首次创建...
                        python -m venv %VENV_DIR%
                        
                        if not exist "%VENV_DIR%\\Scripts\\python.exe" (
                            echo ❌ 虚拟环境创建失败！请确认 Python 已安装。
                            exit /b 1
                        )
                        echo ✅ 虚拟环境首次创建成功
                        "%VENV_DIR%\\Scripts\\python.exe" --version
                    )
                '''
                
                // 2.2 升级 pip
                bat '''
                    echo ===============================================
                    echo 🔧 步骤 2/5：检查并升级 pip 工具链
                    echo ===============================================
                    
                    "%VENV_DIR%\\Scripts\\python.exe" -m pip install --upgrade pip setuptools wheel
                    echo ✅ pip 工具链已是最新
                '''
                
                // 2.3 安装依赖（幂等：已装跳过，缺的才补）
                bat '''
                    echo ===============================================
                    echo 🔧 步骤 3/5：安装/补全项目依赖
                    echo ===============================================
                    
                    echo 正在从 requirements.txt 安装依赖...
                    echo pip install 是幂等的：已安装的包会跳过，只补全缺失的
                    echo ---
                    "%VENV_DIR%\\Scripts\\python.exe" -m pip install -r requirements.txt
                    echo ---
                    echo ✅ 依赖安装/补全完成
                '''
                
                // 2.4 验证依赖
                bat '''
                    echo ===============================================
                    echo 🔧 步骤 4/5：验证依赖包完整性
                    echo ===============================================
                    
                    echo 逐个验证 import...
                    "%VENV_DIR%\\Scripts\\python.exe" -c "import jinja2; print(f'✅ Jinja2 {jinja2.__version__}')"
                    "%VENV_DIR%\\Scripts\\python.exe" -c "import importlib.metadata; print('✅ Faker', importlib.metadata.version('faker'))"
                    "%VENV_DIR%\\Scripts\\python.exe" -c "import emoji; print(f'✅ Emoji {emoji.__version__}')"
                    
                    echo ---
                    echo 📦 虚拟环境中所有已安装包:
                    "%VENV_DIR%\\Scripts\\python.exe" -m pip list
                    
                    echo ================================
                    echo ✅ 依赖验证全部通过！
                '''
                
                // 2.5 清理缓存
                bat '''
                    echo ===============================================
                    echo 🔧 步骤 5/5：清理构建缓存
                    echo ===============================================
                    
                    for /d /r %%d in (__pycache__) do @if exist "%%d" rd /s /q "%%d" 2>nul
                    for /d %%i in (*.egg-info) do rd /s /q "%%i" 2>nul
                    
                    echo ✅ 缓存已清理
                '''
            }
        }
        
        // ===================== 第三阶段：构建 =====================
        stage('构建') {
            steps {
                bat '''
                    echo ===============================================
                    echo 🔨 第三阶段：使用虚拟环境的 Python 进行构建
                    echo ===============================================
                    
                    echo 🐍 使用的 Python: %VENV_DIR%\\Scripts\\python.exe
                    "%VENV_DIR%\\Scripts\\python.exe" --version
                    
                    echo ---
                    echo 📐 执行构建：build.py
                    "%VENV_DIR%\\Scripts\\python.exe" build.py
                    
                    if not exist index.html (
                        echo ❌ 构建失败：index.html 未生成
                        exit /b 1
                    )
                    
                    for %%F in (index.html) do (
                        echo ✅ 构建产物大小: %%~zF 字节
                        echo ✅ 构建产物已就绪
                    )
                    
                    echo ---
                    echo 📄 产物预览（前 40 行）:
                    echo ----------------------------------------------
                    powershell -Command "Get-Content index.html -TotalCount 40"
                '''
            }
        }
        
        // ===================== 第四阶段：部署 =====================
        stage('部署') {
            steps {
                bat '''
                    echo ===============================================
                    echo 🚀 第四阶段：部署到目标目录
                    echo ===============================================
                    
                    echo ----------------------------------------------
                    echo 📦 步骤 1/2：准备部署目录
                    echo ----------------------------------------------
                    
                    if not exist "%DEPLOY_DIR%" mkdir "%DEPLOY_DIR%"
                    
                    if exist "%DEPLOY_DIR%\\index.html" (
                        echo 发现现有版本，正在备份...
                        copy /Y "%DEPLOY_DIR%\\index.html" "%DEPLOY_DIR%\\index.html.prev" >nul
                        echo ✅ 旧版本已备份到 index.html.prev
                    ) else (
                        echo 首次部署，无需备份
                    )
                    
                    echo ----------------------------------------------
                    echo 📦 步骤 2/2：发布构建产物
                    echo ----------------------------------------------
                    
                    copy /Y index.html "%DEPLOY_DIR%\\index.html"
                    copy /Y build.py "%DEPLOY_DIR%\\build.py"
                    copy /Y requirements.txt "%DEPLOY_DIR%\\requirements.txt"
                    echo ✅ 构建产物和源码已同步到部署目录
                    
                    echo ----------------------------------------------
                    echo 📂 部署目录内容:
                    echo ----------------------------------------------
                    dir "%DEPLOY_DIR%"
                    
                    if exist "%DEPLOY_DIR%\\index.html.prev" (
                                            fc "%DEPLOY_DIR%\\index.html" "%DEPLOY_DIR%\\index.html.prev" >nul 2>&1
                                            if errorlevel 1 (
                                                echo 🔄 检测到内容变更！新版本已生效
                                            ) else (
                                                echo 内容与之前一致
                                            )
                                        )
                                        rem fc 返回非零时 Jenkins 会误判为失败，手动复位
                                        exit /b 0
                '''
            }
        }
        
        // ===================== 第五阶段：启动服务（已在运行则跳过） =====================
                stage('启动服务') {
                    steps {
                        bat '''
                            echo ===============================================
                            echo 🌐 第五阶段：启动 HTTP 服务
                            echo ===============================================
                    
                            set ALREADY_RUNNING=
                            for /f "tokens=5" %%a in ('netstat -ano ^| findstr ":%SERVER_PORT%.*LISTENING"') do set ALREADY_RUNNING=1
                    
                            if defined ALREADY_RUNNING (
                                echo ✅ 端口 %SERVER_PORT% 已被占用，服务已在运行，跳过启动
                                echo 💡 Python http.server 每次请求都会重新读取文件
                                echo 💡 新部署的文件已生效，刷新浏览器即可看到更新
                            ) else (
                                echo 🔨 端口 %SERVER_PORT% 空闲，正在启动服务...
                                echo   目录: %DEPLOY_DIR%
                                echo   端口: %SERVER_PORT%
                                echo   Python: %VENV_DIR%\\Scripts\\python.exe
                                start "CI-CD Server (Port %SERVER_PORT%)" cmd /k "@echo off & cd /d %DEPLOY_DIR% & %VENV_DIR%\\Scripts\\python.exe -m http.server %SERVER_PORT%"
                                echo ✅ 服务已启动！
                            )
                    
                            echo 🌐 浏览器访问: http://localhost:%SERVER_PORT%
                            exit /b 0
                        '''
                    }
                }
        
        // ===================== 第六阶段：验证 =====================
        stage('验证') {
            steps {
                bat '''
                    echo ===============================================
                    echo ✅ 最终验证：确认一切就绪
                    echo ===============================================
                    
                    if not exist "%DEPLOY_DIR%\\index.html" (
                        echo ❌ 验证失败：index.html 不存在
                        exit /b 1
                    )
                    echo ✅ 构建产物已部署
                    
                    if not exist "%DEPLOY_DIR%\\build.py" (
                        echo ❌ 验证失败：build.py 未同步
                        exit /b 1
                    )
                    echo ✅ 源码已同步
                    
                    if not exist "%DEPLOY_DIR%\\requirements.txt" (
                        echo ❌ 验证失败：requirements.txt 未同步
                        exit /b 1
                    )
                    echo ✅ 环境描述文件已同步
                    
                    netstat -ano | findstr ":%SERVER_PORT%.*LISTENING" >nul 2>&1
                    if errorlevel 1 (
                        echo ⚠️ 服务可能未在运行（无占用端口）
                        echo 💡 请手动访问 http://localhost:%SERVER_PORT% 确认
                    ) else (
                        echo ✅ HTTP 服务正在监听 %SERVER_PORT% 端口
                    )
                    
                    if exist "%VENV_DIR%\\Scripts\\python.exe" (
                        echo ✅ 虚拟环境存在且可用
                        echo 📊 虚拟环境 Python 版本:
                        "%VENV_DIR%\\Scripts\\python.exe" --version
                    ) else (
                        echo ⚠️ 虚拟环境似乎丢失，下次构建将重新创建
                    )
                    
                    echo ===
                    echo ✅✅✅ 全部验证通过！
                '''
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
║     • 存在则复用，不存在才创建             ║
║     • pip install 幂等补全缺失依赖         ║
║                                          ║
║  📂 部署目录:                             ║
║     F:\\horse_ranch\\ci-cd-demo\\deploy      ║
║                                          ║
║  🌐 预览地址:                             ║
║     http://localhost:8000                 ║
║                                          ║
║  🔄 后续操作:                             ║
║     1. 修改代码 (如 build.py)             ║
║     2. git commit & push                 ║
║     3. Jenkins 自动检测并重跑此 Pipeline   ║
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