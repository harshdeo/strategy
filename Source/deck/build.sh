#!/bin/zsh
# Rebuild the seed and partner masters from operating_model.py and the frozen snapshots in Source/.
# Needs: pptxgenjs (NODE_MODULES_DIR) and python-pptx (PY_LIBS). Writes candidates next to this script.
set -e
cd "$(dirname "$0")"
: ${NODE_MODULES_DIR:?set NODE_MODULES_DIR to a folder containing pptxgenjs}
: ${PY_LIBS:?set PY_LIBS to a folder containing python-pptx}
/opt/homebrew/bin/python3 ../../Financial_Models/operating_model.py --json > model.json
export NODE_PATH=$NODE_MODULES_DIR
node seed.js seed.pptx
[ -f partner.js ] && node partner.js partner.pptx
PYTHONPATH=$PY_LIBS /opt/homebrew/bin/python3 finish_deck.py seed.pptx
[ -f partner.pptx ] && PYTHONPATH=$PY_LIBS /opt/homebrew/bin/python3 finish_deck.py partner.pptx
