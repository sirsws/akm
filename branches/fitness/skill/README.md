<!--
文件：README.md
核心功能：作为 Fitness skill 的英文入口页，说明用途、方法分层、文件构成与输出方向。
输入：Fitness 分支的挖掘逻辑、记录模板、执行提示词与公开版 skill 设计。
输出：供 GitHub 或技能页直接引用的英文 README。
-->

# Fitness Skill

<p align="center">
  <a href="./README.md">English</a> | <a href="./README.zh-CN.md">简体中文</a>
</p>

## Purpose

The Fitness skill is the operational entry point for AKM in training decision workflows.
It is organized as a three-stage method rather than a single prompt.

## Method Layers

1. elicitation
2. structured record
3. execution decision

## Files

- [ELICITATION_PROMPT.md](./ELICITATION_PROMPT.md)
- [RECORD_TEMPLATE.md](./RECORD_TEMPLATE.md)
- [EXECUTION_PROMPT.md](./EXECUTION_PROMPT.md)
- [SKILL.md](./SKILL.md)
- [INPUT_TEMPLATE.md](./INPUT_TEMPLATE.md)

## Output Direction

The core output is not generic workout language.
The core output is a constraint-aware training decision built on body limits, equipment context, time budget, recovery state, and goal hierarchy.