pipeline {
    agent any
    
    triggers {
        // 每 2 分钟检查一次 GitHub 是否有新提交
        pollSCM('H/2 * * * *')
    }
    
    environment {
        // 本地部署目录
        DEPLOY_DIR = 'F:\\horse_ranch\\ci-cd-demo\\deploy'
    }
    
    stages {
        stage('拉取代码') {
            steps {
                echo '📥 从 Git 仓库拉取最新代码...'
                checkout scm
            }
        }
        
        stage('构建') {
            steps {
                echo '🔨 开始构建...'
                bat 'dir'
                bat 'type index.html | findstr "版本:"'
            }
        }
        
        stage('测试') {
            steps {
                echo '✅ 运行测试（模拟）'
                bat 'echo 所有测试通过！'
            }
        }
        
        stage('部署到本地') {
            steps {
                echo '🚀 开始部署到本地目录...'
                bat '''
                    echo 创建部署目录...
                    if not exist "%DEPLOY_DIR%" mkdir "%DEPLOY_DIR%"
                    
                    echo 备份旧版本...
                    if exist "%DEPLOY_DIR%\\index.html" (
                        copy "%DEPLOY_DIR%\\index.html" "%DEPLOY_DIR%\\index.html.backup"
                    )
                    
                    echo 复制新文件到部署目录...
                    copy index.html "%DEPLOY_DIR%\\index.html"
                    
                    echo 部署完成！
                    dir "%DEPLOY_DIR%"
                '''
            }
        }
        
        stage('验证部署') {
            steps {
                echo '🔍 验证部署结果...'
                bat '''
                    echo 检查部署文件...
                    if exist "%DEPLOY_DIR%\\index.html" (
                        echo ✅ 部署成功！文件已更新
                        type "%DEPLOY_DIR%\\index.html" | findstr "版本:"
                    ) else (
                        echo ❌ 部署失败：文件不存在
                        exit /b 1
                    )
                '''
            }
        }
    }
    
    post {
        success {
            echo '✅ 部署成功！访问 http://localhost:8000 查看效果'
        }
        failure {
            echo '❌ 部署失败，请检查日志'
        }
        always {
            echo '📊 Pipeline 执行完毕'
        }
    }
}
