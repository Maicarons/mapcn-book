# 聚合点 Clusters（官方文档研读）

> **研读说明**：本页为 mapcn 官方文档「聚合点 Clusters」的中文研读笔记，内容以官方文档为基线整理，作为正文之外的查阅与补充。
> 相关正文：第 10 章（海量点聚合）。如与官方文档存在出入，请以官方文档为准。

用自动点聚合可视化大规模数据集。

`MapClusterLayer` 组件利用 MapLibre 内置的聚合能力，高效渲染海量点数据。在低
缩放级别下，相邻的点会自动聚合成簇；随着放大，簇会展开为单点。

## 基础示例

点击聚合簇可放大；点击单个点可在弹窗中查看详情。

```tsx
"use client";

import { useState } from "react";
import { Map, MapClusterLayer, MapPopup, MapControls } from "@/registry/map";

interface EarthquakeProperties {
  mag: number;
  place: string;
  tsunami: number;
}

export default function ClusterExample() {
  const [selectedPoint, setSelectedPoint] = useState<{
    coordinates: [number, number];
    properties: EarthquakeProperties;
  } | null>(null);

  return (
    <div className="h-[420px] w-full">
      <Map center={[-103.59, 40.66]} zoom={3.4} fadeDuration={0}>
        <MapClusterLayer<EarthquakeProperties>
          data="https://maplibre.org/maplibre-gl-js/docs/assets/earthquakes.geojson"
          clusterRadius={50}
          clusterMaxZoom={14}
          onPointClick={(feature, coordinates) => {
            setSelectedPoint({ coordinates, properties: feature.properties });
          }}
        />
        {selectedPoint && (
          <MapPopup
            longitude={selectedPoint.coordinates[0]}
            latitude={selectedPoint.coordinates[1]}
            onClose={() => setSelectedPoint(null)}
            closeOnClick={false}
            closeButton
          >
            <p>震级：{selectedPoint.properties.mag}</p>
            <p>海啸：{selectedPoint.properties.tsunami === 1 ? "是" : "否"}</p>
          </MapPopup>
        )}
        <MapControls />
      </Map>
    </div>
  );
}
```

