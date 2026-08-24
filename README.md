# CI/CD 自动部署演示

这是一个全自动的 CI/CD 演示项目：

- **GitHub Actions** 每小时自动修改代码（版本号、颜色、emoji）
- **Jenkins** 每 2 分钟检查一次，发现新提交自动构建部署
- **模拟服务器**（Docker 容器）接收部署并对外提供服务

## 演示效果

访问 http://localhost:9090，每小时会看到：
- 不同的渐变色背景
- 不同的 emoji 图标
- 递增的版本号
- 最新的部署时间

## 架构

```
[GitHub Actions] → 每小时自动修改代码并 push
       ↓
[Jenkins] → 每 2 分钟轮询，检测到变化自动触发 Pipeline
       ↓
[模拟服务器] → SSH 部署，nginx 对外服务
       ↓
[浏览器] → 访问 http://localhost:9090 查看效果
```

## 文件说明

- `index.html` - 演示页面（被 GitHub Actions 自动修改）
- `Jenkinsfile` - Jenkins Pipeline 定义
- `.github/workflows/auto-update.yml` - GitHub Actions 自动更新脚本

## 本地环境搭建

```powershell
# 1. 启动模拟服务器（nginx 容器）
docker run -d --name jenkins-server -p 9090:80 nginx:alpine

# 2. 创建 Jenkins 网络并连接
docker network create jenkins-net
docker network connect jenkins-net jenkins-server
docker network connect jenkins-net jenkins

# 3. 在 Jenkins 创建 Pipeline
# - 新建任务 → 选"Pipeline"
# - Pipeline 定义选"Pipeline script from SCM"
# - 指向这个 GitHub 仓库

# 4. 等待自动部署
# - GitHub Actions 每小时整点运行
# - Jenkins 每 2 分钟检查一次
# - 访问 http://localhost:9090 查看效果
```
