<!--
文件：README.zh-CN.md
核心功能：作为 DaE 分支论文的中文入口页，连接原始 DaE 论文版本、AKM 分支关系与当前 markdown 稿件。
输入：DaE 原始论文线索、AKM 母港结构、旧论文仓公开链接。
输出：供 GitHub 中文读者理解 DaE 论文来源、版本关系与阅读路径的 README。
-->

# DaE Paper

<p align="center">
  <a href="./README.md">English</a> | <a href="./README.zh-CN.md">简体中文</a>
</p>

**AKM 母港中的 DaE 论文规范入口。**

## 定位

这个页面是 AKM 结构中的 DaE 论文入口。
它不替代原始的 DaE 独立论文线，而是负责整理阅读路径，并说明这条研究线如何被放入现在的 AKM 结构中。

## 原始公开论文线

原始 DaE 研究线有两个公开论文版本：

- **arXiv 风格稿：** *Dialogue as Elicitation: Building High-Fidelity Personas for Personalized AI Advisors with LLMs*
- **SSRN 版本：** *Reducing Alignment Debt in AI Advisory: The Dialogue-as-Elicitation Approach*

原始公开资产仍保留在历史研究仓：

- **历史研究仓：** https://github.com/sirsws/DaE-Personal-Strategic-Asset
- **SSRN PDF：** https://raw.githubusercontent.com/sirsws/DaE-Personal-Strategic-Asset/main/papers/dae_ssrn.pdf
- **arXiv draft PDF：** https://raw.githubusercontent.com/sirsws/DaE-Personal-Strategic-Asset/main/papers/dae_arxiv_draft.pdf

## 当前分支中的文件

- [manuscript.md](./manuscript.md)：与原始 DaE 论文线对齐的 markdown 版，保留在 AKM 仓内供分支级阅读。

## 建议阅读顺序

1. 先读原始 SSRN 或 arXiv PDF，理解独立 DaE 论文线。
2. 再读这里的 `manuscript.md`，看 AKM 仓中的 markdown 对应稿。
3. 如果你关心实现而不是论文，再回到 DaE 分支入口页。

## 与 AKM 的关系

AKM 现在是母港框架。
DaE 仍然是 persona 感知顾问场景中的首个完整参考实现。
因此，这条论文线在历史上仍然是 DaE-first，而当前仓库结构则是 AKM-first。