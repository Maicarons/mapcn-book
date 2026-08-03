# Markers

Add interactive markers to your map with popups and tooltips.

Use `MapMarker` to place markers on the map. Each marker can have custom
content, popups that open on click, and tooltips that appear on hover.

> **Performance tip:** `MapMarker` is DOM-based and works best for a few hundred
> markers. For larger datasets, see the
> [GeoJSON layers example](./10-advanced-usage.md) instead. Rendering many DOM
> markers can make the browser sluggish.

## Basic Example

Simple markers with tooltips and popups showing location information.

```tsx
import {
  Map,
  MapMarker,
  MarkerContent,
  MarkerPopup,
  MarkerTooltip,
} from "@/registry/map";

const locations = [
  { id: 1, name: "Empire State Building", lng: -73.9857, lat: 40.7484 },
  { id: 2, name: "Central Park", lng: -73.9654, lat: 40.7829 },
  { id: 3, name: "Times Square", lng: -73.9855, lat: 40.758 },
];

export function MarkersExample() {
  return (
    <div className="h-[420px] w-full">
      <Map center={[-73.98, 40.76]} zoom={12}>
        {locations.map((location) => (
          <MapMarker
            key={location.id}
            longitude={location.lng}
            latitude={location.lat}
          >
            <MarkerContent>
              <div className="bg-primary size-4 rounded-full border-2 border-white shadow-lg" />
            </MarkerContent>
            <MarkerTooltip>{location.name}</MarkerTooltip>
            <MarkerPopup>
              <div className="space-y-1">
                <p className="text-foreground font-medium">{location.name}</p>
                <p className="text-muted-foreground text-xs">
                  {location.lat.toFixed(4)}, {location.lng.toFixed(4)}
                </p>
              </div>
            </MarkerPopup>
          </MapMarker>
        ))}
      </Map>
    </div>
  );
}
```

## Rich Popups

Build complex popups with images, ratings, and action buttons using shadcn/ui
components. (See the `popup-example` in the repository for the full rich
popup markup.)

## Draggable Marker

Create draggable markers that users can move around the map. Click the marker to
see its current coordinates in a popup.

```tsx
"use client";

import { useState } from "react";
import { Map, MapMarker, MarkerContent, MarkerPopup } from "@/registry/map";

export function DraggableMarkerExample() {
  const [pos, setPos] = useState({ lng: -73.98, lat: 40.75 });

  return (
    <div className="h-[420px] w-full">
      <Map center={[-73.98, 40.75]} zoom={12}>
        <MapMarker
          draggable
          longitude={pos.lng}
          latitude={pos.lat}
          onDrag={(lngLat) => setPos({ lng: lngLat.lng, lat: lngLat.lat })}
        >
          <MarkerContent>
            <div className="cursor-move">📍</div>
          </MarkerContent>
          <MarkerPopup>
            <p className="text-muted-foreground text-xs tabular-nums">
              {pos.lat.toFixed(4)}, {pos.lng.toFixed(4)}
            </p>
          </MarkerPopup>
        </MapMarker>
      </Map>
    </div>
  );
}
```
