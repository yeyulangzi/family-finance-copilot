---
name: family-finance-copilot
description: Use when the user wants to set up, maintain, or reuse a household finance management system with family profile, balance sheet, cash-flow safety, insurance, liabilities, IPS, asset allocation, risk buckets, trade decision memos, reviews, and long-term memory. Use this skill for prompts about family finance vaults, personal wealth workflows, investment decision discipline, monthly finance reviews, portfolio rebalancing, or creating reusable Markdown-based finance records, even if the user does not explicitly say "skill" or "memory".
---

# Family Finance Copilot

NO INVESTMENT ACTION BEFORE HOUSEHOLD SAFETY, DATA DATE, RISK BUCKET, AND REVIEW DATE ARE CHECKED.

## Overview

This skill turns household finance work into a repeatable Markdown system: intake, directory creation, memory management, IPS/rules, asset allocation, market-data lookup, decision memos, operation logs, and periodic reviews.

It is for decision support and record keeping. It must not pretend to be a licensed financial adviser, guarantee returns, place trades, or infer missing personal data.

## When to Use

Use this skill when the user asks to:

- create a household finance workspace, vault, second-brain area, or reusable finance folder;
- record or analyze assets, liabilities, cash flow, insurance, housing, emergency funds, or family goals;
- create or revise an IPS, family finance constitution, investment rules, risk bucket, or rebalancing plan;
- decide whether to buy, sell, add, reduce, rebalance, or pause an investment;
- write a trade checklist, decision memo, operation record, company/fund note, or monthly review;
- maintain long-term memory for a household, client, portfolio, company, fund, or lesson learned.

Do not use this skill for:

- tax filing, legal advice, estate planning documents, or regulated financial advice that requires a licensed professional;
- automatic trading, broker login, account scraping, or private API usage;
- one-off market trivia where no household context, decision, or record is needed;
- requests to copy another person's sensitive financial details into a reusable template.

## Required First Move

Classify the task before acting:

| Task type | First action |
| --- | --- |
| New setup | Run or adapt `scripts/init_workspace.py`, then guide intake |
| Record update | Locate latest profile, balance sheet, operation log, and memory registry |
| Decision | Check household safety -> IPS -> risk bucket -> target evidence -> behavior risk |
| Review | Use monthly/decision review templates and write back to memory |
| Market lookup | Use `scripts/market_data.py` or documented free/no-key sources, then cite source and timestamp |
| Memory update | Append to the right L1-L5 memory file and update the registry if a new file is created |

If data is missing, output "需要补信息" with a short missing-data list. Do not fill sensitive fields from imagination.

## Core Workflow

1. Read the latest household profile and data date.
2. Check cash-flow safety, emergency funds, dedicated funds, insurance, housing, and liabilities.
3. Map money into asset classes and risk buckets.
4. Compare current allocation with IPS targets and hard limits.
5. For any target asset, collect current public data, business/fund facts, valuation or cost, and overlap with existing holdings.
6. Run behavior checks: chasing, dip-buying impulse, loss aversion, familiarity bias, sunk-cost logic.
7. Produce an explicit action: allow, deny, wait, observe, rebalance, or request more data.
8. Write the record and set the next review date.
9. Append durable conclusions to memory only when they are reusable.

## Memory Model

Use a five-layer memory structure in the user's finance workspace:

| Layer | Stores | Typical files |
| --- | --- | --- |
| L1 Profile | Household identity, life stage, goals, constraints | `08-记忆系统/L1-画像记忆/家庭画像.md` |
| L2 Rules | IPS, family constitution, decision rules, workflow | `08-记忆系统/L2-规则记忆/` |
| L3 Projects | Active decisions, pending tasks, current task canvas | `08-记忆系统/L3-项目记忆/当前任务画布.md` |
| L4 Topics | Asset allocation, company/fund/industry memories | `08-记忆系统/L4-主题记忆/` |
| L5 Lessons | Review lessons, behavior mistakes, stable anti-patterns | `08-记忆系统/L5-经验教训/` |

Write memory append-only when possible. Every memory entry needs source, date, confidence, and next review condition.

