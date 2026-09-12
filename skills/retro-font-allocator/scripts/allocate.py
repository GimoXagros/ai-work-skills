"""Plan repertoire storage and explicitly declared state-local glyph slots."""
import argparse
import json
from pathlib import Path

def integer(value, label, minimum=0):
    if type(value) is not int or value < minimum:
        raise ValueError(f'{label} must be an integer >= {minimum}')
    return value

def allocate(spec):
    glyphs = spec['glyphs']
    if not isinstance(glyphs, list) or not glyphs or any(not isinstance(g, str) or not g for g in glyphs):
        raise ValueError('glyphs must be nonempty string identities')
    if len(glyphs) != len(set(glyphs)):
        raise ValueError('duplicate glyph identity')
    glyphs = sorted(glyphs)
    cost = integer(spec['bytes_per_glyph'], 'bytes_per_glyph', 1)
    budget = integer(spec['storage_budget_bytes'], 'storage_budget_bytes')
    slots = integer(spec['slot_capacity'], 'slot_capacity', 1)
    reserved = spec.get('reserved_slots', [])
    if len(reserved) != len(set(reserved)) or any(type(s) is not int or not 0 <= s < slots for s in reserved):
        raise ValueError('invalid or duplicate reserved slot')
    pinned = spec.get('pinned', {})
    if any(g not in glyphs for g in pinned) or len(set(pinned.values())) != len(pinned):
        raise ValueError('unknown pinned glyph or slot collision')
    if any(type(s) is not int or s in reserved or not 0 <= s < slots for s in pinned.values()):
        raise ValueError('pinned slot is unavailable')
    required = len(glyphs) * cost
    if required > budget:
        raise ValueError(f'repertoire storage overflow: {required} > {budget}')
    states = spec['states']
    if not isinstance(states, dict) or not states:
        raise ValueError('at least one explicit state/transition working set is required')
    plans = {}
    for state, members in sorted(states.items()):
        if not isinstance(members, list) or len(set(members)) != len(members) or any(g not in glyphs for g in members):
            raise ValueError(f'invalid working set: {state}')
        active = sorted(set(members) | set(pinned))
        assignment = dict(pinned)
        free = [s for s in range(slots) if s not in reserved and s not in pinned.values()]
        unplaced = [g for g in active if g not in pinned]
        if len(unplaced) > len(free):
            raise ValueError(f'active slot overflow in {state}: {len(active)} required')
        assignment.update(zip(unplaced, free))
        plans[state] = {'active_glyphs': len(active), 'slots': assignment}
    return {'storage_bytes': required, 'repertoire_glyphs': len(glyphs), 'states': plans,
            'scope': 'state-local plan only; transition lifetimes, loader and remapping require runtime proof'}

def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('spec', type=Path)
    args = p.parse_args()
    try:
        print(json.dumps(allocate(json.loads(args.spec.read_text(encoding='utf-8-sig'))), indent=2, ensure_ascii=True))
    except (OSError, ValueError, KeyError, TypeError) as exc:
        p.error(str(exc))

if __name__ == '__main__':
    main()
