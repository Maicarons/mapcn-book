# 第 02 章 环境准备与安装

任何组件库的第一步都是把环境搭好。mapcn 对运行环境的要求很低：一个现代 React
项目、Tailwind CSS，以及 shadcn/ui 的基础配置即可。本章带你逐项确认前置条件，
并完成组件的安装。

## 2.1 前置条件

在开始之前，请确认你的项目满足以下条件：

- **React 18+**：mapcn 使用了 `use()`、并发特性等现代 React API；
- **Tailwind CSS**：组件样式完全基于 Tailwind 工具类；
- **shadcn/ui 基础**：需要 `cn()` 工具函数（通常位于 `lib/utils.ts`）与一套
  shadcn 设计令牌（`--background`、`--foreground`、`--border`、`--muted`
   等 CSS 变量）。

如果你的项目还没有 shadcn/ui，可先运行官方初始化：

```bash
npx shadcn@latest init
```

该命令会创建 `components.json`、`lib/utils.ts` 以及 `cn()` 中的设计令牌，
这些正是 mapcn 组件所依赖的。

> **说明：** mapcn 组件内部引用了 `cn()`（来自 `lib/utils.ts`）与一系列语义化
> 颜色令牌。只要你的项目沿用了 shadcn 的约定，组件即可零改动使用。

## 2.2 安装地图组件

mapcn 以 shadcn registry 的形式分发。运行以下命令，即可把 `Map` 组件及其依赖
复制进项目：

```bash
npx shadcn@latest add https://mapcn.dev/r/map.json
```

执行后会发生两件事：

1. 安装运行时依赖 `maplibre-gl`；
2. 在 `components/ui/map.tsx` 写入组件源码（即 `map.tsx` 的内容）。

> **为什么是「复制」而不是「安装」？** 因为 mapcn 的组件源码直接进入你的仓库，
> 你之后对它的任何修改都不会被上游覆盖。这也是它与普通 npm 包最本质的区别。

## 2.3 验证安装结果

安装完成后，项目结构应多出以下关键文件：

```
your-project/
├── components/
│   ├── ui/
│   │   └── map.tsx          # mapcn 地图组件（你拥有的源码）
│   └── ...
├── lib/
│   └── utils.ts             # cn() 工具
├── package.json             # 已包含 maplibre-gl
└── ...
```

你可以用一个最小示例确认一切就绪（完整代码见第 3 章）。若浏览器中能渲染出地图，
说明安装成功。

## 2.4 关于 import 路径

本书所有示例统一使用 shadcn 约定路径：

```ts
import { Map, MapControls } from "@/components/ui/map";
```

其中 `@` 是项目配置的模块别名（指向 `src/`）。若你的项目使用其它别名（如 `~/`），按实际配置调整即可——组件本身不关心路径，只关心导出了哪些符号。

mapcn 导出的顶层符号包括：

- `Map`、`MapControls`：容器与控件；
- `MapMarker`、`MarkerContent`、`MarkerPopup`、`MarkerTooltip`：
  标记相关；
- `MapPopup`：独立弹窗；
- `MapRoute`、`MapArc`、`MapGeoJSON`、`MapClusterLayer`：图形图层；
- `useMap`：访问底层实例的钩子；
- 类型：`MapRef`、`MapViewport`、`MapArcDatum` 等。

## 2.5 常见问题

**Q：需要申请 API Key 吗？**
不需要。默认底图使用 Carto 的免费瓦片，无需密钥。若切换到 MapTiler 等需要
密钥的服务，则按服务商要求配置。

**Q：能用 Next.js / Vite / CRA 吗？**
可以。mapcn 是纯客户端组件库。在 Next.js App Router 下，包含交互逻辑的组件需
加 `"use client"` 指令（详见第 3 章）。

**Q：maplibre-gl 的 CSS 去哪了？**
组件内部已引入 `maplibre-gl` 的样式，你无需手动引入。

## 本章小结

- 前置条件：现代 React + Tailwind CSS + shadcn/ui 基础（提供 `cn()` 与设计令牌）；
- 安装命令：`npx shadcn@latest add https://mapcn.dev/r/map.json`；
- 安装结果：运行时依赖 `maplibre-gl` + 源码 `map.tsx`；
- 组件以「复制进项目」的方式分发，源码归你所有、可自由修改；
- 统一通过 `@/components/ui/map` 引入，导出了 Map、各类图层与 `useMap` 钩子。

下一章，我们渲染出第一张真正可交互的地图。
