# 控件 Controls

为地图添加缩放、指北针、定位与全屏等交互控件。

`MapControls` 组件提供一组可放置在地图任意角落的交互控件。

```tsx
import { Map, MapControls } from "@/registry/map";

export function MapControlsExample() {
  return (
    <div className="h-[420px] w-full">
      <Map center={[2.3522, 48.8566]} zoom={10}>
        <MapControls
          position="top-right"
          showZoom
          showCompass
          showLocate
          showFullscreen
        />
      </Map>
    </div>
  );
}
```

## 属性

| 属性 | 类型 | 默认值 | 说明 |
| --- | --- | --- | --- |
| `position` | `"top-left" \| "top-right" \| "bottom-left" \| "bottom-right"` | `"bottom-right"` | 控件在地图上的位置。 |
| `showZoom` | `boolean` | `true` | 是否显示放大/缩小按钮。 |
| `showCompass` | `boolean` | `false` | 是否显示用于复位方位角的指北针按钮。 |
| `showLocate` | `boolean` | `false` | 是否显示定位按钮以寻找用户位置。 |
| `showFullscreen` | `boolean` | `false` | 是否显示全屏切换按钮。 |
| `className` | `string` | — | 控件容器的附加 CSS 类。 |
| `onLocate` | `(coords: { longitude: number; latitude: number }) => void` | — | 定位成功时的回调，返回用户坐标。 |
