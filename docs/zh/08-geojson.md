# 地理 JSON

将任意 GeoJSON 渲染为填充 + 描边图层，用于分级着色图（choropleth）与区域地图。

使用 `MapGeoJSON` 可以将 GeoJSON 数据源中的点、线、面，以带主题色的填充 + 描边
图层绘制出来。

## 基础地理 JSON

将 `data` 指向一个 GeoJSON URL，该图层会开箱即用地渲染出「主题感知的单色填充 +
发丝级描边」，无需任何样式配置。下面这个例子在 `blank` 地图上叠加了世界地图。

```tsx
import { Map, MapGeoJSON } from "@/registry/map";
import { WORLD_GEOJSON } from "@/lib/use-world-data";

export function GeoJSONExample() {
  return (
    <div className="bg-card h-[420px] w-full">
      <Map blank center={[10, 25]}>
        <MapGeoJSON data={WORLD_GEOJSON} linePaint={false} />
      </Map>
    </div>
  );
}
```

## 在地图上叠加

在地图上叠加形状与区域——高亮某个范围、勾勒某条边界，或描出某个多边形。

```tsx
import { Map, MapGeoJSON } from "@/registry/map";

const area: GeoJSON.FeatureCollection = {
  type: "FeatureCollection",
  features: [
    {
      type: "Feature",
      properties: {},
      geometry: {
        type: "Polygon",
        coordinates: [[
          [-122.42, 37.78], [-122.398, 37.785], [-122.392, 37.768],
          [-122.412, 37.758], [-122.43, 37.77], [-122.42, 37.78],
        ]],
      },
    },
  ],
};

export function MapOverlayExample() {
  return (
    <div className="h-[420px] w-full">
      <Map center={[-122.41, 37.772]} zoom={12}>
        <MapGeoJSON
          data={area}
          fillPaint={{ "fill-color": "#3b82f6", "fill-opacity": 0.25 }}
          linePaint={{ "line-color": "#2563eb", "line-width": 2 }}
        />
      </Map>
    </div>
  );
}
```
