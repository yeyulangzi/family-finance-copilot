#!/usr/bin/env python3
"""Initialize a reusable household finance Markdown workspace."""

from __future__ import annotations

import argparse
import datetime as dt
import shutil
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TEMPLATES = ROOT / "templates"


STRUCTURE = [
    "00-录入表",
    "01-家庭档案",
    "02-规则与IPS",
    "03-账户与现金流",
    "04-投资与资产配置/标的研究",
    "04-投资与资产配置/基金与产品",
    "05-操作与复盘/操作记录",
    "05-操作与复盘/月度复盘",
    "08-记忆系统/L1-画像记忆",
    "08-记忆系统/L2-规则记忆",
    "08-记忆系统/L3-项目记忆",
    "08-记忆系统/L4-主题记忆",
    "08-记忆系统/L5-经验教训",
    "99-模板",
]


FILE_MAP = {
    "家庭基础信息录入表.md": "00-录入表/家庭基础信息录入表.md",
    "资产负债表.md": "01-家庭档案/资产负债表.md",
    "现金流预算.md": "03-账户与现金流/现金流预算-{{MONTH}}.md",
    "家庭财务宪法.md": "02-规则与IPS/家庭财务宪法.md",
    "投资政策声明IPS.md": "02-规则与IPS/投资政策声明IPS.md",
    "资产配置记忆.md": "08-记忆系统/L4-主题记忆/资产配置记忆.md",
    "投资决策Memo.md": "99-模板/投资决策Memo.md",
    "交易前检查清单.md": "99-模板/交易前检查清单.md",
    "操作记录.md": "99-模板/操作记录.md",
    "月度家庭财务复盘.md": "99-模板/月度家庭财务复盘.md",
    "记忆注册表.md": "08-记忆系统/记忆注册表.md",
    "当前任务画布.md": "08-记忆系统/L3-项目记忆/当前任务画布.md",
    "财务复盘教训.md": "08-记忆系统/L5-经验教训/财务复盘教训.md",
}


STARTER_FILES = {
    "README.md": """# {{HOUSEHOLD_NAME}} 家庭财务工作区

建档日期：{{DATE}}
基准币种：{{BASE_CURRENCY}}

## 使用顺序

1. 填写 `00-录入表/家庭基础信息录入表.md`。
2. 更新 `01-家庭档案/资产负债表.md` 和 `03-账户与现金流/`。
3. 修订 `02-规则与IPS/家庭财务宪法.md` 和 `02-规则与IPS/投资政策声明IPS.md`。
4. 每次投资决策使用 `99-模板/投资决策Memo.md` 与 `99-模板/交易前检查清单.md`。
5. 每月复盘后更新 `08-记忆系统/L4-主题记忆/资产配置记忆.md` 和 `08-记忆系统/L5-经验教训/财务复盘教训.md`。

## 隐私提醒

不要在本目录保存密码、身份证号、银行卡号、券商 token、cookie 或 `.env` 凭证。
""",
    "08-记忆系统/L1-画像记忆/家庭画像.md": """# 家庭画像

- 家庭/客户代号：{{HOUSEHOLD_NAME}}
- 建档日期：{{DATE}}
- 基准币种：{{BASE_CURRENCY}}

## 家庭阶段

- 

## 长期目标

- 

## 稳定约束

- 

## 风险偏好

- 
""",
    "08-记忆系统/L2-规则记忆/工作流说明.md": """# 家庭财务工作流说明

每次正式财务或投资决策按以下顺序：

1. 数据日期
2. 家庭安全
3. 资金属性
4. 资产配置
5. 风险桶
6. 标的判断
7. 行为金融自检
8. 执行计划
9. 复盘和记忆写入
""",
}


def render(text: str, values: dict[str, str]) -> str:
    for key, value in values.items():
        text = text.replace("{{" + key + "}}", value)
    return text


def write_file(path: Path, content: str, force: bool) -> bool:
    if path.exists() and not force:
        return False
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")
    return True


def copy_template(src_name: str, dest: Path, values: dict[str, str], force: bool) -> bool:
    src = TEMPLATES / src_name
    content = render(src.read_text(encoding="utf-8"), values)
    return write_file(dest, content, force)


def init_workspace(target: Path, household_name: str, base_currency: str, force: bool) -> list[Path]:
    today = dt.date.today()
    values = {
        "HOUSEHOLD_NAME": household_name,
        "BASE_CURRENCY": base_currency,
        "DATE": today.isoformat(),
        "MONTH": today.strftime("%Y-%m"),
    }

    target.mkdir(parents=True, exist_ok=True)
    changed: list[Path] = []

    for rel in STRUCTURE:
        (target / rel).mkdir(parents=True, exist_ok=True)

    for rel, content in STARTER_FILES.items():
        dest = target / rel
        if write_file(dest, render(content, values), force):
            changed.append(dest)

    for template_name, rel_dest in FILE_MAP.items():
        dest = target / render(rel_dest, values)
        if copy_template(template_name, dest, values, force):
            changed.append(dest)

    for template in TEMPLATES.glob("*.md"):
        dest = target / "99-模板" / template.name
        if not dest.exists() or force:
            shutil.copyfile(template, dest)
            changed.append(dest)

    return changed


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Create a Markdown household finance workspace with memory folders and starter templates."
    )
    parser.add_argument("--target", required=True, help="Target workspace directory.")
    parser.add_argument("--household-name", default="家庭代号", help="Household/client display alias.")
    parser.add_argument("--currency", default="CNY", help="Base currency, e.g. CNY, USD, HKD.")
    parser.add_argument("--force", action="store_true", help="Overwrite existing starter files.")
    args = parser.parse_args()

    target = Path(args.target).expanduser().resolve()
    changed = init_workspace(target, args.household_name, args.currency, args.force)

    print(f"Initialized: {target}")
    print(f"Files written or refreshed: {len(changed)}")
    for path in changed:
        print(f"- {path.relative_to(target)}")
    print("\nNext: fill 00-录入表/家庭基础信息录入表.md, then update 01-家庭档案/资产负债表.md.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
