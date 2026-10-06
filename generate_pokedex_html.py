#!/usr/bin/env python3
"""
Pokemon Emerald Expansion - Game Encyclopedia Generator
Parses game source data (species info, level-up learnsets, trainer parties, wild encounters)
and compiles a modern, responsive, searchable, single-file HTML game encyclopedia.
"""

import json
import os
import re
import sys
from pathlib import Path

# Paths relative to repository root
BASE_DIR = Path(__file__).resolve().parent
SPECIES_DIR = BASE_DIR / "src" / "data" / "pokemon" / "species_info"
LEARNSETS_DIR = BASE_DIR / "src" / "data" / "pokemon" / "level_up_learnsets"
TRAINERS_PARTY_FILE = BASE_DIR / "src" / "data" / "trainers.party"
WILD_ENCOUNTERS_FILE = BASE_DIR / "src" / "data" / "wild_encounters.json"
OUTPUT_HTML = BASE_DIR / "game_encyclopedia.html"

def clean_name(raw: str) -> str:
    """Format constant or macro string into clean display title (e.g. MOVE_VINE_WHIP -> Vine Whip)."""
    if not raw:
        return ""
    # Strip common prefixes
    for prefix in ["SPECIES_", "MOVE_", "ABILITY_", "TYPE_", "ITEM_", "MAP_"]:
        if raw.startswith(prefix):
            raw = raw[len(prefix):]
    # Handle underscores and capitalization
    parts = raw.split('_')
    return ' '.join(word.capitalize() for word in parts)

def parse_learnsets():
    """Parse all level-up learnset files (gen_1.h - gen_9.h)."""
    learnsets = {}
    if not LEARNSETS_DIR.exists():
        print(f"Warning: Learnsets directory not found at {LEARNSETS_DIR}")
        return learnsets

    learnset_regex = re.compile(r'static\s+const\s+struct\s+LevelUpMove\s+(\w+LevelUpLearnset)\[\]\s*=\s*\{([^}]+)\};', re.DOTALL)
    move_regex = re.compile(r'LEVEL_UP_MOVE\(\s*(\d+)\s*,\s*(MOVE_\w+)\)')

    for gen_file in sorted(LEARNSETS_DIR.glob("gen_*.h")):
        try:
            content = gen_file.read_text(encoding='utf-8', errors='ignore')
            for match in learnset_regex.finditer(content):
                learnset_name = match.group(1)
                moves_block = match.group(2)
                moves = []
                for move_match in move_regex.finditer(moves_block):
                    lvl = int(move_match.group(1))
                    move_id = move_match.group(2)
                    moves.append({
                        "level": lvl,
                        "move_id": move_id,
                        "move": clean_name(move_id)
                    })
                learnsets[learnset_name] = moves
        except Exception as e:
            print(f"Error parsing learnset file {gen_file.name}: {e}")

    print(f"Parsed {len(learnsets)} level-up learnsets.")
    return learnsets

