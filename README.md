# CI/CD 自动部署演示

## 架构

```
[本地 Git 仓库] → Jenkins 每 5 分钟拉取最新代码
    ↓
[Jenkins Pipeline]
    ├── 环境检查与修复 (pip install -r requirements.txt)
    ├── 构建 (python build.py)
    └── 部署 (复制到 F:\horse_ranch\ci-cd-demo\deploy\)
    ↓
[浏览器] → 访问 http://localhost:8000 查看效果
```

## 快速开始

### 1. 启动 HTTP 服务器（只需一次）

```powershell
cd F:\horse_ranch\ci-cd-demo\deploy
python -m http.server 8000
```

### 2. 配置 Jenkins Pipeline

1. 打开 [http://localhost:8080](http://localhost:8080/)
2. **新建任务** → 名称 `ci-cd-demo` → 选 **Pipeline**
3. 配置：
   + **Pipeline** → 定义： `Pipeline script from SCM`
   + **SCM** ： `Git`
   + **Repository URL** ：你的 Git 仓库地址
   + **Branch Specifier** ： `*`
   + **Script Path** ： `Jenkinsfile`
4. 保存后点击 **Build Now**

### 3. 提交代码触发自动构建

```powershell
cd F:\horse_ranch\ci-cd-demo
git add .
git commit -m "更新代码"
git push  # 或直接在本地仓库操作
```

Jenkins 会每 5 分钟检测一次，自动执行完整 CI/CD 流程。

## 文件说明

| 文件 | 说明 |
|------|------|
| `Jenkinsfile` | Jenkins Pipeline 定义 |
| `build.py` | Python 构建脚本（Jinja2 + Faker + emoji） |
| `requirements.txt` | Python 依赖描述 |
| `index.html` | 由 build.py 生成的页面 |
| `deploy/` | Jenkins 部署目录 |

## 技术栈

- **Jinja2** - HTML 模板引擎
- **Faker** - 生成随机中文数据
- **emoji** - 处理 emoji 字符

## 工作流程

1. 修改源码（如 `build.py`、`requirements.txt`）
2. git commit & push
3. Jenkins 检测到变更
4. 自动安装/更新依赖
5. 从源码重新构建
6. 部署到本地
7. 刷新浏览器查看效果

## 注意事项

- Jenkins 需要 Python 3.x
- 首次运行会自动下载依赖包
- HTTP 服务器每次请求都会读取最新文件，无需重启
