# 第 09 章 GeoJSON 与区域地图

点、线之外，地图最有力的表达是**面**——国家边界、行政区、商圈、学区。这类数据
几乎总是以 [GeoJSON](https://datatracker.ietf.org/doc/html/rfc7946) 格式存在。
mapcn 的 `MapGeoJSON` 把任意 GeoJSON 渲染成「填充 + 描边」图层，开箱即用、主题
感知，是做分级着色图（choropleth）与区域地图的主力。

## 9.1 为什么需要 blank 底图

上一章的弧线、路线都画在默认街道底图上。而国家/区域地图通常需要一个**干净的
画布**——不希望街道、注记干扰图形本身。这时给 `Map` 加 `blank` 属性：

```tsx
import { Map, MapGeoJSON } from "@/components/ui/map";

// 假设 WORLD_GEOJSON 是一个 FeatureCollection（国家边界）
export function WorldMap() {
  return (
    <div className="h-[420px] w-full">
      <Map blank center={[10, 25]}>
        <MapGeoJSON data={WORLD_GEOJSON} linePaint={false} />
      </Map>
    </div>
  );
}
```

`blank` 是一块透明的、无瓦片画布；单独使用它什么都不显示，必须叠加自己的图层。
`linePaint={false}` 表示只画填充、不画边界线，得到一个纯色的「世界色块」。

## 9.2 在普通底图上叠加区域

更多时候，你想在真实街道底图上**高亮一块区域**（如某商圈）。这时不用 `blank`：

```tsx
import { Map, MapGeoJSON } from "@/components/ui/map";

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

export function OverlayExample() {
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

## 9.3 填充与描边的精细控制

`MapGeoJSON` 的关键样式属性：

| 属性 | 说明 |
| --- | --- |
| `fillPaint` | 多边形填充 paint；传 `false` 可省略填充层 |
| `linePaint` | 描边 paint；传 `false` 可省略描边层 |
| `fillHoverPaint` | 悬停要素的填充样式（需 `interactive`） |
| `promoteId` | 提升为要素 `id` 的属性，悬停/点击联动所需 |
| `interactive` | 是否响应鼠标事件（默认 `false`） |

默认填充是「主题感知的单色」，在浅色/深色下都清晰可读。你可以用 MapLibre
表达式做**数据驱动着色**，例如按人口上色：

```tsx
<MapGeoJSON
  data={provinces}
  promoteId="id"
  interactive
  fillPaint={{
    "fill-color": [
      "interpolate", ["linear"], ["get", "population"],
      1000000, "#fee5d9",
      10000000, "#fc9272",
      50000000, "#de2d26",
    ],
  }}
  fillHoverPaint={{ "fill-opacity": 0.95 }}
  onHover={(e) => e && setHovered(e.feature.properties.name)}
/>
```

这里 `promoteId` 把每个要素的 `id` 属性提升为要素 id，从而使 
`onHover` 的悬停高亮能精确定位到具体省；`onHover` 还能把省名同步到侧栏。

## 9.4 数据来源：内联、URL 或类型化

`MapGeoJSON` 接受四种形式：

1. 内联 `FeatureCollection` / `Feature` / `Geometry`（如上一节）；
2. 一个 URL 字符串，组件会自动 `fetch`；
3. 类型化泛型 `MapGeoJSON<T>`，获得属性类型提示；
4. 通过 `beforeId` 控制图层插入顺序（z-index）。

例如直接拉取在线 GeoJSON：

```tsx
<MapGeoJSON
  data="https://example.com/api/countries.geojson"
  promoteId="iso_code"
  interactive
  fillHoverPaint={{ "fill-color": "#1d4ed8" }}
/>
```

## 本章小结

- `MapGeoJSON` 把任意 GeoJSON 渲染为「填充 + 描边」图层；
- `blank` 底图适合纯区域/数据地图，`linePaint={false}` 可只画线；
- `fillPaint` / `linePaint` 接受 MapLibre 表达式，可做数据驱动分级着色；
- `promoteId` + `interactive` + `onHover` 实现悬停高亮与联动；
- `MapGeoJSON` 支持内联、URL、类型化泛型与 z-order 控制。

下一章，我们处理海量点的聚合。
