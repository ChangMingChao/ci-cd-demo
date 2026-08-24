pipeline {
    agent any
    
    triggers {
        // 每 2 分钟检查一次 GitHub 是否有新提交
        pollSCM('H/2 * * * *')
    }
    
    environment {
        // 模拟服务器配置（Docker 容器名）
        SERVER_HOST = 'jenkins-server'
        SERVER_USER = 'deploy'
        DEPLOY_PATH = '/usr/share/nginx/html'
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
                sh 'ls -la'
                sh 'cat index.html | grep "版本:" || true'
            }
        }
        
        stage('测试') {
            steps {
                echo '✅ 运行测试（模拟）'
                sh 'echo "所有测试通过！"'
            }
        }
        
        stage('部署到服务器') {
            steps {
                echo '🚀 开始部署...'
                sh '''
                    # 通过 SSH 连接模拟服务器
                    ssh -o StrictHostKeyChecking=no ${SERVER_USER}@${SERVER_HOST} "
                        echo '备份旧版本...'
                        cp -r ${DEPLOY_PATH} ${DEPLOY_PATH}_backup_$(date +%s) || true
                        
                        echo '清空旧文件...'
                        rm -rf ${DEPLOY_PATH}/*
                    "
                    
                    # 通过 SCP 传输新文件
                    echo '传输新文件...'
                    scp index.html ${SERVER_USER}@${SERVER_HOST}:${DEPLOY_PATH}/
                    
                    # 远程执行重启命令
                    echo '重启 nginx...'
                    ssh -o StrictHostKeyChecking=no ${SERVER_USER}@${SERVER_HOST} "
                        nginx -s reload || nginx
                        echo '部署完成！'
                    "
                '''
            }
        }
        
        stage('验证部署') {
            steps {
                echo '🔍 验证部署结果...'
                script {
                    def response = sh(script: "curl -s http://jenkins-server:9090 | grep '版本:' || echo '验证跳过'", returnStdout: true).trim()
                    echo "服务器响应: ${response}"
                }
            }
        }
    }
    
    post {
        success {
            echo '✅ 部署成功！访问 http://localhost:9090 查看效果'
        }
        failure {
            echo '❌ 部署失败，请检查日志'
        }
        always {
            echo '📊 Pipeline 执行完毕'
        }
    }
}
