# Every E3 continuation opportunity and original generated source

Local fixture outputs under setup are excluded. No generated source is repaired.

## S101 opportunity 1

Outcome: `local_prelaunch_failure`. External invocation: none.

Native parent: slot 0, training 2.655386350817823; inspiration slots: [].

No generated program or measured proposal fitness.

## S101 opportunity 2

Outcome: `completed`. External invocation: 1.

Native parent: slot 0, training 2.655386350817823; inspiration slots: [].

Valid: True; original training: 2.6542583192329383; duplicate of slot: None.
Original source: `results/e3/continuation_v1/runs/S101/gen_2/main.py`; SHA-256 `f5949d228b1c917cd1e4a88b0d2dcf0d149e05cdef88fdf2b1b36597a2630df3`.

```python
# EVOLVE-BLOCK-START
def policy(own_history, opponent_history):
    return 0 if len(opponent_history) == 0 or opponent_history.count(1) == 0 or (opponent_history.count(1) == 2 and opponent_history[-1] == 0) else 1
# EVOLVE-BLOCK-END
```

Branch explanation: cooperate when `len(opponent_history) == 0 or opponent_history.count(1) == 0 or (opponent_history.count(1) == 2 and opponent_history[-1] == 0)`, otherwise defect.

## S101 opportunity 3

Outcome: `completed`. External invocation: 2.

Native parent: slot 0, training 2.655386350817823; inspiration slots: [2].

Valid: True; original training: 2.5362380146644106; duplicate of slot: None.
Original source: `results/e3/continuation_v1/runs/S101/gen_3/main.py`; SHA-256 `f10d41828a82b0716d21b12e3d60d2102411c4e51c935a7aa9d75a9658be4cb5`.

```python
# EVOLVE-BLOCK-START
def policy(own_history, opponent_history):
    return 0 if len(opponent_history) == 0 else opponent_history[-1]
# EVOLVE-BLOCK-END
```

Branch explanation: cooperate when `len(opponent_history) == 0`, otherwise return `opponent_history[-1]` (0 means cooperate, 1 means defect).

## S101 opportunity 4

Outcome: `completed`. External invocation: 3.

Native parent: slot 0, training 2.655386350817823; inspiration slots: [2].

Valid: True; original training: 2.651720248166949; duplicate of slot: None.
Original source: `results/e3/continuation_v1/runs/S101/gen_4/main.py`; SHA-256 `e1fa704589ca4b2d850fe0a71a6a043001457ee22a35b4ec964154784269e109`.

```python
# EVOLVE-BLOCK-START
def policy(own_history, opponent_history):
    return 0 if len(opponent_history) == 0 or opponent_history.count(1) < 2 else 1
# EVOLVE-BLOCK-END
```

Branch explanation: cooperate when `len(opponent_history) == 0 or opponent_history.count(1) < 2`, otherwise defect.

## S101 opportunity 5

Outcome: `completed`. External invocation: 4.

Native parent: slot 2, training 2.6542583192329383; inspiration slots: [0].

Valid: True; original training: 2.6535532994923856; duplicate of slot: None.
Original source: `results/e3/continuation_v1/runs/S101/gen_5/main.py`; SHA-256 `44070240a78af542443b23dbe317b923133e2f53f7280cbae06a091abdbecd05`.

```python
# EVOLVE-BLOCK-START
def policy(own_history, opponent_history):
    return 0 if len(opponent_history) == 0 or opponent_history.count(1) == 0 or (opponent_history.count(1) == 1 and opponent_history[-1] == 0) else 1
# EVOLVE-BLOCK-END
```

Branch explanation: cooperate when `len(opponent_history) == 0 or opponent_history.count(1) == 0 or (opponent_history.count(1) == 1 and opponent_history[-1] == 0)`, otherwise defect.

## S101 opportunity 6

Outcome: `completed`. External invocation: 5.

Native parent: slot 2, training 2.6542583192329383; inspiration slots: [0].

Valid: True; original training: 2.5362380146644106; duplicate of slot: 3.
Original source: `results/e3/continuation_v1/runs/S101/gen_6/main.py`; SHA-256 `f10d41828a82b0716d21b12e3d60d2102411c4e51c935a7aa9d75a9658be4cb5`.

```python
# EVOLVE-BLOCK-START
def policy(own_history, opponent_history):
    return 0 if len(opponent_history) == 0 else opponent_history[-1]
# EVOLVE-BLOCK-END
```

Branch explanation: cooperate when `len(opponent_history) == 0`, otherwise return `opponent_history[-1]` (0 means cooperate, 1 means defect).

## S101 opportunity 7

Outcome: `completed`. External invocation: 6.

Native parent: slot 2, training 2.6542583192329383; inspiration slots: [0].

Valid: True; original training: 2.655386350817823; duplicate of slot: 0.
Original source: `results/e3/continuation_v1/runs/S101/gen_7/main.py`; SHA-256 `fc938dea6c869791ffb3d7fbbb03f95b21ea86152fb3414345a9d107323d56a1`.

```python
# EVOLVE-BLOCK-START
def policy(own_history, opponent_history):
    return 0 if len(opponent_history) == 0 or opponent_history.count(1) == 0 else 1
# EVOLVE-BLOCK-END
```

Branch explanation: cooperate when `len(opponent_history) == 0 or opponent_history.count(1) == 0`, otherwise defect.

## S101 opportunity 8

Outcome: `completed`. External invocation: 7.

Native parent: slot 7, training 2.655386350817823; inspiration slots: [0].

Valid: True; original training: 2.5362380146644106; duplicate of slot: 3.
Original source: `results/e3/continuation_v1/runs/S101/gen_8/main.py`; SHA-256 `f10d41828a82b0716d21b12e3d60d2102411c4e51c935a7aa9d75a9658be4cb5`.

```python
# EVOLVE-BLOCK-START
def policy(own_history, opponent_history):
    return 0 if len(opponent_history) == 0 else opponent_history[-1]
# EVOLVE-BLOCK-END
```

Branch explanation: cooperate when `len(opponent_history) == 0`, otherwise return `opponent_history[-1]` (0 means cooperate, 1 means defect).

## S101 opportunity 9

Outcome: `completed`. External invocation: 8.

