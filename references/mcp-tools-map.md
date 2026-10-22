# 麦当劳 MCP 工具与评估环节映射表

> 本文件按需加载，列出全部 33 个 MCP 工具及其在评估流程中的用途。

## 核心工具（评估必用）

| 工具名 | 评估阶段 | 用途 | 关键返回字段 |
|---|---|---|---|
| query-my-account | 积分资产评估 | 积分账户四要素 | availablePoints, totalPoints, frozenPoints, expiringPoints |
| order-list | 消费资产清查 | 历史订单明细 | orders[].amount, items, storeTime, status |
| query-meals | 市场比较法 | 菜单挂牌价基准 | meals[].price, code, category |
| query-meal-detail | 市场比较法 | 餐品详情与套餐组成 | meal.combo, options, nutrition |
| calculate-price | 重置成本法 | 当前挂牌价计算 | totalAmount, discountAmount, deliveryFee |
| query-my-coupons | 优惠资产盘点 | 已领券状态 | coupons[].status, discountAmount, expiryDate |
| available-coupons | 优惠资产盘点 | 可领未领券 | coupons[].title, value, conditions |
| query-store-coupons | 优惠资产盘点 | 门店可用券 | coupons[].couponId, applicableItems |
| list-nutrition-foods | 营养价值评估 | 餐品营养成分 | foods[].calories, protein, fat, carbs, sodium, calcium |
| mall-points-products | 积分变现价值 | 积分商城兑换商品 | products[].pointsCost, cashValue, name |

## 辅助工具（评估建议章节使用）

| 工具名 | 用途 | 使用场景 |
|---|---|---|
| campaign-calendar | 查询当月营销活动 | 评估建议：活动期间消费更优惠 |
| query-nearby-stores | 查询附近门店 | 评估建议：门店选择优化 |
| auto-bind-coupons | 一键领券 | 评估建议：自动领取可用优惠券 |
| query-lottery-info | 积分抽奖活动信息 | 评估建议：积分抽奖 vs 兑换的收益对比 |
| now-time-info | 获取当前时间 | 确定评估基准日 |

## 点餐工具（评估流程不直接使用，但可用于模拟重置）

| 工具名 | 用途 |
|---|---|
| delivery-query-addresses | 获取配送地址列表 |
| delivery-create-address | 新增配送地址 |
| delivery-query-stores | 查询可配送门店 |
| query-meal-assistance | 查询助餐服务（团餐） |
| create-order | 创建订单 |
| cancel-order | 取消订单 |
| query-order | 查询订单详情 |

## 积分商城工具

| 工具名 | 用途 |
|---|---|
| mall-product-detail | 查询商城商品详情 |
| mall-create-order | 积分兑换商品下单 |
| mall-order-list | 商城订单查询 |
| mall-order-detail | 商城订单详情 |

## 抽奖工具

| 工具名 | 用途 |
|---|---|
| draw-lottery | 执行积分抽奖 |
| query-my-prizes | 查看抽奖奖品记录 |

## 主题活动工具

| 工具名 | 用途 |
|---|---|
| query-party-city | 主题活动城市列表 |
| query-party-store | 主题活动门店列表 |
| query-partystore-date | 主题活动可预约日期 |
| query-partystore-session | 主题活动可预约场次 |
| party-order-create | 创建主题活动订单 |

## 数据采集策略

1. **批量取数**：阶段一一次性调用 7-9 个工具，减少往返
2. **限流注意**：每分钟最多 600 次请求，评估流程通常 10-20 次调用，远低于限流
3. **数据缺失处理**：某工具返回空或错误时标【待采集】，不阻塞其他工具的取数
4. **缓存复用**：同一评估周期内已获取的数据不重复请求
