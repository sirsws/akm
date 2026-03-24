<!--
文件：README.md
核心功能：作为 Fitness 分支在 AKM 母港中的英文主入口，说明该分支的定位、方法结构、证据形态、论文与 skill 入口，以及适用边界。
输入：健身规则、训练日志、身体指标与 AKM 方法结构。
输出：供 GitHub 分支页直接使用的英文总览页。
-->

# AKM Fitness

**AKM Fitness = build the training profile first, then make the training decision.**

[中文说明](./README.zh-CN.md)

This is not a generic workout-plan generator.
It is built for the harder and more realistic problem: when goals conflict, the body has limits, equipment changes, and time is constrained, what should training actually look like today?

## What it solves

Typical fitness AI systems assume too much:

- one stable goal
- no meaningful body constraints
- full equipment access
- normal recovery and execution conditions

AKM Fitness reverses that logic.
It clarifies the operator first, then allows execution.

## Method structure

1. `Elicitation`
   Clarify goal ranking, body constraints, equipment context, time budget, recovery, and execution risk.
2. `Record`
   Store metrics, baselines, logs, and stage priorities as reusable upstream assets.
3. `Execution`
   Read the profile and output a real training decision with explicit risks and missing inputs.

## Evidence form

This branch can be honestly framed as:

**an n=1 longitudinal self-use AKM system case.**

Its evidence includes logs, metrics, hard constraints, and external model behavior tests.

## Entry points

- [Paper](./paper/README.md)
- [Skill](./skill/README.md)