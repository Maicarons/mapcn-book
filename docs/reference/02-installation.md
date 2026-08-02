# 安装（官方文档研读）

> **研读说明**：本页为 mapcn 官方文档「安装」的中文研读笔记，内容以官方文档为基线整理，作为正文之外的查阅与补充。
> 相关正文：第 2 章（环境准备与安装）。如与官方文档存在出入，请以官方文档为准。

如何在你的项目中安装并配置 mapcn。

## 前置条件

一个已经配置好 [Tailwind CSS](https://tailwindcss.com) 与
[shadcn/ui](https://ui.shadcn.com) 的项目。

## 安装

运行以下命令以添加地图组件：

```bash
npx shadcn@latest add https://mapcn.dev/r/map.json
```

该命令会安装 `maplibre-gl`，并把地图组件添加到你的项目（通常位于
`components/ui/map.tsx`）。

> **注意：** shadcn CLI 会把组件源码复制进你的仓库，因此你完全拥有它。除
> `maplibre-gl` 和 React 之外，运行时不依赖任何其它库。

## 使用

导入并使用地图组件：

```tsx
import { Map, MapControls } from "@/components/ui/map";
import { Card } from "@/components/ui/card";

export function MyMap() {
  return (
    <Card className="h-[320px] p-0 overflow-hidden">
      <Map center={[-74.006, 40.7128]} zoom={11}>
        <MapControls />
      </Map>
    </Card>
  );
}
```

> **注意：** 地图默认使用免费的 CARTO 底图瓦片，并会在浅色与深色主题之间自动
> 切换。

