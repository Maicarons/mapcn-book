# API 参考（官方文档研读）

> **研读说明**：本页为 mapcn 官方文档「API 参考」的中文研读笔记，内容以官方文档为基线整理，作为正文之外的查阅与补充。
> 相关正文：全书组件速查。如与官方文档存在出入，请以官方文档为准。

全部地图组件及其属性的完整参考。

> **注意：** 本库构建于
> [MapLibre GL JS](https://maplibre.org/maplibre-gl-js/docs/API/) 之上，多数组件
> 扩展了原生的 MapLibre 选项。未在此列出的额外选项，请查阅
> [MapLibre Map API](https://maplibre.org/maplibre-gl-js/docs/API/classes/Map/)。

## 组件结构

你可以组合使用的所有部件，用以构建自己的地图。

```tsx
<Map>
  <MapMarker longitude={...} latitude={...}>
    <MarkerContent>
      <MarkerLabel />
    </MarkerContent>
    <MarkerPopup />
    <MarkerTooltip />
  </MapMarker>

  <MapPopup longitude={...} latitude={...} />
  <MapControls />
  <MapRoute coordinates={...} />
  <MapArc data={...} />
  <MapGeoJSON data={...} />
  <MapClusterLayer data={...} />
</Map>
```

## Map

根容器组件，负责初始化 MapLibre GL 并为子组件提供上下文。自动处理浅色/深色主题
切换。

继承自 MapLibre GL 的
[MapOptions](https://maplibre.org/maplibre-gl-js/docs/API/type-aliases/MapOptions/)
（排除 `container` 与 `style`）。

| 属性 | 类型 | 默认值 | 说明 |
| --- | --- | --- | --- |
| `children` | `ReactNode` | — | 子组件（标记、弹窗、控件、路线）。 |
| `className` | `string` | — | 地图容器的附加 CSS 类。 |
| `theme` | `"light" \| "dark"` | — | 地图主题。若不提供，则从文档 class 或系统偏好自动检测。 |
| `styles` | `{ light?: string \| StyleSpecification; dark?: string \| StyleSpecification }` | — | 浅色与深色主题的自定义地图样式，覆盖默认的 Carto 底图瓦片。 |
| `blank` | `boolean` | `false` | 使用透明、无瓦片的底图替换默认 Carto 街道底图。提供显式 `styles` 时此属性被忽略。 |
| `projection` | `ProjectionSpecification` | — | 地图投影类型。使用 `{ type: "globe" }` 可切换为 3D 地球视图。 |
| `viewport` | `Partial<MapViewport>` | — | 受控视口状态。也可单独用于设置初始视口。 |
| `onViewportChange` | `(viewport: MapViewport) => void` | — | 视口变化时持续触发的回调。 |
| `loading` | `boolean` | `false` | 在地图上显示加载指示器。 |

## useMap

提供对 MapLibre 地图实例与加载状态的访问钩子。必须在 `Map` 组件内部使用。

```tsx
const { map, isLoaded } = useMap();
```

返回 `map`（[MapLibre.Map](https://maplibre.org/maplibre-gl-js/docs/API/classes/Map/)）
与 `isLoaded`（布尔值，指示地图是否已加载就绪）。

## MapControls

渲染地图控制按钮（缩放、指北针、定位、全屏）。必须在 `Map` 内部使用。

| 属性 | 类型 | 默认值 | 说明 |
| --- | --- | --- | --- |
| `position` | `"top-left" \| "top-right" \| "bottom-left" \| "bottom-right"` | `"bottom-right"` | 控件位置。 |
| `showZoom` | `boolean` | `true` | 是否显示缩放按钮。 |
| `showCompass` | `boolean` | `false` | 是否显示复位方位角的指北针按钮。 |
| `showLocate` | `boolean` | `false` | 是否显示定位按钮。 |
| `showFullscreen` | `boolean` | `false` | 是否显示全屏切换按钮。 |
| `className` | `string` | — | 控件容器的附加 CSS 类。 |
| `onLocate` | `(coords: { longitude: number; latitude: number }) => void` | — | 定位成功时的回调。 |

## MapMarker

标记相关组件的容器，为其子组件提供上下文并处理标记定位。

继承自 MapLibre GL 的
[MarkerOptions](https://maplibre.org/maplibre-gl-js/docs/API/type-aliases/MarkerOptions/)
（排除 `element`）。

| 属性 | 类型 | 说明 |
| --- | --- | --- |
| `longitude` | `number` | 标记的经度坐标。 |
| `latitude` | `number` | 标记的纬度坐标。 |
| `children` | `ReactNode` | 标记子组件（MarkerContent、MarkerPopup 等）。 |
| `onClick` | `(e: MouseEvent) => void` | 标记被点击时的回调。 |
| `onMouseEnter` | `(e: MouseEvent) => void` | 鼠标进入标记时的回调。 |
| `onMouseLeave` | `(e: MouseEvent) => void` | 鼠标离开标记时的回调。 |
| `onDragStart` | `(lngLat: { lng, lat }) => void` | 拖拽开始时的回调（需 `draggable: true`）。 |
| `onDrag` | `(lngLat: { lng, lat }) => void` | 拖拽过程中的回调（需 `draggable: true`）。 |
| `onDragEnd` | `(lngLat: { lng, lat }) => void` | 拖拽结束时的回调（需 `draggable: true`）。 |

## MarkerContent

渲染标记的可视内容。必须在 `MapMarker` 内部使用。若不提供子组件，则渲染默认的
蓝色圆点标记。

| 属性 | 类型 | 说明 |
| --- | --- | --- |
| `children` | `ReactNode` | 自定义标记内容，默认为蓝色圆点。 |
| `className` | `string` | 标记容器的附加 CSS 类。 |

## MarkerPopup

渲染依附于标记的弹窗，点击时打开。必须在 `MapMarker` 内部使用。

继承自 MapLibre GL 的
[PopupOptions](https://maplibre.org/maplibre-gl-js/docs/API/type-aliases/PopupOptions/)
（排除 `className` 与 `closeButton`）。

| 属性 | 类型 | 默认值 | 说明 |
| --- | --- | --- | --- |
| `children` | `ReactNode` | — | 弹窗内容。 |
| `className` | `string` | — | 弹窗容器的附加 CSS 类。 |
| `closeButton` | `boolean` | `false` | 是否在弹窗中显示关闭按钮。 |

## MarkerTooltip

渲染悬停时出现的提示框。必须在 `MapMarker` 内部使用。

继承自 MapLibre GL 的
[PopupOptions](https://maplibre.org/maplibre-gl-js/docs/API/type-aliases/PopupOptions/)
（排除 `className`、`closeButton` 与 `closeOnClick`）。

| 属性 | 类型 | 说明 |
| --- | --- | --- |
| `children` | `ReactNode` | 提示框内容。 |
| `className` | `string` | 提示框容器的附加 CSS 类。 |

## MarkerLabel

在标记上方或下方渲染文本标签。必须在 `MarkerContent` 内部使用。

| 属性 | 类型 | 默认值 | 说明 |
| --- | --- | --- | --- |
| `children` | `ReactNode` | — | 标签文本。 |
| `className` | `string` | — | 标签的附加 CSS 类。 |
| `position` | `"top" \| "bottom"` | `"top"` | 标签相对标记的位置。 |

## MapPopup

不依赖标记、可在地图上任意位置放置的独立弹窗组件。必须在 `Map` 内部使用。

继承自 MapLibre GL 的
[PopupOptions](https://maplibre.org/maplibre-gl-js/docs/API/type-aliases/PopupOptions/)
（排除 `className` 与 `closeButton`）。

| 属性 | 类型 | 默认值 | 说明 |
| --- | --- | --- | --- |
| `longitude` | `number` | — | 弹窗位置的经度。 |
| `latitude` | `number` | — | 弹窗位置的纬度。 |
| `onClose` | `() => void` | — | 弹窗关闭时的回调。 |
| `children` | `ReactNode` | — | 弹窗内容。 |
| `className` | `string` | — | 弹窗容器的附加 CSS 类。 |
| `closeButton` | `boolean` | `false` | 是否在弹窗中显示关闭按钮。 |

## MapRoute

在地图上渲染连接坐标点的线段/路线。必须在 `Map` 内部使用，支持点击与悬停交互，
便于构建路线选择界面。

| 属性 | 类型 | 默认值 | 说明 |
| --- | --- | --- | --- |
| `id` | `string` | 自动生成 | 路线图层的可选唯一标识。 |
| `coordinates` | `[number, number][]` | — | `[经度, 纬度]` 坐标对数组。 |
| `color` | `string` | `"#4285F4"` | 线条颜色（CSS 颜色值）。 |
| `width` | `number` | `3` | 线条宽度（像素）。 |
| `opacity` | `number` | `0.8` | 线条不透明度（0 到 1）。 |
| `dashArray` | `[number, number]` | — | 虚线样式 `[线段长, 间隔长]`。 |
| `onClick` | `() => void` | — | 路线被点击时的回调。 |
| `onMouseEnter` | `() => void` | — | 鼠标进入路线时的回调。 |
| `onMouseLeave` | `() => void` | — | 鼠标离开路线时的回调。 |
| `interactive` | `boolean` | `false` | 是否响应鼠标事件（悬停、光标、回调）。 |

## MapArc

在坐标对之间使用经纬度空间的二次贝塞尔曲线绘制弧线。必须在 `Map` 内部使用，
支持点击与悬停交互。

基于 MapLibre 的
[line 图层](https://maplibre.org/maplibre-style-spec/layers/#line)——
`paint` 与 `layout` 属性接受 `LineLayerSpecification` 中的任意字段。可将任意
[paint 值](https://maplibre.org/maplibre-style-spec/expressions/) 设为 MapLibre
表达式，以按要素着色。

| 属性 | 类型 | 默认值 | 说明 |
| --- | --- | --- | --- |
| `data` | `MapArcDatum[]` | — | 要渲染的弧线。每条需唯一 `id` 与 `[lng, lat]` 的 `from` / `to`。 |
| `id` | `string` | auto | 底层 source/图层的前缀。 |
| `curvature` | `number` | `0.2` | 弧线偏离直线的弯曲程度。 |
| `samples` | `number` | `64` | 每条弧线的采样点数，越大越平滑。 |
| `paint` | `LineLayerSpecification['paint']` | `{ "line-color": "#4285F4", "line-width": 2, "line-opacity": 0.85 }` | 覆盖于默认值之上的 paint 属性。 |
| `layout` | `LineLayerSpecification['layout']` | `{ "line-join": "round", "line-cap": "round" }` | 覆盖于默认值之上的 layout 属性。 |
| `hoverPaint` | `LineLayerSpecification['paint']` | — | 悬停弧线时通过 feature-state 应用的 paint 覆盖。 |
| `onClick` | `(e: MapArcEvent) => void` | — | 弧线被点击时触发。 |
| `onHover` | `(e: MapArcEvent \| null) => void` | — | 悬停弧线变化时的回调。 |
| `interactive` | `boolean` | `true` | 是否响应鼠标事件。 |
| `beforeId` | `string` | — | 将弧线图层插入到该图层之前。 |

## MapGeoJSON

将任意 GeoJSON 渲染为填充 + 描边图层。必须在 `Map` 内部使用——通常配合 `blank`
属性用于分级着色图与区域/数据地图。接受 `FeatureCollection`、`Feature`、
`Geometry`，或用于拉取的 URL 字符串。支持泛型类型参数以约束要素属性：
`MapGeoJSON<MyProperties>`。

| 属性 | 类型 | 说明 |
| --- | --- | --- |
| `data` | `FeatureCollection \| Feature \| Geometry \| string` | GeoJSON 数据，或用于拉取的 URL 字符串。 |
| `id` | `string` | 底层 source/图层的前缀。 |
| `promoteId` | `string` | 提升为要素 `id` 的属性。悬停 feature-state 所需。 |
| `fillPaint` | `FillLayerSpecification['paint'] \| false` | 多边形填充图层 paint。传 `false` 可省略填充层。 |
| `linePaint` | `LineLayerSpecification['paint'] \| false` | 描边图层 paint。传 `false` 可省略描边层。 |
| `fillHoverPaint` | `FillLayerSpecification['paint']` | 悬停要素时叠加到填充层的 paint。需 `promoteId`。 |
| `onClick` | `(e: MapGeoJSONEvent) => void` | 要素被点击时触发。 |
| `onHover` | `(e: MapGeoJSONEvent \| null) => void` | 悬停要素变化时的回调。 |
| `interactive` | `boolean` | 是否响应鼠标事件（默认 `false`）。 |
| `beforeId` | `string` | 将图层插入到该图层之前。 |

## MapClusterLayer

使用 MapLibre GL 原生聚合能力渲染聚合点数据。必须在 `Map` 内部使用。支持泛型
类型参数：`MapClusterLayer<MyProperties>`。

| 属性 | 类型 | 默认值 | 说明 |
| --- | --- | --- | --- |
| `data` | `string \| GeoJSON.FeatureCollection` | — | 聚合点 GeoJSON 数据，或用于拉取的 URL。 |
| `clusterMaxZoom` | `number` | `14` | 进行点聚合的最大缩放级别。 |
| `clusterRadius` | `number` | `50` | 聚合半径（像素）。 |
| `clusterColors` | `[string, string, string]` | `["#3b82f6", "#1d4ed8", "#1e3a8a"]` | 簇圆配色：`[小, 中, 大]`。 |
| `clusterThresholds` | `[number, number]` | `[100, 750]` | 配色/尺寸分级的点数阈值。 |
| `pointColor` | `string` | `"#3b82f6"` | 未聚合单点颜色。 |
| `onPointClick` | `(feature, coordinates) => void` | — | 未聚合单点被点击时的回调。 |
| `onClusterClick` | `(clusterId, coordinates, pointCount) => void` | — | 簇被点击时的回调。若不提供，则放大进入该簇。 |

