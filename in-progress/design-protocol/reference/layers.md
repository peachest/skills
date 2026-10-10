# The 7 layers

Bottom-up. Each layer: what it decides, required fields (mirrored by the JSON Schemas in `schemas/`), and a worked example. Build only the layers the project needs; L1 + L2 are the minimum.

## L1 Token — semantic atoms (W3C DTCG)

Decides: the closed set of values. The AI never invents "12px vs 16px" — the token table answers.

```json
{
  "spacing": {
    "sm": {"$type": "dimension", "$value": "8px"},
    "md": {"$type": "dimension", "$value": "16px"}
  },
  "color": {
    "primary": {"$type": "color", "$value": "#3B82F6"},
    "primary-hover": {"$type": "color", "$value": "#2563EB"}
  }
}
```

Naming: primitive (blue-500) vs semantic (color-primary) — semantic is what consumers use. Token values are edited here only.

## L2 Component — behavior contract

Decides: what exists and what it may do. Variants are a closed set; constraints are explicit.

```json
{
  "name": "button", "category": "interaction",
  "variants": ["default", "secondary", "destructive", "ghost"],
  "props": {
    "size": {"type": "enum", "values": ["sm", "md", "lg"], "default": "md"},
    "disabled": {"type": "boolean", "default": false}
  },
  "constraints": {"max_label_length": 20, "min_touch_target": "44px"}
}
```

One file per component in `components/`. If the codebase has a component the protocol omits, extract it — the protocol mirrors reality, not aspiration.

## L3 Direction — design intent

Decides: what "tech-feeling" or "friendly" means as a constraint set, so style words stop being vibes.

```yaml
name: tech-future
mood: professional, innovative, clean
color_strategy: primary dominant, gradient accents
density: comfortable
motion: subtle, purposeful
```

## L4 Scene — direction × business context

Decides: how one direction behaves differently per context (dashboard vs landing page).

```yaml
name: data-dashboard
direction: tech-future
density_override: compact
layout_pattern: grid-12
component_preferences:
  data_display: [chart, metric-card, data-table]
```

## L5 Page — section composition

Decides: page structure once, so the AI stops re-inventing it per generation.

```yaml
name: landing-page
scene: marketing-showcase
sections:
  - {type: hero, required: true, position: first}
  - {type: features, required: true, max_items: 6}
  - {type: cta, required: true, position: last}
```

## L6 Exhibition — display context

Decides: viewport and interaction modality (web vs car screen, portrait vs landscape).

```yaml
name: desktop-web
medium: web
orientation: any
viewport: >=1280px
interaction_modalities: [pointer, keyboard]
```

## L7 Template — bundled decisions

Decides: a named, reusable bundle of L1–L6 file references. The AI personalizes inside a template instead of choosing layers fresh.

```yaml
name: saas-starter
includes:
  tokens: tokens.json
  components: components/
  direction: direction.json
  scene: scene.json
```

## Cross-layer references

Scene→Direction, Page→Scene, Template→everything are by name. `validate.py` checks schema shape; it does not chase cross-file names — when adding an entry, confirm the referenced layer entry exists (a dangling reference fails at Consume time, which is the expensive place to find it).
