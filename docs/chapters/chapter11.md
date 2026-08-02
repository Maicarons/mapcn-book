# 第 11 章 深入 MapLibre 实例

声明式组件覆盖了 90% 的场景，但总有 10% 需要直接操作地图引擎——自定义动画、
监听原生事件、增删任意图层。mapcn 为此留了两个出口：`ref` 与 `useMap` 钩子。本章把它们讲透。

## 11.1 用 ref 拿到底层 map

`Map` 的 `ref` 指向原生的 `MapRef` 实例（`MapRef` 类型即别名）。在事件
处理函数或副作用里调用它即可：

```tsx
import { Map, type MapRef } from "@/components/ui/map";
import { useRef } from "react";

function FlyToButton() {
  const mapRef = useRef<MapRef>(null);

  return (
    <>
      <button onClick={() => mapRef.current?.flyTo({ center: [-74, 40.7], zoom: 12 })}>
        飞往纽约
      </button>
      <Map ref={mapRef} center={[-74, 40.7]} zoom={10} />
    </>
  );
}
```

`flyTo()`、`setCenter()`、`getSource()`、`addLayer()`、`removeLayer()`……凡是
MapLibre Map 上的方法，这里都能直接用。

## 11.2 用 useMap 钩子

当你的自定义组件**渲染在 `Map` 内部**时，用 `useMap` 更自然——它返回
`{ map, isLoaded }`，无需手动传 ref：

```tsx
"use client";

import { Map, useMap } from "@/components/ui/map";
import { useEffect } from "react";

function MapEventListener() {
  const { map, isLoaded } = useMap();

  useEffect(() => {
    if (!map || !isLoaded) return;
    const handleClick = (e: any) => console.log("点击位置：", e.lngLat);
    map.on("click", handleClick);
    return () => map.off("click", handleClick);
  }, [map, isLoaded]);

  return null;
}

export function Demo() {
  return (
    <Map center={[-74, 40.7]} zoom={10}>
      <MapEventListener />
    </Map>
  );
}
```

> **关键：** `useMap` 必须在 `Map` 内调用，否则会抛错。`isLoaded` 表示地图
> 样式已加载就绪——在它变 `true` 之前，不要急着 `map.on()`。

## 11.3 示例：自定义控件

用 `useMap` 做一个「3D 视角 / 复位」控制器，实时显示 `pitch` 与 `bearing`：

```tsx
"use client";

import { useEffect, useState } from "react";
import { Map, useMap } from "@/components/ui/map";
import { Button } from "@/components/ui/button";

function Controller() {
  const { map, isLoaded } = useMap();
  const [pitch, setPitch] = useState(0);
  const [bearing, setBearing] = useState(0);

  useEffect(() => {
    if (!map || !isLoaded) return;
    const onMove = () => {
      setPitch(Math.round(map.getPitch()));
      setBearing(Math.round(map.getBearing()));
    };
    map.on("move", onMove);
    return () => map.off("move", onMove);
  }, [map, isLoaded]);

  if (!isLoaded) return null;

  return (
    <div className="absolute top-3 left-3 flex flex-col gap-2">
      <Button size="sm" variant="secondary"
              onClick={() => map?.easeTo({ pitch: 60, bearing: -20, duration: 1000 })}>
        3D 视角
      </Button>
      <Button size="sm" variant="secondary"
              onClick={() => map?.easeTo({ pitch: 0, bearing: 0, duration: 1000 })}>
        复位
      </Button>
      <div className="font-mono text-xs">pitch: {pitch}° / bearing: {bearing}°</div>
    </div>
  );
}
```

## 11.4 示例：自定义 GeoJSON 图层

当内置的 `MapGeoJSON` 不够用时，直接在 `map` 里增删 MapLibre 原生图层。下面
给纽约的两座公园加填充 + 描边：

```tsx
"use client";

import { useEffect } from "react";
import { Map, useMap } from "@/components/ui/map";

const parks = {
  type: "FeatureCollection" as const,
  features: [
    { type: "Feature" as const, properties: { name: "中央公园" },
      geometry: { type: "Polygon" as const, coordinates: [[
        [-73.9731, 40.7644], [-73.9819, 40.7681], [-73.958, 40.8006],
        [-73.9493, 40.7969], [-73.9731, 40.7644],
      ]] } },
  ],
};

function ParkLayer() {
  const { map, isLoaded } = useMap();

  useEffect(() => {
    if (!map || !isLoaded) return;
    if (!map.getSource("parks")) {
      map.addSource("parks", { type: "geojson", data: parks });
    }
    if (!map.getLayer("parks-fill")) {
      map.addLayer({
        id: "parks-fill",
        type: "fill",
        source: "parks",
        paint: { "fill-color": "#22c55e", "fill-opacity": 0.4 },
      });
    }
    if (!map.getLayer("parks-line")) {
      map.addLayer({
        id: "parks-line",
        type: "line",
        source: "parks",
        paint: { "line-color": "#16a34a", "line-width": 2 },
      });
    }
  }, [map, isLoaded]);

  return null;
}
```

要点：**先判断 `getSource` / `getLayer` 是否存在再添加**，避免重复添加报错；所有
增删都应在 `isLoaded` 为真后进行。

## 11.5 事件清理的重要性

自定义图层与事件监听**不会**被 mapcn 自动清理。组件卸载时务必移除，否则会造成
内存泄漏或「幽灵图层」：

```tsx
useEffect(() => {
  if (!map || !isLoaded) return;
  const handler = () => {/* ... */};
  map.on("click", handler);
  return () => map.off("click", handler); // 必须清理
}, [map, isLoaded]);
```

## 本章小结

- 两个底层出口：`ref`（指向原生 `MapRef`）与 `useMap`（内部组件用）；
- `useMap` 返回 `{ map, isLoaded }`，且必须在 `Map` 内调用；
- 自定义控件/图层都在 `isLoaded` 为真后操作 `map` 实例；
- 增删图层前先判断是否存在；事件监听务必在卸载时清理。

下一章，我们谈主题、样式与自定义底图。
