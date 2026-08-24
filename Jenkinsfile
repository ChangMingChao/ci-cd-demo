pipeline {
    agent any
    
    triggers {
        // 每 5 分钟检查一次 Git 仓库是否有新提交
        pollSCM('H/5 * * * *')
    }
    
    environment {
        DEPLOY_DIR = 'F:\\horse_ranch\\ci-cd-demo\\deploy'
    }
    
    stages {
        stage('拉取源码') {
            steps {
                echo '📥 从 Git 仓库拉取最新源码...'
                checkout scm
                
                echo '📋 查看拉取的代码:'
                bat '''
                    dir /b
                    echo ---
                    type requirements.txt
                '''
            }
        }
        
        stage('环境检查与修复') {
            steps {
                echo '🔍 检查并修复环境依赖...'
                bat '''
                    echo Python 版本:
                    python --version
                    
                    echo 当前安装的包:
                    pip list
                    
                    echo 安装 requirements.txt 中的依赖...
                    pip install -r requirements.txt
                '''
            }
        }
        
        stage('构建') {
            steps {
                echo '🔨 使用源码构建页面...'
                bat '''
                    echo 执行构建脚本...
                    python build.py
                    
                    echo ---
                    echo 构建完成，生成 index.html
                '''
            }
        }
        
        stage('部署') {
            steps {
                echo '🚀 部署构建产物...'
                bat """
                    echo 创建部署目录...
                    if not exist "%DEPLOY_DIR%" mkdir "%DEPLOY_DIR%"
                    
                    echo 备份旧文件...
                    if exist "%DEPLOY_DIR%\\index.html" (
                        copy "%%DEPLOY_DIR%%\\index.html" "%%DEPLOY_DIR%%\\index.html.backup.bak"
                    )
                    
                    echo 复制新构建的文件到部署目录...
                    copy index.html "%%DEPLOY_DIR%%%\\index.html"
                    copy build.py "%%DEPLOY_DIR%%%\\build.py"
                    copy requirements.txt "%%DEPLOY_DIR%%%\\requirements.txt"
                    
                    echo ---
                    echo 部署目录内容:
                    dir "%%DEPLOY_DIR%%"
                """
            }
        }
        
        stage('启动服务') {
            steps {
                echo '🌐 部署完成，访问 http://localhost:8000 查看效果'
                echo '💡 HTTP 服务器在每次请求时都会读取文件，不需要重启'
            }
        }
        
        stage('验证') {
            steps {
                echo '✅ 验证部署是否成功'
                bat """
                    if exist "%DEPLOY_DIR%\\index.html" (
                        echo ✅ 部署验证通过
                        echo 🌐 预览地址: http://localhost:8000
                    ) else (
                        echo ❌ 部署验证失败
                        exit /b 1
                    )
                """
            }
        }
    }
    
    post {
        success {
            echo '✅ ✅ 全部完成！Pipeline 成功执行'
            echo '🌐 访问: http://localhost:8000'
            echo '📂 部署目录: %DEPLOY_DIR%'
            echo '---'
            echo '后续步骤:'
            echo '  1. 在浏览器中刷新 http://localhost:8000'
            echo '  2. 修改 build.py 或 requirements.txt 并提交到 Git'
            echo '  3. Jenkins 会自动检测到变更并重新构建'
        }
        failure {
            echo '❌ ❌ 构建失败！'
            echo '请查看上方错误日志，常见问题:'
            echo '  • Python 版本不兼容'
            echo '  • requirements.txt 中有不存在的包'
            echo '  • build.py 运行时报错'
        }
        always {
            echo '📊 Jenkins Pipeline 结束'
        }
    }
}
