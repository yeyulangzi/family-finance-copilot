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

### Option A: Install with `npx skills`

Yes, once this project is published to GitHub, it should be installable through the Skills CLI if the user's agent host is supported.

For a single-skill repository:

```bash
npx skills add yeyulangzi/family-finance-copilot
```

If the repository later contains multiple skills:

```bash
npx skills add yeyulangzi/family-finance-copilot --skill family-finance-copilot
```

After installation, restart or reload your agent host so it can discover the new skill.

Note: different agent hosts may read skills from different directories. If the CLI installs successfully but your agent cannot see the skill, check the install location and your agent's skill directory.

### Option B: Install with GitHub CLI

GitHub CLI has a `gh skill` command in public preview. Once available in your environment, you can install from a GitHub repository and target a specific agent:

```bash
gh skill install yeyulangzi/family-finance-copilot family-finance-copilot --agent codex
gh skill install yeyulangzi/family-finance-copilot family-finance-copilot --agent claude-code
```

Use `gh skill --help` to confirm the exact flags supported by your installed GitHub CLI version.

### Option C: Manual Install

Copy the skill folder into your agent's skill directory.

Common locations:

```text
~/.codex/skills/family-finance-copilot/
~/.claude/skills/family-finance-copilot/
~/.agents/skills/family-finance-copilot/
```

The folder must include `SKILL.md` at its root.

## Quick Start

Create a new household finance workspace:

```bash
python scripts/init_workspace.py \
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
