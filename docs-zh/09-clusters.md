# 聚合点 Clusters

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
