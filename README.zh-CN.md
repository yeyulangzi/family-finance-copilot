# Family Finance Copilot

> 一个可复用的 Agent Skill，用来搭建 Markdown-first 的家庭财务管理系统。

语言：[English](README.md) | 简体中文

Family Finance Copilot 帮助 AI 编码代理创建并维护一套结构化的家庭财务工作区，覆盖家庭画像、资产负债表、现金流安全、保险与负债、IPS、资产配置、风险桶、投资决策 Memo、操作记录、月度复盘和长期记忆。

它的定位是决策支持与记录系统，不会自动交易，不会登录券商账户，不会保存凭证，也不替代持牌财务、税务、法律或投资顾问。

![Family Finance Copilot overview](docs/assets/overview.svg)

## 为什么需要它

很多家庭财务工作流不是败在“不会分析”，而是败在信息分散：

一个表格记录资产，一个笔记写交易想法，一个聊天窗口保存推理过程，月度复盘又常常被跳过。过了半年，很难回答这些问题：

- 当时为什么做这个决策？
- 是哪条规则允许它发生？
- 当时的数据是不是最新？
- 什么条件会证明这个决策错了？
- 最后赚钱是因为判断正确，还是只是运气好？

Family Finance Copilot 把这些分散的信息收束成一套可复用的 Agent 工作流。

核心链路是：

```text
家庭安全 -> 数据日期 -> IPS/规则 -> 风险桶 -> 标的证据 -> 行为检查 -> 记录 -> 复盘 -> 记忆
```

这个 skill 会强制 Agent 先看家庭上下文，再讨论任何投资标的。

## 设计原则

### 1. 家庭安全优先于投资机会

skill 内置一条硬规则：

```text
NO INVESTMENT ACTION BEFORE HOUSEHOLD SAFETY, DATA DATE, RISK BUCKET, AND REVIEW DATE ARE CHECKED.
```

它的目的很明确：防止 Agent 从“这个资产看起来不错”直接跳到“可以买”。

### 2. Markdown-first，本地优先

初始化出来的工作区全部是普通 Markdown 文件，可以放在 Obsidian、VS Code、GitHub、Cursor、Claude Code、Codex 或任何文件型工作流里。

不需要数据库，不绑定某个私有应用。

### 3. 记忆是产品层，不是附属记录

生成的工作区内置五层记忆系统：

| 层级 | 作用 |
| --- | --- |
| L1 画像记忆 | 家庭阶段、目标、约束、风险偏好 |
| L2 规则记忆 | IPS、家庭财务宪法、决策规则、工作流 |
| L3 项目记忆 | 进行中决策、待办、当前任务画布 |
| L4 主题记忆 | 资产配置、公司、基金、行业记忆 |
| L5 经验教训 | 复盘教训、行为偏差、长期反模式 |

重点不是保存所有信息，而是沉淀可复用结论，并保留来源、日期、置信度和复核条件。

### 4. 确定性任务交给脚本

skill 内置两个脚本：

- `scripts/init_workspace.py`：创建完整家庭财务工作区。
- `scripts/market_data.py`：使用免费、无 key 的公开行情源查询数据，并输出 JSON。

Agent 应该用脚本处理确定性任务，而不是每次重新手写目录结构或临时拼接口。

### 5. 默认只使用公开免费数据

行情查询默认使用 Yahoo public chart data、Stooq CSV、AKShare、Eastmoney public fund endpoint 等免费/无 key 数据源。

默认不使用券商 OpenAPI、cookie、账户登录、私有 token 或付费数据 API。

## 产品架构

![Product architecture](docs/assets/product-architecture.svg)

项目由四层组成：

| 层级 | 文件 | 作用 |
| --- | --- | --- |
| Skill 入口 | `SKILL.md` | 触发条件、工作流规则、决策闸门、输出标准 |
| 知识参考 | `references/` | 家庭财务框架与行情数据规则 |
| 确定性工具 | `scripts/` | 工作区初始化、免费行情查询 |
| 可复用产出 | `templates/` | 录入表、IPS、宪法、Memo、操作记录、复盘、记忆文件 |

## 仓库结构

```text
family-finance-copilot/
├── SKILL.md
├── README.md
├── README.zh-CN.md
├── manifest.json
├── examples.md
├── quality_check.md
├── docs/
│   └── assets/
│       ├── overview.svg
│       └── product-architecture.svg
├── references/
│   ├── framework.md
│   └── market_data.md
├── scripts/
│   ├── init_workspace.py
│   └── market_data.py
├── templates/
│   ├── 家庭基础信息录入表.md
│   ├── 资产负债表.md
│   ├── 现金流预算.md
│   ├── 家庭财务宪法.md
│   ├── 投资政策声明IPS.md
│   ├── 投资决策Memo.md
│   ├── 操作记录.md
│   ├── 月度家庭财务复盘.md
│   ├── 资产配置记忆.md
│   ├── 记忆注册表.md
│   ├── 当前任务画布.md
│   └── 财务复盘教训.md
└── evals/
    └── evals.json
```