def parse_species(learnsets):
    """Parse all species info files (gen_1_families.h - gen_9_families.h)."""
    species_list = []
    if not SPECIES_DIR.exists():
        print(f"Warning: Species directory not found at {SPECIES_DIR}")
        return species_list

    # Regex for species block: [SPECIES_XXX] = { ... }
    entry_regex = re.compile(r'\[(SPECIES_\w+)\]\s*=\s*\{(.*?)\n\s*\},', re.DOTALL)

    for gen_idx in range(1, 10):
        gen_file = SPECIES_DIR / f"gen_{gen_idx}_families.h"
        if not gen_file.exists():
            continue
        try:
            content = gen_file.read_text(encoding='utf-8', errors='ignore')
            for match in entry_regex.finditer(content):
                species_id = match.group(1)
                body = match.group(2)

                # Skip SPECIES_NONE or placeholder species
                if species_id in ("SPECIES_NONE", "SPECIES_EGG"):
                    continue

                # Species Name
                name_match = re.search(r'\.speciesName\s*=\s*_\("([^"]+)"\)', body)
                name = name_match.group(1) if name_match else clean_name(species_id)

                # Nat Dex Num
                dex_match = re.search(r'\.natDexNum\s*=\s*NATIONAL_DEX_(\w+)', body)
                dex_num_str = dex_match.group(1) if dex_match else str(len(species_list) + 1)

                # Category / Height / Weight
                cat_match = re.search(r'\.categoryName\s*=\s*_\("([^"]+)"\)', body)
                category = cat_match.group(1) if cat_match else "Pokémon"

                height_match = re.search(r'\.height\s*=\s*(\d+)', body)
                height = int(height_match.group(1)) if height_match else 0  # in decimeters (0.1m)

                weight_match = re.search(r'\.weight\s*=\s*(\d+)', body)
                weight = int(weight_match.group(1)) if weight_match else 0  # in hectograms (0.1kg)

                # Description
                desc_match = re.search(r'\.description\s*=\s*(?:COMPOUND_STRING\(|_\()?"(.*?)"\)?', body, re.DOTALL)
                description = desc_match.group(1).replace('\\n', ' ').replace('\n', ' ').replace('"', '') if desc_match else ""

                # Stats
                hp = int(m.group(1)) if (m := re.search(r'\.baseHP\s*=\s*(\d+)', body)) else 0
                atk = int(m.group(1)) if (m := re.search(r'\.baseAttack\s*=\s*(\d+)', body)) else 0
                defe = int(m.group(1)) if (m := re.search(r'\.baseDefense\s*=\s*(\d+)', body)) else 0
                speed = int(m.group(1)) if (m := re.search(r'\.baseSpeed\s*=\s*(\d+)', body)) else 0
                spatk = int(m.group(1)) if (m := re.search(r'\.baseSpAttack\s*=\s*(\d+)', body)) else 0
                spdef = int(m.group(1)) if (m := re.search(r'\.baseSpDefense\s*=\s*(\d+)', body)) else 0
                bst = hp + atk + defe + speed + spatk + spdef

                # Types: MON_TYPES(TYPE_GRASS, TYPE_POISON) or MON_TYPES(TYPE_FIRE)
                types = []
                type_match = re.search(r'\.types\s*=\s*MON_TYPES\(([^)]+)\)', body)
                if type_match:
                    type_tokens = [t.strip() for t in type_match.group(1).split(',')]
                    for t in type_tokens:
                        cleaned_t = clean_name(t)
                        if cleaned_t and cleaned_t not in types:
                            types.append(cleaned_t)
                if not types:
                    types = ["Normal"]

                # Abilities: .abilities = { ABILITY_OVERGROW, ABILITY_NONE, ABILITY_CHLOROPHYLL }
                abilities = []
                ab_match = re.search(r'\.abilities\s*=\s*\{([^}]+)\}', body)
                if ab_match:
                    ab_tokens = [a.strip() for a in ab_match.group(1).split(',')]
                    for a in ab_tokens:
                        if a and "ABILITY_NONE" not in a:
                            cleaned_ab = clean_name(a)
                            if cleaned_ab and cleaned_ab not in abilities:
                                abilities.append(cleaned_ab)

                # Learnset link
                learnset_key_match = re.search(r'\.levelUpLearnset\s*=\s*(\w+LevelUpLearnset)', body)
                learnset_key = learnset_key_match.group(1) if learnset_key_match else ""
                moves = learnsets.get(learnset_key, [])

                species_list.append({
                    "id": species_id,
                    "name": name,
                    "gen": gen_idx,
                    "dex": dex_num_str,
                    "types": types,
                    "category": category,
                    "height": height / 10.0, # meters
                    "weight": weight / 10.0, # kg
                    "stats": {
                        "hp": hp,
                        "atk": atk,
                        "def": defe,
                        "spa": spatk,
                        "spd": spdef,
                        "spe": speed,
                        "bst": bst
                    },
                    "abilities": abilities,
                    "description": description,
                    "moves": moves,
                    "encounters": []  # Will be populated from wild encounters
                })
        except Exception as e:
            print(f"Error parsing {gen_file.name}: {e}")

    print(f"Parsed {len(species_list)} Pokémon species.")
    return species_list

def parse_trainers():
    """Parse trainer parties from src/data/trainers.party."""
    trainers = []
    if not TRAINERS_PARTY_FILE.exists():
        print(f"Warning: Trainers party file not found at {TRAINERS_PARTY_FILE}")
        return trainers

    content = TRAINERS_PARTY_FILE.read_text(encoding='utf-8', errors='ignore')

    # Remove C style comment blocks
    content = re.sub(r'/\*.*?\*/', '', content, flags=re.DOTALL)

    # Split by trainer header: === TRAINER_XXXX ===
    sections = re.split(r'===\s*(TRAINER_\w+)\s*===', content)

    for i in range(1, len(sections), 2):
        trainer_id = sections[i].strip()
        trainer_body = sections[i+1].strip()

        if trainer_id == "TRAINER_NONE":
            continue

        # Split into trainer header info and party pokemon blocks
        sub_blocks = [b.strip() for b in re.split(r'\n\s*\n', trainer_body) if b.strip()]
        if not sub_blocks:
            continue

        header_lines = sub_blocks[0].splitlines()
        info = {
            "id": trainer_id,
            "name": clean_name(trainer_id),
            "class": "Trainer",
            "pic": "",
            "gender": "Male",
            "double": False,
            "party": []
        }

        for line in header_lines:
            line = line.strip()
            if line.startswith("Name:"):
                info["name"] = line[len("Name:"):].strip() or clean_name(trainer_id)
            elif line.startswith("Class:"):
                info["class"] = line[len("Class:"):].strip()
            elif line.startswith("Pic:"):
                info["pic"] = line[len("Pic:"):].strip()
            elif line.startswith("Gender:"):
                info["gender"] = line[len("Gender:"):].strip()
            elif line.startswith("Double Battle:"):
                info["double"] = "yes" in line.lower()

        # Parse Party Pokemon (sub_blocks[1:])
        for p_block in sub_blocks[1:]:
            p_lines = [l.strip() for l in p_block.splitlines() if l.strip()]
            if not p_lines:
                continue

            first_line = p_lines[0]
            # Match showdown format: Nickname (Species) (M/F) @ Item OR Species @ Item
            species_raw = first_line
            held_item = ""
            if "@" in first_line:
                species_raw, held_item = first_line.split("@", 1)
                species_raw = species_raw.strip()
                held_item = clean_name(held_item.strip())

            # Check parentheses for species / nickname
            species_match = re.search(r'\(([^)]+)\)', species_raw)
            if species_match:
                spec_name = clean_name(species_match.group(1))
            else:
                # Remove gender tags like (M) or (F)
                clean_spec = re.sub(r'\([MF]\)', '', species_raw).strip()
                spec_name = clean_name(clean_spec)

            mon = {
                "species": spec_name,
                "level": 100,
                "item": held_item,
                "ability": "",
                "moves": []
            }

            for l in p_lines[1:]:
                if l.startswith("Level:"):
                    try:
                        mon["level"] = int(l[len("Level:"):].strip())
                    except:
                        pass
                elif l.startswith("Ability:"):
                    mon["ability"] = clean_name(l[len("Ability:"):].strip())
                elif l.startswith("-"):
                    move_name = clean_name(l.lstrip("- ").strip())
                    if move_name:
                        mon["moves"].append(move_name)

            info["party"].append(mon)

        if info["party"] or info["name"]:
            trainers.append(info)

    print(f"Parsed {len(trainers)} trainers.")
    return trainers

