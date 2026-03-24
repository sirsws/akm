<!--
文件：README.zh-CN.md
核心功能：作为 DaE 分支在 AKM 母港中的中文说明页，供 GitHub 读者从英文主页切换进入。
输入：AKM 母定义、DaE 发布资产与研究资产。
输出：供 GitHub 使用的中文分支总览页。
-->

# DaE

**DaE 是 AKM 在 Persona / 顾问协作场景下的首个完整参考实现。**

[English](./README.md)

DaE 不再作为与 AKM 平行的独立母概念存在。

它现在的角色非常明确：

**如果 AKM 解决的是“先把人建模出来”，那么 DaE 解决的是“在 persona 感知协作任务里，怎样把这件事做成一个可复用系统”。**

## 这个分支解决什么问题

很多协作型 agent 的问题，不是不会回答，而是还没理解用户就开始工作。

DaE 通过先构建 `PersonaProfile` 来修正这层上游失真。

## 分支定位

- 母概念：AKM
- 场景：Persona / 顾问协作
- 上游资产：`PersonaProfile`
- 角色：首个完整参考实现

## 入口

- [Paper](./paper/README.md)
- [Skill](./skill/README.md)