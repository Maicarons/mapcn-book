# 弧线 Arcs（官方文档研读）

> **研读说明**：本页为 mapcn 官方文档「弧线 Arcs」的中文研读笔记，内容以官方文档为基线整理，作为正文之外的查阅与补充。
> 相关正文：第 8 章（弧线连接）。如与官方文档存在出入，请以官方文档为准。

在两点坐标之间绘制曲线连接，并支持悬停与点击。

使用 `MapArc` 可以在坐标对之间绘制曲线。弧线非常适合表现航线、航运通道，或任何
「直连线条会显得平淡」的起点—终点连接。

## 基础弧线

向 `data` 属性传入弧线数组。每条弧线都需要一个唯一的 `id`，以及以
`[经度, 纬度]` 表示的 `from` / `to` 坐标。

```tsx
import { Map, MapArc, MapMarker, MarkerContent, MarkerLabel } from "@/registry/map";

const hub = { name: "伦敦", lng: -0.1276, lat: 51.5074 };
const destinations = [
  { name: "纽约", lng: -74.006, lat: 40.7128 },
  { name: "圣保罗", lng: -46.6333, lat: -23.5505 },
  { name: "东京", lng: 139.6917, lat: 35.6895 },
];

const arcs = destinations.map((dest) => ({
  id: dest.name,
  from: [hub.lng, hub.lat] as [number, number],
  to: [dest.lng, dest.lat] as [number, number],
}));

export function ArcExample() {
  return (
    <div className="h-[420px] w-full">
      <Map center={[hub.lng, hub.lat]} zoom={1} projection={{ type: "globe" }}>
        <MapArc
          data={arcs}
          paint={{ "line-color": "#3b82f6", "line-dasharray": [2, 2] }}
          interactive={false}
        />
      </Map>
    </div>
  );
}
```

## 交互式弧线

将 `hoverPaint` 与 `onHover` 结合，可以高亮某条弧线并在 `MapPopup` 中展示详情。
使用 `line-color` 上的 `match` 表达式，可以按类别为弧线着色——下面的例子中，
航线与海运通道采用不同的样式。

```tsx
"use client";

import { useState } from "react";
import type { ExpressionSpecification } from "maplibre-gl";
import {
  Map,
  MapArc,
  MapMarker,
  MapPopup,
  MarkerContent,
  MarkerLabel,
  type MapArcDatum,
} from "@/registry/map";

interface Lane extends MapArcDatum {
  origin: string;
  destination: string;
  volume: string;
  mode: "air" | "sea";
}

const lanes: Lane[] = [
  { id: "dxb-jfk", origin: "迪拜", destination: "纽约", from: [55.2708, 25.2048], to: [-74.006, 40.7128], volume: "980 吨", mode: "air" },
  { id: "sin-rtm", origin: "新加坡", destination: "鹿特丹", from: [103.8198, 1.3521], to: [4.4777, 51.9244], volume: "9.4k TEU", mode: "sea" },
];

const modeColorExpression: ExpressionSpecification = [
  "match", ["get", "mode"], "air", "#a78bfa", "sea", "#34d399", "#888",
];

export function InteractiveArcExample() {
  const [selected, setSelected] = useState<Lane | null>(null);
  return (
    <div className="h-[420px] w-full">
      <Map center={[20, 20]} zoom={0.8}>
        <MapArc<Lane>
          data={lanes}
          paint={{ "line-color": modeColorExpression, "line-width": 1.5 }}
          hoverPaint={{ "line-width": 3, "line-opacity": 1 }}
          onHover={(e) => setSelected(e ? e.arc : null)}
        />
        {selected && (
          <MapPopup longitude={selected.from[0]} latitude={selected.from[1]}>
            {selected.origin} → {selected.destination}（{selected.volume}）
          </MapPopup>
        )}
      </Map>
    </div>
  );
}
```

