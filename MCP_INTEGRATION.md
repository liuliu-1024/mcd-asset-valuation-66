# MCP 集成说明

## 一、接入的 MCP 服务

| 项目 | 内容 |
|---|---|
| 服务名 | mcd-mcp |
| 类型 | streamablehttp |
| 接入地址 | `https://mcp.mcd.cn` |
| 鉴权方式 | Bearer Token |
| Token 获取 | [open.mcd.cn](https://open.mcd.cn) → 登录 → 控制台 → 激活 |
| 限流 | 600 次/分钟 |

## 二、配置方法

在 WorkBuddy 中配置自定义连接器：

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

> 请妥善保管 MCP Token，避免泄露。本项目中所有配置仅使用占位符。

## 三、使用的 MCP 工具清单

### 核心工具（评估必用，9个）

| 工具 | 评估阶段 | 用途 | 关键返回字段 |
|---|---|---|---|
| query-my-account | 积分资产评估 | 积分账户四要素 | availablePoints, totalPoints, frozenPoints, expiringPoints |
| order-list | 消费资产清查 | 历史订单明细 | orders[].amount, items, storeTime, status |
| query-meals | 市场比较法 | 菜单挂牌价基准 | meals[].price, code, category |
| query-meal-detail | 市场比较法 | 餐品详情与套餐组成 | meal.combo, options |
| calculate-price | 重置成本法 | 当前挂牌价计算 | totalAmount, discountAmount |
| query-my-coupons | 优惠资产盘点 | 已领券状态 | coupons[].status, discountAmount, expiryDate |
| available-coupons | 优惠资产盘点 | 可领未领券 | coupons[].title, value |
| list-nutrition-foods | 营养价值评估 | 餐品营养成分 | foods[].calories, protein, fat, sodium |
| mall-points-products | 积分变现价值 | 积分商城兑换商品 | products[].pointsCost, cashValue |

### 辅助工具（评估建议章节使用）

| 工具 | 用途 |
|---|---|
| query-store-coupons | 查询门店可用优惠券 |
| campaign-calendar | 查询当月营销活动 |
| query-nearby-stores | 查询附近门店 |
| auto-bind-coupons | 一键领取麦麦省优惠券 |
| now-time-info | 获取当前时间（确定评估基准日） |

## 四、数据流

```
麦当劳 MCP Server (mcp.mcd.cn)
        |
        v
  阶段一：数据采集（9个工具批量取数）
  ├── query-my-account → 积分四要素
  ├── order-list → 历史订单明细
  ├── query-meals → 菜单挂牌价
  ├── calculate-price → 重置成本
  ├── query-my-coupons → 优惠券状态
  ├── available-coupons → 可领券
  ├── list-nutrition-foods → 营养成分
  └── mall-points-products → 积分变现单价
        |
        v
  阶段二：清查核实（逐笔核对 + 交叉验证）
        |
        v
  阶段三：评定估算（三大方法分别计算）
  ├── 市场比较法 → 消费性价比系数 + 评级
  ├── 重置成本法 → 优惠券节约净值 + 利用率
  └── 收益现值法 → 积分资产现值 + 减值预警
        |
        v
  阶段四：出具报告（10章节评估报告）
```

## 五、错误处理

| 错误码 | 原因 | 处理 |
|---|---|---|
| 401 | Token 无效/过期 | 提示用户重新获取 Token |
| 429 | 限流（>600次/分） | 降低请求频率，已获数据照常评估 |
| 空返回 | 账号无对应数据 | 标【待采集】，不阻塞其他工具 |

## 六、安全说明

- MCP Token 是用户私密数据，本 Skill 不会索要、记录或输出 Token
- 所有配置仅使用环境变量占位符 `YOUR_MCP_TOKEN`
- 网络请求仅发往麦当劳官方 MCP 服务 `mcp.mcd.cn`