def parse_wild_encounters(species_dict):
    """Parse wild encounters JSON and link to species."""
    locations = []
    if not WILD_ENCOUNTERS_FILE.exists():
        print(f"Warning: Wild encounters file not found at {WILD_ENCOUNTERS_FILE}")
        return locations

    try:
        data = json.loads(WILD_ENCOUNTERS_FILE.read_text(encoding='utf-8'))
        groups = data.get("wild_encounter_groups", [])

        for group in groups:
            fields = group.get("fields", [])
            field_types = [f.get("type") for f in fields if "type" in f]
            enc_rates_map = {f.get("type"): f.get("encounter_rates", []) for f in fields if "type" in f}

            encounters = group.get("encounters", [])
            for enc in encounters:
                map_raw = enc.get("map", "")
                map_name = clean_name(map_raw)
                if not map_name:
                    continue

                location_entry = {
                    "map_id": map_raw,
                    "map_name": map_name,
                    "tables": []
                }

                for f_type in field_types:
                    if f_type in enc:
                        table_data = enc[f_type]
                        mons = table_data.get("mons", [])
                        rates = enc_rates_map.get(f_type, [])

                        mons_list = []
                        for idx, mon in enumerate(mons):
                            spec_id = mon.get("species", "")
                            min_lvl = mon.get("min_level", 1)
                            max_lvl = mon.get("max_level", 1)
                            rate_pct = rates[idx] if idx < len(rates) else 0

                            spec_clean = clean_name(spec_id)
                            mons_list.append({
                                "species_id": spec_id,
                                "species": spec_clean,
                                "min_level": min_lvl,
                                "max_level": max_lvl,
                                "rate": rate_pct
                            })

                            # Link back to species dictionary
                            if spec_id in species_dict:
                                species_dict[spec_id]["encounters"].append({
                                    "location": map_name,
                                    "type": clean_name(f_type),
                                    "min_level": min_lvl,
                                    "max_level": max_lvl,
                                    "rate": rate_pct
                                })

                        if mons_list:
                            location_entry["tables"].append({
                                "type": clean_name(f_type),
                                "mons": mons_list
                            })

                if location_entry["tables"]:
                    locations.append(location_entry)

    except Exception as e:
        print(f"Error parsing wild encounters: {e}")

    print(f"Parsed {len(locations)} encounter locations.")
    return locations

def generate_html(species_list, trainers_list, locations_list):
    """Generate modern, responsive, standalone game encyclopedia HTML file."""
    print("Compiling HTML encyclopedia...")

    # Compact JSON data
    data_json = json.dumps({
        "species": species_list,
        "trainers": trainers_list,
        "locations": locations_list
    }, separators=(',', ':'))

    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Pokeemerald-Expansion - Game Encyclopedia</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;600&display=swap" rel="stylesheet">
<style>
:root {{
    --bg-primary: #0a0e17;
    --bg-secondary: #131b2e;
    --bg-card: #18233c;
    --bg-card-hover: #202e50;
    --accent: #3b82f6;
    --accent-glow: rgba(59, 130, 246, 0.35);
    --text-primary: #f1f5f9;
    --text-secondary: #94a3b8;
    --text-muted: #64748b;
    --border: rgba(255, 255, 255, 0.08);
    --border-bright: rgba(255, 255, 255, 0.15);
    --radius-sm: 8px;
    --radius-md: 14px;
    --radius-lg: 20px;
}}

* {{
    box-sizing: border-box;
    margin: 0;
    padding: 0;
}}

body {{
    font-family: 'Outfit', sans-serif;
    background: var(--bg-primary);
    color: var(--text-primary);
    min-height: 100vh;
    display: flex;
    flex-direction: column;
    overflow-x: hidden;
}}

/* Navbar */
header {{
    background: rgba(19, 27, 46, 0.85);
    backdrop-filter: blur(16px);
    border-bottom: 1px solid var(--border);
    position: sticky;
    top: 0;
    z-index: 100;
    padding: 1rem 2rem;
    display: flex;
    flex-wrap: wrap;
    justify-content: space-between;
    align-items: center;
    gap: 1rem;
}}

.logo-group {{
    display: flex;
    align-items: center;
    gap: 0.8rem;
}}

