<!--
文件：README.md
核心功能：说明 Fashion 分支论文 LaTeX 工程的结构、编译方式与当前产物。
输入：main.tex、refs.bib、paper 目录下的 markdown 稿、摘要、关键词与参考文献清单。
输出：供后续继续修订、复编和提交 SSRN 使用的工程说明。
-->

# Fashion LaTeX Paper

## 当前文件

- `main.tex`：论文主文件
- `refs.bib`：BibTeX 条目
- `main.pdf`：编译产物

## 编译命令

```powershell
& 'd:\Program Files\MiKTeX\miktex\bin\x64\pdflatex.exe' -interaction=nonstopmode -halt-on-error 'main.tex'
& 'd:\Program Files\MiKTeX\miktex\bin\x64\bibtex.exe' 'main'
& 'd:\Program Files\MiKTeX\miktex\bin\x64\pdflatex.exe' -interaction=nonstopmode -halt-on-error 'main.tex'
& 'd:\Program Files\MiKTeX\miktex\bin\x64\pdflatex.exe' -interaction=nonstopmode -halt-on-error 'main.tex'
```

## 当前策略

- 复用 AKM 母论文模板，先生成可提交 SSRN 的英文稿
- 参考文献只使用 `../references.md` 已核验条目
- markdown 稿继续作为内容源，LaTeX 稿作为正式投递工程
