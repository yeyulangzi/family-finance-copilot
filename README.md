# Family Finance Copilot

> A reusable Agent Skill for building a Markdown-first household finance operating system.

Languages: English | [简体中文](README.zh-CN.md)

Family Finance Copilot helps an AI coding agent set up and maintain a structured household finance workspace: family profile, balance sheet, cash-flow safety, insurance and liabilities, IPS, asset allocation, risk buckets, investment decision memos, operation logs, monthly reviews, and long-term memory.

It is designed for decision support and record keeping. It does not place trades, log in to broker accounts, store credentials, or provide licensed financial advice.

![Family Finance Copilot overview](docs/assets/overview.svg)

## Why This Exists

Most personal finance workflows fail for a boring reason: the data, rules, decisions, and reviews live in different places.

One spreadsheet stores assets. Another note stores a trade idea. A chat thread contains the reasoning. A monthly review is skipped. Six months later, nobody can answer:

- Why did we make this decision?
- Which rule allowed it?
- What data was fresh at the time?
- What would make the decision wrong?
- Did the outcome prove the thesis, or did we just get lucky?

Family Finance Copilot turns that mess into a reusable agent workflow.

The core idea is simple:

```text
Household safety -> data date -> IPS/rules -> risk bucket -> target evidence -> behavior check -> record -> review -> memory
```

The skill forces the agent to start from household context before talking about any investment target.

## Design Principles

### 1. Household Safety Before Investment Opportunity

The skill uses one hard rule:

```text
NO INVESTMENT ACTION BEFORE HOUSEHOLD SAFETY, DATA DATE, RISK BUCKET, AND REVIEW DATE ARE CHECKED.
```

This prevents the agent from jumping straight from "this asset looks interesting" to "buy it."

### 2. Markdown-First, Local-First

The generated workspace is plain Markdown. It works in Obsidian, VS Code, GitHub, Cursor, Claude Code, Codex, and any file-based workflow.

There is no database requirement and no proprietary app lock-in.

### 3. Memory Is a First-Class Product Layer

The workspace includes a five-layer memory system:

| Layer | Purpose |
| --- | --- |
| L1 Profile | Household stage, goals, constraints, risk preference |
| L2 Rules | IPS, constitution, decision rules, workflow |
| L3 Projects | Active decisions, pending tasks, current task canvas |
| L4 Topics | Asset allocation, company/fund/industry memory |
| L5 Lessons | Review lessons, behavior mistakes, durable anti-patterns |

The point is not to save every note. The point is to preserve reusable conclusions with source, date, confidence, and review condition.

### 4. Scripts Do Deterministic Work

The skill includes scripts for repeatable tasks:

- `scripts/init_workspace.py` creates the full household finance workspace.
- `scripts/market_data.py` fetches free/no-key public market data and returns JSON.

The agent should use scripts for deterministic work instead of reinventing folder structures or scraping data ad hoc.

### 5. Public Data Only by Default

Market data lookup uses free/no-key sources such as Yahoo public chart data, Stooq CSV, AKShare, and Eastmoney public fund endpoints.

The skill does not use broker OpenAPI, cookies, account login, private tokens, or paid data APIs by default.

## Product Architecture

![Product architecture](docs/assets/product-architecture.svg)

The package has four main layers:

| Layer | Files | Purpose |
| --- | --- | --- |
| Skill entry | `SKILL.md` | Triggering, workflow rules, decision gates, output standards |
| Knowledge references | `references/` | Household finance framework and market-data rules |
| Deterministic tools | `scripts/` | Workspace initialization and free market-data lookup |
| Reusable outputs | `templates/` | Intake forms, IPS, constitution, memo, operation log, review, memory files |

## Repository Structure

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

## Installation

Pick the path that matches the agent tool you use. If you are not sure, use **Manual install**; it works anywhere that understands the `SKILL.md` format.

### Quick Recommendation

| You use | Recommended install |
| --- | --- |
| Codex | Use the Skills CLI command below, or manually copy to `~/.codex/skills/` / `~/.agents/skills/` |
| Claude Code | Copy to `~/.claude/skills/family-finance-copilot/` |
| Qoder / QoderWork | Copy to `~/.qoder/skills/family-finance-copilot/`, or project `.qoder/skills/` |
| WorkBuddy | Use its SkillHub/plugin UI first; manual path only if your version exposes one |
| Other SKILL.md-compatible tools | Copy the folder to that tool's skills directory |

### Install with the Skills CLI

If you already use the Skills CLI, this is the easiest path. Use `-g` for a user-level install so the skill is available outside one project.

```bash
# Codex
npx skills add yeyulangzi/family-finance-copilot -g --agent codex --copy -y

# Claude Code
npx skills add yeyulangzi/family-finance-copilot -g --agent claude-code --copy -y

# Qoder / QoderWork
npx skills add yeyulangzi/family-finance-copilot -g --agent qoder --copy -y
```

Then restart or reload your agent tool and ask:

```text
Use family-finance-copilot to set up a household finance workspace.
```

If the command succeeds but the skill does not appear, your tool may read skills from a different directory. Use the manual install path below for your agent.

Tip: after installation, trust the CLI's `Installation Summary`. For example, current Skills CLI versions place Codex skills under `~/.agents/skills/` when using `--agent codex`.

### Manual Install

Clone the repository:

```bash
git clone https://github.com/yeyulangzi/family-finance-copilot.git
```

Copy the whole folder into your agent's skills directory:

```bash
# Codex
mkdir -p ~/.codex/skills
cp -R family-finance-copilot ~/.codex/skills/

# Claude Code
mkdir -p ~/.claude/skills
cp -R family-finance-copilot ~/.claude/skills/

# Generic Agent Skills location
mkdir -p ~/.agents/skills
cp -R family-finance-copilot ~/.agents/skills/
```

