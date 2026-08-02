# 第 12 章 主题、样式与自定义底图

地图不是孤立的视觉元素——它要融入你的整体设计系统。本章讲清三件事：浅/深主题
如何自动切换、如何替换底图、以及 3D 地球等投影玩法。

## 12.1 主题自动切换

`Map` 默认读取文档根元素的 `dark` / `light` class（兼容 next-themes 的
`dark` 与 `light` 两种模式），并监听系统偏好变化，
在 Carto 的浅色（Positron）与深色（Dark Matter）底图间无缝切换。你**无需写任何
切换代码**。

若想强制指定：

```tsx
<Map theme="dark" center={[-74.006, 40.7128]} zoom={11} />
```

## 12.2 替换底图：styles 属性

`styles` 接受一个分别针对浅/深主题的样式对象，覆盖默认 Carto 底图：

```tsx
const myStyles = {
  light: "https://tiles.openfreemap.org/styles/bright",
  dark: "https://tiles.openfreemap.org/styles/liberty",
};

<Map styles={myStyles} center={[-0.1276, 51.5074]} zoom={15} />
```

也可以使用完整的 MapLibre `StyleSpecification` 对象（而非 URL），便于完全程序化
构建样式。注意：一旦显式提供 `styles`，`style` 属性会被忽略。

## 12.3 空白画布 blank

`blank` 用一块透明无瓦片的画布替换街道底图，是数据可视化的理想基底（分级着色图、
世界弧线、点阵图都在此之上绘制自己的图层）：

```tsx
<Map blank center={[10, 25]}>
  <MapGeoJSON data={WORLD_GEOJSON} />
</Map>
```

透明背景会让下方的主题容器透出，因此浅色/深色模式下都自然协调。

## 12.4 投影与 3D 地球

`projection` 属性控制地图投影。传入 `{ type: "globe" }` 即可切换到 3D 地球视图，
弧线与全球航线在地球上最具表现力：

```tsx
<Map center={[0, 20]} zoom={1} projection={{ type: "globe" }}>
  <MapArc data={globalArcs} />
</Map>
```

也可以在用户交互后动态切换投影（需地图样式已加载）：

```tsx
map.setProjection({ type: "globe" });
```

## 12.5 组件外观的 Tailwind 化

mapcn 组件的外观完全由 Tailwind 类驱动，因此「换肤」就是改类：把标记的蓝点改成
品牌色，只需换 `bg-primary` → `bg-rose-500`；把弹窗内边距调小，直接在
`className` 上改 `p-3`。没有独立的「主题配置文件」需要维护。

## 12.6 小结：样式优先级

当多个样式来源冲突时，优先级如下：

1. 显式 `style`/`styles` 属性（最高）；
2. `blank` 透明画布；
3. 默认 Carto 浅/深底图（随主题自动）。

图层类的样式（`MapRoute` 的 `paint`、`MapGeoJSON` 的 `fillPaint`）始终叠加在底图
之上，不受底图切换影响。

## 本章小结

- 主题默认按文档 class 与系统偏好自动切换，可用 `theme` 覆盖；
- `styles` 分别指定浅/深底图（URL 或 StyleSpecification），会屏蔽 `style`；
- `blank` 是透明画布，适合数据可视化；
- `projection` 切换 3D 地球；
- 组件外观即 Tailwind 类，换肤=改类，无需主题配置文件。

下一章，我们聚焦性能与最佳实践。
