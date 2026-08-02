# 第 06 章 弹窗与提示框

弹窗（Popup）是地图与用户对话的主要媒介：点击店铺看详情、悬停标记看名称，都离
不开它。mapcn 区分两种弹窗——**依附于标记的弹窗**（`MarkerPopup`）与**独立于
标记的弹窗**（`MapPopup`）——本章逐一讲解。

## 6.1 MarkerPopup：依附于标记

`MarkerPopup` 必须放在 `MapMarker` 内部，点击标记时弹出：

```tsx
<MapMarker longitude={lng} latitude={lat}>
  <MarkerContent>
    <div className="size-4 rounded-full bg-blue-500 border-2 border-white" />
  </MarkerContent>
  <MarkerPopup>
    <p className="font-medium">帝国大厦</p>
    <p className="text-muted-foreground text-xs">纽约 · 观景台</p>
  </MarkerPopup>
</MapMarker>
```

它的内容是任意 React 节点，因此可以嵌入图片、评分、按钮等富内容，与 shadcn/ui
组件无缝结合。

## 6.2 富交互弹窗

借助 shadcn 的 `Button`、`Star` 与 `Navigation` 图标，可以拼出信息卡风格
的弹窗：

```tsx
import { Button } from "@/components/ui/button";
import { Star, Navigation } from "lucide-react";

<MarkerPopup className="w-62">
  <div className="space-y-2 p-3">
    <h3 className="font-semibold">大都会艺术博物馆</h3>
    <div className="flex items-center gap-1 text-sm">
      <Star className="size-3.5 fill-amber-400 text-amber-400" />
      <span className="font-medium">4.8</span>
      <span className="text-muted-foreground">(12,453)</span>
    </div>
    <Button size="sm" className="w-full">
      <Navigation className="size-3.5" /> 导航
    </Button>
  </div>
</MarkerPopup>
```

> **样式提示：** mapcn 已重置 MapLibre 弹窗的默认样式以避免冲突，请使用组件自身
> 的 `className` 与 shadcn 令牌来定制外观，而不是覆盖 MapLibre 的 `maplibre-gl` 默认样式 /
> 弹窗容器。

## 6.3 关闭按钮

默认弹窗不带关闭按钮（点击地图其它处即可消失）。需要显式关闭按钮时，传
`closeButton`：

```tsx
<MarkerPopup closeButton>
  <p>可关闭的内容</p>
</MarkerPopup>
```

## 6.4 MarkerTooltip：轻量提示

`MarkerTooltip` 在悬停时出现、移出即消失，适合展示极短的信息（名称、状态）：

```tsx
<MarkerTooltip>{loc.name}</MarkerTooltip>
```

它是对 `MarkerPopup` 的封装，但刻意排除了 `closeButton`，因为提示框本就不该
被点击关闭。

## 6.5 MapPopup：独立弹窗

`MapPopup` 不依赖标记，可在地图任意经纬度放置，并通过状态**编程控制**。它必须
放在 `Map` 内部。

```tsx
"use client";

import { useState } from "react";
import { Map, MapPopup } from "@/components/ui/map";
import { Button } from "@/components/ui/button";

export function StandalonePopup() {
  const [show, setShow] = useState(true);

  return (
    <div className="relative h-[420px] w-full">
      <Map center={[-74.006, 40.7128]} zoom={13}>
        {show && (
          <MapPopup
            longitude={-74.006}
            latitude={40.7128}
            onClose={() => setShow(false)}
            closeButton
            closeOnClick={false}
          >
            <div className="space-y-2">
              <h3 className="font-semibold">纽约市</h3>
              <p className="text-sm text-muted-foreground">人口：830 万</p>
              <Button size="sm" variant="outline" className="w-full"
                      onClick={() => setShow(false)}>关闭</Button>
            </div>
          </MapPopup>
        )}
      </Map>
      {!show && (
        <Button className="absolute bottom-4 left-4"
                onClick={() => setShow(true)}>显示弹窗</Button>
      )}
    </div>
  );
}
```

常见用法：点击列表项 → 在对应坐标弹出 `MapPopup`；或聚合点被点击 → 在聚合中心
弹出详情（见第 10 章）。

## 本章小结

- `MarkerPopup` 依附于标记，点击弹出，内容可任意富化；
- 用 `closeButton` 开启关闭按钮，样式走 `className` + shadcn 令牌；
- `MarkerTooltip` 是悬停提示，轻量、自动消失；
- `MapPopup` 独立、可编程，靠 `longitude`/`latitude` 定位，适合列表联动；
- 两者都基于 MapLibre `Popup`，但排除了会引发样式冲突的字段。

下一章，我们绘制连接坐标的路线。
