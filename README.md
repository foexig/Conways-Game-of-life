# Conway's Game of Life

A small interactive version of [Conway's Game of Life](https://en.wikipedia.org/wiki/Conway%27s_Game_of_Life), written in Python with pygame.

Draw cells by hand or stamp classic patterns (glider, Gosper glider gun, ...), then watch them evolve. The grid wraps around at the edges, so patterns that leave one side come back on the other.

## Rules

Every step, each cell looks at its 8 neighbours:

- A live cell with 2 or 3 live neighbours survives.
- A dead cell with exactly 3 live neighbours comes alive.
- Every other cell dies or stays dead.

## Run it

Requires Python 3 and pygame.

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python main.py
```

## Controls

**Menu**

| Key | Action |
|---|---|
| `Tab` | Start the game |
| `O` | Options |

**Options**

| Key | Action |
|---|---|
| `↑` / `↓` | Step interval +/- 10 ms (lower = faster) |
| `Tab` | Start the game |
| `Backspace` | Back to the menu |

**Game**

| Input | Action |
|---|---|
| `Space` | Start / pause the simulation |
| `U` | Advance a single step |
| `R` | Clear the grid |
| Left click | Toggle a cell (pauses the simulation) |
| `S` | Toggle stamp mode (shows a preview under the mouse) |
| `1`–`4` | Pick a stamp: glider, arch, Gosper glider gun, block |
| Mouse wheel | Rotate the stamp |
| Left click (stamp mode) | Place the stamp |

## Project layout

```
main.py           the game
fonts/            DS-Digital font + its license (DIGITAL.TXT)
requirements.txt  Python dependencies
```

The earlier prototypes (pixel version, grid version, level mode) are kept on the `original` branch and the `v0-original` tag.

## Credits

Font: DS-Digital by Dusit Supasawat, see `fonts/DIGITAL.TXT`.
