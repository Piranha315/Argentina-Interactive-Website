#!/usr/bin/env bash
# Downloads the Natural Earth layers that scripts/geo.py projects into data/geo.json (about 45 MB, not committed).
set -euo pipefail
cd "$(dirname "$0")/../data/raw" && mkdir -p naturalearth && cd naturalearth
base=https://raw.githubusercontent.com/nvkelso/natural-earth-vector/master/geojson
for f in ne_50m_admin_0_countries ne_10m_admin_1_states_provinces ne_50m_rivers_lake_centerlines ne_50m_lakes; do
  curl -sSL -o "$f.geojson" "$base/$f.geojson" && echo "fetched $f"
done
