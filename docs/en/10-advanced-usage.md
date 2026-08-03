# Advanced

Access the underlying MapLibre GL instance for advanced customization.

Access the underlying MapLibre GL map instance to use any feature from the
MapLibre GL JS API. You can use either a `ref` or the `useMap` hook.

> **Tip:** Check the
> [MapLibre GL JS documentation](https://maplibre.org/maplibre-gl-js/docs/API/classes/Map/)
> for the full list of available methods and events.

## Using a Ref

The simplest way to access the map instance. Use a `ref` to call map methods
from event handlers or effects.

```tsx
import { Map, type MapRef } from "@/components/ui/map";
import { useRef } from "react";

function MyMapComponent() {
  const mapRef = useRef<MapRef>(null);

  const handleFlyTo = () => {
    mapRef.current?.flyTo({ center: [-74, 40.7], zoom: 12 });
  };

  return (
    <>
      <button onClick={handleFlyTo}>Fly to NYC</button>
      <Map ref={mapRef} center={[-74, 40.7]} zoom={10} />
    </>
  );
}
```

## Using the Hook

For child components rendered inside `Map`, use the `useMap` hook to access the
map instance and listen to events.

```tsx
import { Map, useMap } from "@/components/ui/map";
import { useEffect } from "react";

function MapEventListener() {
  const { map, isLoaded } = useMap();

  useEffect(() => {
    if (!map || !isLoaded) return;
    const handleClick = (e: any) => console.log("Clicked at:", e.lngLat);
    map.on("click", handleClick);
    return () => map.off("click", handleClick);
  }, [map, isLoaded]);

  return null;
}

// Usage
<Map center={[-74, 40.7]} zoom={10}>
  <MapEventListener />
</Map>
```

## Example: Custom Controls

This example shows how to create custom controls that manipulate the map's
pitch and bearing, and listen to map events to display real-time values. (See
`advanced-usage-example.tsx` in the repository.)

## Example: Custom GeoJSON Layer

Add custom GeoJSON data as layers with fill and outline styles. This example
shows NYC parks with hover interactions. (See `custom-layer-example.tsx`.)

## Example: Markers via Layers

When displaying hundreds or thousands of markers, use GeoJSON layers instead of
DOM-based `MapMarker` components. This approach renders markers on the WebGL
canvas, providing significantly better performance. (See `layer-markers-example.tsx`.)

## Extend to Build

You can extend this to build custom features like:

- **Real-time tracking** — Live location updates for delivery, rides, or fleet
  management
- **Geofencing** — Trigger actions when users enter or leave specific areas
- **Heatmaps** — Visualize density data like population, crime, or activity
  hotspots
- **Drawing tools** — Let users draw polygons, lines, or place markers for
  custom areas
- **3D buildings** — Extrude building footprints for urban visualization
- **Animations** — Animate markers along routes or create fly-through
  experiences
- **Custom data layers** — Overlay weather, traffic, or satellite imagery