## 安装方式

先选你正在使用的 Agent 工具。如果不确定，直接用“手动安装”，只要工具支持 `SKILL.md` 格式就能用。

### 快速选择

| 你使用的工具 | 推荐安装方式 |
| --- | --- |
| Codex | 优先用下面的 Skills CLI 命令；手动安装时复制到 `~/.codex/skills/` 或 `~/.agents/skills/` |
| Claude Code | 复制到 `~/.claude/skills/family-finance-copilot/` |
| Qoder / QoderWork | 复制到 `~/.qoder/skills/family-finance-copilot/`，或项目级 `.qoder/skills/` |
| WorkBuddy | 优先用 SkillHub / 插件市场 / 本地导入；只有版本明确支持时再手动复制 |
| 其他兼容 SKILL.md 的工具 | 复制到该工具的 skills 目录 |

### 通过 Skills CLI 安装

如果你已经在用 Skills CLI，这是最省事的方式。建议加 `-g` 做用户级安装，这样不只在某一个项目里可用。

```bash
# Codex
npx skills add yeyulangzi/family-finance-copilot -g --agent codex --copy -y

# Claude Code
npx skills add yeyulangzi/family-finance-copilot -g --agent claude-code --copy -y

# Qoder / QoderWork
npx skills add yeyulangzi/family-finance-copilot -g --agent qoder --copy -y
```

安装后重启或刷新你的 Agent 工具，然后测试：

```text
Use family-finance-copilot to set up a household finance workspace.
```

如果命令成功但工具里看不到 skill，通常是因为该工具读取的 skills 目录和 CLI 安装目录不同。此时请用下面的手动安装方式。

提示：安装完成后，以 CLI 输出的 `Installation Summary` 为准。例如当前 Skills CLI 使用 `--agent codex` 时，会把 skill 放到 `~/.agents/skills/`。

### 手动安装

先克隆仓库：

```bash
git clone https://github.com/yeyulangzi/family-finance-copilot.git
```

然后把整个文件夹复制到你的 Agent skills 目录：

```bash
# Codex
mkdir -p ~/.codex/skills
cp -R family-finance-copilot ~/.codex/skills/

# Claude Code
mkdir -p ~/.claude/skills
cp -R family-finance-copilot ~/.claude/skills/

# 通用 Agent Skills 目录
mkdir -p ~/.agents/skills
cp -R family-finance-copilot ~/.agents/skills/
```

最终目录应类似这样：

```text
~/.codex/skills/family-finance-copilot/SKILL.md
```

或：

```text
~/.claude/skills/family-finance-copilot/SKILL.md
```

重点：`SKILL.md` 必须直接位于 `family-finance-copilot` 文件夹根部。

### Qoder / QoderWork

用户级安装：

```bash
git clone https://github.com/yeyulangzi/family-finance-copilot.git
mkdir -p ~/.qoder/skills
cp -R family-finance-copilot ~/.qoder/skills/
```

项目级安装：

```bash
git clone https://github.com/yeyulangzi/family-finance-copilot.git
mkdir -p .qoder/skills
cp -R family-finance-copilot .qoder/skills/
```

重启 Qoder，然后通过 `/skill` 或产品里的 Skill 面板查看是否已识别。如果提示无效，检查：

- 文件夹名是否为 `family-finance-copilot`；
- `SKILL.md` 是否直接在该文件夹根部；
- `SKILL.md` frontmatter 是否包含 `name` 和 `description`。

### WorkBuddy

WorkBuddy 不同版本的安装方式可能不同，建议按这个顺序：

1. 打开 WorkBuddy 的 SkillHub / Skills / 插件 / Marketplace 面板。
2. 搜索这个仓库，或在支持本地导入时导入整个 `family-finance-copilot/` 文件夹。
3. 重启或刷新 WorkBuddy。
4. 测试：`Use family-finance-copilot to set up a household finance workspace.`

如果你的 WorkBuddy 版本明确支持本地 skills 目录，可以尝试：

```bash
git clone https://github.com/yeyulangzi/family-finance-copilot.git
mkdir -p ~/.workbuddy/skills
cp -R family-finance-copilot ~/.workbuddy/skills/
```

注意：部分 WorkBuddy 版本会把 Skill 当作插件安装到 marketplace 目录，而不是直接读取 `~/.workbuddy/skills`。如果复制后看不到，请优先使用 WorkBuddy 内置 SkillHub/插件安装方式，或让 WorkBuddy 检查当前生效的 skill/plugin 目录。

