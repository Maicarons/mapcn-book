# 第 04 章 地图控件与交互

一张静态地图只能看，加上控件后才能「用」。mapcn 的 `MapControls` 把缩放、指北
针、定位、全屏等常用控件打包成一个声明式组件，你可以按需在任意角落开关它们。

## 4.1 一行加全套控件

```tsx
import { Map, MapControls } from "@/components/ui/map";

export function MapWithControls() {
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

四个开关含义如下：

- `showZoom`：放大/缩小按钮（默认开启）；
- `showCompass`：复位方位角的指北针（点击后 `bearing` 归零、`pitch` 归零）；
- `showLocate`：调用浏览器地理定位，飞到用户所在位置；
- `showFullscreen`：切换地图容器的全屏状态。

## 4.2 控制位置

`position` 决定控件落在哪个角，可选值：

```
"top-left" | "top-right" | "bottom-left" | "bottom-right"   // 默认 bottom-right
```

多数产品把缩放放在右下，把「定位/全屏」放在右上，避免与底部版权信息重叠。

## 4.3 定位回调

当用户点击定位按钮并授权后，`MapControls` 会回调其坐标，便于你做进一步处理
（例如记录、或在列表中高亮）：

```tsx
<MapControls
  showLocate
  onLocate={(coords) => {
    console.log("用户位于", coords.longitude, coords.latitude);
  }}
/>
```

> **注意：** 定位依赖浏览器的 Geolocation API，必须在 HTTPS（或
> `localhost`）环境下、且用户明确授权后才会成功。被拒绝时按钮会自动复位，不会
> 卡死。

## 4.4 受控之外的交互底色

`MapControls` 本质上是对 MapLibre 原生控件的轻封装。例如放大按钮调用的是
`map.zoomIn()`，全屏则操作地图容器的
`requestFullscreen()`。理解了这一点，当你需要完全自定义控件时，就能自然地过渡到
第 11 章的「直接操作 `map` 实例」。

## 4.5 自定义控件示例（预览）

如果你想要文档站里那种「3D 视角 / 复位」按钮，思路是：用 `useMap` 拿到
`map`，在按钮里调用 `map.easeTo()`。完整代码见第 11 章，这里先看个骨架：

```tsx
"use client";

import { Map, useMap } from "@/components/ui/map";
import { Button } from "@/components/ui/button";

function Controller() {
  const { map, isLoaded } = useMap();
  if (!isLoaded) return null;
  return (
    <Button size="sm" onClick={() => map?.easeTo({ pitch: 60, duration: 800 })}>
      3D 视角
    </Button>
  );
}
```

## 本章小结

- `MapControls` 一行即可叠加缩放/指北针/定位/全屏控件；
- 用 `position` 控制角落，`show*` 系列开关控制显示哪些；
- `onLocate` 在用户授权定位后回调坐标；
- 控件是对 MapLibre 原生能力的封装，自定义控件应走第 11 章的 `useMap` 路线。

下一章，我们在地图上放置标记点。
