# mpc-solver-approx
## Compilation params
- field size = 28948022309329048855892746252171976963363056481941560715954676764349967630337 (Pasta p parameter)

## How to run

Assuming that mp-spdz is in the same dir as this repo (../MP-SPDZ-0.3.7/), 

1. to generate random ptx params, run `python3 gen-params.py` (the swap intent is hardcoded)
2. run `sh compile-run.sh strategy` to compile strategy.mpc

## Solving strategies

### First algorithm (two-party exact intent matching)
- `U1` has `H1` amount of asset `A` and wants `W1` amount of asset `B`. 
- `U2` has `H2` amount of asset `C` and wants `W2` amount of asset `D`. 

The solver receives the intents, and checks that:
- `A = D` and `B = C` (asset types match)
- `H1 = W2` and `H2 = W1` (amounts match)

### Second algorithm (two-party intent matching, variable amounts)
- `U1` has asset `A` and wants asset `B` and wants to trade them in relation `H1 : W1`, spending at most `C` of asset `A`.
- `U2` has asset `E` and wants asset `F` and wants to trade them in relation `H2 : W2`, spending at most `G` of asset `E`.

The ratio is expressed in a form `h:w`, where `h` is the amount of owned asset, `w` is the amount of wanted asset. The ratios are compatible if they are mirrored or imply users to receive more or spend less (e.g. the ratios `1:2` and `3:1` are compatible, the ratios `1:3` and `2:1` aren’t). In the presence of variable compatible ratios, for simplicity we always let one user receive more rather than the other to spend less. In practice, the decision might depend on the exact case. 

The solver receives the intents and:
1. Checks that:
    1. asset types match: `A = F` and `B = E`
    2. the ratios are compatible:
        - if `H1 = W2`, check that `H2 >= W1`
        - otherwise:
            - reassign `H1 = W2 = LCM(H1, W2)`, 
            - multiply `H2` and `W1` by the corresponding coefficients (for `H2`: `LCM(H1, W2) / W2`, for `H1`: `LCM(H1, W2) / H1`) to preserve the original relation
            - check `H2 >= W1`
        - note that we can also check the other pair of equality equations (`W1 = H2` and `H1 >= W2`) instead. In the end what matters is that one pair contains equal values and the other pair has the H parameter bigger than the W parameter
2. Determines the amount to be sent by each user wrt to the ratios and the max spend constraints. After the first step we have `H1 = W2, H2 >= W1`, the exchange ratio is `H1 : H2` (following the “give more” strategy described above. Otherwise the second parameter could be between `W1` and `H2`). To determine the exact values to be exchanged by U1 and U2:
      1. denote `U1 -> U2: X, 0 <= X <= C`
      2. denote `U2 -> U1: Y, 0 <= Y <= G`,
      3. note that `Y * H1 = X * H2`
      4. from 1 and 3: `0 <= Y * H1 <= G * H1`,
      5. from 2 and 3: `0 <= X * H2 <= C * H2`
      6. define `X * H2 = Y * H1 = min(C * H2, G * H1) = W`. Note that with such choice none of the users overpays:
          1. let's assume `W = C * H2`. Then `X = C, Y = C * H2 / H1`. Can `C * H2 / H1 > G` (the value paid by `U2` be above the upper spend limit set by `U2`)?
          2. If yes, then `C * H2 > G * H1`, which is impossible because `C * H2 = min(C * H2, G * H1)` as defined in step 6.
          3. the same reasoning works for when `W = G * H1`
      8. Define `X = W / H2, Y = W / H1`
      9. Sanity check:
         1. `W = C * H2, X = C, Y = C * H2 / H1, X : Y = H1 : H2`
         2. `W = G * H1, X = G * H1 / H2, Y = G, X : Y = H1 : H2`