Native parent: slot 0, training 2.655386350817823; inspiration slots: [7].

Valid: True; original training: 2.5362380146644106; duplicate of slot: 3.
Original source: `results/e3/continuation_v1/runs/S101/gen_9/main.py`; SHA-256 `f10d41828a82b0716d21b12e3d60d2102411c4e51c935a7aa9d75a9658be4cb5`.

```python
# EVOLVE-BLOCK-START
def policy(own_history, opponent_history):
    return 0 if len(opponent_history) == 0 else opponent_history[-1]
# EVOLVE-BLOCK-END
```

Branch explanation: cooperate when `len(opponent_history) == 0`, otherwise return `opponent_history[-1]` (0 means cooperate, 1 means defect).

## S101 opportunity 10

Outcome: `completed`. External invocation: 9.

Native parent: slot 5, training 2.6535532994923856; inspiration slots: [0].

Valid: True; original training: 2.655386350817823; duplicate of slot: 0.
Original source: `results/e3/continuation_v1/runs/S101/gen_10/main.py`; SHA-256 `fc938dea6c869791ffb3d7fbbb03f95b21ea86152fb3414345a9d107323d56a1`.

```python
# EVOLVE-BLOCK-START
def policy(own_history, opponent_history):
    return 0 if len(opponent_history) == 0 or opponent_history.count(1) == 0 else 1
# EVOLVE-BLOCK-END
```

Branch explanation: cooperate when `len(opponent_history) == 0 or opponent_history.count(1) == 0`, otherwise defect.

## S101 opportunity 11

Outcome: `completed`. External invocation: 10.

Native parent: slot 10, training 2.655386350817823; inspiration slots: [0].

Valid: True; original training: 2.5362380146644106; duplicate of slot: 3.
Original source: `results/e3/continuation_v1/runs/S101/gen_11/main.py`; SHA-256 `f10d41828a82b0716d21b12e3d60d2102411c4e51c935a7aa9d75a9658be4cb5`.

```python
# EVOLVE-BLOCK-START
def policy(own_history, opponent_history):
    return 0 if len(opponent_history) == 0 else opponent_history[-1]
# EVOLVE-BLOCK-END
```

Branch explanation: cooperate when `len(opponent_history) == 0`, otherwise return `opponent_history[-1]` (0 means cooperate, 1 means defect).

## S101 opportunity 12

Outcome: `completed`. External invocation: 11.

Native parent: slot 0, training 2.655386350817823; inspiration slots: [7].

Valid: True; original training: 2.5362380146644106; duplicate of slot: 3.
Original source: `results/e3/continuation_v1/runs/S101/gen_12/main.py`; SHA-256 `f10d41828a82b0716d21b12e3d60d2102411c4e51c935a7aa9d75a9658be4cb5`.

```python
# EVOLVE-BLOCK-START
def policy(own_history, opponent_history):
    return 0 if len(opponent_history) == 0 else opponent_history[-1]
# EVOLVE-BLOCK-END
```

Branch explanation: cooperate when `len(opponent_history) == 0`, otherwise return `opponent_history[-1]` (0 means cooperate, 1 means defect).

## S101 opportunity 13

Outcome: `completed`. External invocation: 12.

Native parent: slot 4, training 2.651720248166949; inspiration slots: [0].

Valid: True; original training: 2.5362380146644106; duplicate of slot: 3.
Original source: `results/e3/continuation_v1/runs/S101/gen_13/main.py`; SHA-256 `f10d41828a82b0716d21b12e3d60d2102411c4e51c935a7aa9d75a9658be4cb5`.

```python
# EVOLVE-BLOCK-START
def policy(own_history, opponent_history):
    return 0 if len(opponent_history) == 0 else opponent_history[-1]
# EVOLVE-BLOCK-END
```

Branch explanation: cooperate when `len(opponent_history) == 0`, otherwise return `opponent_history[-1]` (0 means cooperate, 1 means defect).

## S101 opportunity 14

Outcome: `completed`. External invocation: 13.

Native parent: slot 8, training 2.5362380146644106; inspiration slots: [0].

Valid: True; original training: 2.655386350817823; duplicate of slot: 0.
Original source: `results/e3/continuation_v1/runs/S101/gen_14/main.py`; SHA-256 `fc938dea6c869791ffb3d7fbbb03f95b21ea86152fb3414345a9d107323d56a1`.

```python
# EVOLVE-BLOCK-START
def policy(own_history, opponent_history):
    return 0 if len(opponent_history) == 0 or opponent_history.count(1) == 0 else 1
# EVOLVE-BLOCK-END
```

Branch explanation: cooperate when `len(opponent_history) == 0 or opponent_history.count(1) == 0`, otherwise defect.

## S101 opportunity 15

Outcome: `completed`. External invocation: 14.

Native parent: slot 14, training 2.655386350817823; inspiration slots: [0].

Valid: True; original training: 2.5362380146644106; duplicate of slot: 3.
Original source: `results/e3/continuation_v1/runs/S101/gen_15/main.py`; SHA-256 `f10d41828a82b0716d21b12e3d60d2102411c4e51c935a7aa9d75a9658be4cb5`.

```python
# EVOLVE-BLOCK-START
def policy(own_history, opponent_history):
    return 0 if len(opponent_history) == 0 else opponent_history[-1]
# EVOLVE-BLOCK-END
```

Branch explanation: cooperate when `len(opponent_history) == 0`, otherwise return `opponent_history[-1]` (0 means cooperate, 1 means defect).

## S101 opportunity 16

Outcome: `completed`. External invocation: 15.

Native parent: slot 14, training 2.655386350817823; inspiration slots: [0].

Valid: True; original training: 2.5362380146644106; duplicate of slot: 3.
Original source: `results/e3/continuation_v1/runs/S101/gen_16/main.py`; SHA-256 `f10d41828a82b0716d21b12e3d60d2102411c4e51c935a7aa9d75a9658be4cb5`.

```python
# EVOLVE-BLOCK-START
def policy(own_history, opponent_history):
    return 0 if len(opponent_history) == 0 else opponent_history[-1]
# EVOLVE-BLOCK-END
```

Branch explanation: cooperate when `len(opponent_history) == 0`, otherwise return `opponent_history[-1]` (0 means cooperate, 1 means defect).

