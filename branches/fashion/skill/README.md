<!--
文件：README.md
核心功能：作为 Fashion skill 的入口说明，明确其用途、输入要求、方法分层与输出形式。
输入：Fashion 分支的挖掘逻辑、记录模板、执行提示词与公开版 skill 设计。
输出：供技能页或仓库子目录直接复用的说明文档。
-->

# Fashion Skill

Fashion skill 是 `AKM -> Fashion` 分支下的可执行入口。

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

Fashion 分支的核心不是“生成穿搭建议”，而是：

**先把用户的体型、场景、衣橱资产、功能约束和风格偏好建模清楚，再让执行模块做裁决。**

## 为什么它值得单独成支

因为它不是泛用审美描述，而是一个带用户建模和衣橱资产建模的 AKM 场景系统。
