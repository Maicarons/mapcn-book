# 第 01 章 初识 mapcn：地图组件的另一种可能

在 Web 前端，给页面加一张可交互的地图，似乎从来都不是一件轻松的事。开发者往往
要在「引入一个庞大的地图 SDK」「配置 API Key」「与一堆命令式 API 搏斗」之间反复
横跳。mapcn 试图把这件事变得更像写普通 UI：组件化、可组合、可定制，且代码归你
所有。

本章将回答三个问题：mapcn 是什么、它和主流方案有何不同、以及我们应当怎样看待
它适用的边界。

## 1.1 mapcn 是什么

mapcn 是一套**免费、开源、可复制粘贴**的 React 地图组件库。它构建于
[MapLibre GL](https://maplibre.org) 之上，使用 [Tailwind CSS](https://tailwindcss.com)
进行样式设计，并刻意契合 [shadcn/ui](https://ui.shadcn.com) 的使用习惯。

与「安装一个 npm 包、然后 import 它导出的黑盒组件」不同，mapcn 沿用了 shadcn 的
哲学：**组件源码直接复制进你的项目**。这意味着：

- 你拥有全部源码，可以逐行修改；
- 没有运行时锁定，升级、裁剪、分叉都由你决定；
- 组件天然融入你既有的 Tailwind 与 shadcn 设计令牌（design tokens）。

一句话概括：mapcn 把「地图」从外部依赖，变成了你代码库里的一等公民。

## 1.2 为什么不直接用 MapLibre

MapLibre GL JS 本身是优秀的开源地图引擎，但它是**命令式**的：你拿到一个
 `Map` 实例，然后调用 `setCenter()`、`flyTo()` 这样的 API。
在 React 的声明式世界里，这种写法容易与组件生命周期、状态同步产生摩擦。

mapcn 的价值，正是架在 MapLibre 与 React 之间那层薄而稳的桥：

- 用 `Map`、`MapControls`、`MapMarker` 这类声明式组件描述「想要什么」；
- 把 MapLibre 的初始化、主题切换、图层增删、事件清理等脏活封装起来；
- 当你确实需要底层能力时，`useMap` 钩子与 `MapRef` 又能让你随时下沉到原生实例。

它不是要取代 MapLibre，而是让你**默认用 React 的方式思考，必要时才用 MapLibre 的方式**。

## 1.3 mapcn 与同类方案的对比

| 维度 | 传统地图 SDK | 图表库附带地图 | mapcn |
| --- | --- | --- | --- |
| 使用方式 | 命令式 API | 配置对象 | 声明式组件 |
| 代码归属 | 黑盒依赖 | 黑盒依赖 | 复制进项目，完全拥有 |
| 主题切换 | 手动适配 | 有限 | 浅/深自动切换 |
| 与 shadcn/Tailwind | 割裂 | 割裂 | 原生契合 |
| 底层控制 | 直接 | 受限 | `useMap` / `map` 直达 |

理解这张表，有助于判断 mapcn 是否适合你的项目：它最适合「想快速交付、又不愿
放弃控制权」的团队，尤其是已经采用 shadcn/ui 与 Tailwind 的 React 应用。

## 1.4 它能兼容哪些底图

mapcn 不绑定任何特定服务商。只要符合
[MapLibre 样式规范](https://maplibre.org/maplibre-style-spec/) 的瓦片都能用，包括
OpenStreetMap、Carto、MapTiler、Stadia Maps、Thunderforest 等。默认情况下，mapcn
使用 Carto 的免费底图瓦片，且无需任何 API Key。

> **提示：** 本书后续所有示例默认使用 mapcn 自带的 Carto 底图。当你需要品牌化
> 样式或离线底图时，再用 `style` 属性替换即可（见第 12 章）。

## 1.5 适用边界与本书路线

mapcn 并非银弹。以下场景需要你清醒评估：

- **超大规模实时数据**（十万级以上动态要素）：应更多依赖原生 MapLibre 图层与
 `WebGL` 能力，必要时绕过组件封装；
- **复杂的地图编辑/绘制编辑器**：mapcn 提供基础能力，但专业编辑器仍需自行扩展；
- **非 React 技术栈**：mapcn 是 React 组件库，不适用于 Vue、Svelte 等。

本书的路线由浅入深：

1. **入门（第 2–6 章）**：环境、安装、第一张地图、控件、标记与弹窗；
2. **图形与数据（第 7–10 章）**：路线、弧线、GeoJSON、聚合点；
3. **进阶（第 11–13 章）**：深入实例、主题样式、性能实践；
4. **实战（第 14 章）**：综合构建一个门店地图应用。

## 本章小结

- mapcn 是构建于 MapLibre 之上的、可复制粘贴的 React 地图组件库；
- 它的核心优势是「声明式 + 代码归你所有 + 与 shadcn/Tailwind 契合」；
- 它与 MapLibre 是协作而非替代关系，`Map` / `useMap` 提供底层出口；
- 它兼容任意 MapLibre 样式规范的底图，默认使用免费 Carto 瓦片；
- 适合快速交付且不愿放弃控制权的 React 团队，超大规模或专业编辑器场景需另行评估。

下一章，我们动手把 mapcn 装进你的项目。