## S101 opportunity 17

Outcome: `completed`. External invocation: 16.

Native parent: slot 7, training 2.655386350817823; inspiration slots: [0].

Valid: True; original training: 2.5362380146644106; duplicate of slot: 3.
Original source: `results/e3/continuation_v1/runs/S101/gen_17/main.py`; SHA-256 `f10d41828a82b0716d21b12e3d60d2102411c4e51c935a7aa9d75a9658be4cb5`.

```python
# EVOLVE-BLOCK-START
def policy(own_history, opponent_history):
    return 0 if len(opponent_history) == 0 else opponent_history[-1]
# EVOLVE-BLOCK-END
```

Branch explanation: cooperate when `len(opponent_history) == 0`, otherwise return `opponent_history[-1]` (0 means cooperate, 1 means defect).

## S101 opportunity 18

Outcome: `completed`. External invocation: 17.

Native parent: slot 17, training 2.5362380146644106; inspiration slots: [0].

Valid: True; original training: 2.655386350817823; duplicate of slot: 0.
Original source: `results/e3/continuation_v1/runs/S101/gen_18/main.py`; SHA-256 `fc938dea6c869791ffb3d7fbbb03f95b21ea86152fb3414345a9d107323d56a1`.

```python
# EVOLVE-BLOCK-START
def policy(own_history, opponent_history):
    return 0 if len(opponent_history) == 0 or opponent_history.count(1) == 0 else 1
# EVOLVE-BLOCK-END
```

Branch explanation: cooperate when `len(opponent_history) == 0 or opponent_history.count(1) == 0`, otherwise defect.

## S101 opportunity 19

Outcome: `completed`. External invocation: 18.

Native parent: slot 18, training 2.655386350817823; inspiration slots: [0].

Valid: False; original training: -1.0; duplicate of slot: None.
Original source: `results/e3/continuation_v1/runs/S101/gen_19/main.py`; SHA-256 `9fff818bcb869468115eb09c5319c781db3744ab881244cd51c7322d58212be5`.

```python
# EVOLVE-BLOCK-START
def policy(own_history, opponent_history):
    return 0 if len(opponent_history) == 0 else 1 if len(opponent_history) >= 3 and opponent_history[-3:] == (1, 1, 1) else 0 if own_history[-1] == opponent_history[-1] else 1
# EVOLVE-BLOCK-END
```

Branch explanation: cooperate when `len(opponent_history) == 0`, otherwise defect when `len(opponent_history) >= 3 and opponent_history[-3:] == (1, 1, 1)`, otherwise cooperate when `own_history[-1] == opponent_history[-1]`, otherwise defect.

## S101 opportunity 20

Outcome: `completed`. External invocation: 19.

Native parent: slot 7, training 2.655386350817823; inspiration slots: [0].

Valid: True; original training: 2.5362380146644106; duplicate of slot: 3.
Original source: `results/e3/continuation_v1/runs/S101/gen_20/main.py`; SHA-256 `f10d41828a82b0716d21b12e3d60d2102411c4e51c935a7aa9d75a9658be4cb5`.

```python
# EVOLVE-BLOCK-START
def policy(own_history, opponent_history):
    return 0 if len(opponent_history) == 0 else opponent_history[-1]
# EVOLVE-BLOCK-END
```

Branch explanation: cooperate when `len(opponent_history) == 0`, otherwise return `opponent_history[-1]` (0 means cooperate, 1 means defect).

## S202 opportunity 1

Outcome: `completed`. External invocation: 20.

Native parent: slot 0, training 2.655386350817823; inspiration slots: [].

Valid: True; original training: 2.330936266215454; duplicate of slot: None.
Original source: `results/e3/continuation_v1/runs/S202/gen_1/main.py`; SHA-256 `2ab741fec7547c757b9c7836b2be61350e06427a5aea12c847739fff1bb832d0`.

```python
# EVOLVE-BLOCK-START
def policy(own_history, opponent_history):
    if len(opponent_history) == 0:
        return 0
    elif len(opponent_history) == 1:
        return 1
    elif opponent_history[0] == 0 and opponent_history[1] == 0:
        return 0 if opponent_history.count(1) == 1 else 1
    else:
        return 1
# EVOLVE-BLOCK-END
```

Branch explanation: If `len(opponent_history) == 0`: cooperate. Otherwise: If `len(opponent_history) == 1`: defect. Otherwise: Otherwise: If `opponent_history[0] == 0 and opponent_history[1] == 0`: cooperate when `opponent_history.count(1) == 1`, otherwise defect. Otherwise: Otherwise: Otherwise: defect.

## S202 opportunity 2

Outcome: `completed`. External invocation: 21.

Native parent: slot 0, training 2.655386350817823; inspiration slots: [1].

Valid: True; original training: 2.5362380146644106; duplicate of slot: None.
Original source: `results/e3/continuation_v1/runs/S202/gen_2/main.py`; SHA-256 `7509a8317f7009e4634e3bbf2322edbb59c97f7f8c4a89b187c0277f29a43e67`.

```python
# EVOLVE-BLOCK-START
def policy(own_history, opponent_history):
    return 0 if len(opponent_history) == 0 or opponent_history[-1] == 0 else 1
# EVOLVE-BLOCK-END
```

Branch explanation: cooperate when `len(opponent_history) == 0 or opponent_history[-1] == 0`, otherwise defect.

## S202 opportunity 3

Outcome: `completed`. External invocation: 22.

Native parent: slot 2, training 2.5362380146644106; inspiration slots: [0].

Valid: True; original training: 2.651720248166949; duplicate of slot: None.
Original source: `results/e3/continuation_v1/runs/S202/gen_3/main.py`; SHA-256 `f75616963be773f87e1f763e19da530af6529cecb2f9c28fab0fc1c8d15bd67a`.

```python
# EVOLVE-BLOCK-START
def policy(own_history, opponent_history):
    return 0 if opponent_history.count(1) < 2 else 1
# EVOLVE-BLOCK-END
```

Branch explanation: cooperate when `opponent_history.count(1) < 2`, otherwise defect.

## S202 opportunity 4

Outcome: `completed`. External invocation: 23.

Native parent: slot 3, training 2.651720248166949; inspiration slots: [0].

