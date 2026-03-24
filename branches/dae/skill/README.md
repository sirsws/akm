<!--
文件：README.md
核心功能：作为 DaE skill 在 AKM 母港中的入口说明，明确其安装、用途、边界与对上游 AKM 的依赖。
输入：DaE 既有 skill 包、AKM 母港结构与 DaE 分支定位。
输出：供外部技能页或技能仓入口直接复用的说明文档。
-->

# DaE Skill

DaE skill 是 `AKM -> DaE` 这条分支下的可执行入口。

它只做一件事：

**先通过追问建立 `PersonaProfile`，再把这份上游画像交给下游智能体使用。**

## 文件

- [SKILL.md](./SKILL.md)
- [references/](./references/)
