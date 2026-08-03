# Map

The simplest way to add an interactive map to your application.

## Basic Usage

The `Map` component handles MapLibre GL setup, theming, and provides context
for child components.

```tsx
import { Map } from "@/registry/map";

export function BasicMapExample() {
  return (
    <div className="h-[420px] w-full">
      <Map center={[-74.006, 40.7128]} zoom={12} />
    </div>
  );
}
```

## Controlled Mode

Use the `viewport` and `onViewportChange` props to control the map's viewport
externally. This is useful when you need to sync the map state with your
application or respond to viewport changes.

```tsx
"use client";

import { useState } from "react";
import { Map, type MapViewport } from "@/registry/map";

export function ControlledMapExample() {
  const [viewport, setViewport] = useState<MapViewport>({
    center: [-74.006, 40.7128],
    zoom: 8,
    bearing: 0,
    pitch: 0,
  });

  return (
    <div className="h-[420px] w-full">
      <Map viewport={viewport} onViewportChange={setViewport} />
    </div>
  );
}
```

## Blank Basemap

The `blank` prop swaps the default street basemap for a transparent, tile-less
canvas — perfect for data visualizations where you draw your own layers instead
of showing streets and labels.

> **Note:** `blank` is a blank canvas. Used alone, `<Map blank />` renders
> nothing — you must add your own layers on top (e.g. `MapGeoJSON`, `MapArc`, or
> markers). See [GeoJSON](./08-geojson.md) for more on rendering shapes on a
> blank map.

Here, a `MapGeoJSON` layer renders world country borders on top of the
transparent canvas.

```tsx
import { Map, MapGeoJSON } from "@/registry/map";
import { WORLD_GEOJSON } from "@/lib/use-world-data";

export function BlankMapExample() {
  return (
    <div className="h-[420px] w-full">
      <Map blank center={[10, 25]}>
        <MapGeoJSON data={WORLD_GEOJSON} />
      </Map>
    </div>
  );
}
```

## Custom Styles

Use the `styles` prop to provide custom map styles. This example uses free
vector tiles from [OpenFreeMap](https://openfreemap.org), an open-source
project; the data comes from OpenStreetMap.

```tsx
"use client";

import { useState, useEffect, useRef } from "react";
import { Map, type MapRef } from "@/registry/map";

const styles = {
  default: undefined,
  openstreetmap: "https://tiles.openfreemap.org/styles/bright",
  openstreetmap3d: "https://tiles.openfreemap.org/styles/liberty",
};

export function CustomStyleExample() {
  const mapRef = useRef<MapRef>(null);
  const [style, setStyle] = useState("default");

  useEffect(() => {
    mapRef.current?.easeTo({
      pitch: style === "openstreetmap3d" ? 60 : 0,
      duration: 500,
    });
  }, [style]);

  return (
    <div className="h-[420px] w-full">
      <Map
        ref={mapRef}
        center={[-0.1276, 51.5074]}
        zoom={15}
        styles={
          style === "default"
            ? undefined
            : {
                light: styles[style],
                dark: styles[style],
              }
        }
      />
    </div>
  );
}
```
