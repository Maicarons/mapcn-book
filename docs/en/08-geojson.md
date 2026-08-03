# GeoJSON

Render arbitrary GeoJSON as fill and outline layers for choropleths and region
maps.

Use `MapGeoJSON` to draw polygons, lines, and points from a GeoJSON source as
themed fill + outline layers.

## Basic GeoJSON

Point `data` at a GeoJSON URL and the layer renders with a theme-aware
monochrome fill and hairline outline out of the box, no styling required. Here
it loads a world map onto a `blank` map.

```tsx
import { Map, MapGeoJSON } from "@/registry/map";
import { WORLD_GEOJSON } from "@/lib/use-world-data";

export function GeoJSONExample() {
  return (
    <div className="bg-card h-[420px] w-full">
      <Map blank center={[10, 25]}>
        <MapGeoJSON data={WORLD_GEOJSON} linePaint={false} />
      </Map>
    </div>
  );
}
```

## Overlay on a Map

Overlay shapes and regions on a map — highlight an area, outline a zone, or
trace a boundary.

```tsx
import { Map, MapGeoJSON } from "@/registry/map";

const area: GeoJSON.FeatureCollection = {
  type: "FeatureCollection",
  features: [
    {
      type: "Feature",
      properties: {},
      geometry: {
        type: "Polygon",
        coordinates: [[
          [-122.42, 37.78], [-122.398, 37.785], [-122.392, 37.768],
          [-122.412, 37.758], [-122.43, 37.77], [-122.42, 37.78],
        ]],
      },
    },
  ],
};

export function MapOverlayExample() {
  return (
    <div className="h-[420px] w-full">
      <Map center={[-122.41, 37.772]} zoom={12}>
        <MapGeoJSON
          data={area}
          fillPaint={{ "fill-color": "#3b82f6", "fill-opacity": 0.25 }}
          linePaint={{ "line-color": "#2563eb", "line-width": 2 }}
        />
      </Map>
    </div>
  );
}
```
