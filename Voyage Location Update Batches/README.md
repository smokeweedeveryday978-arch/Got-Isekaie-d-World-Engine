# Voyage Locations — Cumulative Full-State Checkpoints

These are complete, valid `Locations` files created to avoid Voyage's per-edit embedding limit. Every checkpoint contains all 165 locations. Nothing needs to be merged, interpreted, appended, or reconstructed by the AI.

## Exact application process

1. Open `01-heartgate-basin.json`.
2. Replace the complete contents of Voyage's `Locations` section with that file.
3. Save and wait for the state edit to finish successfully.
4. Repeat with files 02 through 11 in numerical order.
5. Never combine checkpoints or submit more than one in the same edit.

Each checkpoint already includes every change from the preceding checkpoints. Voyage therefore sees only the 4–7 newly changed location entries at each step while still receiving a complete 165-location state.

If an earlier attempt partially succeeded, applying the checkpoints from 01 remains safe: matching entries stay identical, absent progress is restored, and no duplicate locations are created.

| Checkpoint | File | New changes from preceding state | Regions completed |
|---:|---|---:|---|
| 01 | `01-heartgate-basin.json` | 5 | Heartgate Basin |
| 02 | `02-veiled-fox-sanctuary.json` | 4 | Veiled Fox Sanctuary |
| 03 | `03-first-meadow-and-threshold-march.json` | 5 | The First Meadow, The Threshold March |
| 04 | `04-stone-rise-and-mirror-mere.json` | 5 | The Stone Rise, The Mirror Mere |
| 05 | `05-still-frontier-and-pale-reaches.json` | 4 | The Still Frontier, The Pale Reaches |
| 06 | `06-north-field-fold-and-veiled-edge.json` | 6 | The North Field, The Fold, The Veiled Edge |
| 07 | `07-dim-grey-and-open-horizon.json` | 5 | The Dim March, The Grey Boundary, The Open Horizon |
| 08 | `08-fade-and-last-edge.json` | 4 | The Fade, The Last Edge |
| 09 | `09-low-reaches-hollow-vale-and-deep-expanse.json` | 6 | The Low Reaches, The Hollow Vale, The Deep Expanse |
| 10 | `10-southroll-rift-march-and-quiet-shore.json` | 6 | The Southroll, The Rift March, The Quiet Shore |
| 11 | `11-westreach-dawn-barrow-and-easthold.json` | 7 | The Westreach, The Dawn Barrow, The Easthold |

Checkpoint 11 is exactly identical to the canonical `Locations` file on `main`. These checkpoints update only the 57 Demi-Plane locations. Aerfála locations remain identical throughout.
