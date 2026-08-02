# 简介（官方文档研读）

> **研读说明**：本页为 mapcn 官方文档「简介」的中文研读笔记，内容以官方文档为基线整理，作为正文之外的查阅与补充。
> 相关正文：第 1 章（初识 mapcn）。如与官方文档存在出入，请以官方文档为准。

**mapcn** 提供设计精美、可访问且可高度定制的地图组件。它构建于
[MapLibre GL](https://maplibre.org) 之上，使用
[Tailwind CSS](https://tailwindcss.com) 进行样式设计，并与
[shadcn/ui](https://ui.shadcn.com) 无缝协作。

## 设计理念

mapcn 在地图领域沿用 shadcn 的理念：组件以「复制即拥有」的方式提供，零锁定、
合理默认值、开箱即用。

地图组件常常被封装成隐藏在包装库与繁琐 SDK 背后的「黑箱」。mapcn 反其道而行：
它贴近 MapLibre，保持接口熟悉，并在需要更强控制力时，允许你直接下沉到原始的
地图实例。

目标很简单：让地图用起来像你技术栈中的其他 UI 一样——可组合、可换肤、可访问，
并能够用 Tailwind 与 shadcn 的模式轻松定制。

## 为什么选择 mapcn？

大多数 React 地图方案要么过于固执己见，要么过于笨重。mapcn 面向的是希望快速
交付、又不肯放弃控制权的团队：

- **代码归你所有**：将组件复制进项目，自由定制每一处细节。
- **上手极快**：一条命令即可渲染出第一张地图，并带生产级默认配置。
- **安全扩展**：直接在 MapLibre 之上构建，需要时在底层原生 API 上做文章。
- **设计系统友好**：使用 Tailwind 样式，天然契合 shadcn/ui 的使用习惯。

## 任意地图样式

mapcn 兼容任何
[MapLibre 风格的瓦片](https://maplibre.org/maplibre-style-spec/)。这意味着你
几乎可以使用任何服务商的瓦片：

- [OpenStreetMap](https://www.openstreetmap.org) — 社区驱动的开源地图数据
- [Carto](https://carto.com/basemaps) — 干净、极简的底图，最适合数据可视化
- [MapTiler](https://www.maptiler.com) — 漂亮的矢量瓦片，可深度定制
- [Stadia Maps](https://stadiamaps.com) — 快速、可靠的瓦片托管，多种样式
- [Thunderforest](https://www.thunderforest.com) — 面向户外、骑行、交通的专题地图
- 以及任何支持 MapLibre 样式规范的其它服务商

## 特性

- **零配置**：开箱即用，使用免费地图瓦片，无需 API Key。
- **主题感知**：在浅色与深色地图样式之间自动切换。
- **可组合**：用简单、可组合的组件构建复杂界面。
- **TypeScript**：完整类型安全，全面的 TypeScript 支持。
- **复制即粘贴**：代码归你所有，没有运行时依赖，直接复制进项目即可。
- **任意地图样式**：支持任何 MapLibre 兼容瓦片：MapTiler、Carto、OpenStreetMap 等。

