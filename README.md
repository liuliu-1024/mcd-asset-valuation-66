# 麦麦资产评估报告 McValuation

> 当资产评估师开始认真对待你的麦当劳消费记录……

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Platform](https://img.shields.io/badge/Platform-WorkBuddy-blue.svg)](https://www.workbuddy.cn)
[![MCP](https://img.shields.io/badge/MCP-McDonald's-red.svg)](https://open.mcd.cn)

## 这是什么

执业资产评估师 + 房地产估价师开发的 WorkBuddy Skill，连接麦当劳 MCP，用**真正的资产评估三大方法论**（市场比较法 / 重置成本法 / 收益现值法），给你的麦当劳消费数据出具一份正式的**《资产评估报告》**。

不是"省了多少"小工具，是带评估基准日、价值类型、评估假设、评估师声明的**专业报告**。

## 为什么这个项目不一样

| 别人在做 | 我们在做 |
|---|---|
| 算卡路里 | 用市场比较法评估消费性价比 |
| 领优惠券 | 用重置成本法评估优惠资产净值 |
| 查积分余额 | 用收益现值法评估积分资产现值 |
| "你省了XX元" | "你的麦麦净资产评估值为 ¥945.40" |

**核心差异化**：
- 三大评估方法全部映射到真实 MCP 数据，不是套模板
- 积分也能算现值，还能预警减值（即将过期的积分 = 资产贬值）
- 评估师签名级别的报告格式，专业反差感拉满

## 效果展示

报告包含 10 个章节，以下是核心部分：

### 评估结果汇总表

| 资产类别 | 评估方法 | 评估值(元) | 占比 |
|---|---|---|---|
| 消费已实现节约价值 | 市场比较法 | 855.80 | 90.5% |
| 积分资产净值 | 收益现值法 | 89.60 | 9.5% |
| **麦麦净资产评估值** | | **¥945.40** | **100%** |

### 积分减值预警

> ⚠️ **减值预警**：即将过期积分 **3,200 分**，计提减值准备 **¥25.60**。
> 建议在过期日前兑换积分商城等值商品，避免减值实现。

完整示例报告见 [examples/sample-report-output.md](examples/sample-report-output.md)

## 快速开始

### 1. 申请麦当劳 MCP Token

前往 [open.mcd.cn](https://open.mcd.cn) → 登录 → 控制台 → 激活 → 复制 Token

### 2. 在 WorkBuddy 中配置 MCP 连接器

打开 WorkBuddy → 左侧【专家·技能·连接器】→【连接器】→【自定义连接器】→【配置MCP】，填入：

```json
{
  "mcpServers": {
    "mcd-mcp": {
      "type": "streamablehttp",
      "url": "https://mcp.mcd.cn",
      "headers": {
        "Authorization": "Bearer YOUR_MCP_TOKEN"
      }
    }
  }
}
```

> 记得替换 `YOUR_MCP_TOKEN` 为实际 Token！

### 3. 安装 Skill 并使用

将本仓库的 `SKILL.md` 和 `references/` 目录安装到 WorkBuddy Skills 中，然后在对话框输入：

```
帮我评估我的麦麦资产，出具评估报告
```

一句话拿到你的麦麦资产评估报告。

## 三大评估方法怎么用

| 评估方法 | 评估什么 | 怎么算 | MCP 数据源 |
|---|---|---|---|
| **市场比较法** | 消费资产 | 实付金额 vs 菜单挂牌价，算性价比系数 | order-list + query-meals |
| **重置成本法** | 优惠资产 | 按当前菜单重置全价 - 实付 = 优惠券节约净值 | calculate-price + query-my-coupons |
| **收益现值法** | 积分资产 | 预测未来积分收益流，折现到今天算现值 | query-my-account + mall-points-products |

## 功能清单

- [x] 历史订单消费资产评估（市场比较法）
- [x] 优惠券利用率分析（重置成本法）
- [x] 积分资产估值 + 即将过期减值预警（收益现值法）
- [x] 营养摄入分析（对照每日推荐量基准）
- [x] 综合麦麦净资产 + 优化建议
- [x] 评估结果校验脚本（积分折现复算 / 优惠率勾稽 / 汇总表平衡）
- [x] Markdown 报告输出（支持 Word 输出）

## 项目结构

```
mcd-asset-valuation/
├── README.md                    # 你正在看的这个
├── CONTEST_DECLARATION.md       # 参赛声明
├── MCP_INTEGRATION.md           # MCP 集成说明
├── SKILL.md                     # Skill 核心定义
├── workbuddy.md                 # WorkBuddy 开发对话记录
├── LICENSE                      # MIT 许可证
├── references/                  # 按需加载的参考资料
│   ├── valuation-methodology.md # 三大评估方法论详解
│   ├── report-templates.md      # 报告模板骨架
│   ├── mcp-tools-map.md         # MCP 工具映射表
│   ├── nutrition-benchmark.md   # 营养参考标准
│   └── failure-modes.md         # 失败模式与降级
├── scripts/
│   └── valuation_check.py       # 评估结果校验脚本
└── examples/
    └── sample-report-output.md  # 示例评估报告
```

## 参赛信息

- **赛事**：1024 程序员节 · 麦当劳程序员创意开发大赛（M-CODE）
- **工具**：WorkBuddy + 麦当劳 MCP
- **作者**：执业资产评估师 x 房地产估价师

> 如果觉得有意思，点个 Star 支持一下执业评估师的跨界整活

## License

MIT