Valid: True; original training: 2.655386350817823; duplicate of slot: 0.
Original source: `results/e3/continuation_v1/runs/S202/gen_4/main.py`; SHA-256 `fc938dea6c869791ffb3d7fbbb03f95b21ea86152fb3414345a9d107323d56a1`.

```python
# EVOLVE-BLOCK-START
def policy(own_history, opponent_history):
    return 0 if len(opponent_history) == 0 or opponent_history.count(1) == 0 else 1
# EVOLVE-BLOCK-END
```

Branch explanation: cooperate when `len(opponent_history) == 0 or opponent_history.count(1) == 0`, otherwise defect.

## S202 opportunity 5

Outcome: `completed`. External invocation: 24.

Native parent: slot 4, training 2.655386350817823; inspiration slots: [0].

Valid: True; original training: 2.5362380146644106; duplicate of slot: None.
Original source: `results/e3/continuation_v1/runs/S202/gen_5/main.py`; SHA-256 `f10d41828a82b0716d21b12e3d60d2102411c4e51c935a7aa9d75a9658be4cb5`.

```python
# EVOLVE-BLOCK-START
def policy(own_history, opponent_history):
    return 0 if len(opponent_history) == 0 else opponent_history[-1]
# EVOLVE-BLOCK-END
```

Branch explanation: cooperate when `len(opponent_history) == 0`, otherwise return `opponent_history[-1]` (0 means cooperate, 1 means defect).

## S202 opportunity 6

Outcome: `completed`. External invocation: 25.

Native parent: slot 4, training 2.655386350817823; inspiration slots: [0].

Valid: True; original training: 2.6402989283699942; duplicate of slot: None.
Original source: `results/e3/continuation_v1/runs/S202/gen_6/main.py`; SHA-256 `ab7b755dbacfea291382276db6f0cc47f4c7b25c797be51ed91709d1dab13234`.

```python
# EVOLVE-BLOCK-START
def policy(own_history, opponent_history):
    return 0 if len(opponent_history) == 0 or opponent_history.count(1) == 0 or len(opponent_history) % 50 < 2 else 1
# EVOLVE-BLOCK-END
```

Branch explanation: cooperate when `len(opponent_history) == 0 or opponent_history.count(1) == 0 or len(opponent_history) % 50 < 2`, otherwise defect.

## S202 opportunity 7

Outcome: `completed`. External invocation: 26.

Native parent: slot 3, training 2.651720248166949; inspiration slots: [0].

Valid: True; original training: 2.5362380146644106; duplicate of slot: 5.
Original source: `results/e3/continuation_v1/runs/S202/gen_7/main.py`; SHA-256 `f10d41828a82b0716d21b12e3d60d2102411c4e51c935a7aa9d75a9658be4cb5`.

```python
# EVOLVE-BLOCK-START
def policy(own_history, opponent_history):
    return 0 if len(opponent_history) == 0 else opponent_history[-1]
# EVOLVE-BLOCK-END
```

Branch explanation: cooperate when `len(opponent_history) == 0`, otherwise return `opponent_history[-1]` (0 means cooperate, 1 means defect).

## S202 opportunity 8

Outcome: `completed`. External invocation: 27.

Native parent: slot 4, training 2.655386350817823; inspiration slots: [0].

Valid: True; original training: 2.5362380146644106; duplicate of slot: 5.
Original source: `results/e3/continuation_v1/runs/S202/gen_8/main.py`; SHA-256 `f10d41828a82b0716d21b12e3d60d2102411c4e51c935a7aa9d75a9658be4cb5`.

```python
# EVOLVE-BLOCK-START
def policy(own_history, opponent_history):
    return 0 if len(opponent_history) == 0 else opponent_history[-1]
# EVOLVE-BLOCK-END
```

Branch explanation: cooperate when `len(opponent_history) == 0`, otherwise return `opponent_history[-1]` (0 means cooperate, 1 means defect).

## S202 opportunity 9

Outcome: `completed`. External invocation: 28.

Native parent: slot 5, training 2.5362380146644106; inspiration slots: [0].

Valid: True; original training: 2.655386350817823; duplicate of slot: 0.
Original source: `results/e3/continuation_v1/runs/S202/gen_9/main.py`; SHA-256 `fc938dea6c869791ffb3d7fbbb03f95b21ea86152fb3414345a9d107323d56a1`.

```python
# EVOLVE-BLOCK-START
def policy(own_history, opponent_history):
    return 0 if len(opponent_history) == 0 or opponent_history.count(1) == 0 else 1
# EVOLVE-BLOCK-END
```

Branch explanation: cooperate when `len(opponent_history) == 0 or opponent_history.count(1) == 0`, otherwise defect.

## S202 opportunity 10

Outcome: `completed`. External invocation: 29.

Native parent: slot 3, training 2.651720248166949; inspiration slots: [0].

Valid: True; original training: 2.655386350817823; duplicate of slot: 0.
Original source: `results/e3/continuation_v1/runs/S202/gen_10/main.py`; SHA-256 `fc938dea6c869791ffb3d7fbbb03f95b21ea86152fb3414345a9d107323d56a1`.

```python
# EVOLVE-BLOCK-START
def policy(own_history, opponent_history):
    return 0 if len(opponent_history) == 0 or opponent_history.count(1) == 0 else 1
# EVOLVE-BLOCK-END
```

Branch explanation: cooperate when `len(opponent_history) == 0 or opponent_history.count(1) == 0`, otherwise defect.

## S202 opportunity 11

Outcome: `completed`. External invocation: 30.

Native parent: slot 9, training 2.655386350817823; inspiration slots: [0].

Valid: True; original training: 2.5362380146644106; duplicate of slot: 5.
Original source: `results/e3/continuation_v1/runs/S202/gen_11/main.py`; SHA-256 `f10d41828a82b0716d21b12e3d60d2102411c4e51c935a7aa9d75a9658be4cb5`.

```python
# EVOLVE-BLOCK-START
def policy(own_history, opponent_history):
    return 0 if len(opponent_history) == 0 else opponent_history[-1]
# EVOLVE-BLOCK-END
```

Branch explanation: cooperate when `len(opponent_history) == 0`, otherwise return `opponent_history[-1]` (0 means cooperate, 1 means defect).

