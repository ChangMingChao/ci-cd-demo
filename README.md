# CI/CD 自动部署演示（本地版）

全自动 CI/CD 演示：GitHub Actions 自动更新代码 + Jenkins 自动构建部署到本地。

## 演示效果

访问 http://localhost:8000   
每5分钟会看到：
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
[本地部署] → 复制文件到 F:\horse_ranch\ci-cd-demo\deploy\
       ↓
[本地服务器] → Python http.server 对外服务
       ↓
[浏览器] → 访问 http://localhost:8000 查看效果
```

## 快速开始

### 1. 启动本地 HTTP 服务器

```powershell
cd F:\horse_ranch\ci-cd-demo\deploy
python -m http.server 8000
```

保持这个窗口开着，浏览器访问 http://localhost:8000

### 2. 配置 Jenkins Pipeline

1. 打开 http://localhost:8080
2. **新建任务** → 名称 `ci-cd-demo` → 选 **Pipeline**
3. 配置：
   - **Pipeline** → 定义：`Pipeline script from SCM`
   - **SCM**：`Git`
   - **Repository URL**：你的 GitHub 仓库地址
   - **Branch Specifier**：`*/master`
   - **Script Path**：`Jenkinsfile`
4. 保存后点击 **Build Now**

### 3. 启用 GitHub Actions

推送到 GitHub 后，Actions 自动启用：
- **自动触发**：每5分钟整点
- **手动触发**：GitHub → Actions → Auto Update Demo → Run workflow

## 文件说明

- `index.html` - 演示页面（被 GitHub Actions 自动修改）
- `Jenkinsfile` - Jenkins Pipeline 定义（本地部署）
- `deploy/` - 部署目录（Jenkins 自动更新）
- `.github/workflows/auto-update.yml` - GitHub Actions 脚本

## 查看效果

```powershell
# 打开演示页面
Start-Process "http://localhost:8000"

# 查看部署目录
dir F:\horse_ranch\ci-cd-demo\deploy

# 查看 Jenkins 构建历史
Start-Process "http://localhost:8080/job/ci-cd-demo/"
```
