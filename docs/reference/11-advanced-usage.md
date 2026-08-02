# 进阶用法（官方文档研读）

> **研读说明**：本页为 mapcn 官方文档「进阶用法」的中文研读笔记，内容以官方文档为基线整理，作为正文之外的查阅与补充。
> 相关正文：第 11–13 章（进阶与实战）。如与官方文档存在出入，请以官方文档为准。

访问底层的 MapLibre GL 实例，进行更高级的定制。

通过 MapLibre GL JS API 暴露的能力，可以操作地图实例的任意特性。你可以使用
`ref`，也可以使用 `useMap` 钩子。

> **提示：** 完整的可用方法与时事件清单，请查阅
> [MapLibre GL JS 文档](https://maplibre.org/maplibre-gl-js/docs/API/classes/Map/)。

## 使用 ref

访问地图实例最简单的方式。用 `ref` 即可在事件处理函数或副作用中调用地图方法。

```tsx
import { Map, type MapRef } from "@/components/ui/map";
import { useRef } from "react";

function MyMapComponent() {
  const mapRef = useRef<MapRef>(null);

  const handleFlyTo = () => {
    mapRef.current?.flyTo({ center: [-74, 40.7], zoom: 12 });
  };

  return (
    <>
      <button onClick={handleFlyTo}>飞往纽约</button>
      <Map ref={mapRef} center={[-74, 40.7]} zoom={10} />
    </>
  );
}
```

## 使用钩子

对于渲染在 `Map` 内部的子组件，使用 `useMap` 钩子访问地图实例并监听事件。

```tsx
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

// 使用
<Map center={[-74, 40.7]} zoom={10}>
  <MapEventListener />
</Map>
```

## 示例：自定义控件

该示例展示如何创建自定义控件来操纵地图的倾角（pitch）与方位角（bearing），并
监听地图事件以实时显示数值（详见仓库中的 `advanced-usage-example.tsx`）。

## 示例：自定义地理 JSON 图层

以「填充 + 描边」的图层形式添加自定义 GeoJSON 数据。该示例展示带悬停交互的
纽约公园（详见 `custom-layer-example.tsx`）。

## 示例：用图层渲染标记

当需要显示成百上千个标记时，应改用 GeoJSON 图层而非基于 DOM 的 `MapMarker`
组件。这种方式在 WebGL 画布上渲染标记，性能显著更优（详见 `layer-markers-example.tsx`）。

## 可扩展方向

你可以基于 mapcn 构建如下自定义能力：

- **实时追踪** — 配送、出行或车队管理的实时位置更新
- **地理围栏** — 当用户进入或离开特定区域时触发动作
- **热力图** — 可视化人口密度、犯罪率或活动热度等数据
- **绘制工具** — 让用户绘制多边形、线段，或放置自定义区域的标记
- **3D 建筑** — 拉伸建筑底面用于城市可视化
- **动画** — 让标记沿路线运动，或制作飞行穿越体验
- **自定义数据图层** — 叠加天气、交通或卫星影像