## S202 opportunity 12

Outcome: `completed`. External invocation: 31.

Native parent: slot 6, training 2.6402989283699942; inspiration slots: [0].

Valid: True; original training: 2.651720248166949; duplicate of slot: 3.
Original source: `results/e3/continuation_v1/runs/S202/gen_12/main.py`; SHA-256 `f75616963be773f87e1f763e19da530af6529cecb2f9c28fab0fc1c8d15bd67a`.

```python
# EVOLVE-BLOCK-START
def policy(own_history, opponent_history):
    return 0 if opponent_history.count(1) < 2 else 1
# EVOLVE-BLOCK-END
```

Branch explanation: cooperate when `opponent_history.count(1) < 2`, otherwise defect.

## S202 opportunity 13

Outcome: `completed`. External invocation: 32.

Native parent: slot 10, training 2.655386350817823; inspiration slots: [0].

Valid: True; original training: 2.5362380146644106; duplicate of slot: 5.
Original source: `results/e3/continuation_v1/runs/S202/gen_13/main.py`; SHA-256 `f10d41828a82b0716d21b12e3d60d2102411c4e51c935a7aa9d75a9658be4cb5`.

```python
# EVOLVE-BLOCK-START
def policy(own_history, opponent_history):
    return 0 if len(opponent_history) == 0 else opponent_history[-1]
# EVOLVE-BLOCK-END
```

Branch explanation: cooperate when `len(opponent_history) == 0`, otherwise return `opponent_history[-1]` (0 means cooperate, 1 means defect).

## S202 opportunity 14

Outcome: `completed`. External invocation: 33.

Native parent: slot 12, training 2.651720248166949; inspiration slots: [0].

Valid: True; original training: 2.5362380146644106; duplicate of slot: 5.
Original source: `results/e3/continuation_v1/runs/S202/gen_14/main.py`; SHA-256 `f10d41828a82b0716d21b12e3d60d2102411c4e51c935a7aa9d75a9658be4cb5`.

```python
# EVOLVE-BLOCK-START
def policy(own_history, opponent_history):
    return 0 if len(opponent_history) == 0 else opponent_history[-1]
# EVOLVE-BLOCK-END
```

Branch explanation: cooperate when `len(opponent_history) == 0`, otherwise return `opponent_history[-1]` (0 means cooperate, 1 means defect).

## S202 opportunity 15

Outcome: `completed`. External invocation: 34.

Native parent: slot 14, training 2.5362380146644106; inspiration slots: [0].

Valid: True; original training: 2.596587704455725; duplicate of slot: None.
Original source: `results/e3/continuation_v1/runs/S202/gen_15/main.py`; SHA-256 `7e8d1f3b0bbe4f5bce2db5bb7e234d5b6153a8646a20ca257812515ae694f32a`.

```python
# EVOLVE-BLOCK-START
def policy(own_history, opponent_history):
    return 0 if len(opponent_history) == 0 or opponent_history.count(1) == 0 or (len(opponent_history) > 1 and opponent_history[-1] == 0 and opponent_history[-2] == 0) else 1
# EVOLVE-BLOCK-END
```

Branch explanation: cooperate when `len(opponent_history) == 0 or opponent_history.count(1) == 0 or (len(opponent_history) > 1 and opponent_history[-1] == 0 and (opponent_history[-2] == 0))`, otherwise defect.

## S202 opportunity 16

Outcome: `completed`. External invocation: 35.

Native parent: slot 9, training 2.655386350817823; inspiration slots: [0].

Valid: True; original training: 2.5362380146644106; duplicate of slot: 5.
Original source: `results/e3/continuation_v1/runs/S202/gen_16/main.py`; SHA-256 `f10d41828a82b0716d21b12e3d60d2102411c4e51c935a7aa9d75a9658be4cb5`.

```python
# EVOLVE-BLOCK-START
def policy(own_history, opponent_history):
    return 0 if len(opponent_history) == 0 else opponent_history[-1]
# EVOLVE-BLOCK-END
```

Branch explanation: cooperate when `len(opponent_history) == 0`, otherwise return `opponent_history[-1]` (0 means cooperate, 1 means defect).

## S202 opportunity 17

Outcome: `completed`. External invocation: 36.

Native parent: slot 4, training 2.655386350817823; inspiration slots: [0].

Valid: True; original training: 2.6259165256627184; duplicate of slot: None.
Original source: `results/e3/continuation_v1/runs/S202/gen_17/main.py`; SHA-256 `cf4f2ba132accc8d045654f68e70b620b648020580dae517a8be829a873ea314`.

```python
# EVOLVE-BLOCK-START
def policy(own_history, opponent_history):
    return 0 if len(opponent_history) == 0 or opponent_history.count(1) == 0 or (len(opponent_history) >= 3 and opponent_history[-1] == 0 and opponent_history[-2] == 0 and opponent_history[-3] == 0) else 1
# EVOLVE-BLOCK-END
```

Branch explanation: cooperate when `len(opponent_history) == 0 or opponent_history.count(1) == 0 or (len(opponent_history) >= 3 and opponent_history[-1] == 0 and (opponent_history[-2] == 0) and (opponent_history[-3] == 0))`, otherwise defect.

## S202 opportunity 18

Outcome: `completed`. External invocation: 37.

Native parent: slot 0, training 2.655386350817823; inspiration slots: [4].

Valid: True; original training: 2.3367174280879865; duplicate of slot: None.
Original source: `results/e3/continuation_v1/runs/S202/gen_18/main.py`; SHA-256 `d381a190e7d53948c5ccabe5e633828f810871b0e2632685b912add4ad75792a`.

```python
# EVOLVE-BLOCK-START
def policy(own_history, opponent_history):
    return 0 if len(opponent_history) == 0 else (1 if opponent_history.count(1) > 0 or len(opponent_history) > 5 else 0)
# EVOLVE-BLOCK-END
```

Branch explanation: cooperate when `len(opponent_history) == 0`, otherwise defect when `opponent_history.count(1) > 0 or len(opponent_history) > 5`, otherwise cooperate.

## S202 opportunity 19

Outcome: `completed`. External invocation: 38.

