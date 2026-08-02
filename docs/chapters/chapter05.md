# 第 05 章 标记点 Markers

标记（Marker）是地图最常见的元素：它把现实世界中的一个点，钉在地图的某个经纬度
上。mapcn 用一组可组合的组件描述一个标记——内容、提示、弹窗、标签各司其职，你
按需嵌套即可。

## 5.1 组件结构

一个完整标记由外到内是这样组合的：

```tsx
<MapMarker longitude={...} latitude={...}>
  <MarkerContent>      {/* 标记的可视内容（默认是蓝点） */}
    <MarkerLabel />    {/* 可选：文本标签 */}
  </MarkerContent>
  <MarkerTooltip>      {/* 可选：悬停提示框 */}
    提示文字
  </MarkerTooltip>
  <MarkerPopup>        {/* 可选：点击弹窗 */}
    弹窗内容
  </MarkerPopup>
</MapMarker>
```

- `MapMarker`：标记容器，负责定位与事件；
- `MarkerContent`：渲染标记本体，不传子组件时显示默认蓝点；
- `MarkerLabel`：在标记上方/下方显示文字；
- `MarkerTooltip`：悬停时出现的轻量提示；
- `MarkerPopup`：点击标记时弹出的卡片。

## 5.2 基础标记

一个带提示框与弹窗的标记列表：

```tsx
import {
  Map,
  MapMarker,
  MarkerContent,
  MarkerPopup,
  MarkerTooltip,
} from "@/components/ui/map";

const locations = [
  { id: 1, name: "帝国大厦", lng: -73.9857, lat: 40.7484 },
  { id: 2, name: "中央公园", lng: -73.9654, lat: 40.7829 },
  { id: 3, name: "时代广场", lng: -73.9855, lat: 40.758 },
];

export function MarkersExample() {
  return (
    <div className="h-[420px] w-full">
      <Map center={[-73.98, 40.76]} zoom={12}>
        {locations.map((loc) => (
          <MapMarker key={loc.id} longitude={loc.lng} latitude={loc.lat}>
            <MarkerContent>
              <div className="bg-primary size-4 rounded-full border-2 border-white shadow-lg" />
            </MarkerContent>
            <MarkerTooltip>{loc.name}</MarkerTooltip>
            <MarkerPopup>
              <div className="space-y-1">
                <p className="font-medium">{loc.name}</p>
                <p className="text-muted-foreground text-xs">
                  {loc.lat.toFixed(4)}, {loc.lng.toFixed(4)}
                </p>
              </div>
            </MarkerPopup>
          </MapMarker>
        ))}
      </Map>
    </div>
  );
}
```

`bg-primary` 之类的类来自 shadcn 设计令牌，因此标记颜色会随你的主题自动协调。

## 5.3 文本标签

`MarkerLabel` 在标记旁显示文字，默认在上方，可用 `position` 改为 `bottom`：

```tsx
<MarkerContent>
  <div className="size-5 rounded-full bg-rose-500 border-2 border-white" />
  <MarkerLabel position="bottom">我的位置</MarkerLabel>
</MarkerContent>
```

## 5.4 自定义标记内容

`MarkerContent` 的子组件可以是任何 React 节点。配合 `MapPin` 图标，可以
做出「图钉」「店铺」等富样式标记：

```tsx
import { MapPin } from "lucide-react";

<MarkerContent>
  <MapPin className="fill-black stroke-white dark:fill-white" size={28} />
</MarkerContent>
```

## 5.5 可拖拽标记

给 `MapMarker` 加 `draggable`，并通过 `onDrag` 把最新坐标写回状态：

```tsx
"use client";

import { useState } from "react";
import { Map, MapMarker, MarkerContent, MarkerPopup } from "@/components/ui/map";

export function DraggableMarker() {
  const [pos, setPos] = useState({ lng: -73.98, lat: 40.75 });

  return (
    <div className="h-[420px] w-full">
      <Map center={[-73.98, 40.75]} zoom={12}>
        <MapMarker
          draggable
          longitude={pos.lng}
          latitude={pos.lat}
          onDrag={(lngLat) => setPos({ lng: lngLat.lng, lat: lngLat.lat })}
        >
          <MarkerContent>
            <div className="cursor-move">📍</div>
          </MarkerContent>
          <MarkerPopup>
            <p className="text-xs tabular-nums">
              {pos.lat.toFixed(4)}, {pos.lng.toFixed(4)}
            </p>
          </MarkerPopup>
        </MapMarker>
      </Map>
    </div>
  );
}
```

`MapMarker` 还提供 `onClick`、`onMouseEnter`、`onMouseLeave`、`onDrag`、
`onDragEnd` 等事件回调，覆盖大多数交互需求。

## 5.6 性能边界

`MapMarker` 是**基于 DOM** 的：每个标记都是一个真实 DOM 节点。在几百个标记以内
它表现良好；但当数据量达到几千、上万时，DOM 标记会让浏览器卡顿。此时应改用
第 10 章介绍的图层方式（GeoJSON 点图层）来渲染海量点。

## 本章小结

- 标记由 `MapMarker` 容器 + `MarkerContent`（本体）+ 可选的 `MarkerLabel` /
  `MarkerTooltip` / `MarkerPopup` 组合而成；
- `MarkerContent` 不传子组件时显示默认蓝点，传任意节点即可自定义外观；
- 加 `draggable` 与 `onDrag` 可实现可拖拽标记；
- `MapMarker` 支持点击、悬停、拖拽等多类事件回调；
- DOM 标记适合数百量级，更大规模请转向 GeoJSON 图层方案。

下一章，我们深入弹窗与提示框的细节。
