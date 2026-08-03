# Arcs

Draw curved connections between two coordinates with hover and click support.

Use `MapArc` to draw curved lines between coordinate pairs. Arcs are great for
showing flight paths, shipping lanes, or any origin–destination connection
where a straight line would feel flat.

## Basic Arc

Pass an array of arcs to the `data` prop. Each arc needs a unique `id` and
`from` / `to` coordinates as `[longitude, latitude]` tuples.

```tsx
import { Map, MapArc, MapMarker, MarkerContent, MarkerLabel } from "@/registry/map";

const hub = { name: "London", lng: -0.1276, lat: 51.5074 };
const destinations = [
  { name: "New York", lng: -74.006, lat: 40.7128 },
  { name: "São Paulo", lng: -46.6333, lat: -23.5505 },
  { name: "Tokyo", lng: 139.6917, lat: 35.6895 },
];

const arcs = destinations.map((dest) => ({
  id: dest.name,
  from: [hub.lng, hub.lat] as [number, number],
  to: [dest.lng, dest.lat] as [number, number],
}));

export function ArcExample() {
  return (
    <div className="h-[420px] w-full">
      <Map center={[hub.lng, hub.lat]} zoom={1} projection={{ type: "globe" }}>
        <MapArc
          data={arcs}
          paint={{ "line-color": "#3b82f6", "line-dasharray": [2, 2] }}
          interactive={false}
        />
      </Map>
    </div>
  );
}
```

## Interactive Arcs

Combine `hoverPaint` with `onHover` to highlight an arc and surface details in
a `MapPopup`. Use a `match` expression on `line-color` to style arcs by
category. Here, air and sea lanes are styled differently.

```tsx
"use client";

import { useState } from "react";
import type { ExpressionSpecification } from "maplibre-gl";
import {
  Map,
  MapArc,
  MapMarker,
  MapPopup,
  MarkerContent,
  MarkerLabel,
  type MapArcDatum,
} from "@/registry/map";

interface Lane extends MapArcDatum {
  origin: string;
  destination: string;
  volume: string;
  mode: "air" | "sea";
}

const lanes: Lane[] = [
  { id: "dxb-jfk", origin: "Dubai", destination: "New York", from: [55.2708, 25.2048], to: [-74.006, 40.7128], volume: "980 tons", mode: "air" },
  { id: "sin-rtm", origin: "Singapore", destination: "Rotterdam", from: [103.8198, 1.3521], to: [4.4777, 51.9244], volume: "9.4k TEU", mode: "sea" },
];

const modeColorExpression: ExpressionSpecification = [
  "match", ["get", "mode"], "air", "#a78bfa", "sea", "#34d399", "#888",
];

export function InteractiveArcExample() {
  const [selected, setSelected] = useState<Lane | null>(null);
  return (
    <div className="h-[420px] w-full">
      <Map center={[20, 20]} zoom={0.8}>
        <MapArc<Lane>
          data={lanes}
          paint={{ "line-color": modeColorExpression, "line-width": 1.5 }}
          hoverPaint={{ "line-width": 3, "line-opacity": 1 }}
          onHover={(e) => setSelected(e ? e.arc : null)}
        />
        {selected && (
          <MapPopup longitude={selected.from[0]} latitude={selected.from[1]}>
            {selected.origin} → {selected.destination} ({selected.volume})
          </MapPopup>
        )}
      </Map>
    </div>
  );
}
```