Native parent: slot 3, training 2.651720248166949; inspiration slots: [0].

Valid: True; original training: 2.655386350817823; duplicate of slot: 0.
Original source: `results/e3/continuation_v1/runs/S202/gen_19/main.py`; SHA-256 `fc938dea6c869791ffb3d7fbbb03f95b21ea86152fb3414345a9d107323d56a1`.

```python
# EVOLVE-BLOCK-START
def policy(own_history, opponent_history):
    return 0 if len(opponent_history) == 0 or opponent_history.count(1) == 0 else 1
# EVOLVE-BLOCK-END
```

Branch explanation: cooperate when `len(opponent_history) == 0 or opponent_history.count(1) == 0`, otherwise defect.

## S202 opportunity 20

Outcome: `completed`. External invocation: 39.

Native parent: slot 9, training 2.655386350817823; inspiration slots: [0].

Valid: False; original training: -1.0; duplicate of slot: None.
Original source: `results/e3/continuation_v1/runs/S202/gen_20/main.py`; SHA-256 `2ef6bb2476bdc911bd7bfa7d685092a524da2b17e7b4f3414f4c8ce7ae6136f3`.

```python
# EVOLVE-BLOCK-START
def policy(own_history, opponent_history):
    return 0 if len(opponent_history) == 0 or opponent_history.count(1) == 0 or (len(opponent_history) >= 3 and opponent_history[-3:] == (0, 0, 0)) else 1
# EVOLVE-BLOCK-END
```

Branch explanation: cooperate when `len(opponent_history) == 0 or opponent_history.count(1) == 0 or (len(opponent_history) >= 3 and opponent_history[-3:] == (0, 0, 0))`, otherwise defect.

## S303 opportunity 1

Outcome: `completed`. External invocation: 40.

Native parent: slot 0, training 2.655386350817823; inspiration slots: [].

Valid: True; original training: 2.5362380146644106; duplicate of slot: None.
Original source: `results/e3/continuation_v1/runs/S303/gen_1/main.py`; SHA-256 `f10d41828a82b0716d21b12e3d60d2102411c4e51c935a7aa9d75a9658be4cb5`.

```python
# EVOLVE-BLOCK-START
def policy(own_history, opponent_history):
    return 0 if len(opponent_history) == 0 else opponent_history[-1]
# EVOLVE-BLOCK-END
```

Branch explanation: cooperate when `len(opponent_history) == 0`, otherwise return `opponent_history[-1]` (0 means cooperate, 1 means defect).

## S303 opportunity 2

Outcome: `completed`. External invocation: 41.

Native parent: slot 0, training 2.655386350817823; inspiration slots: [1].

Valid: True; original training: 2.4740552735476595; duplicate of slot: None.
Original source: `results/e3/continuation_v1/runs/S303/gen_2/main.py`; SHA-256 `f6d1e447fb48167251b26f699102abc502b6e36a7d6ab2e47d76336b8e0a731a`.

```python
# EVOLVE-BLOCK-START
def policy(own_history, opponent_history):
    return 1 if len(opponent_history) > 1 and opponent_history[-1] == 1 and opponent_history[-2] == 1 else 0
# EVOLVE-BLOCK-END
```

Branch explanation: defect when `len(opponent_history) > 1 and opponent_history[-1] == 1 and (opponent_history[-2] == 1)`, otherwise cooperate.

## S303 opportunity 3

Outcome: `completed`. External invocation: 42.

Native parent: slot 1, training 2.5362380146644106; inspiration slots: [0].

Valid: True; original training: 2.655386350817823; duplicate of slot: 0.
Original source: `results/e3/continuation_v1/runs/S303/gen_3/main.py`; SHA-256 `fc938dea6c869791ffb3d7fbbb03f95b21ea86152fb3414345a9d107323d56a1`.

```python
# EVOLVE-BLOCK-START
def policy(own_history, opponent_history):
    return 0 if len(opponent_history) == 0 or opponent_history.count(1) == 0 else 1
# EVOLVE-BLOCK-END
```

Branch explanation: cooperate when `len(opponent_history) == 0 or opponent_history.count(1) == 0`, otherwise defect.

## S303 opportunity 4

Outcome: `completed`. External invocation: 43.

Native parent: slot 0, training 2.655386350817823; inspiration slots: [3].

Valid: True; original training: 2.084743372814439; duplicate of slot: None.
Original source: `results/e3/continuation_v1/runs/S303/gen_4/main.py`; SHA-256 `e3e547f798beadeb83b2bf93e999d69b685ea91eecf92ba65eec61b797f3f354`.

```python
# EVOLVE-BLOCK-START
def policy(own_history, opponent_history):
    return 0 if len(opponent_history) == 0 else (1 if opponent_history.count(1) == 0 and len(opponent_history) >= 8 else (0 if opponent_history[-1] == 1 else 1 if own_history[-1] == 1 else 0))
# EVOLVE-BLOCK-END
```

Branch explanation: cooperate when `len(opponent_history) == 0`, otherwise defect when `opponent_history.count(1) == 0 and len(opponent_history) >= 8`, otherwise cooperate when `opponent_history[-1] == 1`, otherwise defect when `own_history[-1] == 1`, otherwise cooperate.

## S303 opportunity 5

Outcome: `completed`. External invocation: 44.

Native parent: slot 1, training 2.5362380146644106; inspiration slots: [0].

Valid: True; original training: 2.655386350817823; duplicate of slot: 0.
Original source: `results/e3/continuation_v1/runs/S303/gen_5/main.py`; SHA-256 `fc938dea6c869791ffb3d7fbbb03f95b21ea86152fb3414345a9d107323d56a1`.

```python
# EVOLVE-BLOCK-START
def policy(own_history, opponent_history):
    return 0 if len(opponent_history) == 0 or opponent_history.count(1) == 0 else 1
# EVOLVE-BLOCK-END
```

Branch explanation: cooperate when `len(opponent_history) == 0 or opponent_history.count(1) == 0`, otherwise defect.

## S303 opportunity 6

Outcome: `completed`. External invocation: 45.

Native parent: slot 5, training 2.655386350817823; inspiration slots: [0].

