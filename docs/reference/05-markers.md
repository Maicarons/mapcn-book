# 标记点 Markers（官方文档研读）

> **研读说明**：本页为 mapcn 官方文档「标记点 Markers」的中文研读笔记，内容以官方文档为基线整理，作为正文之外的查阅与补充。
> 相关正文：第 5 章（标记点）。如与官方文档存在出入，请以官方文档为准。

在地图上添加可交互的标记，并配合弹窗与提示框使用。

使用 `MapMarker` 在地图上放置标记。每个标记都可以拥有自定义内容、点击时弹出的
弹窗，以及悬停时出现的提示框。

> **性能提示：** `MapMarker` 基于 DOM，最适合几百个标记以内的场景。若数据集更大，
> 请改用[地理JSON 图层示例](./11-advanced-usage.md)。渲染大量 DOM 标记会让浏览器
> 变得卡顿。

## 基础示例

简单的标记，配合显示位置信息的提示框与弹窗。

```tsx
import {
  Map,
  MapMarker,
  MarkerContent,
  MarkerPopup,
  MarkerTooltip,
} from "@/registry/map";

const locations = [
  { id: 1, name: "Empire State Building", lng: -73.9857, lat: 40.7484 },
  { id: 2, name: "Central Park", lng: -73.9654, lat: 40.7829 },
  { id: 3, name: "Times Square", lng: -73.9855, lat: 40.758 },
];

export function MarkersExample() {
  return (
    <div className="h-[420px] w-full">
      <Map center={[-73.98, 40.76]} zoom={12}>
        {locations.map((location) => (
          <MapMarker
            key={location.id}
            longitude={location.lng}
            latitude={location.lat}
          >
            <MarkerContent>
              <div className="bg-primary size-4 rounded-full border-2 border-white shadow-lg" />
            </MarkerContent>
            <MarkerTooltip>{location.name}</MarkerTooltip>
            <MarkerPopup>
              <div className="space-y-1">
                <p className="text-foreground font-medium">{location.name}</p>
                <p className="text-muted-foreground text-xs">
                  {location.lat.toFixed(4)}, {location.lng.toFixed(4)}
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

## 富交互弹窗

借助 shadcn/ui 组件，可以构建包含图片、评分与操作按钮的复杂弹窗（完整富弹窗标记
见仓库中的 `popup-example`）。

## 可拖拽标记

创建可拖拽的标记，用户可以在地图上自由拖动。点击标记即可在弹窗中看到当前坐标。

```tsx
"use client";

import { useState } from "react";
import { Map, MapMarker, MarkerContent, MarkerPopup } from "@/registry/map";

export function DraggableMarkerExample() {
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
            <p className="text-muted-foreground text-xs tabular-nums">
              {pos.lat.toFixed(4)}, {pos.lng.toFixed(4)}
            </p>
          </MarkerPopup>
        </MapMarker>
      </Map>
    </div>
  );
}
```

