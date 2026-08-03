# Controls

Add interactive controls to your map for zoom, compass, location, and
fullscreen.

The `MapControls` component provides a set of interactive controls that can be
positioned on any corner of the map.

```tsx
import { Map, MapControls } from "@/registry/map";

export function MapControlsExample() {
  return (
    <div className="h-[420px] w-full">
      <Map center={[2.3522, 48.8566]} zoom={10}>
        <MapControls
          position="top-right"
          showZoom
          showCompass
          showLocate
          showFullscreen
        />
      </Map>
    </div>
  );
}
```

## Props

| Prop | Type | Default | Description |
| --- | --- | --- | --- |
| `position` | `"top-left" \| "top-right" \| "bottom-left" \| "bottom-right"` | `"bottom-right"` | Position of the controls on the map. |
| `showZoom` | `boolean` | `true` | Show zoom in/out buttons. |
| `showCompass` | `boolean` | `false` | Show compass button to reset bearing. |
| `showLocate` | `boolean` | `false` | Show locate button to find user's location. |
| `showFullscreen` | `boolean` | `false` | Show fullscreen toggle button. |
| `className` | `string` | — | Additional CSS classes for the controls container. |
| `onLocate` | `(coords: { longitude: number; latitude: number }) => void` | — | Callback with user coordinates when located. |
