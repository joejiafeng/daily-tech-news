# Daily Tech News 生成系统

> 整合 V2EX、Hacker News、科技媒体 RSS，每日自动化生成科技简报.


## ✨ 是什么

一个全自动的科技新闻聚合与简报生成系统，每天自动抓取技术社区热点，通过 AI 分析整理成结构化简报。

### 核心价值

- **省时**：无需手动浏览多个网站，一份简报掌握当日科技动态
- **智能**：AI 自动筛选热点、提炼趋势、生成摘要
- **全面**：覆盖中文社区、国际资讯、科技媒体等多维度内容
- **自动化**：每天定时生成，自动推送到仓库

### 简报示例

每日简报包含四大板块：

```
1. 今日热点 - V2EX/Hacker News 最热话题
2. 技术趋势 - AI、云计算、编程语言动态
3. 产品观察 - 新产品发布、设计洞察
4. 推荐阅读 - 精选深度文章
```

## 🎯 为什么

### 解决的问题

| 痛点 | 解决方案 |
|------|----------|
| 信息分散，需要浏览 10+ 个网站 | 整合 V2EX、HN、RSS 等多个数据源 |
| 内容太多，没时间细看 | AI 筛选精华，生成 1500 字简报 |
| 缺乏上下文，不知道什么重要 | AI 分析重要性，标注趋势 |
| 需要收藏和归档 | 自动保存 Markdown + HTML 格式 |

### 适用场景

- **开发者**：快速了解技术趋势、热门项目
- **产品经理**：获取行业动态、竞品信息
- **创业者**：关注投资风向、创业资讯
- **学生**：拓展技术视野、学习前沿知识

## 🚀 怎么用

### 方式一：直接查看（推荐）

如果已配置 GitHub Pages，访问你的 Pages 地址查看最新简报，无需任何配置。

### 方式二：本地运行

```bash
# 进入项目目录
cd daily-tech-news

# 安装依赖（推荐使用 uv，速度更快）
# 方式一：使用 uv（推荐）
curl -LsSf https://astral.sh/uv/install.sh | sh  # 首次安装 uv
uv pip install -r requirements.txt

# 方式二：使用传统 pip
python -m pip install -r requirements.txt

# 配置 API Key
# 方式一：使用 .env 文件（推荐，本地开发）
# 在项目根目录创建 .env 文件，内容如下：
# ANTHROPIC_API_KEY=your-siliconflow-api-key
# ANTHROPIC_BASE_URL=https://api.siliconflow.cn/v1

# 方式二：使用环境变量
export ANTHROPIC_API_KEY="your-siliconflow-api-key"
export ANTHROPIC_BASE_URL="https://api.siliconflow.cn/v1"

# 运行生成
python scripts/tech_digest.py

# 查看生成的简报
cat digests/latest.md
```

### 方式三：使用 GitHub Actions 自动化

1. **配置 GitHub Secrets**：在仓库设置中添加 `ANTHROPIC_API_KEY`（你的 SiliconFlow API Key）
2. **启用 GitHub Actions**（默认已启用）
3. **等待每天 8:00（北京时间）自动生成**

如需自定义，可修改配置文件：

| 文件 | 用途 |
|------|------|
| `scripts/config.json` | RSS 源、模型配置 |
| `.github/workflows/daily-tech-digest.yml` | 定时任务配置 |

## 📁 项目结构

```
daily-tech-news/
├── .github/workflows/        # GitHub Actions 配置
│   └── daily-tech-digest.yml
├── scripts/                  # 核心脚本
│   ├── tech_digest.py        # 主脚本（数据抓取 + AI 生成）
│   ├── generate_html.py      # HTML 索引生成
│   ├── generate_page.py      # GitHub Pages 生成
│   ├── siliconflow_client.py # SiliconFlow API 封装
│   ├── config.json           # 配置文件
│   └── use_agent_sdk.py      # Agent SDK 使用示例
├── digests/                  # 简报输出目录
│   ├── 2026-01-17.md
│   ├── latest.md
│   └── index.html
├── index.html                # GitHub Pages 入口
├── requirements.txt          # Python 依赖
└── README.md
```

## 🔧 配置说明

### 数据源

当前配置的数据源（可在 `scripts/config.json` 修改）：

| 类别 | 来源 | 数量 |
|------|------|------|
| 技术社区 | V2EX 热门话题 | 20 条 |
| 国际资讯 | Hacker News Top | 20 条 |
| 科技媒体 | 36氪、少数派、虎嗅、InfoQ、开源中国、Solidot | 60 条 |

### AI 配置

使用 SiliconFlow 的 Anthropic 兼容 API：

**本地开发**：推荐使用 `.env` 文件（已在 `.gitignore` 中，不会被提交）
```bash
# 在项目根目录创建 .env 文件
ANTHROPIC_API_KEY=your-siliconflow-api-key
ANTHROPIC_BASE_URL=https://api.siliconflow.cn/v1
```

**GitHub Actions**：在仓库 Settings → Secrets 中配置 `ANTHROPIC_API_KEY`

**模型配置**（`scripts/config.json`）：
```json
{
  "llm": {
    "model": "Pro/zai-org/GLM-4.7",
    "base_url": "https://api.siliconflow.cn/v1"
  }
}
```

### 定时任务

GitHub Actions 默认配置：每天北京时间 8:00 运行

```yaml
schedule:
  - cron: '0 22 * * *'  # UTC 22:00 = 北京 8:00
```

## 📊 工作原理

```
┌─────────────────┐
│  定时触发        │
│  (每天 8:00)     │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  数据抓取        │
│  • V2EX API     │
│  • HN Firebase  │
│  • RSS 源       │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  AI 分析生成     │
│  • 筛选热点      │
│  • 提炼趋势      │
│  • 生成摘要      │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  保存与发布      │
│  • Markdown     │
│  • HTML         │
│  • Git 提交      │
└─────────────────┘
```

## 🛠️ 开发指南

### 添加新的 RSS 源

编辑 `scripts/config.json`：

```json
{
  "rss_feeds": {
    "new-source": {
      "url": "https://example.com/feed",
      "name": "新来源",
      "category": "分类"
    }
  }
}
```

### 修改简报结构

编辑 `scripts/tech_digest.py` 中的 `prompt` 变量，调整 AI 输出格式。

### 自定义样式

编辑 `scripts/generate_page.py` 中的 CSS 样式。

## 📝 许可证

MIT License

## 🙏 致谢

- [V2EX](https://www.v2ex.com/) - 中文技术社区
- [Hacker News](https://news.ycombinator.com/) - 科技资讯
- [SiliconFlow](https://siliconflow.cn/) - 提供 GLM-4.7 模型 API

---