### 可选：GitHub CLI

如果你的 GitHub CLI 支持 `gh skill`，可以直接从 GitHub 安装：

```bash
gh skill install yeyulangzi/family-finance-copilot family-finance-copilot --agent codex --scope user
gh skill install yeyulangzi/family-finance-copilot family-finance-copilot --agent claude-code --scope user
gh skill install yeyulangzi/family-finance-copilot family-finance-copilot --agent qoder --scope user
```

请先运行下面命令确认你的 GitHub CLI 版本支持这些参数：

```bash
gh skill install --help
```

`gh skill` 仍处于 preview，参数可能变化；如果你想要更稳，优先用 Skills CLI 或手动安装。

### 验证是否安装成功

安装后，重启或刷新 Agent 工具，然后发送：

```text
Use family-finance-copilot to create a demo household finance workspace under ./demo-vault.
```

如果安装成功，Agent 应该能创建或引导你创建：

- 家庭基础信息录入表；
- 资产负债表；
- 现金流预算；
- IPS；
- 投资决策 Memo 和复盘模板；
- L1-L5 记忆目录结构。

## 快速开始

创建一个新的家庭财务工作区：

```bash
python3 scripts/init_workspace.py \
  --target ~/FamilyFinanceVault \
  --household-name "Sample Household" \
  --currency CNY
```

脚本会生成：

- 录入表；
- 家庭画像；
- 资产负债表；
- 现金流预算；
- 家庭财务宪法；
- IPS；
- 投资决策 Memo 模板；
- 操作记录模板；
- 月度复盘模板；
- L1-L5 记忆系统；
- 记忆注册表和当前任务画布。

优先填写这几个文件：

1. `00-录入表/家庭基础信息录入表.md`
2. `01-家庭档案/资产负债表.md`
3. `02-规则与IPS/家庭财务宪法.md`
4. `02-规则与IPS/投资政策声明IPS.md`

## 行情数据查询

查询报价或历史数据：

```bash
python scripts/market_data.py quote --symbol AAPL --source yahoo
python scripts/market_data.py history --symbol 600519.SS --source yahoo --range 1mo --interval 1d
python scripts/market_data.py history --symbol aapl.us --source stooq --interval d
python scripts/market_data.py fund --code 000001 --source eastmoney
```

每次成功返回都会包含：

- 数据源；
- symbol/code；
- 获取时间；
- 原始数据字段；
- 关于延迟、覆盖范围或公开数据可靠性的 caveat。

如果数据源失败，脚本会返回错误，并明确提醒 Agent 不要编造当前价格。

## 示例 Prompt

```text
Use family-finance-copilot to set up a new household finance workspace under ./demo-vault.
```

```text
I want to buy a new fund, but my balance sheet is not updated. Can you decide whether you can give me a buy recommendation?
```

```text
Look up AAPL recent market data using a free source and prepare a note that can be pasted into an investment memo.
```

```text
Create a monthly household finance review and update allocation memory if there is a durable conclusion.
```

## 这个 Skill 会拒绝做什么

它不应该：

- 自动交易；
- 登录券商账户；
- 抓取私人账户页面；
- 保存凭证、cookie、API key 或 `.env` 文件；
- 编造缺失的资产、持仓、价格或日期；
- 提供法律、税务、遗产规划或受监管投资建议；
- 在关键家庭数据缺失时给出强买入/卖出建议。

## 隐私边界

本仓库不包含任何真实家庭资产、个人姓名、券商账户、持仓、交易历史、cookie、token 或私有 API key。

生成的工作区是本地文件。用户需要自行决定保存哪些财务数据，以及是否同步到云端。

## 质量状态

见 [quality_check.md](quality_check.md)。

当前已检查：

- `SKILL.md` 以 `Use when` 开头；
- `SKILL.md` 小于 500 行；
- 确定性任务已放到脚本；
- references 和 templates 采用渐进式加载；
- 初始化工作区内置 L1-L5 记忆系统；
- 免费/无 key 行情查询返回 source 和 timestamp；
- 包内已移除敏感个人数据。

## Roadmap

- 增加更多公募基金数据适配器，并明确公开数据源 caveat。
- 增加已有家庭资产表的 CSV 导入路径。
- 为内置 eval prompts 增加 benchmark 输出。
- 增加理财顾问/客户协作和单家庭自用场景示例。
- 增加 release tags，方便用户通过 skill package managers 固定版本安装。

## 免责声明

本项目用于教育、工作流自动化、记录管理和决策支持，不构成财务、法律、税务或投资建议。任何财务决策前，请使用官方来源复核数据。

## License

MIT。见 [LICENSE](LICENSE)。