Valid: True; original training: 2.5362380146644106; duplicate of slot: None.
Original source: `results/e3/continuation_v1/runs/S303/gen_6/main.py`; SHA-256 `7509a8317f7009e4634e3bbf2322edbb59c97f7f8c4a89b187c0277f29a43e67`.

```python
# EVOLVE-BLOCK-START
def policy(own_history, opponent_history):
    return 0 if len(opponent_history) == 0 or opponent_history[-1] == 0 else 1
# EVOLVE-BLOCK-END
```

Branch explanation: cooperate when `len(opponent_history) == 0 or opponent_history[-1] == 0`, otherwise defect.

## S303 opportunity 7

Outcome: `completed`. External invocation: 46.

Native parent: slot 0, training 2.655386350817823; inspiration slots: [3].

Valid: True; original training: 2.5362380146644106; duplicate of slot: 1.
Original source: `results/e3/continuation_v1/runs/S303/gen_7/main.py`; SHA-256 `f10d41828a82b0716d21b12e3d60d2102411c4e51c935a7aa9d75a9658be4cb5`.

```python
# EVOLVE-BLOCK-START
def policy(own_history, opponent_history):
    return 0 if len(opponent_history) == 0 else opponent_history[-1]
# EVOLVE-BLOCK-END
```

Branch explanation: cooperate when `len(opponent_history) == 0`, otherwise return `opponent_history[-1]` (0 means cooperate, 1 means defect).

## S303 opportunity 8

Outcome: `completed`. External invocation: 47.

Native parent: slot 6, training 2.5362380146644106; inspiration slots: [0].

Valid: True; original training: 2.655386350817823; duplicate of slot: 0.
Original source: `results/e3/continuation_v1/runs/S303/gen_8/main.py`; SHA-256 `fc938dea6c869791ffb3d7fbbb03f95b21ea86152fb3414345a9d107323d56a1`.

```python
# EVOLVE-BLOCK-START
def policy(own_history, opponent_history):
    return 0 if len(opponent_history) == 0 or opponent_history.count(1) == 0 else 1
# EVOLVE-BLOCK-END
```

Branch explanation: cooperate when `len(opponent_history) == 0 or opponent_history.count(1) == 0`, otherwise defect.

## S303 opportunity 9

Outcome: `completed`. External invocation: 48.

Native parent: slot 0, training 2.655386350817823; inspiration slots: [3].

Valid: True; original training: 2.067540891144952; duplicate of slot: None.
Original source: `results/e3/continuation_v1/runs/S303/gen_9/main.py`; SHA-256 `5e2435f26659ecd839a1ddb3d5d8696625158ba6040ec89d13a8521072e065e1`.

```python
# EVOLVE-BLOCK-START
def policy(own_history, opponent_history):
    return 0 if len(opponent_history) == 0 else (1 if opponent_history[-1] == 0 and opponent_history.count(1) == 0 and len(opponent_history) % 83 == 0 else (0 if opponent_history[-1] == 1 and own_history[-1] == 1 else opponent_history[-1]))
# EVOLVE-BLOCK-END
```

Branch explanation: cooperate when `len(opponent_history) == 0`, otherwise defect when `opponent_history[-1] == 0 and opponent_history.count(1) == 0 and (len(opponent_history) % 83 == 0)`, otherwise cooperate when `opponent_history[-1] == 1 and own_history[-1] == 1`, otherwise return `opponent_history[-1]` (0 means cooperate, 1 means defect).

## S303 opportunity 10

Outcome: `completed`. External invocation: 49.

Native parent: slot 8, training 2.655386350817823; inspiration slots: [0].

Valid: True; original training: 2.655386350817823; duplicate of slot: None.
Original source: `results/e3/continuation_v1/runs/S303/gen_10/main.py`; SHA-256 `d3dfd85d89b59cb346276d4913e3fc3af812a3cf56fc4eeabfb09d461f27eb7a`.

```python
# EVOLVE-BLOCK-START
def policy(own_history, opponent_history):
    return 1 if len(opponent_history) > 0 and opponent_history.count(1) > 0 else 0
# EVOLVE-BLOCK-END
```

Branch explanation: defect when `len(opponent_history) > 0 and opponent_history.count(1) > 0`, otherwise cooperate.

## S303 opportunity 11

Outcome: `completed`. External invocation: 50.

Native parent: slot 2, training 2.4740552735476595; inspiration slots: [0].

Valid: True; original training: 2.655386350817823; duplicate of slot: 0.
Original source: `results/e3/continuation_v1/runs/S303/gen_11/main.py`; SHA-256 `fc938dea6c869791ffb3d7fbbb03f95b21ea86152fb3414345a9d107323d56a1`.

```python
# EVOLVE-BLOCK-START
def policy(own_history, opponent_history):
    return 0 if len(opponent_history) == 0 or opponent_history.count(1) == 0 else 1
# EVOLVE-BLOCK-END
```

Branch explanation: cooperate when `len(opponent_history) == 0 or opponent_history.count(1) == 0`, otherwise defect.

## S303 opportunity 12

Outcome: `completed`. External invocation: 51.

Native parent: slot 0, training 2.655386350817823; inspiration slots: [3].

Valid: True; original training: 2.5362380146644106; duplicate of slot: 1.
Original source: `results/e3/continuation_v1/runs/S303/gen_12/main.py`; SHA-256 `f10d41828a82b0716d21b12e3d60d2102411c4e51c935a7aa9d75a9658be4cb5`.

```python
# EVOLVE-BLOCK-START
def policy(own_history, opponent_history):
    return 0 if len(opponent_history) == 0 else opponent_history[-1]
# EVOLVE-BLOCK-END
```

Branch explanation: cooperate when `len(opponent_history) == 0`, otherwise return `opponent_history[-1]` (0 means cooperate, 1 means defect).

## S303 opportunity 13

Outcome: `completed`. External invocation: 52.

Native parent: slot 12, training 2.5362380146644106; inspiration slots: [0].

Valid: True; original training: 2.4740552735476595; duplicate of slot: 2.
Original source: `results/e3/continuation_v1/runs/S303/gen_13/main.py`; SHA-256 `f6d1e447fb48167251b26f699102abc502b6e36a7d6ab2e47d76336b8e0a731a`.

