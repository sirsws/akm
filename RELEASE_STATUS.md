<!--
文件：RELEASE_STATUS.md
核心功能：作为 AKM 母港的统一发布状态表，汇总当前各分支的完成度、可发布程度与剩余待办。
输入：AKM 母港当前目录结构、论文稿、skill 包、测试报告与发布文案。
输出：供后续 GitHub 推送、技能市场上架与 SSRN 链接回填时快速查看的状态总表。
-->

# AKM Release Status

## 总体判断

AKM 母港当前已经从“方案与素材堆”推进到“可发布资产包”。

更准确地说：

- 结构已完成
- 叙事已统一
- Fitness / Fashion 已有可发布 skill 包
- DaE 已完成并入口径
- 外部模型测试已完成一轮
- 剩余工作主要是发布动作，不再是方法搭建

## 母港层

### AKM 母港首页

- 状态：`Ready`
- 文件：`README.md`
- 说明：已明确 AKM 母概念、母论文与三条分支关系

### AKM 母定义

- 状态：`Ready`
- 文件：`AKM.md`
- 说明：作为母概念上游文件存在

### AKM 母论文入口

- 状态：`Ready`
- 文件：`papers/akm/README.md`
- 说明：母论文入口已建立，SSRN 公网链接待回填

## 分支层

### DaE

- 状态：`Ready for GitHub unification`
- 分支入口：`branches/dae/README.md`
- 论文入口：`branches/dae/paper/README.md`
- skill 入口：`branches/dae/skill/SKILL.md`
- 说明：已完成“DaE 是 AKM 首个完整参考实现”的并入口径
- 剩余动作：旧独立仓的对外说明回链到 AKM 母港

### Fitness

- 状态：`Ready for public skill release`
- 分支入口：`branches/fitness/README.md`
- 论文稿：`branches/fitness/paper/manuscript.md`
- skill 入口：`branches/fitness/skill/SKILL.md`
- 测试状态：已完成 DeepSeek 行为测试，并完成一次修正后复测
- 说明：当前定位为 `n=1 长期纵向自用系统`
- 剩余动作：决定是否进一步收紧低置信度场景下的动作建议

### Fashion

- 状态：`Ready for public skill release`
- 分支入口：`branches/fashion/README.md`
- 论文稿：`branches/fashion/paper/manuscript.md`
- skill 入口：`branches/fashion/skill/SKILL.md`
- 测试状态：已完成 DeepSeek 行为测试
- 说明：当前定位为 `单用户长期自用的系统设计与方法案例`
- 剩余动作：可选压缩商店页追问风格，使其更短更利落

## 测试层

### 外部模型测试

- 状态：`Ready`
- 文件：`deepseek_test_report_2026-03-24.md`
- 说明：已验证两条分支都不是单 Prompt，而是 AKM 场景方法

## 发布层

### GitHub 母港发布

- 状态：`Pending push`
- 说明：本地母港结构与文案已完成，待推送到远端仓

### 技能市场发布文案

- 状态：`Ready`
- 说明：Fitness / Fashion 已有长版与短版文案

### SSRN 链接回填

- 状态：`Waiting on SSRN`
- 说明：待母论文 SSRN URL 稳定后回填母港与旧记录

## 当前最值得做的 3 件事

1. 推送 AKM 母港到 GitHub
2. 先发布 Fitness 与 Fashion 的 skill 页面
3. 等 SSRN URL 稳定后补双向链接

## 当前不值得再做的事

- 继续讨论这两条分支值不值得写论文
- 再去扩新分支
- 为了看起来更像产品而稀释 AKM 的方法锋芒