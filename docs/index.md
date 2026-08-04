---
layout: home

hero:
  name: "Mapcn 从入门到进阶"
  text: "基于官方文档的系统性实战指南"
  tagline: 复制粘贴 · 组件化 · 可定制 —— 一本既能入门、又能进阶的 MapLibre React 地图组件中文专著
  actions:
    - theme: brand
      text: 开始阅读
      link: /chapters/chapter01
    - theme: alt
      text: 下载 PDF / 讲义
      link: /downloads
  image:
    alt: Mapcn 书封
    light: /downloads/cover-light.svg
    dark: /downloads/cover-dark.svg

features:
  - icon: 🗺️
    title: 由浅入深，四大板块
    details: 入门与环境 → 地图基础与交互 → 图形与数据 → 进阶与实战，共 14 章、4 大部分。
  - icon: 🎯
    title: 事实可溯，代码可运行
    details: 内容以 mapcn 官方文档为基线整理；所有示例均基于真实组件 API，可在项目中直接复用。
  - icon: 🧩
    title: 复制粘贴即拥有
    details: mapcn 是 copy-paste 式的组件库，书中逐章拆解 Map / Marker / Route / Arc / GeoJSON / Cluster 等核心能力。
  - icon: 📎
    title: 配套 PDF / DOCX / 讲义 PPT
    details: 提供整书 PDF（在线阅览 + 下载）、可编辑 DOCX 源文件，以及 92 页配套教学 PPTX 讲义，便于教学与离线阅读。
  - icon: 🌐
    title: 官方文档中英对照
    details: 同一套官方文档提供中文译稿与英文原版，可在站点内对照阅读，精准理解组件 API。
---

## 这本书讲什么

在 Web 前端，"给页面加一张可交互的地图"似乎从来都不是一件轻松的事：开发者往往要在「引入一个庞大的地图 SDK」「配置 API Key」「与一堆命令式 API 搏斗」之间反复横跳。**mapcn** 试图把这件事变得更像写普通 UI：组件化、可组合、可定制，且代码归你所有。

mapcn 是一套**免费、开源、可复制粘贴**的 React 地图组件库。它构建于 [MapLibre GL](https://maplibre.org) 之上，使用 [Tailwind CSS](https://tailwindcss.com) 进行样式设计，并刻意契合 [shadcn/ui](https://ui.shadcn.com) 的使用习惯。你不必把整座地图引擎"安装"进项目，只需要把需要的组件文件复制进来，它们就是你的代码。

本书完全建立在 mapcn 官方文档的基础之上，按"由浅入深、面面俱到"的原则重新编排，力求给中文世界的 React 开发者一本"既能入门、又能进阶"的 mapcn 专著。

## 如何阅读

- **完全的初学者**：建议从第 1 章顺序读到第 6 章，把基础打牢。
- **有 React / 地图开发经验**：可跳过入门铺垫，直接从地图交互或图形数据部分切入。
- **想深入引擎**：第四部分（进阶与实战）值得精读，尤其是"深入 MapLibre 实例"一章。

每章末尾都配有"本章小结"，便于复习与速查。建议读者在自己的项目中动手敲一遍代码——mapcn 的"复制即拥有"特性，让即时实验的成本几乎为零。

## 官方文档（中英对照）

除了本书的系统性讲解，站点还直接收录了 mapcn **官方文档的中文译稿与英文原版**，便于你对照查阅原始 API 描述、或在英文术语与中文表述之间来回切换：

<div class="docs-entry">
  <a class="docs-card" href="/zh/00-introduction">
    <span class="docs-card-flag">🇨🇳</span>
    <span class="docs-card-title">官方文档（中文）</span>
    <span class="docs-card-desc">完整中文译稿，从组件总览到 API 参考逐一对照，适合以中文精读。</span>
    <span class="docs-card-go">阅读中文文档 →</span>
  </a>
  <a class="docs-card" href="/en/00-introduction">
    <span class="docs-card-flag">🇬🇧</span>
    <span class="docs-card-title">Official Docs (English)</span>
    <span class="docs-card-desc">The original English documentation, verbatim from mapcn.dev — best for precise API terms.</span>
    <span class="docs-card-go">Read English docs →</span>
  </a>
</div>

这两套文档与本书「参考资料（官方文档研读）」互为补充：研读摘要帮你快速抓住重点，完整官方文档则保留全部细节。
