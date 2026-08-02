# 第 10 章 海量点聚合 Clusters

当数据点从「几十个」增长到「成千上万个」——地震震中、充电桩、门店分布——逐一
渲染标记既卡又乱。地图的经典解法是**聚合（clustering）**：低缩放时把邻近点收拢
成「数字气泡」，放大后再展开为单点。mapcn 的 `MapClusterLayer` 直接封装了
MapLibre 原生的聚合能力。

## 10.1 一行启用聚合

```tsx
"use client";

import { useState } from "react";
import { Map, MapClusterLayer, MapPopup, MapControls } from "@/components/ui/map";

interface QuakeProps {
  mag: number;
  place: string;
  tsunami: number;
}

export default function ClusterExample() {
  const [point, setPoint] = useState<{
    coordinates: [number, number];
    properties: QuakeProps;
  } | null>(null);

  return (
    <div className="h-[420px] w-full">
      <Map center={[-103.59, 40.66]} zoom={3.4}>
        <MapClusterLayer<QuakeProps>
          data="https://maplibre.org/maplibre-gl-js/docs/assets/earthquakes.geojson"
          clusterRadius={50}
          clusterMaxZoom={14}
          onPointClick={(feature, coordinates) => setPoint({ coordinates, properties: feature.properties })}
        />
        {point && (
          <MapPopup
            longitude={point.coordinates[0]}
            latitude={point.coordinates[1]}
            onClose={() => setPoint(null)}
            closeOnClick={false}
            closeButton
          >
            <p>震级：{point.properties.mag}</p>
            <p>海啸：{point.properties.tsunami === 1 ? "是" : "否"}</p>
          </MapPopup>
        )}
        <MapControls />
      </Map>
    </div>
  );
}
```

点击聚合气泡会自动放大展开；点击未聚合的单点则触发 `onPointClick`，我们在回调里
弹出一个 `MapPopup` 显示详情。

## 10.2 关键属性

| 属性 | 说明 | 默认值 |
| --- | --- | --- |
| `data` | GeoJSON 点集合，或用于拉取的 URL | — |
| `clusterMaxZoom` | 进行聚合的最大缩放级别 | `14` |
| `clusterRadius` | 聚合半径（像素） | `50` |
| `clusterColors` | 簇圆配色（浅→深，按点数分级） | 自动 |
| `color` | 未聚合单点颜色 | 自动 |
| `onPointClick` | 单点被点击的回调 | — |
| `onClusterClick` | 簇被点击的回调（不提供则放大） | — |

簇圆的大小与颜色会随包含点数，按 `clusterColors` 分级变化——点数越多，圆越
大、颜色越深。

## 10.3 泛型与类型安全

`MapClusterLayer<T>` 让 `data` 拥有类型，回调里能直接
访问 `properties` 而不必任何类型断言。这是 mapcn 对 GeoJSON 图层一贯的类型化
思路（与第 9 章 `MapGeoJSON` 一致）。

## 10.4 与海量标记方案的对比

| 方案 | 适用规模 | 特点 |
| --- | --- | --- |
| `MapMarker`（DOM） | 数百 | 富样式、易交互，但 DOM 开销大 |
| `MapGeoJSON` 点图层 | 数千~数万 | WebGL 渲染，性能好，样式较统一 |
| `MapClusterLayer` | 数千~数十万 | 自动聚合，最佳可读性 |

经验法则：点数过千就应考虑聚合；需要「每个点有独立 DOM 样式」时才用 `MapMarker`。

## 本章小结

- `MapClusterLayer` 封装 MapLibre 原生聚合，低缩放收拢、放大展开；
- 通过 `clusterRadius` / `clusterMaxZoom` / `clusterColors` / 
`color` 调聚合外观；
- `onPointClick` / `onClusterClick` 分别处理单点与簇的交互；
- 泛型 `MapClusterLayer<T>` 提供属性类型安全；
- 点数过千优先聚合，富样式单点才用 DOM 标记。

下一章，我们深入底层 MapLibre 实例。
