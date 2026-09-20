# Voyage Locations — Split Update Batches

The canonical `Locations` file remains unchanged. These files divide only its 57 Demi-Plane location updates into smaller state edits so Voyage does not exceed its embedding-update limit.

## Apply each batch

Apply the files in numeric order, one completed state edit at a time.

For every batch:

1. Open the JSON file.
2. Merge its top-level entries into the existing `Locations` object by exact location name.
3. Replace only the listed location entries.
4. Preserve every location not listed in that batch.
5. Save and finish that state edit before applying the next file.
6. Do not replace the full `Locations` object with a batch.

Each batch is idempotent: applying it again writes the same location values and does not create duplicates.

| Batch | File | Locations | Regions |
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

After batch 11, all 57 Demi-Plane location updates exactly match the canonical `Locations` file. No Aerfála location is included in these batches.
