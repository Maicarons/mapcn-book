# API Reference

Complete reference for all map components and their props.

> **Note:** This library is built on top of
> [MapLibre GL JS](https://maplibre.org/maplibre-gl-js/docs/API/). Most
> components extend the native MapLibre options. Refer to the
> [MapLibre Map API](https://maplibre.org/maplibre-gl-js/docs/API/classes/Map/)
> for additional options not listed here.

## Component Anatomy

All parts of the component that you can use and combine to build your map.

```tsx
<Map>
  <MapMarker longitude={...} latitude={...}>
    <MarkerContent>
      <MarkerLabel />
    </MarkerContent>
    <MarkerPopup />
    <MarkerTooltip />
  </MapMarker>

  <MapPopup longitude={...} latitude={...} />
  <MapControls />
  <MapRoute coordinates={...} />
  <MapArc data={...} />
  <MapGeoJSON data={...} />
  <MapClusterLayer data={...} />
</Map>
```

## Map

The root container component that initializes MapLibre GL and provides context
to child components. Automatically handles theme switching between light and
dark modes.

Extends [MapOptions](https://maplibre.org/maplibre-gl-js/docs/API/type-aliases/MapOptions/)
from MapLibre GL (excluding `container` and `style`).

| Prop | Type | Default | Description |
| --- | --- | --- | --- |
| `children` | `ReactNode` | — | Child components (markers, popups, controls, routes). |
| `className` | `string` | — | Additional CSS classes for the map container. |
| `theme` | `"light" \| "dark"` | — | Theme for the map. If not provided, automatically detects from document class or system preference. |
| `styles` | `{ light?: string \| StyleSpecification; dark?: string \| StyleSpecification }` | — | Custom map styles for light and dark themes. Overrides the default Carto base map tiles. |
| `blank` | `boolean` | `false` | Use a transparent, tile-less basemap instead of the default Carto street basemap. Ignored when an explicit `styles` prop is provided. |
| `projection` | `ProjectionSpecification` | — | Map projection type. Use `{ type: "globe" }` for 3D globe view. |
| `viewport` | `Partial<MapViewport>` | — | Controlled viewport state. Can also be used alone for initial viewport. |
| `onViewportChange` | `(viewport: MapViewport) => void` | — | Callback fired continuously as the viewport changes. |
| `loading` | `boolean` | `false` | Show a loading indicator on the map. |

## useMap

A hook that provides access to the MapLibre map instance and loading state.
Must be used within a `Map` component.

```tsx
const { map, isLoaded } = useMap();
```

Returns `map` ([MapLibre.Map](https://maplibre.org/maplibre-gl-js/docs/API/classes/Map/))
and `isLoaded` (boolean) telling you if the map is loaded and ready to use.

## MapControls

Renders map control buttons (zoom, compass, locate, fullscreen). Must be used
inside `Map`.

| Prop | Type | Default | Description |
| --- | --- | --- | --- |
| `position` | `"top-left" \| "top-right" \| "bottom-left" \| "bottom-right"` | `"bottom-right"` | Position of the controls on the map. |
| `showZoom` | `boolean` | `true` | Show zoom in/out buttons. |
| `showCompass` | `boolean` | `false` | Show compass button to reset bearing. |
| `showLocate` | `boolean` | `false` | Show locate button to find user's location. |
| `showFullscreen` | `boolean` | `false` | Show fullscreen toggle button. |
| `className` | `string` | — | Additional CSS classes for the controls container. |
| `onLocate` | `(coords: { longitude: number; latitude: number }) => void` | — | Callback with user coordinates when located. |

## MapMarker

A container for marker-related components. Provides context for its children
and handles marker positioning.

Extends [MarkerOptions](https://maplibre.org/maplibre-gl-js/docs/API/type-aliases/MarkerOptions/)
from MapLibre GL (excluding `element`).

| Prop | Type | Description |
| --- | --- | --- |
| `longitude` | `number` | Longitude coordinate for marker position. |
| `latitude` | `number` | Latitude coordinate for marker position. |
| `children` | `ReactNode` | Marker subcomponents (MarkerContent, MarkerPopup, etc). |
| `onClick` | `(e: MouseEvent) => void` | Callback when marker is clicked. |
| `onMouseEnter` | `(e: MouseEvent) => void` | Callback when mouse enters marker. |
| `onMouseLeave` | `(e: MouseEvent) => void` | Callback when mouse leaves marker. |
| `onDragStart` | `(lngLat: { lng, lat }) => void` | Callback when marker drag starts (requires `draggable: true`). |
| `onDrag` | `(lngLat: { lng, lat }) => void` | Callback during marker drag (requires `draggable: true`). |
| `onDragEnd` | `(lngLat: { lng, lat }) => void` | Callback when marker drag ends (requires `draggable: true`). |

## MarkerContent

Renders the visual content of a marker. Must be used inside `MapMarker`. If no
children provided, renders a default blue dot marker.

| Prop | Type | Description |
| --- | --- | --- |
| `children` | `ReactNode` | Custom marker content. Defaults to a blue dot. |
| `className` | `string` | Additional CSS classes for the marker container. |

## MarkerPopup

Renders a popup attached to the marker that opens on click. Must be used inside
`MapMarker`.

Extends [PopupOptions](https://maplibre.org/maplibre-gl-js/docs/API/type-aliases/PopupOptions/)
from MapLibre GL (excluding `className` and `closeButton`).

| Prop | Type | Default | Description |
| --- | --- | --- | --- |
| `children` | `ReactNode` | — | Popup content. |
| `className` | `string` | — | Additional CSS classes for the popup container. |
| `closeButton` | `boolean` | `false` | Show a close button in the popup. |

## MarkerTooltip

Renders a tooltip that appears on hover. Must be used inside `MapMarker`.

Extends [PopupOptions](https://maplibre.org/maplibre-gl-js/docs/API/type-aliases/PopupOptions/)
from MapLibre GL (excluding `className`, `closeButton`, and `closeOnClick`).

| Prop | Type | Description |
| --- | --- | --- |
| `children` | `ReactNode` | Tooltip content. |
| `className` | `string` | Additional CSS classes for the tooltip container. |

## MarkerLabel

Renders a text label above or below the marker. Must be used inside
`MarkerContent`.

| Prop | Type | Default | Description |
| --- | --- | --- | --- |
| `children` | `ReactNode` | — | Label text content. |
| `className` | `string` | — | Additional CSS classes for the label. |
| `position` | `"top" \| "bottom"` | `"top"` | Position of the label relative to the marker. |

## MapPopup

A standalone popup component that can be placed anywhere on the map without a
marker. Must be used inside `Map`.

Extends [PopupOptions](https://maplibre.org/maplibre-gl-js/docs/API/type-aliases/PopupOptions/)
from MapLibre GL (excluding `className` and `closeButton`).

| Prop | Type | Default | Description |
| --- | --- | --- | --- |
| `longitude` | `number` | — | Longitude coordinate for popup position. |
| `latitude` | `number` | — | Latitude coordinate for popup position. |
| `onClose` | `() => void` | — | Callback when popup is closed. |
| `children` | `ReactNode` | — | Popup content. |
| `className` | `string` | — | Additional CSS classes for the popup container. |
| `closeButton` | `boolean` | `false` | Show a close button in the popup. |

## MapRoute

Renders a line/route on the map connecting coordinate points. Must be used
inside `Map`. Supports click and hover interactions for building route
selection UIs.

| Prop | Type | Default | Description |
| --- | --- | --- | --- |
| `id` | `string` | auto-generated | Optional unique identifier for the route layer. |
| `coordinates` | `[number, number][]` | — | Array of `[longitude, latitude]` coordinate pairs. |
| `color` | `string` | `"#4285F4"` | Line color (CSS color value). |
| `width` | `number` | `3` | Line width in pixels. |
| `opacity` | `number` | `0.8` | Line opacity (0 to 1). |
| `dashArray` | `[number, number]` | — | Dash pattern `[dash length, gap length]` for dashed lines. |
| `onClick` | `() => void` | — | Callback when the route line is clicked. |
| `onMouseEnter` | `() => void` | — | Callback when mouse enters the route line. |
| `onMouseLeave` | `() => void` | — | Callback when mouse leaves the route line. |
| `interactive` | `boolean` | `false` | Respond to mouse events (hover, cursor, callbacks). |

## MapArc

Renders curved lines between coordinate pairs using a quadratic Bézier in
longitude/latitude space. Must be used inside `Map`. Supports click and hover
interactions.

Built on a MapLibre [line layer](https://maplibre.org/maplibre-style-spec/layers/#line)
— the `paint` and `layout` props accept any field from
`LineLayerSpecification`. Style per arc by passing a
[MapLibre expression](https://maplibre.org/maplibre-style-spec/expressions/)
as any paint value.

| Prop | Type | Default | Description |
| --- | --- | --- | --- |
| `data` | `MapArcDatum[]` | — | Arcs to render. Each needs a unique `id` and `from` / `to` as `[lng, lat]`. |
| `id` | `string` | auto | Id prefix for the underlying source/layers. |
| `curvature` | `number` | `0.2` | How far the arc bows away from a straight line. |
| `samples` | `number` | `64` | Points per arc. Higher = smoother. |
| `paint` | `LineLayerSpecification['paint']` | `{ "line-color": "#4285F4", "line-width": 2, "line-opacity": 0.85 }` | Paint props merged over defaults. |
| `layout` | `LineLayerSpecification['layout']` | `{ "line-join": "round", "line-cap": "round" }` | Layout props merged over defaults. |
| `hoverPaint` | `LineLayerSpecification['paint']` | — | Paint overrides applied to the hovered arc via feature-state. |
| `onClick` | `(e: MapArcEvent) => void` | — | Fired when an arc is clicked. |
| `onHover` | `(e: MapArcEvent \| null) => void` | — | Fired when the hovered arc changes. |
| `interactive` | `boolean` | `true` | Respond to mouse events. |
| `beforeId` | `string` | — | Insert the arc layers before this layer id. |

## MapGeoJSON

Renders arbitrary GeoJSON as fill + outline layers. Must be used inside `Map` —
typically with the `blank` prop for choropleths and region/data maps. Accepts a
`FeatureCollection`, `Feature`, `Geometry`, or a URL string to fetch from.
Supports a generic type parameter for typed feature properties:
`MapGeoJSON<MyProperties>`.

| Prop | Type | Description |
| --- | --- | --- |
| `data` | `FeatureCollection \| Feature \| Geometry \| string` | GeoJSON data or a URL string to fetch it from. |
| `id` | `string` | Id prefix for the underlying source/layers. |
| `promoteId` | `string` | Feature property to promote to the feature id. Required for hover feature-state. |
| `fillPaint` | `FillLayerSpecification['paint'] \| false` | Paint for the polygon fill layer. Pass `false` to omit the fill layer. |
| `linePaint` | `LineLayerSpecification['paint'] \| false` | Paint for the outline layer. Pass `false` to omit the outline layer. |
| `fillHoverPaint` | `FillLayerSpecification['paint']` | Paint merged onto the fill layer for the hovered feature. Requires `promoteId`. |
| `onClick` | `(e: MapGeoJSONEvent) => void` | Fired when a feature is clicked. |
| `onHover` | `(e: MapGeoJSONEvent \| null) => void` | Fired when the hovered feature changes. |
| `interactive` | `boolean` | Respond to mouse events (default `false`). |
| `beforeId` | `string` | Insert the layers before this layer id. |

## MapClusterLayer

Renders clustered point data using MapLibre GL's native clustering. Must be used
inside `Map`. Supports a generic type parameter: `MapClusterLayer<MyProperties>`.

| Prop | Type | Default | Description |
| --- | --- | --- | --- |
| `data` | `string \| GeoJSON.FeatureCollection` | — | GeoJSON FeatureCollection data or URL to fetch GeoJSON from. |
| `clusterMaxZoom` | `number` | `14` | Maximum zoom level to cluster points on. |
| `clusterRadius` | `number` | `50` | Radius of each cluster when clustering points (in pixels). |
| `clusterColors` | `[string, string, string]` | `["#3b82f6", "#1d4ed8", "#1e3a8a"]` | Colors for cluster circles: `[small, medium, large]`. |
| `clusterThresholds` | `[number, number]` | `[100, 750]` | Point count thresholds for color/size steps. |
| `pointColor` | `string` | `"#3b82f6"` | Color for unclustered individual points. |
| `onPointClick` | `(feature, coordinates) => void` | — | Callback when an unclustered point is clicked. |
| `onClusterClick` | `(clusterId, coordinates, pointCount) => void` | — | Callback when a cluster is clicked. If not provided, zooms into the cluster. |