```python
# EVOLVE-BLOCK-START
def policy(own_history, opponent_history):
    return 1 if len(opponent_history) > 1 and opponent_history[-1] == 1 and opponent_history[-2] == 1 else 0
# EVOLVE-BLOCK-END
```

Branch explanation: defect when `len(opponent_history) > 1 and opponent_history[-1] == 1 and (opponent_history[-2] == 1)`, otherwise cooperate.

## S303 opportunity 14

Outcome: `completed`. External invocation: 53.

Native parent: slot 11, training 2.655386350817823; inspiration slots: [0].

Valid: True; original training: 2.5362380146644106; duplicate of slot: 1.
Original source: `results/e3/continuation_v1/runs/S303/gen_14/main.py`; SHA-256 `f10d41828a82b0716d21b12e3d60d2102411c4e51c935a7aa9d75a9658be4cb5`.

```python
# EVOLVE-BLOCK-START
def policy(own_history, opponent_history):
    return 0 if len(opponent_history) == 0 else opponent_history[-1]
# EVOLVE-BLOCK-END
```

Branch explanation: cooperate when `len(opponent_history) == 0`, otherwise return `opponent_history[-1]` (0 means cooperate, 1 means defect).

## S303 opportunity 15

Outcome: `completed`. External invocation: 54.

Native parent: slot 7, training 2.5362380146644106; inspiration slots: [0].

Valid: True; original training: 2.655386350817823; duplicate of slot: 0.
Original source: `results/e3/continuation_v1/runs/S303/gen_15/main.py`; SHA-256 `fc938dea6c869791ffb3d7fbbb03f95b21ea86152fb3414345a9d107323d56a1`.

```python
# EVOLVE-BLOCK-START
def policy(own_history, opponent_history):
    return 0 if len(opponent_history) == 0 or opponent_history.count(1) == 0 else 1
# EVOLVE-BLOCK-END
```

Branch explanation: cooperate when `len(opponent_history) == 0 or opponent_history.count(1) == 0`, otherwise defect.

## S303 opportunity 16

Outcome: `completed`. External invocation: 55.

Native parent: slot 6, training 2.5362380146644106; inspiration slots: [0].

Valid: True; original training: 2.655386350817823; duplicate of slot: 0.
Original source: `results/e3/continuation_v1/runs/S303/gen_16/main.py`; SHA-256 `fc938dea6c869791ffb3d7fbbb03f95b21ea86152fb3414345a9d107323d56a1`.

```python
# EVOLVE-BLOCK-START
def policy(own_history, opponent_history):
    return 0 if len(opponent_history) == 0 or opponent_history.count(1) == 0 else 1
# EVOLVE-BLOCK-END
```

Branch explanation: cooperate when `len(opponent_history) == 0 or opponent_history.count(1) == 0`, otherwise defect.

## S303 opportunity 17

Outcome: `completed`. External invocation: 56.

Native parent: slot 10, training 2.655386350817823; inspiration slots: [0].

Valid: True; original training: 2.084743372814439; duplicate of slot: None.
Original source: `results/e3/continuation_v1/runs/S303/gen_17/main.py`; SHA-256 `9126992e4c91e4830228675374b36e58ee00c3c4c66e4700eb35bc7048ddcac6`.

```python
# EVOLVE-BLOCK-START
def policy(own_history, opponent_history):
    return 1 if len(opponent_history) == 8 and opponent_history.count(1) == 0 else (1 if len(opponent_history) > 8 and opponent_history.count(1) == 0 else 0)
# EVOLVE-BLOCK-END
```

Branch explanation: defect when `len(opponent_history) == 8 and opponent_history.count(1) == 0`, otherwise defect when `len(opponent_history) > 8 and opponent_history.count(1) == 0`, otherwise cooperate.

## S303 opportunity 18

Outcome: `completed`. External invocation: 57.

Native parent: slot 3, training 2.655386350817823; inspiration slots: [0].

Valid: True; original training: 2.5362380146644106; duplicate of slot: None.
Original source: `results/e3/continuation_v1/runs/S303/gen_18/main.py`; SHA-256 `9831bfc751805300bf341d2bb9c649e5e30916c3114e4d39ac7af8115c91078f`.

```python
# EVOLVE-BLOCK-START
def policy(own_history, opponent_history):
    return 0 if len(own_history) == 0 else (own_history[-1] if own_history[-1] == opponent_history[-1] else (1 - own_history[-1]))
# EVOLVE-BLOCK-END
```

Branch explanation: cooperate when `len(own_history) == 0`, otherwise return `own_history[-1]` (0 means cooperate, 1 means defect) when `own_history[-1] == opponent_history[-1]`, otherwise return `1 - own_history[-1]` (0 means cooperate, 1 means defect).

## S303 opportunity 19

Outcome: `completed`. External invocation: 58.

Native parent: slot 10, training 2.655386350817823; inspiration slots: [0].

Valid: True; original training: 2.5362380146644106; duplicate of slot: 6.
Original source: `results/e3/continuation_v1/runs/S303/gen_19/main.py`; SHA-256 `7509a8317f7009e4634e3bbf2322edbb59c97f7f8c4a89b187c0277f29a43e67`.

```python
# EVOLVE-BLOCK-START
def policy(own_history, opponent_history):
    return 0 if len(opponent_history) == 0 or opponent_history[-1] == 0 else 1
# EVOLVE-BLOCK-END
```

Branch explanation: cooperate when `len(opponent_history) == 0 or opponent_history[-1] == 0`, otherwise defect.

## S303 opportunity 20

Outcome: `completed`. External invocation: 59.

Native parent: slot 8, training 2.655386350817823; inspiration slots: [0].

Valid: True; original training: 2.5362380146644106; duplicate of slot: 1.
Original source: `results/e3/continuation_v1/runs/S303/gen_20/main.py`; SHA-256 `f10d41828a82b0716d21b12e3d60d2102411c4e51c935a7aa9d75a9658be4cb5`.

```python
# EVOLVE-BLOCK-START
def policy(own_history, opponent_history):
    return 0 if len(opponent_history) == 0 else opponent_history[-1]
# EVOLVE-BLOCK-END
```

Branch explanation: cooperate when `len(opponent_history) == 0`, otherwise return `opponent_history[-1]` (0 means cooperate, 1 means defect).
