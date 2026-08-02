# 路线 Routes（官方文档研读）

> **研读说明**：本页为 mapcn 官方文档「路线 Routes」的中文研读笔记，内容以官方文档为基线整理，作为正文之外的查阅与补充。
> 相关正文：第 7 章（路线与路径规划）。如与官方文档存在出入，请以官方文档为准。

在地图上绘制连接坐标的线段与路径。

使用 `MapRoute` 可以绘制连接一系列坐标的线段。非常适合展示路线、轨迹，或任意
两点之间的路径。

## 基础路线

绘制一条沿途带有序号站点标记的路线。

```tsx
import {
  Map,
  MapMarker,
  MarkerContent,
  MarkerTooltip,
  MapRoute,
} from "@/registry/map";

const route = [
  [-74.006, 40.7128],
  [-73.9857, 40.7484],
  [-73.9772, 40.7527],
  [-73.9654, 40.7829],
] as [number, number][];

const stops = [
  { name: "市政厅", lng: -74.006, lat: 40.7128 },
  { name: "帝国大厦", lng: -73.9857, lat: 40.7484 },
  { name: "中央车站", lng: -73.9772, lat: 40.7527 },
  { name: "中央公园", lng: -73.9654, lat: 40.7829 },
];

export function RouteExample() {
  return (
    <div className="h-[420px] w-full">
      <Map center={[-73.98, 40.75]} zoom={11.2}>
        <MapRoute coordinates={route} color="#3b82f6" width={4} opacity={0.8} />
        {stops.map((stop, index) => (
          <MapMarker key={stop.name} longitude={stop.lng} latitude={stop.lat}>
            <MarkerContent>
              <div className="flex size-4.5 items-center justify-center rounded-full border-2 border-white bg-blue-500 text-xs font-semibold text-white shadow-lg">
                {index + 1}
              </div>
            </MarkerContent>
            <MarkerTooltip>{stop.name}</MarkerTooltip>
          </MapMarker>
        ))}
      </Map>
    </div>
  );
}
```

## 路线规划

展示多条备选路线，并让用户在其中切换。下面的例子从
[OSRM API](https://project-osrm.org/) 获取真实的驾车导航结果。点击路线或使用
按钮即可切换。

```tsx
"use client";

import { useEffect, useState } from "react";
import { Map, MapMarker, MarkerContent, MapRoute, MarkerLabel } from "@/registry/map";

const start = { name: "阿姆斯特丹", lng: 4.9041, lat: 52.3676 };
const end = { name: "鹿特丹", lng: 4.4777, lat: 51.9244 };

export function OsrmRouteExample() {
  const [routes, setRoutes] = useState<[number, number][][]>([]);
  const [selected, setSelected] = useState(0);

  useEffect(() => {
    fetch(
      `https://router.project-osrm.org/route/v1/driving/${start.lng},${start.lat};${end.lng},${end.lat}?overview=full&geometries=geojson&alternatives=true`
    )
      .then((r) => r.json())
      .then((data) => {
        if (data.routes?.length > 0) {
          setRoutes(data.routes.map((r: any) => r.geometry.coordinates));
        }
      });
  }, []);

  return (
    <div className="h-[500px] w-full">
      <Map center={[4.69, 52.14]} zoom={8.5}>
        {routes.map((coords, i) => (
          <MapRoute
            key={i}
            coordinates={coords}
            color={i === selected ? "#6366f1" : "#94a3b8"}
            width={i === selected ? 6 : 5}
            onClick={() => setSelected(i)}
          />
        ))}
        <MapMarker longitude={start.lng} latitude={start.lat}>
          <MarkerContent>
            <div className="size-5 rounded-full bg-green-500 border-2 border-white shadow-lg" />
            <MarkerLabel position="top">{start.name}</MarkerLabel>
          </MarkerContent>
        </MapMarker>
        <MapMarker longitude={end.lng} latitude={end.lat}>
          <MarkerContent>
            <div className="size-5 rounded-full bg-red-500 border-2 border-white shadow-lg" />
            <MarkerLabel position="bottom">{end.name}</MarkerLabel>
          </MarkerContent>
        </MapMarker>
      </Map>
    </div>
  );
}
```

