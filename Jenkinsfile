pipeline {
    agent any
    
    triggers {
        pollSCM('H/2 * * * *')
    }
    
    environment {
        DEPLOY_DIR = 'F:\\horse_ranch\\ci-cd-demo\\deploy'
    }
    
    stages {
        stage('拉取代码') {
            steps {
                echo '📥 从 Git 仓库拉取最新代码...'
                checkout scm
            }
        }
        
        stage('安装 Python 依赖') {
            steps {
                echo '📦 安装 requirements.txt 中的依赖...'
                bat 'python --version'
                bat 'pip install -r requirements.txt'
            }
        }
        
        stage('构建') {
            steps {
                echo '🔨 使用 Python 构建页面...'
                bat 'python build.py'
            }
        }
        
        stage('部署到本地') {
            steps {
                echo '🚀 部署到本地目录...'
                bat """
                    if not exist "%DEPLOY_DIR%" mkdir "%DEPLOY_DIR%"
                    copy index.html "%DEPLOY_DIR%\\index.html"
                    echo 部署完成！
                """
            }
        }
        
        stage('验证部署') {
            steps {
                echo '🔍 验证部署结果...'
                bat """
                    if exist "%DEPLOY_DIR%\\index.html" (
                        echo ✅ 部署成功！
                        type "%DEPLOY_DIR%\\index.html" | findstr "版本:"
                        echo 🌐 访问 http://localhost:8000
                    ) else (
                        echo ❌ 部署失败
                        exit /b 1
                    )
                """
            }
        }
    }
    
    post {
        success {
            echo '✅ 全部完成！访问 http://localhost:8000 查看效果'
        }
        failure {
            echo '❌ 构建失败，请检查日志'
        }
        always {
            echo '📊 Pipeline 执行完毕'
        }
    }
}
