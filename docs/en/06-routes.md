# Routes

Draw lines and paths connecting coordinates on the map.

Use `MapRoute` to draw lines connecting a series of coordinates. Perfect for
showing directions, trails, or any path between points.

## Basic Route

Draw a route with numbered stop markers along the path.

```tsx
import {
  Map,
  MapMarker,
  MarkerContent,
  MarkerTooltip,
  MapRoute,
} from "@/registry/map";

const route = [
  [-74.006, 40.7128],
  [-73.9857, 40.7484],
  [-73.9772, 40.7527],
  [-73.9654, 40.7829],
] as [number, number][];

const stops = [
  { name: "City Hall", lng: -74.006, lat: 40.7128 },
  { name: "Empire State Building", lng: -73.9857, lat: 40.7484 },
  { name: "Grand Central Terminal", lng: -73.9772, lat: 40.7527 },
  { name: "Central Park", lng: -73.9654, lat: 40.7829 },
];

export function RouteExample() {
  return (
    <div className="h-[420px] w-full">
      <Map center={[-73.98, 40.75]} zoom={11.2}>
        <MapRoute coordinates={route} color="#3b82f6" width={4} opacity={0.8} />
        {stops.map((stop, index) => (
          <MapMarker key={stop.name} longitude={stop.lng} latitude={stop.lat}>
            <MarkerContent>
              <div className="flex size-4.5 items-center justify-center rounded-full border-2 border-white bg-blue-500 text-xs font-semibold text-white shadow-lg">
                {index + 1}
              </div>
            </MarkerContent>
            <MarkerTooltip>{stop.name}</MarkerTooltip>
          </MapMarker>
        ))}
      </Map>
    </div>
  );
}
```

## Route Planning

Display multiple route options and let users select between them. This example
fetches real driving directions from the [OSRM API](https://project-osrm.org/).
Click on a route or use the buttons to switch.

```tsx
"use client";

import { useEffect, useState } from "react";
import { Map, MapMarker, MarkerContent, MapRoute, MarkerLabel } from "@/registry/map";

const start = { name: "Amsterdam", lng: 4.9041, lat: 52.3676 };
const end = { name: "Rotterdam", lng: 4.4777, lat: 51.9244 };

export function OsrmRouteExample() {
  const [routes, setRoutes] = useState<[number, number][][]>([]);
  const [selected, setSelected] = useState(0);

  useEffect(() => {
    fetch(
      `https://router.project-osrm.org/route/v1/driving/${start.lng},${start.lat};${end.lng},${end.lat}?overview=full&geometries=geojson&alternatives=true`
    )
      .then((r) => r.json())
      .then((data) => {
        if (data.routes?.length > 0) {
          setRoutes(data.routes.map((r: any) => r.geometry.coordinates));
        }
      });
  }, []);

  return (
    <div className="h-[500px] w-full">
      <Map center={[4.69, 52.14]} zoom={8.5}>
        {routes.map((coords, i) => (
          <MapRoute
            key={i}
            coordinates={coords}
            color={i === selected ? "#6366f1" : "#94a3b8"}
            width={i === selected ? 6 : 5}
            onClick={() => setSelected(i)}
          />
        ))}
        <MapMarker longitude={start.lng} latitude={start.lat}>
          <MarkerContent>
            <div className="size-5 rounded-full bg-green-500 border-2 border-white shadow-lg" />
            <MarkerLabel position="top">{start.name}</MarkerLabel>
          </MarkerContent>
        </MapMarker>
        <MapMarker longitude={end.lng} latitude={end.lat}>
          <MarkerContent>
            <div className="size-5 rounded-full bg-red-500 border-2 border-white shadow-lg" />
            <MarkerLabel position="bottom">{end.name}</MarkerLabel>
          </MarkerContent>
        </MapMarker>
      </Map>
    </div>
  );
}
```