The final layout should look like this:

```text
~/.codex/skills/family-finance-copilot/SKILL.md
```

or:

```text
~/.claude/skills/family-finance-copilot/SKILL.md
```

`SKILL.md` must be directly inside the `family-finance-copilot` folder.

### Qoder / QoderWork

For user-level installation:

```bash
git clone https://github.com/yeyulangzi/family-finance-copilot.git
mkdir -p ~/.qoder/skills
cp -R family-finance-copilot ~/.qoder/skills/
```

For project-level installation:

```bash
git clone https://github.com/yeyulangzi/family-finance-copilot.git
mkdir -p .qoder/skills
cp -R family-finance-copilot .qoder/skills/
```

Restart Qoder, then open the skill list with `/skill` or the product's skill panel. If Qoder reports that a skill is invalid, check that:

- the folder name is `family-finance-copilot`;
- `SKILL.md` is directly inside that folder;
- `SKILL.md` contains `name` and `description` frontmatter.

### WorkBuddy

WorkBuddy versions differ in how skills are installed. Use this order:

1. Open WorkBuddy's SkillHub / Skills / Plugins / Marketplace panel.
2. Search for this repository or import the local `family-finance-copilot/` folder if local import is supported.
3. Restart or reload WorkBuddy.
4. Test with: `Use family-finance-copilot to set up a household finance workspace.`

If your WorkBuddy version documents a local skills directory, you can try:

```bash
git clone https://github.com/yeyulangzi/family-finance-copilot.git
mkdir -p ~/.workbuddy/skills
cp -R family-finance-copilot ~/.workbuddy/skills/
```

Some WorkBuddy versions package skills as plugins under marketplace directories instead of reading `~/.workbuddy/skills`. If the skill does not appear, use WorkBuddy's built-in SkillHub/plugin installer or ask WorkBuddy to inspect its active skill/plugin directory.

### Optional: GitHub CLI

If your GitHub CLI supports `gh skill`, you can install directly from GitHub:

```bash
gh skill install yeyulangzi/family-finance-copilot family-finance-copilot --agent codex --scope user
gh skill install yeyulangzi/family-finance-copilot family-finance-copilot --agent claude-code --scope user
gh skill install yeyulangzi/family-finance-copilot family-finance-copilot --agent qoder --scope user
```

Run `gh skill install --help` first to confirm your installed GitHub CLI version supports these flags. `gh skill` is still in preview, so the Skills CLI or manual install is usually the more predictable option.

### Verify Installation

After installing, restart or reload your agent and send:

```text
Use family-finance-copilot to create a demo household finance workspace under ./demo-vault.
```

A working install should create or guide you toward:

- a household intake form;
- a balance sheet;
- a cash-flow budget;
- an IPS;
- decision memo and review templates;
- an L1-L5 memory folder structure.

## Quick Start

Create a new household finance workspace:

```bash
python3 scripts/init_workspace.py \
  --target ~/FamilyFinanceVault \
  --household-name "Sample Household" \
  --currency CNY
```

The script creates:

- intake form;
- household profile;
- balance sheet;
- cash-flow budget;
- household finance constitution;
- IPS;
- investment decision memo template;
- operation log template;
- monthly review template;
- L1-L5 memory system;
- memory registry and current task canvas.

Then fill these files first:

1. `00-录入表/家庭基础信息录入表.md`
2. `01-家庭档案/资产负债表.md`
3. `02-规则与IPS/家庭财务宪法.md`
4. `02-规则与IPS/投资政策声明IPS.md`

## Market Data Lookup

Fetch quote or history data:

```bash
python scripts/market_data.py quote --symbol AAPL --source yahoo
python scripts/market_data.py history --symbol 600519.SS --source yahoo --range 1mo --interval 1d
python scripts/market_data.py history --symbol aapl.us --source stooq --interval d
python scripts/market_data.py fund --code 000001 --source eastmoney
```

Every successful result includes:

- source;
- symbol/code;
- retrieval time;
- raw data fields;
- caveat about delay, coverage, or public-data reliability.

If a source fails, the script returns an error and explicitly warns the agent not to fabricate a current price.

## Example Agent Prompts

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

## What This Skill Will Refuse To Do

The skill should not:

- place trades;
- log in to broker accounts;
- scrape private account pages;
- store credentials, cookies, API keys, or `.env` files;
- invent missing balances, holdings, prices, or dates;
- provide legal, tax, estate-planning, or regulated investment advice;
- turn a missing-data situation into a strong buy/sell recommendation.

## Privacy Boundary

This repository contains no real household balances, personal names, broker accounts, holdings, transaction history, cookies, tokens, or private API keys.

Generated workspaces are local files. Users are responsible for deciding what financial data they store and where they sync it.

## Quality Status

See [quality_check.md](quality_check.md).

Current checks:

- `SKILL.md` starts with `Use when`;
- `SKILL.md` is under 500 lines;
- deterministic work is offloaded to scripts;
- references and templates are progressively loaded;
- L1-L5 memory is built into the generated workspace;
- free/no-key market lookup returns source and timestamp;
- sensitive personal data has been removed from the package.

## Roadmap

- Add more fund-data adapters with clear public-source caveats.
- Add an optional CSV import path for existing household balance sheets.
- Add benchmark outputs for the included eval prompts.
- Add examples for adviser/client workflows and single-household self-management.
- Add release tags so users can pin installs through skill package managers.

## Disclaimer

This project is for education, workflow automation, record keeping, and decision support. It is not financial, legal, tax, or investment advice. Always verify data with official sources before making financial decisions.

## License

MIT. See [LICENSE](LICENSE).