.logo-badge {{
    background: linear-gradient(135deg, #ef4444, #3b82f6);
    color: white;
    font-weight: 800;
    font-size: 1.1rem;
    padding: 0.4rem 0.8rem;
    border-radius: var(--radius-sm);
    box-shadow: 0 0 15px rgba(59, 130, 246, 0.4);
}}

h1.app-title {{
    font-size: 1.4rem;
    font-weight: 700;
    background: linear-gradient(to right, #fff, #94a3b8);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}}

.nav-tabs {{
    display: flex;
    background: rgba(10, 14, 23, 0.6);
    padding: 0.3rem;
    border-radius: var(--radius-md);
    border: 1px solid var(--border);
    gap: 0.3rem;
}}

.tab-btn {{
    background: transparent;
    border: none;
    color: var(--text-secondary);
    font-family: 'Outfit', sans-serif;
    font-weight: 600;
    font-size: 0.95rem;
    padding: 0.6rem 1.4rem;
    border-radius: 10px;
    cursor: pointer;
    transition: all 0.2s ease;
    display: flex;
    align-items: center;
    gap: 0.5rem;
}}

.tab-btn:hover {{
    color: var(--text-primary);
    background: rgba(255, 255, 255, 0.05);
}}

.tab-btn.active {{
    background: var(--accent);
    color: white;
    box-shadow: 0 0 16px var(--accent-glow);
}}

/* Main Container */
main {{
    flex: 1;
    max-width: 1400px;
    width: 100%;
    margin: 0 auto;
    padding: 2rem;
}}

/* Control Bar (Search, Filters, Stats) */
.controls-card {{
    background: var(--bg-secondary);
    border: 1px solid var(--border);
    border-radius: var(--radius-lg);
    padding: 1.25rem 1.75rem;
    margin-bottom: 2rem;
    display: flex;
    flex-wrap: wrap;
    align-items: center;
    justify-content: space-between;
    gap: 1rem;
    box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
}}

.search-wrapper {{
    flex: 1;
    min-width: 280px;
    position: relative;
}}

.search-input {{
    width: 100%;
    background: var(--bg-primary);
    border: 1px solid var(--border-bright);
    color: var(--text-primary);
    padding: 0.75rem 1.25rem;
    padding-left: 2.8rem;
    border-radius: var(--radius-md);
    font-size: 1rem;
    font-family: inherit;
    transition: border-color 0.2s;
}}

.search-input:focus {{
    outline: none;
    border-color: var(--accent);
    box-shadow: 0 0 10px var(--accent-glow);
}}

.search-icon {{
    position: absolute;
    left: 1rem;
    top: 50%;
    transform: translateY(-50%);
    color: var(--text-muted);
    font-size: 1.1rem;
}}

.filters-wrapper {{
    display: flex;
    flex-wrap: wrap;
    gap: 0.8rem;
    align-items: center;
}}

.custom-select {{
    background: var(--bg-primary);
    border: 1px solid var(--border-bright);
    color: var(--text-primary);
    padding: 0.75rem 1rem;
    border-radius: var(--radius-md);
    font-family: inherit;
    font-size: 0.9rem;
    cursor: pointer;
    outline: none;
}}

.count-indicator {{
    font-size: 0.9rem;
    font-weight: 600;
    color: var(--text-secondary);
    background: rgba(255, 255, 255, 0.05);
    padding: 0.5rem 1rem;
    border-radius: var(--radius-sm);
    border: 1px solid var(--border);
}}

/* Grid & Cards */
.grid-view {{
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
    gap: 1.5rem;
}}

.card {{
    background: var(--bg-secondary);
    border: 1px solid var(--border);
    border-radius: var(--radius-lg);
    padding: 1.25rem;
    transition: transform 0.2s ease, border-color 0.2s ease, box-shadow 0.2s ease;
    cursor: pointer;
    display: flex;
    flex-direction: column;
    position: relative;
    overflow: hidden;
}}

.card:hover {{
    transform: translateY(-4px);
    border-color: var(--border-bright);
    box-shadow: 0 12px 28px rgba(0, 0, 0, 0.4);
}}

.card-header {{
    display: flex;
    justify-content: space-between;
    align-items: flex-start;
    margin-bottom: 0.75rem;
}}

.dex-tag {{
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.8rem;
    font-weight: 600;
    color: var(--text-muted);
    background: rgba(0, 0, 0, 0.3);
    padding: 0.2rem 0.5rem;
    border-radius: 6px;
}}

.card-title {{
    font-size: 1.25rem;
    font-weight: 700;
    color: var(--text-primary);
    margin-bottom: 0.25rem;
}}

.card-subtitle {{
    font-size: 0.85rem;
    color: var(--text-muted);
    margin-bottom: 0.75rem;
}}

/* Types Badges */
.type-badges {{
    display: flex;
    gap: 0.4rem;
    margin-bottom: 1rem;
}}

.type-badge {{
    font-size: 0.75rem;
    font-weight: 700;
    text-transform: uppercase;
    padding: 0.25rem 0.65rem;
    border-radius: 6px;
    color: white;
    letter-spacing: 0.5px;
}}

.type-normal {{ background: #9fa19f; }}
.type-fire {{ background: #e62829; }}
.type-water {{ background: #2980ef; }}
.type-electric {{ background: #fac000; color: #111; }}
.type-grass {{ background: #3fa129; }}
.type-ice {{ background: #3dcef3; color: #111; }}
.type-fighting {{ background: #ff8000; }}
.type-poison {{ background: #9141cb; }}
.type-ground {{ background: #915121; }}
.type-flying {{ background: #81b9ef; color: #111; }}
.type-psychic {{ background: #ef4179; }}
.type-bug {{ background: #91a119; }}
.type-rock {{ background: #afa981; }}
.type-ghost {{ background: #704170; }}
.type-dragon {{ background: #5060e1; }}
.type-steel {{ background: #60a1b8; }}
.type-dark {{ background: #50413f; }}
.type-fairy {{ background: #ef70ef; }}
.type-stellar {{ background: linear-gradient(135deg, #38bdf8, #ec4899); }}

/* Mini Stat Bars */
.stat-rows {{
    display: flex;
    flex-direction: column;
    gap: 0.35rem;
    margin-top: auto;
    font-size: 0.8rem;
    background: rgba(0,0,0,0.2);
    padding: 0.6rem 0.8rem;
    border-radius: var(--radius-sm);
}}

.stat-row {{
    display: flex;
    align-items: center;
    gap: 0.5rem;
}}

.stat-label {{
    width: 40px;
    font-weight: 600;
    color: var(--text-secondary);
    font-family: 'JetBrains Mono', monospace;
}}

.stat-val {{
    width: 32px;
    font-weight: 700;
    font-family: 'JetBrains Mono', monospace;
    text-align: right;
}}

.stat-bar-bg {{
    flex: 1;
    height: 6px;
    background: rgba(255, 255, 255, 0.08);
    border-radius: 3px;
    overflow: hidden;
}}

.stat-bar-fill {{
    height: 100%;
    border-radius: 3px;
    background: var(--accent);
}}

/* Trainer Card */
.trainer-card {{
    background: var(--bg-secondary);
    border: 1px solid var(--border);
    border-radius: var(--radius-lg);
    padding: 1.25rem;
    transition: all 0.2s ease;
}}

.trainer-card:hover {{
    border-color: var(--border-bright);
    box-shadow: 0 8px 24px rgba(0, 0, 0, 0.35);
}}

.trainer-header {{
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-bottom: 0.75rem;
}}

.party-chips {{
    display: flex;
    flex-direction: column;
    gap: 0.5rem;
    margin-top: 0.75rem;
}}

.party-chip {{
    display: flex;
    justify-content: space-between;
    align-items: center;
    background: rgba(0, 0, 0, 0.25);
    padding: 0.5rem 0.75rem;
    border-radius: var(--radius-sm);
    font-size: 0.85rem;
}}

/* Locations Table */
.location-group {{
    background: var(--bg-secondary);
    border: 1px solid var(--border);
    border-radius: var(--radius-lg);
    padding: 1.5rem;
    margin-bottom: 1.5rem;
}}

.location-title {{
    font-size: 1.3rem;
    font-weight: 700;
    color: var(--text-primary);
    margin-bottom: 1rem;
    display: flex;
    align-items: center;
    gap: 0.6rem;
}}

.enc-table {{
    width: 100%;
    border-collapse: collapse;
    font-size: 0.9rem;
    margin-top: 0.5rem;
}}

.enc-table th, .enc-table td {{
    padding: 0.6rem 0.8rem;
    text-align: left;
    border-bottom: 1px solid var(--border);
}}

.enc-table th {{
    color: var(--text-muted);
    font-weight: 600;
}}

/* Modal Detail View */
.modal-overlay {{
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: rgba(0, 0, 0, 0.75);
    backdrop-filter: blur(8px);
    display: none;
    justify-content: center;
    align-items: center;
    z-index: 1000;
    padding: 1.5rem;
}}

.modal-card {{
    background: var(--bg-secondary);
    border: 1px solid var(--border-bright);
    border-radius: var(--radius-lg);
    max-width: 800px;
    width: 100%;
    max-height: 90vh;
    overflow-y: auto;
    padding: 2rem;
    position: relative;
    box-shadow: 0 20px 50px rgba(0,0,0,0.6);
}}

.modal-close {{
    position: absolute;
    top: 1.25rem;
    right: 1.25rem;
    background: rgba(255, 255, 255, 0.08);
    border: none;
    color: var(--text-primary);
    font-size: 1.2rem;
    width: 36px;
    height: 36px;
    border-radius: 50%;
    cursor: pointer;
    display: flex;
    align-items: center;
    justify-content: center;
    transition: background 0.2s;
}}

.modal-close:hover {{
    background: rgba(255, 255, 255, 0.2);
}}

.learnset-table {{
    width: 100%;
    border-collapse: collapse;
    font-size: 0.88rem;
    margin-top: 1rem;
}}

.learnset-table th, .learnset-table td {{
    padding: 0.5rem 0.75rem;
    text-align: left;
    border-bottom: 1px solid var(--border);
}}

.learnset-table th {{
    color: var(--text-muted);
    font-weight: 600;
}}

/* Responsive */
@media (max-width: 768px) {{
    header {{
        padding: 1rem;
    }}
    main {{
        padding: 1rem;
    }}
    .nav-tabs {{
        width: 100%;
        justify-content: center;
    }}
}}
</style>
</head>
<body>

<header>
    <div class="logo-group">
        <span class="logo-badge">POKÉ-EXP</span>
        <h1 class="app-title">Game Encyclopedia</h1>
    </div>
    <div class="nav-tabs">
        <button class="tab-btn active" onclick="switchTab('pokemon')">⚡ Pokémon DB</button>
        <button class="tab-btn" onclick="switchTab('trainers')">⚔️ Trainers</button>
        <button class="tab-btn" onclick="switchTab('locations')">🗺️ Wild Encounters</button>
    </div>
</header>

<main>
    <!-- Controls Bar -->
    <div class="controls-card">
        <div class="search-wrapper">
            <span class="search-icon">🔍</span>
            <input type="text" id="searchInput" class="search-input" placeholder="Search by name, species, type, move..." oninput="handleSearch()">
        </div>
        <div class="filters-wrapper" id="filterControls">
            <!-- Dynamic filters injected based on active tab -->
        </div>
        <div class="count-indicator" id="resultsCount">Loading...</div>
    </div>

    <!-- Content Sections -->
    <section id="pokemonSection" class="grid-view"></section>
    <section id="trainersSection" class="grid-view" style="display: none;"></section>
    <section id="locationsSection" style="display: none;"></section>
</main>

<!-- Detail Modal -->
<div class="modal-overlay" id="detailModal" onclick="closeModal(event)">
    <div class="modal-card" id="modalContent"></div>
</div>

<script>
const GAME_DATA = {data_json};

let activeTab = 'pokemon';
let filterType = 'all';
let filterGen = 'all';

function switchTab(tab) {{
    activeTab = tab;
    document.querySelectorAll('.tab-btn').forEach(btn => btn.classList.remove('active'));
    event.target.classList.add('active');

    document.getElementById('pokemonSection').style.display = tab === 'pokemon' ? 'grid' : 'none';
    document.getElementById('trainersSection').style.display = tab === 'trainers' ? 'grid' : 'none';
    document.getElementById('locationsSection').style.display = tab === 'locations' ? 'block' : 'none';

    document.getElementById('searchInput').value = '';
    renderFilters();
    handleSearch();
}}

function renderFilters() {{
    const container = document.getElementById('filterControls');
    if (activeTab === 'pokemon') {{
        container.innerHTML = `
            <select class="custom-select" id="genFilter" onchange="handleSearch()">
                <option value="all">All Generations</option>
                ${{Array.from({{length: 9}}, (_, i) => `<option value="${{i+1}}">Gen ${{i+1}}</option>`).join('')}}
            </select>
            <select class="custom-select" id="typeFilter" onchange="handleSearch()">
                <option value="all">All Types</option>
                ${{["Normal", "Fire", "Water", "Electric", "Grass", "Ice", "Fighting", "Poison", "Ground", "Flying", "Psychic", "Bug", "Rock", "Ghost", "Dragon", "Steel", "Dark", "Fairy"]
                    .map(t => `<option value="${{t}}">${{t}}</option>`).join('')}}
            </select>
            <select class="custom-select" id="sortFilter" onchange="handleSearch()">
                <option value="dex">Sort: Dex #</option>
                <option value="name">Sort: Name</option>
                <option value="bst">Sort: Base Stat Total</option>
                <option value="hp">Sort: HP</option>
                <option value="atk">Sort: Attack</option>
                <option value="def">Sort: Defense</option>
                <option value="spe">Sort: Speed</option>
            </select>
        `;
    }} else if (activeTab === 'trainers') {{
        const classes = Array.from(new Set(GAME_DATA.trainers.map(t => t.class))).sort();
        container.innerHTML = `
            <select class="custom-select" id="classFilter" onchange="handleSearch()">
                <option value="all">All Trainer Classes</option>
                ${{classes.map(c => `<option value="${{c}}">${{c}}</option>`).join('')}}
            </select>
        `;
    }} else {{
        container.innerHTML = '';
    }}
}}

function getStatBarColor(val) {{
    if (val >= 130) return '#10b981';
    if (val >= 100) return '#3b82f6';
    if (val >= 70) return '#eab308';
    if (val >= 50) return '#f97316';
    return '#ef4444';
}}

function renderPokemon(list) {{
    const container = document.getElementById('pokemonSection');
    if (!list.length) {{
        container.innerHTML = `<div style="grid-column: 1/-1; text-align: center; color: var(--text-muted); padding: 3rem;">No Pokémon found matching criteria.</div>`;
        return;
    }}

    container.innerHTML = list.map(p => `
        <div class="card" onclick="openPokemonModal('${{p.id}}')">
            <div class="card-header">
                <div>
                    <h3 class="card-title">${{p.name}}</h3>
                    <div class="card-subtitle">${{p.category}} Pokémon • Gen ${{p.gen}}</div>
                </div>
                <span class="dex-tag">#${{p.dex}}</span>
            </div>
            <div class="type-badges">
                ${{p.types.map(t => `<span class="type-badge type-${{t.toLowerCase()}}">${{t}}</span>`).join('')}}
            </div>
            <div class="stat-rows">
                <div class="stat-row">
                    <span class="stat-label">HP</span>
                    <span class="stat-val">${{p.stats.hp}}</span>
                    <div class="stat-bar-bg"><div class="stat-bar-fill" style="width: ${{Math.min(100, (p.stats.hp/255)*100)}}%; background: ${{getStatBarColor(p.stats.hp)}}"></div></div>
                </div>
                <div class="stat-row">
                    <span class="stat-label">ATK</span>
                    <span class="stat-val">${{p.stats.atk}}</span>
                    <div class="stat-bar-bg"><div class="stat-bar-fill" style="width: ${{Math.min(100, (p.stats.atk/255)*100)}}%; background: ${{getStatBarColor(p.stats.atk)}}"></div></div>
                </div>
                <div class="stat-row">
                    <span class="stat-label">DEF</span>
                    <span class="stat-val">${{p.stats.def}}</span>
                    <div class="stat-bar-bg"><div class="stat-bar-fill" style="width: ${{Math.min(100, (p.stats.def/255)*100)}}%; background: ${{getStatBarColor(p.stats.def)}}"></div></div>
                </div>
                <div class="stat-row">
                    <span class="stat-label">SPE</span>
                    <span class="stat-val">${{p.stats.spe}}</span>
                    <div class="stat-bar-bg"><div class="stat-bar-fill" style="width: ${{Math.min(100, (p.stats.spe/255)*100)}}%; background: ${{getStatBarColor(p.stats.spe)}}"></div></div>
                </div>
                <div style="display: flex; justify-content: space-between; margin-top: 0.3rem; font-weight: 700; color: var(--text-secondary);">
                    <span>BST Total</span>
                    <span>${{p.stats.bst}}</span>
                </div>
            </div>
        </div>
    `).join('');
}}

function renderTrainers(list) {{
    const container = document.getElementById('trainersSection');
    if (!list.length) {{
        container.innerHTML = `<div style="grid-column: 1/-1; text-align: center; color: var(--text-muted); padding: 3rem;">No Trainers found matching criteria.</div>`;
        return;
    }}

    container.innerHTML = list.map(t => `
        <div class="trainer-card">
            <div class="trainer-header">
                <div>
                    <h3 class="card-title">${{t.name}}</h3>
                    <div class="card-subtitle">${{t.class}} ${{t.double ? '• Double Battle' : ''}}</div>
                </div>
                <span class="dex-tag">${{t.party.length}} PkMn</span>
            </div>
            <div class="party-chips">
                ${{t.party.map(p => `
                    <div class="party-chip">
                        <div>
                            <strong>${{p.species}}</strong>
                            ${{p.item ? `<span style="color: var(--text-muted); font-size: 0.75rem;"> @ ${{p.item}}</span>` : ''}}
                        </div>
                        <span class="dex-tag">Lv. ${{p.level}}</span>
                    </div>
                `).join('')}}
            </div>
        </div>
    `).join('');
}}

function renderLocations(list) {{
    const container = document.getElementById('locationsSection');
    if (!list.length) {{
        container.innerHTML = `<div style="text-align: center; color: var(--text-muted); padding: 3rem;">No Encounter locations found.</div>`;
        return;
    }}

    container.innerHTML = list.map(loc => `
        <div class="location-group">
            <div class="location-title">📍 ${{loc.map_name}}</div>
            ${{loc.tables.map(tbl => `
                <div style="margin-bottom: 1rem;">
                    <h4 style="color: var(--accent); font-size: 0.95rem; margin-bottom: 0.4rem;">${{tbl.type}}</h4>
                    <table class="enc-table">
                        <thead>
                            <tr>
                                <th>Pokémon</th>
                                <th>Level Range</th>
                                <th>Encounter Rate</th>
                            </tr>
                        </thead>
                        <tbody>
                            ${{tbl.mons.map(m => `
                                <tr>
                                    <td><strong>${{m.species}}</strong></td>
                                    <td>Lv. ${{m.min_level}}${{m.min_level !== m.max_level ? ` - ${{m.max_level}}` : ''}}</td>
                                    <td>${{m.rate}}%</td>
                                </tr>
                            `).join('')}}
                        </tbody>
                    </table>
                </div>
            `).join('')}}
        </div>
    `).join('');
}}

function openPokemonModal(speciesId) {{
    const p = GAME_DATA.species.find(s => s.id === speciesId);
    if (!p) return;

    const modal = document.getElementById('detailModal');
    const content = document.getElementById('modalContent');

    content.innerHTML = `
        <button class="modal-close" onclick="closeModalDirect()">✕</button>
        <div style="display: flex; justify-content: space-between; align-items: baseline; margin-bottom: 0.5rem;">
            <h2 style="font-size: 1.8rem; font-weight: 800;">${{p.name}}</h2>
            <span class="dex-tag" style="font-size: 1rem;">#${{p.dex}}</span>
        </div>
        <div class="type-badges" style="margin-bottom: 1rem;">
            ${{p.types.map(t => `<span class="type-badge type-${{t.toLowerCase()}}" style="font-size: 0.85rem;">${{t}}</span>`).join('')}}
        </div>
        <p style="color: var(--text-secondary); margin-bottom: 1.5rem; line-height: 1.5;">${{p.description || 'No Pokédex entry available.'}}</p>

        <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(180px, 1fr)); gap: 1rem; margin-bottom: 1.5rem; background: rgba(0,0,0,0.3); padding: 1rem; border-radius: var(--radius-md);">
            <div><span style="color: var(--text-muted); font-size: 0.8rem;">Height:</span> <strong>${{p.height}} m</strong></div>
            <div><span style="color: var(--text-muted); font-size: 0.8rem;">Weight:</span> <strong>${{p.weight}} kg</strong></div>
            <div><span style="color: var(--text-muted); font-size: 0.8rem;">Abilities:</span> <strong>${{p.abilities.join(', ') || 'None'}}</strong></div>
            <div><span style="color: var(--text-muted); font-size: 0.8rem;">Generation:</span> <strong>Gen ${{p.gen}}</strong></div>
        </div>

        <h3 style="margin-bottom: 0.8rem; font-size: 1.1rem;">Base Stats (BST: ${{p.stats.bst}})</h3>
        <div class="stat-rows" style="margin-bottom: 1.5rem;">
            ${{Object.entries(p.stats).filter(([k]) => k !== 'bst').map(([k, v]) => `
                <div class="stat-row">
                    <span class="stat-label">${{k.toUpperCase()}}</span>
                    <span class="stat-val">${{v}}</span>
                    <div class="stat-bar-bg"><div class="stat-bar-fill" style="width: ${{Math.min(100, (v/255)*100)}}%; background: ${{getStatBarColor(v)}}"></div></div>
                </div>
            `).join('')}}
        </div>

        ${{p.moves && p.moves.length ? `
            <h3 style="margin-bottom: 0.5rem; font-size: 1.1rem;">Level-Up Moves</h3>
            <table class="learnset-table">
                <thead><tr><th>Level</th><th>Move</th></tr></thead>
                <tbody>
                    ${{p.moves.map(m => `<tr><td><strong>Lv. ${{m.level}}</strong></td><td>${{m.move}}</td></tr>`).join('')}}
                </tbody>
            </table>
        ` : ''}}

        ${{p.encounters && p.encounters.length ? `
            <h3 style="margin-top: 1.5rem; margin-bottom: 0.5rem; font-size: 1.1rem;">Wild Encounter Locations</h3>
            <table class="learnset-table">
                <thead><tr><th>Location</th><th>Method</th><th>Level Range</th><th>Rate</th></tr></thead>
                <tbody>
                    ${{p.encounters.map(e => `<tr><td>${{e.location}}</td><td>${{e.type}}</td><td>Lv. ${{e.min_level}}${{e.min_level !== e.max_level ? ` - ${{e.max_level}}` : ''}}</td><td>${{e.rate}}%</td></tr>`).join('')}}
                </tbody>
            </table>
        ` : ''}}
    `;

    modal.style.display = 'flex';
}}

function closeModal(event) {{
    if (event.target.id === 'detailModal') {{
        document.getElementById('detailModal').style.display = 'none';
    }}
}}

function closeModalDirect() {{
    document.getElementById('detailModal').style.display = 'none';
}}

function handleSearch() {{
    const query = document.getElementById('searchInput').value.toLowerCase().trim();
    const countEl = document.getElementById('resultsCount');

    if (activeTab === 'pokemon') {{
        const genVal = document.getElementById('genFilter') ? document.getElementById('genFilter').value : 'all';
        const typeVal = document.getElementById('typeFilter') ? document.getElementById('typeFilter').value : 'all';
        const sortVal = document.getElementById('sortFilter') ? document.getElementById('sortFilter').value : 'dex';

        let list = GAME_DATA.species.filter(p => {{
            const matchQuery = !query || p.name.toLowerCase().includes(query) || p.types.some(t => t.toLowerCase().includes(query)) || p.abilities.some(a => a.toLowerCase().includes(query)) || (p.moves && p.moves.some(m => m.move.toLowerCase().includes(query)));
            const matchGen = genVal === 'all' || p.gen.toString() === genVal;
            const matchType = typeVal === 'all' || p.types.includes(typeVal);
            return matchQuery && matchGen && matchType;
        }});

        if (sortVal === 'name') {{
            list.sort((a, b) => a.name.localeCompare(b.name));
        }} else if (sortVal === 'bst') {{
            list.sort((a, b) => b.stats.bst - a.stats.bst);
        }} else if (['hp', 'atk', 'def', 'spe'].includes(sortVal)) {{
            list.sort((a, b) => b.stats[sortVal] - a.stats[sortVal]);
        }}

        countEl.innerText = `${{list.length}} Pokémon shown`;
        renderPokemon(list);
    }} else if (activeTab === 'trainers') {{
        const classVal = document.getElementById('classFilter') ? document.getElementById('classFilter').value : 'all';
        let list = GAME_DATA.trainers.filter(t => {{
            const matchQuery = !query || t.name.toLowerCase().includes(query) || t.class.toLowerCase().includes(query) || t.party.some(p => p.species.toLowerCase().includes(query));
            const matchClass = classVal === 'all' || t.class === classVal;
            return matchQuery && matchClass;
        }});
        countEl.innerText = `${{list.length}} Trainers shown`;
        renderTrainers(list);
    }} else if (activeTab === 'locations') {{
        let list = GAME_DATA.locations.filter(loc => {{
            return !query || loc.map_name.toLowerCase().includes(query) || loc.tables.some(tbl => tbl.mons.some(m => m.species.toLowerCase().includes(query)));
        }});
        countEl.innerText = `${{list.length}} Locations shown`;
        renderLocations(list);
    }}
}}

// Initialize
renderFilters();
handleSearch();
</script>
</body>
</html>
"""

    OUTPUT_HTML.write_text(html_content, encoding='utf-8')
    print(f"Successfully generated {OUTPUT_HTML.name} ({len(html_content):,} bytes).")

def main():
    print("=== Pokeemerald-Expansion Encyclopedia Generator ===")
    learnsets = parse_learnsets()
    species = parse_species(learnsets)
    species_dict = {s["id"]: s for s in species}
    trainers = parse_trainers()
    locations = parse_wild_encounters(species_dict)
    generate_html(species, trainers, locations)
    print("=== Done! Open game_encyclopedia.html in any browser. ===")

if __name__ == "__main__":
    main()
