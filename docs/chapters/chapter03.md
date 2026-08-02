# 第 03 章 你的第一张地图

安装就绪后，第一步自然是让地图出现在页面上。mapcn 的 `Map` 组件把 MapLibre
的初始化、主题、上下文都封装好了，因此渲染一张地图只需要几行代码。

## 3.1 最小的地图

新建一个组件，引入 `Map`，给它一个高度合适的容器即可：

```tsx
import { Map } from "@/components/ui/map";

export function BasicMap() {
  return (
    <div className="h-[420px] w-full">
      <Map center={[-74.006, 40.7128]} zoom={12} />
    </div>
  );
}
```

这里有两个关键点：

- `center` 是 `[经度, 纬度]`（注意顺序是**经度在前**），本例指向纽约；
- `zoom` 是缩放级别，`12` 大致是「城市街区」的尺度。

地图容器必须**有明确的高度**，否则地图会塌陷为 0 高度而看不见。常见做法是用
`h-[420px]` 这类 Tailwind 工具类，或把地图放进一张 `Card` 里。

## 3.2 在 shadcn Card 中展示

把地图放进卡片，是文档站中最常见的布局：

```tsx
import { Map, MapControls } from "@/components/ui/map";
import { Card } from "@/components/ui/card";

export function MapInCard() {
  return (
    <Card className="h-[320px] p-0 overflow-hidden">
      <Map center={[-74.006, 40.7128]} zoom={11}>
        <MapControls />
      </Map>
    </Card>
  );
}
```

`Card` 提供了圆角与裁剪（`rounded`），`MapControls` 则叠加了缩放等
交互控件（详见第 4 章）。

## 3.3 Next.js 下的 "use client"

在 Next.js App Router 等「默认服务端渲染」的框架里，任何用到状态、事件、浏览器
API 的组件都必须标注为客户端组件：

```tsx
"use client";

import { Map } from "@/components/ui/map";

export function ClientMap() {
  return (
    <div className="h-[420px] w-full">
      <Map center={[-74.006, 40.7128]} zoom={12} />
    </div>
  );
}
```

原则上，只要组件链中**任何一个**用到了 `useState`、`useEffect`、事件处理或
浏览器 API，其所在文件（及所有交互子组件）都应加 `"use client"`。纯展示的静态地图
在严格的服务端环境下也能渲染外壳，但加上它最省心。

## 3.4 视口：center、zoom、bearing、pitch

`Map` 暴露了完整（且类型安全）的视口属性，常用的有：

| 属性 | 含义 | 典型取值 |
| --- | --- | --- |
| `center` | 中心坐标 `[经度, 纬度]` | `[-74, 40.7]` |
| `zoom` | 缩放级别（0=世界，22=楼栋） | `12` |
| `bearing` | 方位角（顺时针旋转，度） | `0` |
| `pitch` | 倾角（2D→3D，度） | `0` |

例如，让地图带一点 3D 倾角：

```tsx
<Map center={[-73.9857, 40.7484]} zoom={15} pitch={60} bearing={-20} />
```

## 3.5 受控模式

当 `viewport` 与 `onViewportChange` 同时传入时，地图进入**受控模式**：视口完全
由你的状态驱动，地图的平移、缩放、旋转都会回调给你。

```tsx
"use client";

import { useState } from "react";
import { Map, type MapViewport } from "@/components/ui/map";

export function ControlledMap() {
  const [viewport, setViewport] = useState<MapViewport>({
    center: [-74.006, 40.7128],
    zoom: 8,
    bearing: 0,
    pitch: 0,
  });

  return (
    <div className="relative h-[420px] w-full">
      <Map viewport={viewport} onViewportChange={setViewport} />
      <div className="absolute top-2 left-2 rounded border px-2 py-1 font-mono text-xs">
        <div>lng: {viewport.center[0].toFixed(3)}</div>
        <div>lat: {viewport.center[1].toFixed(3)}</div>
        <div>zoom: {viewport.zoom.toFixed(1)}</div>
      </div>
    </div>
  );
}
```

受控模式的典型用途：把地图状态写进 URL 以便分享、与外部滑块联动、或做「地图与
列表双向高亮」。非受控场景下，仅用 `onViewportChange` 也能单纯「监听」变化，不
接管控制权。

## 3.6 主题自动切换

`Map` 会读取文档根元素的 `dark` / `light` class（兼容 next-themes），并监听
系统偏好变化，自动在浅色/深色底图间切换。你**无需写任何额外代码**。

若想强制指定主题，可传 `theme` 属性：

```tsx
<Map theme="dark" center={[-74.006, 40.7128]} zoom={11} />
```

## 本章小结

- 渲染地图只需 `Map` 组件（`<Map center={...} zoom={...} />`），容器必须有确定高度；
- 把地图放进 `Card` 是常见且优雅的布局；
- Next.js 等环境下，含交互逻辑的组件需加 `"use client"`；
- 视口属性 `center`/`zoom`/`bearing`/`pitch` 类型安全，受控模式用
  `viewport` + `onViewportChange`；
- 主题默认根据文档 class 与系统偏好自动切换，可用 `theme` 覆盖。

下一章，我们为地图加上交互控件。
