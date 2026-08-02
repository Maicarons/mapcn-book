# 第 14 章 实战：构建一个门店地图应用

从前 13 章走到这里，你已经掌握了 mapcn 的全部核心能力。本章把它们串成一个完整
可运行的「门店地图」：左侧是可筛选的门店列表，右侧是地图，二者通过选中状态双向
联动；地图用聚合呈现全部门店，点击单点弹出详情；并带搜索与主题切换。

## 14.1 数据结构

```ts
interface Store {
  id: string;
  name: string;
  category: string;     // 餐饮 / 零售 / 服务
  lng: number;
  lat: number;
  address: string;
  rating: number;
}
```

把若干门店组织成 GeoJSON `FeatureCollection`，便于交给 `MapClusterLayer`：

```ts
const storesToFC = (stores: Store[]): GeoJSON.FeatureCollection => ({
  type: "FeatureCollection",
  features: stores.map((s) => ({
    type: "Feature",
    properties: { id: s.id, name: s.name, category: s.category, rating: s.rating },
    geometry: { type: "Point", coordinates: [s.lng, s.lat] },
  })),
});
```

## 14.2 主组件骨架

```tsx
"use client";

import { useMemo, useState } from "react";
import { Map, MapClusterLayer, MapPopup, MapControls } from "@/components/ui/map";
import { Card } from "@/components/ui/card";

export function StoreMap({ stores }: { stores: Store[] }) {
  const [selected, setSelected] = useState<Store | null>(null);
  const [query, setQuery] = useState("");

  const filtered = useMemo(
    () => stores.filter((s) => s.name.includes(query) || s.category.includes(query)),
    [stores, query],
  );
  const fc = useMemo(() => storesToFC(filtered), [filtered]);

  return (
    <div className="grid h-[600px] grid-cols-[320px_1fr] gap-4">
      {/* 左侧列表 */}
      <Card className="overflow-auto p-3">
        <input
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          placeholder="搜索门店…"
          className="mb-3 w-full rounded border px-2 py-1 text-sm"
        />
        {filtered.map((s) => (
          <button
            key={s.id}
            onClick={() => setSelected(s)}
            className="block w-full rounded px-2 py-1.5 text-left text-sm hover:bg-accent"
          >
            <div className="font-medium">{s.name}</div>
            <div className="text-muted-foreground text-xs">{s.category} · {s.rating}★</div>
          </button>
        ))}
      </Card>

      {/* 右侧地图 */}
      <Card className="relative overflow-hidden p-0">
        <Map center={[116.4, 39.9]} zoom={10}>
          <MapClusterLayer<Store>
            data={fc}
            onPointClick={(f) => {
              const p = f.properties;
              setSelected(stores.find((s) => s.id === p.id) ?? null);
            }}
          />
          {selected && (
            <MapPopup
              longitude={selected.lng}
              latitude={selected.lat}
              onClose={() => setSelected(null)}
              closeButton
              closeOnClick={false}
            >
              <div className="space-y-1">
                <p className="font-semibold">{selected.name}</p>
                <p className="text-muted-foreground text-xs">{selected.address}</p>
                <p className="text-xs">{selected.category} · {selected.rating}★</p>
              </div>
            </MapPopup>
          )}
          <MapControls />
        </Map>
      </Card>
    </div>
  );
}
```

## 14.3 联动逻辑解析

- **列表 → 地图**：点击列表项 `setSelected(s)`，地图中对应的 `MapPopup` 在
   `selected` 坐标处弹出；
- **地图 → 列表**：点击聚合中的单点触发 `onPointClick`，用要素 `id` 反查 
  `stores` 得到完整对象并 `setSelected(...)`，列表可用 `selected` 高亮当前项（此处略去高亮样式）；
- **搜索**：`query` 过滤 `filtered`，`useMemo` 派生 `fc`，聚合层随之更新——这正符合
  第 13 章「大数据用 `useMemo` 缓存」的建议。

## 14.4 还能怎么扩展

这个骨架已经覆盖了真实项目最常见的模式，接下来可自然延伸：

- **分类筛选**：用 `paint` 表达式为不同 `category` 着色（见第 8 章）；
- **路由规划**：选中两个门店后，调用 OSRM 画出驾车路线（见第 7 章）；
- **详情弹窗富化**：把 `MapPopup` 内容换成带图片、评分、按钮的卡片（见第 6 章）；
- **性能**：门店过万时，`MapClusterLayer` 的聚合天然扛得住，无需改动结构。

## 14.5 收尾：你已经学到了什么

回顾全书：

1. 第 1–2 章：理解 mapcn 的定位并完成安装；
2. 第 3–4 章：渲染第一张地图、加上控件；
3. 第 5–6 章：标记、弹窗、提示框；
4. 第 7–10 章：路线、弧线、GeoJSON、聚合；
5. 第 11–12 章：深入实例、主题与自定义底图；
6. 第 13 章：性能与最佳实践；
7. 第 14 章：用一个完整案例落地。

你现在已经具备用 mapcn 构建生产级地图应用的能力。

## 本章小结

- 门店地图 = `MapClusterLayer`（聚合）+ `MapPopup`（详情）+ 列表（侧栏）的联动；
- 列表与地图通过共享 `selected` 状态双向联动；
- 搜索用 `useMemo` 派生 GeoJSON，聚合层自动更新；
- 骨架可直接扩展为分类着色、路线规划、富弹窗等；
- 至此，你已掌握从入门到进阶的全部核心能力。

愿你的地图，既好看，又好用。
