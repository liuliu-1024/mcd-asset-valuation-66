#!/usr/bin/env python3
"""
麦麦资产评估报告 - 评估结果复算校验脚本

功能：
1. 积分折现复算：验证积分资产现值计算是否正确
2. 优惠率勾稽：验证优惠券节约率与明细数据是否一致
3. 汇总表平衡：验证各分项加总是否等于汇总值

用法：
  python3 valuation_check.py --report <报告JSON数据>
  python3 valuation_check.py --self-test

输出：
  PASS / FAIL + 具体差异行
"""

import json
import sys
import argparse
from typing import Dict, Any, List, Tuple


def check_points_discount(data: Dict) -> Tuple[bool, str]:
    """积分折现复算：验证积分资产现值计算"""
    try:
        account = data.get("points_account", {})
        params = data.get("valuation_params", {})

        available = account.get("available_points", 0)
        monthly_avg = params.get("monthly_avg_points", 0)
        discount_rate = params.get("discount_rate", 0.08)
        unit_value = params.get("unit_value", 0.008)
        period_months = params.get("period_months", 12)

        # 复算：简化年金现值（年化折现，按月折半近似）
        # PV = monthly_avg * period_months * unit_value / (1 + discount_rate/2)
        expected_pv = monthly_avg * period_months * unit_value / (1 + discount_rate / 2)
        reported_pv = data.get("results", {}).get("points_present_value", 0)

        # 自检数据中 reported_pv 应等于 expected_pv
        diff = abs(expected_pv - reported_pv)
        tolerance = max(0.01, expected_pv * 0.02)  # 2% 容差

        if diff <= tolerance:
            return True, f"积分折现复算通过（现值 ¥{reported_pv:.2f}，复算 ¥{expected_pv:.2f}，差异 ¥{diff:.2f}）"
        else:
            return False, f"积分折现复算失败（报告值 ¥{reported_pv:.2f}，复算值 ¥{expected_pv:.2f}，差异 ¥{diff:.2f} 超容差 ¥{tolerance:.2f}）"
    except Exception as e:
        return False, f"积分折现复算异常：{e}"


def check_coupon_rate(data: Dict) -> Tuple[bool, str]:
    """优惠率勾稽：验证优惠券节约率"""
    try:
        orders = data.get("orders", [])
        total_paid = sum(o.get("paid_amount", 0) for o in orders)
        total_list = sum(o.get("list_price", 0) for o in orders)

        if total_list == 0:
            return True, "优惠率勾稽跳过（无订单数据）"

        expected_savings = total_list - total_paid
        expected_rate = (expected_savings / total_list) * 100

        reported_savings = data.get("results", {}).get("coupon_savings", 0)
        reported_rate = data.get("results", {}).get("coupon_utilization_rate", 0)

        savings_diff = abs(expected_savings - reported_savings)
        rate_diff = abs(expected_rate - reported_rate)

        if savings_diff <= 0.01 and rate_diff <= 0.1:
            return True, f"优惠率勾稽通过（节约 ¥{reported_savings:.2f}，利率 {reported_rate:.1f}%）"
        else:
            return False, f"优惠率勾稽失败（节约差异 ¥{savings_diff:.2f}，利率差异 {rate_diff:.1f}%）"
    except Exception as e:
        return False, f"优惠率勾稽异常：{e}"


def check_summary_balance(data: Dict) -> Tuple[bool, str]:
    """汇总表平衡：验证各分项加总等于汇总值"""
    try:
        results = data.get("results", {})
        items = [
            ("consumption_savings", "消费已实现节约价值"),
            ("coupon_net_value", "优惠资产净值"),
            ("points_net_value", "积分资产净值"),
        ]

        total = 0
        for key, label in items:
            total += results.get(key, 0)

        reported_total = results.get("total_net_value", 0)
        diff = abs(total - reported_total)
        tolerance = 0.01

        if diff <= tolerance:
            return True, f"汇总表平衡通过（合计 ¥{reported_total:.2f} = 各分项之和 ¥{total:.2f}）"
        else:
            return False, f"汇总表不平衡（各分项之和 ¥{total:.2f} != 报告合计 ¥{reported_total:.2f}，差异 ¥{diff:.2f}）"
    except Exception as e:
        return False, f"汇总表平衡异常：{e}"


def run_checks(data: Dict) -> bool:
    """运行全部校验"""
    checks = [
        ("积分折现复算", check_points_discount),
        ("优惠率勾稽", check_coupon_rate),
        ("汇总表平衡", check_summary_balance),
    ]

    all_pass = True
    print("=" * 60)
    print("麦麦资产评估报告 - 校验结果")
    print("=" * 60)

    for name, func in checks:
        passed, msg = func(data)
        status = "PASS" if passed else "FAIL"
        print(f"[{status}] {name}: {msg}")
        if not passed:
            all_pass = False

    print("=" * 60)
    print(f"总体结果: {'PASS - 校验通过' if all_pass else 'FAIL - 存在不一致项，请修正后重新出报告'}")
    print("=" * 60)
    return all_pass


def self_test():
    """自检模式：使用测试数据验证校验逻辑"""
    test_data = {
        "points_account": {
            "available_points": 12480,
            "total_points": 12480,
            "frozen_points": 0,
            "expiring_points": 3200,
        },
        "valuation_params": {
            "monthly_avg_points": 1248,
            "discount_rate": 0.08,
            "unit_value": 0.008,
            "period_months": 12,
        },
        "orders": [
            {"paid_amount": 45.50, "list_price": 55.00},
            {"paid_amount": 38.00, "list_price": 42.00},
            {"paid_amount": 52.00, "list_price": 60.00},
        ],
        "results": {
            "points_present_value": 115.20,  # 1248*12*0.008/(1+0.04) = 115.20
            "coupon_savings": 21.50,  # (55+42+60) - (45.5+38+52) = 157-135.5 = 21.5
            "coupon_utilization_rate": 13.7,  # 21.5/157*100 = 13.69...
            "consumption_savings": 855.80,
            "coupon_net_value": 0,  # 优惠券节约已计入消费节约
            "points_net_value": 89.60,  # 115.20 - 3200*0.008 = 115.20-25.60
            "total_net_value": 945.40,  # 855.80 + 0 + 89.60
        },
    }

    print("运行自检...\n")
    success = run_checks(test_data)
    return success


def main():
    parser = argparse.ArgumentParser(description="麦麦资产评估报告校验脚本")
    parser.add_argument("--report", type=str, help="评估报告 JSON 数据文件路径")
    parser.add_argument("--self-test", action="store_true", help="运行自检")
    args = parser.parse_args()

    if args.self_test:
        success = self_test()
        sys.exit(0 if success else 1)

    if args.report:
        with open(args.report, "r", encoding="utf-8") as f:
            data = json.load(f)
        success = run_checks(data)
        sys.exit(0 if success else 1)

    parser.print_help()


if __name__ == "__main__":
    main()
