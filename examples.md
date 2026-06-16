# Examples

## Example 1: 初始化工作区

Input:

> 帮我为一个新家庭客户建立家庭财务管理目录，基准币种人民币，不要放真实数据，先给他填录入表。

Expected behavior:

1. Run `scripts/init_workspace.py --target ... --household-name ... --currency CNY`.
2. Tell the user which files were created.
3. Ask the user to fill the smallest intake set first.
4. Do not generate fake balances or holdings.

## Example 2: 判断能否买入基金

Input:

> 我想买一只沪深300ETF，帮我判断能不能买。

Expected behavior:

1. Ask for or read latest balance sheet date, cash safety, IPS targets, current risk bucket, current holding, and proposed amount.
2. Use free/no-key market lookup only if symbol is known.
3. If key household data is missing, output "需要补信息" instead of a buy recommendation.
4. Produce a decision memo with forbidden actions and review date.

## Example 3: 月度复盘

Input:

> 做一次 2026-06 的家庭财务月度复盘，顺便更新资产配置记忆。

Expected behavior:

1. Use `templates/月度家庭财务复盘.md`.
2. Separate decision quality from investment result.
3. Append stable allocation conclusions to L4.
4. Append reusable behavior lessons to L5 only when there is a real lesson.
