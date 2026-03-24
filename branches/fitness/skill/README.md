<!--
文件：README.md
核心功能：作为 Fitness skill 的入口说明，明确其用途、输入要求、方法分层与输出形式。
输入：Fitness 分支的挖掘逻辑、记录模板、执行提示词与公开版 skill 设计。
输出：供技能页或仓库子目录直接复用的说明文档。
-->

# Fitness Skill

Fitness skill 是 `AKM -> Fitness` 分支下的可执行入口。

它不是一个单 Prompt，而是一套三段式方法：

1. 前置挖掘
2. 结构化记录
3. 裁决式执行

## 文件

- [ELICITATION_PROMPT.md](./ELICITATION_PROMPT.md)
- [RECORD_TEMPLATE.md](./RECORD_TEMPLATE.md)
- [EXECUTION_PROMPT.md](./EXECUTION_PROMPT.md)
- [SKILL.md](./SKILL.md)
- [INPUT_TEMPLATE.md](./INPUT_TEMPLATE.md)

## 方法核

Fitness 分支的核心不是“生成训练计划”，而是：

**先把用户的身体约束、器械环境、时间预算、恢复状态和主线目标建模清楚，再让执行模块做裁决。**

## 为什么它值得单独成支

因为它不是泛用健身建议，而是一个长期运行的 AKM 场景系统：

- 有前置挖掘
- 有结构化状态记录
- 有 append-only 训练日志
- 有当日裁决逻辑
