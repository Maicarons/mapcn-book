# 地图 Map（官方文档研读）

> **研读说明**：本页为 mapcn 官方文档「地图 Map」的中文研读笔记，内容以官方文档为基线整理，作为正文之外的查阅与补充。
> 相关正文：第 3 章（你的第一张地图）。如与官方文档存在出入，请以官方文档为准。

为应用添加交互式地图的最简单方式。

## 基础用法

`Map` 组件负责初始化 MapLibre GL、处理主题，并为子组件提供上下文环境。

```tsx
import { Map } from "@/registry/map";

export function BasicMapExample() {
  return (
    <div className="h-[420px] w-full">
      <Map center={[-74.006, 40.7128]} zoom={12} />
    </div>
  );
}
```

## 受控模式

通过 `viewport` 与 `onViewportChange` 两个属性，可以在外部控制地图的视口。当你
需要把地图状态与自己的应用同步、或响应视口变化时，这一模式非常有用。

```tsx
"use client";

import { useState } from "react";
import { Map, type MapViewport } from "@/registry/map";

export function ControlledMapExample() {
  const [viewport, setViewport] = useState<MapViewport>({
    center: [-74.006, 40.7128],
    zoom: 8,
    bearing: 0,
    pitch: 0,
  });

  return (
    <div className="h-[420px] w-full">
      <Map viewport={viewport} onViewportChange={setViewport} />
    </div>
  );
}
```

## 空白底图

`blank` 属性用一块透明的、无瓦片的画布替换默认街道底图——非常适合数据可视化，
此时你绘制自己的图层，而不再显示街道与注记。

> **注意：** `blank` 是一块空白画布。单独使用时，`<Map blank />` 不会渲染任何
> 内容——你必须在上面叠加自己的图层（例如 `MapGeoJSON`、`MapArc` 或标记点）。
> 关于在空白地图上绘制图形，详见[地理JSON 章节](./09-geojson.md)。

下面的例子中，`MapGeoJSON` 图层在透明画布之上渲染了世界各国边界。

```tsx
import { Map, MapGeoJSON } from "@/registry/map";
import { WORLD_GEOJSON } from "@/lib/use-world-data";

export function BlankMapExample() {
  return (
    <div className="h-[420px] w-full">
      <Map blank center={[10, 25]}>
        <MapGeoJSON data={WORLD_GEOJSON} />
      </Map>
    </div>
  );
}
```

## 自定义样式

使用 `styles` 属性可以传入自定义的地图样式。下面这个例子使用
[OpenFreeMap](https://openfreemap.org)（一个开源项目，数据来自 OpenStreetMap）
提供的免费矢量瓦片。

```tsx
"use client";

import { useState, useEffect, useRef } from "react";
import { Map, type MapRef } from "@/registry/map";

const styles = {
  default: undefined,
  openstreetmap: "https://tiles.openfreemap.org/styles/bright",
  openstreetmap3d: "https://tiles.openfreemap.org/styles/liberty",
};

export function CustomStyleExample() {
  const mapRef = useRef<MapRef>(null);
  const [style, setStyle] = useState("default");

  useEffect(() => {
    mapRef.current?.easeTo({
      pitch: style === "openstreetmap3d" ? 60 : 0,
      duration: 500,
    });
  }, [style]);

  return (
    <div className="h-[420px] w-full">
      <Map
        ref={mapRef}
        center={[-0.1276, 51.5074]}
        zoom={15}
        styles={
          style === "default"
            ? undefined
            : { light: styles[style], dark: styles[style] }
        }
      />
    </div>
  );
}
```

