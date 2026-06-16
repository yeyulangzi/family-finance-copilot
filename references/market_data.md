# 免费行情与基金数据说明

## 1. 原则

本 skill 只默认使用免费、无 key、适合研究和记录的行情路径。它不登录券商，不调用付费 API，不使用用户账户数据，不保证数据实时性或商用稳定性。

每次输出行情都要写：

- 数据源；
- 获取时间；
- 代码和市场；
- 数据是否延迟或 best-effort；
- 如果接口失败，明确说失败，不补编价格。

## 2. 推荐来源

| 场景 | 默认方式 | 说明 |
| --- | --- | --- |
| 美股 / 港股 / ETF / 全球基金 | yfinance 或 Yahoo public chart data | yfinance 文档说明其使用 Yahoo publicly available APIs，适合研究/教育和个人用途，使用前应遵守 Yahoo 条款 |
| CSV 日线/报价 | Stooq CSV | 免费、无 key，覆盖范围取决于 symbol |
| A 股 / 中国 ETF / 公募基金 | AKShare | 开源财经数据接口库，覆盖股票、公募基金、指数、宏观等数据；需要安装 Python 包 |
| 中国公募基金净值简查 | Eastmoney public web endpoint | best-effort fallback，可能改版或限流 |

参考：

- AKShare 文档：https://akshare.akfamily.xyz/
- yfinance 文档：https://ranaroussi.github.io/yfinance/
- Stooq CSV 示例入口：https://stooq.com/q/d/l/

## 3. 脚本用法

```bash
python scripts/market_data.py quote --symbol AAPL --source yahoo
python scripts/market_data.py history --symbol MSFT --source yahoo --range 1mo --interval 1d
python scripts/market_data.py fund --code 000001 --source eastmoney
python scripts/market_data.py history --symbol aapl.us --source stooq --interval d
```

输出为 JSON，便于复制进报告或继续处理。

## 4. 代码格式提示

| 市场 | Yahoo 示例 | Stooq 示例 |
| --- | --- | --- |
| 美股 | `AAPL` | `aapl.us` 或 `AAPL.US` |
| 港股 | `0700.HK` | `0700.hk` 视覆盖而定 |
| 上交所 A 股 | `600519.SS` | 覆盖不稳定 |
| 深交所 A 股 | `000001.SZ` | 覆盖不稳定 |
| ETF | `SPY`, `510300.SS` | 视覆盖而定 |

## 5. 失败处理

如果接口返回空、字段缺失、网络失败或 symbol 不存在：

1. 输出失败原因。
2. 建议用户确认代码格式和市场后重试。
3. 不要根据记忆或搜索结果捏造当前价格。
4. 如果用户要正式决策，要求使用券商、基金公司、交易所或官方披露文件复核。
