# 本地测试与部署指南

## 📋 本地测试步骤

### 1. 安装 uv（如果还没有）

```bash
# macOS/Linux
curl -LsSf https://astral.sh/uv/install.sh | sh

# 或者使用 Homebrew
brew install uv

# 验证安装
uv --version
```

### 2. 创建虚拟环境并安装依赖

```bash
# 进入项目目录
cd daily-tech-news

# 使用 uv 创建虚拟环境（推荐）
uv venv

# 激活虚拟环境
# macOS/Linux:
source .venv/bin/activate
# Windows:
# .venv\Scripts\activate

# 使用 uv 安装依赖（比 pip 快很多）
uv pip install -r requirements.txt
```

### 3. 配置 API Key

在项目根目录创建 `.env` 文件：

```bash
# 创建 .env 文件
touch .env
```

编辑 `.env` 文件，添加你的 SiliconFlow API Key：

```env
ANTHROPIC_API_KEY=your-siliconflow-api-key-here
ANTHROPIC_BASE_URL=https://api.siliconflow.cn/v1
```

**获取 API Key**：
1. 访问 https://siliconflow.cn/
2. 注册/登录账号
3. 在控制台获取 API Key

### 4. 测试数据抓取（可选，验证网络连接）

```bash
# 测试 V2EX API（应该返回 JSON）
curl https://www.v2ex.com/api/topics/hot.json | head -20

# 测试 Hacker News API
curl https://hacker-news.firebaseio.com/v0/topstories.json | head -20
```

### 5. 运行主脚本测试

```bash
# 确保虚拟环境已激活
# 运行主脚本生成简报
python scripts/tech_digest.py
```

**预期输出**：
- 如果成功，会看到：
  ```
  已生成: digests/YYYY-MM-DD.md
  已更新: digests/latest.md
  ```
- 如果失败，检查：
  - API Key 是否正确
  - 网络连接是否正常
  - 依赖是否完整安装

### 6. 检查生成的文件

```bash
# 查看最新简报
cat digests/latest.md

# 查看今日的源数据（JSON）
cat digests/$(date +%Y-%m-%d).sources.json | head -50

# 检查文件是否存在
ls -lh digests/
```

### 7. 测试 HTML 生成

```bash
# 生成 digests/index.html
python scripts/generate_html.py

# 生成根目录 index.html
python scripts/generate_page.py

# 检查生成的文件
ls -lh digests/index.html index.html
```

### 8. 本地预览 HTML（可选）

```bash
# 使用 Python 简单 HTTP 服务器预览
python -m http.server 8000

# 然后在浏览器打开
# http://localhost:8000
```

## ✅ 测试检查清单

- [ ] uv 已安装并能正常使用
- [ ] 虚拟环境创建成功
- [ ] 所有依赖安装完成（无错误）
- [ ] `.env` 文件已创建并配置 API Key
- [ ] `tech_digest.py` 能成功运行并生成 Markdown
- [ ] `generate_html.py` 能生成 `digests/index.html`
- [ ] `generate_page.py` 能生成根目录 `index.html`
- [ ] 生成的 Markdown 内容格式正确
- [ ] 生成的 HTML 可以正常打开查看

## 🚀 GitHub 配置步骤

### 1. 创建 GitHub 仓库

```bash
# 如果还没有初始化 git
git init

# 添加所有文件（.env 会被 .gitignore 忽略）
git add .

# 提交
git commit -m "Initial commit: Daily tech digest system"

# 在 GitHub 上创建新仓库，然后：
git remote add origin https://github.com/your-username/daily-tech-news.git
git branch -M main
git push -u origin main
```

### 2. 配置 GitHub Secrets

1. 进入你的 GitHub 仓库
2. 点击 **Settings** → **Secrets and variables** → **Actions**
3. 点击 **New repository secret**
4. 添加以下 Secrets：

   **ANTHROPIC_API_KEY**
   - Name: `ANTHROPIC_API_KEY`
   - Value: 你的 SiliconFlow API Key

   **ANTHROPIC_BASE_URL**（可选）
   - Name: `ANTHROPIC_BASE_URL`
   - Value: `https://api.siliconflow.cn/v1`
   - 如果不设置，会使用 `config.json` 中的默认值

### 3. 启用 GitHub Actions

1. 进入仓库的 **Actions** 标签页
2. 如果提示需要启用 Actions，点击 **I understand my workflows, enable them**
3. 检查 workflow 文件是否正确：
   - 路径：`.github/workflows/daily-tech-digest.yml`
   - 应该能看到 "Daily Tech Digest" workflow

### 4. 手动触发测试（可选）

1. 进入 **Actions** 标签页
2. 选择 **Daily Tech Digest** workflow
3. 点击 **Run workflow** → **Run workflow**
4. 等待执行完成，检查是否成功

### 5. 配置 GitHub Pages（可选，用于展示简报）

1. 进入仓库 **Settings** → **Pages**
2. Source 选择：**Deploy from a branch**
3. Branch 选择：`main`（或你的主分支）
4. Folder 选择：`/ (root)`
5. 点击 **Save**
6. 等待几分钟，访问：`https://your-username.github.io/daily-tech-news/`

### 6. 验证自动化运行

- 等待到每天 8:00（北京时间）自动运行
- 或者手动触发 workflow 测试
- 检查 Actions 日志，确认：
  - 依赖安装成功
  - 脚本执行成功
  - 文件已提交到仓库

## 🔧 常见问题排查

### 问题 1: API Key 错误
```
错误: 请设置 ANTHROPIC_API_KEY 环境变量
```
**解决**：检查 `.env` 文件是否存在且格式正确

### 问题 2: 依赖安装失败
```
ERROR: Could not find a version that satisfies the requirement...
```
**解决**：
```bash
# 更新 uv
uv self update

# 或者使用传统 pip
python -m pip install -r requirements.txt
```

### 问题 3: 网络请求失败
```
requests.exceptions.RequestException: ...
```
**解决**：检查网络连接，可能需要代理

### 问题 4: GitHub Actions 失败
**检查**：
- Secrets 是否配置正确
- workflow 文件语法是否正确
- 查看 Actions 日志中的具体错误信息

## 📝 后续维护

- **更新依赖**：修改 `requirements.txt` 后运行 `uv pip install -r requirements.txt`
- **修改配置**：编辑 `scripts/config.json`
- **查看日志**：GitHub Actions 会自动记录每次运行的日志
- **手动触发**：在 Actions 页面可以随时手动触发 workflow
