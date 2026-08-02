# 独立弹窗 Standalone Popups（官方文档研读）

> **研读说明**：本页为 mapcn 官方文档「独立弹窗 Standalone Popups」的中文研读笔记，内容以官方文档为基线整理，作为正文之外的查阅与补充。
> 相关正文：第 6 章（弹窗与提示框）。如与官方文档存在出入，请以官方文档为准。

在地图上任意位置显示弹窗，而无需依附于标记。

使用 `MapPopup` 可以在地图任意位置显示弹窗。与 `MarkerPopup` 不同，独立弹窗
不依附于标记，可以通过编程方式控制。

```tsx
"use client";

import { useState } from "react";
import { Map, MapPopup } from "@/registry/map";
import { Button } from "@/components/ui/button";

export function StandalonePopupExample() {
  const [showPopup, setShowPopup] = useState(true);

  return (
    <div className="relative h-[420px] w-full">
      <Map center={[-74.006, 40.7128]} zoom={13}>
        {showPopup && (
          <MapPopup
            longitude={-74.006}
            latitude={40.7128}
            onClose={() => setShowPopup(false)}
            closeButton
            closeOnClick={false}
          >
            <div className="space-y-2">
              <h3 className="text-foreground font-semibold">纽约市</h3>
              <p className="text-muted-foreground text-sm">
                不夜城。人口：830 万
              </p>
              <Button
                size="sm"
                variant="outline"
                className="w-full"
                onClick={() => setShowPopup(false)}
              >
                关闭
              </Button>
            </div>
          </MapPopup>
        )}
      </Map>

      {!showPopup && (
        <Button
          size="sm"
          className="absolute bottom-4 left-4 z-10"
          onClick={() => setShowPopup(true)}
        >
          显示弹窗
        </Button>
      )}
    </div>
  );
}
```

## 属性

| 属性 | 类型 | 说明 |
| --- | --- | --- |
| `longitude` | `number` | 弹窗位置的经度。 |
| `latitude` | `number` | 弹窗位置的纬度。 |
| `onClose` | `() => void` | 弹窗关闭时的回调。 |
| `children` | `ReactNode` | 弹窗内容。 |
| `className` | `string` | 弹窗容器的附加 CSS 类。 |
| `closeButton` | `boolean` | 是否在弹窗中显示关闭按钮（默认 `false`）。 |

