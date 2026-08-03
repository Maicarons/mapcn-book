# Mapcn 从入门到进阶

> 基于 **mapcn** 官方文档的系统性实战指南 —— 构建于 MapLibre GL 之上的 React 地图组件库，从入门到进阶。

[![Deploy to GitHub Pages](https://github.com/Maicarons/mapcn-book/actions/workflows/deploy.yml/badge.svg)](https://github.com/Maicarons/mapcn-book/actions/workflows/deploy.yml)

- 📖 在线文档站（GitHub Pages）：<https://maicarons.github.io/mapcn-book/>
- 📘 整书 PDF / DOCX / 教学 PPTX：见站点内「下载与资源」页

## 本书结构

全书分为 **4 大部分、共 14 章**：

| 部分 | 章节 | 主题 |
| --- | --- | --- |
| 第一部分 入门与环境 | 第 1–2 章 | mapcn 是什么、环境准备与安装 |
| 第二部分 地图基础与交互 | 第 3–6 章 | 第一张地图、控件与视口交互、标记点、弹窗与提示框 |
| 第三部分 图形与数据 | 第 7–10 章 | 路线、弧线、GeoJSON 区域地图、海量点聚合 |
| 第四部分 进阶与实战 | 第 11–14 章 | 深入 MapLibre 实例、主题与自定义底图、性能与最佳实践、门店地图实战 |

另含「参考资料」板块，收录对官方文档（简介 / 安装 / 地图 / 控件 / 标记点 / 弹窗 / 路线 / 弧线 / GeoJSON / 聚合 / 进阶 / API 参考）的研读摘要。

## 仓库结构（GitHub 结构）

```text
mapcn-book/
├── .github/workflows/deploy.yml   # GitHub Pages 自动构建与部署
├── docs/                          # VitePress 内容根目录
│   ├── .vitepress/                # 站点配置与主题
│   ├── public/downloads/          # PDF / DOCX / PPTX / 封面 SVG（发布资源）
│   ├── chapters/                  # 14 章正文（规范性标题）
│   ├── reference/                 # 官方文档研读摘要（12 篇）
│   ├── index.md                   # 首页
│   ├── preface.md                 # 前言
│   ├── downloads.md               # 下载与在线阅览
│   ├── zh/                        # 官方文档中文译稿（12 篇，可在线浏览）
│   └── en/                        # 官方文档英文原版（12 篇，可在线浏览）
├── tools/                         # 内容生产流水线
│   ├── normalize_chapters.py      # 章节标题规范化（第 NN 章 …）
│   ├── escape_angle.py            # 转义非代码块中的裸 <Component>
│   ├── gen_reference.py           # 由 docs/zh 生成 reference/ 研读笔记
│   └── build_book.py              # 14 章 -> 整书 Markdown
│   └── build_pptx.py              # 14 章 -> 教学 PPTX（配套讲义）
├── manuscript/book.md             # 由 14 章汇编而成的整书 Markdown
├── package.json                   # VitePress 依赖与脚本
└── README.md
```

> `docs/zh/` 与 `docs/en/` 为从项目文档（`src/app/(main)/docs`）导出的中文译稿与英文原版，既是整书与研读笔记的**原始素材**，也已直接发布到 VitePress 站点（中文文档 / English 两个侧栏分组），可在浏览器中对照阅读。

## 本地开发

```bash
npm install
npm run docs:dev      # 本地预览 http://localhost:5173
npm run docs:build    # 构建到 docs/.vitepress/dist
```

> 注意：仓库 `base` 为 `/mapcn-book/`，对应项目页路径；本地 `docs:dev` 预览时资源以根路径解析，属正常现象，构建产物部署到 GitHub Pages 后路径正确。

## 内容生产流水线

```bash
python tools/escape_angle.py     # 转义非代码块中的裸 <Component>
python tools/normalize_chapters.py   # 统一章节标题（第 NN 章 …）
python tools/gen_reference.py    # 由 docs/zh 生成 reference/ 研读笔记
python tools/build_book.py       # 生成 manuscript/book.md（整书）
python tools/build_pptx.py       # 生成 docs/public/downloads/mapcn-teaching.pptx（教学讲义）
```

整书 PDF / DOCX 由 `manuscript/book.md` 经 Pandoc + XeLaTeX（CJK 字体：Microsoft YaHei）转换生成，存放于 `docs/public/downloads/`：

```bash
pandoc manuscript/book.md -o docs/public/downloads/mapcn-book.pdf \
  --pdf-engine=xelatex --toc --toc-depth=2 -V CJKmainfont="Microsoft YaHei"
pandoc manuscript/book.md -o docs/public/downloads/mapcn-book.docx --toc --toc-depth=2
```

## 部署（GitHub Pages · GitHub Actions 自动部署）

站点已上线：<https://maicarons.github.io/mapcn-book/>

采用 **GitHub Actions 自动部署**：每次 push `main` 即自动构建并发布。

- 工作流文件：`.github/workflows/deploy.yml`（`checkout` → Setup Node 22 → `npm install` → `npm run docs:build` → 上传 Pages 产物 → `actions/deploy-pages` 发布）；
- 仓库 Pages **部署源已设为 GitHub Actions**。

## 版权与免责声明

本书由 AI 辅助文档生成流程编撰，内容以 mapcn 官方文档为基线整理，仅供学习与技术参考。mapcn 基于 MapLibre GL 构建，相关商标与版权归原权利人所有。涉及生产环境的关键决策，请以官方文档与社区最新结论为准。详见站点内免责声明与 `DISCLAIMER.md`。
