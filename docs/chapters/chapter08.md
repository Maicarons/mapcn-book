# 第 08 章 弧线连接 Arcs

直线适合「路线」，但当你要表现**起点—终点的连接关系**——航线、物流通道、资金
流向——一根稍微弯曲的弧线往往比直线更有信息张力。mapcn 的 `MapArc` 专门为这类
场景设计：它在经纬度空间里用二次贝塞尔曲线把两点连成弧。

## 8.1 数据形态

每条弧线是一个 `MapArcDatum`：唯一 `id` + `from` + `to`（均为 `[number, number]`）。
把多条弧线组成数组传给 `data`：

```tsx
import { Map, MapArc, MapMarker, MarkerContent, MarkerLabel } from "@/components/ui/map";

const hub = { name: "伦敦", lng: -0.1276, lat: 51.5074 };
const destinations = [
  { name: "纽约", lng: -74.006, lat: 40.7128 },
  { name: "圣保罗", lng: -46.6333, lat: -23.5505 },
  { name: "东京", lng: 139.6917, lat: 35.6895 },
];

const arcs = destinations.map((d) => ({
  id: d.name,
  from: [hub.lng, hub.lat] as [number, number],
  to: [d.lng, d.lat] as [number, number],
}));

export function ArcExample() {
  return (
    <div className="h-[420px] w-full">
      <Map center={[hub.lng, hub.lat]} zoom={1} projection={{ type: "globe" }}>
        <MapArc data={arcs} paint={{ "line-color": "#3b82f6", "line-dasharray": [2, 2] }} interactive={false} />
      </Map>
    </div>
  );
}
```

注意这里通过 `projection` 属性传入 `{ type: "globe" }`，把地图切换为 3D 地球——弧线在地球
上看起来最自然。

## 8.2 弯曲程度与采样

| 属性 | 说明 | 默认值 |
| --- | --- | --- |
| `curvature` | 弧线偏离直线的程度，0 为直线，负值向另一侧弯 | `0.5` |
| `steps` | 每条弧线的采样点数，越大越平滑 | `60` |
| `id` | 底层 source/图层前缀 | 自动 |

想让弧线更「拱」，就调大 `curvature`；想要笔直连线，设 `0`。

## 8.3 用 MapLibre 表达式按类别着色

`MapArc` 的 `paint` 接受任意 `line-*` 字段，因此可以用 MapLibre
表达式按数据字段着色。下面的例子用 `match` 表达式，把「空运」染成紫色、「海运」
染成绿色：

```tsx
"use client";

import { useState } from "react";
import type { ExpressionSpecification } from "maplibre-gl";
import { Map, MapArc, MapPopup, type MapArcDatum } from "@/components/ui/map";

interface Lane extends MapArcDatum {
  origin: string;
  destination: string;
  mode: "air" | "sea";
}

const lanes: Lane[] = [
  { id: "dxb-jfk", origin: "迪拜", destination: "纽约", from: [55.2708, 25.2048], to: [-74.006, 40.7128], mode: "air" },
  { id: "sin-rtm", origin: "新加坡", destination: "鹿特丹", from: [103.8198, 1.3521], to: [4.4777, 51.9244], mode: "sea" },
];

const colorExpr: ExpressionSpecification = [
  "match", ["get", "mode"], "air", "#a78bfa", "sea", "#34d399", "#888",
];

export function ColoredArcs() {
  const [sel, setSel] = useState<Lane | null>(null);
  return (
    <div className="h-[420px] w-full">
      <Map center={[20, 20]} zoom={0.8}>
        <MapArc<Lane>
          data={lanes}
          paint={{ "line-color": colorExpr, "line-width": 1.5 }}
          hoverPaint={{ "line-width": 3, "line-opacity": 1 }}
          onHover={(e) => setSel(e ? e.arc : null)}
        />
        {sel && (
          <MapPopup longitude={sel.from[0]} latitude={sel.from[1]}>
            {sel.origin} → {sel.destination}
          </MapPopup>
        )}
      </Map>
    </div>
  );
}
```

这里出现了两个进阶属性：

- `hoverPaint`：悬停某条弧线时叠加的样式（通过 feature-state 实现，只影响当前弧）；
- `onHover`：悬停变化时的回调，可用于联动弹窗或侧栏。

## 8.4 进阶样式入口

`MapArc` 暴露了完整的 `paint` 与 `hoverPaint` 属性，等价于直接配置一个 MapLibre
`line` 图层。常见可用字段：

- `line-color` / `line-width` / `line-opacity` / `line-dasharray`
- （虚线）
- `line-cap` / `line-join`（连接与端点样式）

当内置属性不够用时，使用第 11 章的 `useMap` 直接操作底层图层是最灵活的退路。

## 本章小结

- `MapArc` 用 `data`（每条含 `from`/`to`）绘制经纬度空间的贝塞尔弧线；
- `curvature` 控制弯曲程度，`steps` 控制平滑度；
- `paint` 接受完整 MapLibre 表达式，可按字段着色（如空运/海运）；
- `hoverPaint` + `onHover` 实现悬停高亮与联动；
- 样式不足时，可下沉到 `useMap` 直接操作 line 图层。

下一章，我们用 GeoJSON 渲染面状区域。
