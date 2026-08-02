# Introduction

**mapcn** provides beautifully designed, accessible, and customizable map
components. Built on [MapLibre GL](https://maplibre.org), styled with
[Tailwind CSS](https://tailwindcss.com), and designed to work with
[shadcn/ui](https://ui.shadcn.com).

## Philosophy

mapcn follows the shadcn model for maps: copy-paste components you can own,
with zero lock-in and sensible defaults that work immediately.

Maps are often treated as black boxes hidden behind wrapper libraries and
configuration-heavy SDKs. mapcn takes a different approach. It stays close to
MapLibre, keeps the API familiar, and lets you drop down to the raw map
instance whenever you need more control.

The goal is simple: make maps feel like the rest of your UI stack — composable,
themeable, accessible, and easy to customize with Tailwind and shadcn patterns.

## Why mapcn?

Most React map setups are either too opinionated or too heavy. mapcn is built
for teams that want to ship quickly without giving up control:

- **Own Your Code:** Copy the components into your project and customize
  everything.
- **Start Fast:** Run one command and render your first map with
  production-ready defaults.
- **Scale Safely:** Build on top of MapLibre directly, then drop to raw APIs
  when needed.
- **Design-System Friendly:** Styled with Tailwind and made to fit naturally
  with shadcn/ui patterns.

## Any Map Style

mapcn works with any [MapLibre-compatible tiles](https://maplibre.org/maplibre-style-spec/).
This means you can use tiles from virtually any provider:

- [OpenStreetMap](https://www.openstreetmap.org) — Community-driven, open-source
  map data
- [Carto](https://carto.com/basemaps) — Clean, minimal basemaps perfect for
  data visualization
- [MapTiler](https://www.maptiler.com) — Beautiful vector tiles with extensive
  customization options
- [Stadia Maps](https://stadiamaps.com) — Fast, reliable tile hosting with
  multiple styles
- [Thunderforest](https://www.thunderforest.com) — Specialized maps for
  outdoors, cycling, and transport
- And any other provider that supports the MapLibre style spec

## Features

- **Zero Config** — Works out of the box with free map tiles. No API keys
  needed.
- **Theme Aware** — Automatically switches between light and dark map styles.
- **Composable** — Build complex UIs with simple, composable components.
- **TypeScript** — Full type safety with comprehensive TypeScript support.
- **Copy & Paste** — Own your code. No dependencies, just copy into your
  project.
- **Any Map Style** — Use any MapLibre-compatible tiles: MapTiler, Carto,
  OpenStreetMap, and more.
