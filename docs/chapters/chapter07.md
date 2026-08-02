# 第 07 章 路线与路径规划

在地图上把一系列坐标连成线，就能表达「路线、轨迹、管线、迁徙路径」等概念。mapcn
的 `MapRoute` 用一行声明画出一条线；结合外部路由服务，还能做真实的驾车导航。

## 7.1 基础路线

`MapRoute` 接收 `coordinates`（一串 `[经度, 纬度]`）即可画线：

```tsx
import { Map, MapRoute } from "@/components/ui/map";

const route: [number, number][] = [
  [-74.006, 40.7128],   // 市政厅
  [-73.9857, 40.7484],  // 帝国大厦
  [-73.9772, 40.7527],  // 中央车站
  [-73.9654, 40.7829],  // 中央公园
];

export function RouteExample() {
  return (
    <div className="h-[420px] w-full">
      <Map center={[-73.98, 40.75]} zoom={11.2}>
        <MapRoute coordinates={route} color="#3b82f6" width={4} opacity={0.8} />
      </Map>
    </div>
  );
}
```

可调样式包括：

| 属性 | 说明 | 默认值 |
| --- | --- | --- |
| `color` | 线条颜色（CSS 颜色） | `#3b82f6` |
| `width` | 线宽（像素） | `4` |
| `opacity` | 不透明度 0–1 | `0.8` |
| `dashArray` | 虚线 `[实, 虚]` | — |
| `interactive` | 是否响应点击/悬停 | `true` |

例如虚线：`<MapRoute dashArray={[2, 2]} />`。

## 7.2 路线 + 站点标记

把 `MapRoute` 与 `MapMarker` 组合，是「带有序号站点的路线」的标准写法：

```tsx
import {
  Map,
  MapMarker,
  MarkerContent,
  MarkerTooltip,
  MapRoute,
} from "@/components/ui/map";

const stops = [
  { name: "市政厅", lng: -74.006, lat: 40.7128 },
  { name: "帝国大厦", lng: -73.9857, lat: 40.7484 },
  { name: "中央公园", lng: -73.9654, lat: 40.7829 },
];

export function RouteWithStops() {
  return (
    <div className="h-[420px] w-full">
      <Map center={[-73.98, 40.75]} zoom={11.2}>
        <MapRoute coordinates={stops.map((s) => [s.lng, s.lat]) as [number, number][]} />
        {stops.map((stop, i) => (
          <MapMarker key={stop.name} longitude={stop.lng} latitude={stop.lat}>
            <MarkerContent>
              <div className="flex size-4.5 items-center justify-center rounded-full border-2 border-white bg-blue-500 text-xs font-semibold text-white">
                {i + 1}
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

## 7.3 接入真实导航：OSRM

`MapRoute` 只负责「画线」，不负责「算路」。要得到真实的驾车路线，需要调用路由
服务，例如免费的 [OSRM](https://project-osrm.org/)。下面这个例子获取阿姆斯特丹
到鹿特丹的备选路线，并允许点击切换：

```tsx
"use client";

import { useEffect, useState } from "react";
import { Map, MapMarker, MarkerContent, MapRoute, MarkerLabel } from "@/components/ui/map";

const start = { name: "阿姆斯特丹", lng: 4.9041, lat: 52.3676 };
const end = { name: "鹿特丹", lng: 4.4777, lat: 51.9244 };

export function OsrmRoute() {
  const [routes, setRoutes] = useState<[number, number][][]>([]);
  const [selected, setSelected] = useState(0);

  useEffect(() => {
    const url =
      `https://router.project-osrm.org/route/v1/driving/` +
      `${start.lng},${start.lat};${end.lng},${end.lat}` +
      `?overview=full&geometries=geojson&alternatives=true`;
    fetch(url)
      .then((r) => r.json())
      .then((data) => {
        if (data.routes?.length) {
          setRoutes(data.routes.map((r: any) => r.geometry.coordinates));
        }
      })
      .catch((e) => console.error("路线获取失败", e));
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
          <MarkerContent><div className="size-5 rounded-full bg-green-500 border-2 border-white" /></MarkerContent>
          <MarkerLabel position="top">{start.name}</MarkerLabel>
        </MapMarker>
        <MapMarker longitude={end.lng} latitude={end.lat}>
          <MarkerContent><div className="size-5 rounded-full bg-red-500 border-2 border-white" /></MarkerContent>
          <MarkerLabel position="bottom">{end.name}</MarkerLabel>
        </MapMarker>
      </Map>
    </div>
  );
}
```

要点：

- OSRM 返回的 `geometry.coordinates` 正是 `[number, number][]` 格式，直接喂给
`MapRoute` 的 `coordinates`；
- 用 `selected` 状态高亮当前路线，`onClick` 切换；
- 这是「前端取数 + mapcn 画线」的典型分层：路由算法交给专业服务，渲染交给组件。

## 本章小结

- `MapRoute` 用 `coordinates` 一串坐标即可画线，可设颜色/线宽/虚线；
- 与 `MapMarker` 组合可表达「带站点的路线」；
- `MapRoute` 只画线、不算路；真实导航需调用 OSRM 等路由服务；
- 典型分层：路由算法交给后端/服务，渲染交给 mapcn。

下一章，我们用弧线表达起点—终点连接。