## Market Data Rules

Prefer free, no-key, public or open-source data paths:

- Global stocks, ETFs, and funds: yfinance or Yahoo public chart data for research/personal use.
- CSV quotes or history: Stooq public CSV endpoints when symbol coverage is enough.
- China stocks, ETFs, and public funds: AKShare if Python package installation is acceptable; otherwise use documented public web endpoints through `scripts/market_data.py` only as a best-effort fallback.

Every market-data output must include:

- symbol/code and market;
- data source;
- retrieval time;
- whether data is delayed, unofficial, or best-effort;
- a warning if the source failed or coverage is uncertain.

Never use paid APIs, broker OpenAPI, account login, cookies, tokens, `.env`, or private credentials unless the user explicitly supplies and scopes them for their own environment.

## Output Standards

For decision outputs, use this shape:

```markdown
# [Decision / Review Title]

## 一句话结论
- 结论：
- 动作：
- 禁止动作：
- 复盘日期：

## 数据口径
- 最新资产数据日期：
- 市场数据来源和时间：
- 缺失信息：

## 家庭安全闸门
- 现金流：
- 安全垫：
- 保险与负债：
- 大额支出：

## 资产配置与风险桶
- 当前偏离：
- 风险桶状态：
- 本次操作影响：

## 标的判断
- 质量/产品逻辑：
- 估值/成本/性价比：
- 替代方案：
- 失效条件：

## 行为金融自检
- 最可能自我欺骗处：
- 冷静期：

## 记录与记忆写入
- 操作记录：
- 主题记忆：
- 经验教训：
```

## Common Mistakes

| Mistake | Fix |
| --- | --- |
| Starting from a stock idea | Start from household safety and IPS |
| Treating a profitable bad process as good | Score decision quality separately from result |
| Updating a report but not memory | Append reusable conclusions to L4/L5 and cite the report |
| Using exact personal examples from the source system | Replace with placeholders and intake prompts |
| Using a paid or credentialed market API | Use free/no-key sources and mark reliability limits |
| Giving strong advice with stale data | Ask for updated balance sheet and data date |

## Red Flags

If you catch yourself thinking any of these, stop and restart from the gate:

- "The target looks good, so household cash flow can be checked later."
- "The user probably has enough emergency fund."
- "This is just a small trade, no need to record it."
- "The price dropped, so buying more is automatically safer."
- "I can reuse this real person's amounts as a sample."
- "The source did not return data, but I can estimate a current price."

## Reference Routing

| Priority | Need | Read | If skipped |
| --- | --- | --- | --- |
| Required | Understand the full household finance framework | `references/framework.md` | The agent may start from a stock idea and skip household safety gates |
| Required | Create folders and starter files | `scripts/init_workspace.py --help` | The workspace may miss memory folders, intake forms, or review templates |
| Required for market lookup | Use free/no-key data paths and caveats | `references/market_data.md` | The agent may use paid/private APIs or omit source and timestamp caveats |
| Recommended | Need concrete document examples | `templates/` | Outputs may be structurally incomplete or inconsistent |
| Recommended | Need realistic test prompts | `evals/evals.json` | Changes become harder to evaluate against real scenarios |

## Quick Reference

| Scenario | Do |
| --- | --- |
| New user says "帮我搭一套家庭财务系统" | Run init script, then ask them to fill intake |
| User asks "这只基金能买吗" | Data date -> safety -> risk bucket -> fund/product check -> memo |
| User asks "更新资产配置记忆" | Append L4 entry with source/date/confidence |
| User asks "做月度复盘" | Use monthly review template and write L5 lessons if reusable |
| User asks "查一下价格" | Use free data script, cite source and timestamp, avoid account APIs |

## Completion Check

Before claiming done:

- [ ] The workspace or requested document exists.
- [ ] No personal sensitive sample data was copied into reusable artifacts.
- [ ] Any market data has source and retrieval time.
- [ ] Missing data is explicit.
- [ ] Decision outputs include action, forbidden action, trigger, and review date.
- [ ] Memory writes are append-only and routed to L1-L5 correctly.
