# Installation

How to install and set up mapcn in your project.

## Prerequisites

A project with [Tailwind CSS](https://tailwindcss.com) and
[shadcn/ui](https://ui.shadcn.com) set up.

## Installation

Run the following command to add the map component:

```bash
npx shadcn@latest add https://mapcn.dev/r/map.json
```

This will install `maplibre-gl` and add the map component to your project
(typically at `components/ui/map.tsx`).

> **Note:** The shadcn CLI copies the component source into your repository so
> you fully own it. No runtime dependency beyond `maplibre-gl` and React is
> required.

## Usage

Import and use the map component:

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

> **Note:** The map uses free CARTO basemap tiles by default. Tiles
> automatically switch between light and dark themes.
