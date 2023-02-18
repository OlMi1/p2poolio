# P2Pool IO
Python program to read data from the [Monero P2Pool](https://github.com/SChernykh/p2pool) Log File

## Usage
### Dependencies
Not really a necessary step since all dependencies should already be there. However you may not use them in your project, so here you go:
- time
- datetime
- os
- json (for debugging)

### Calling the reader

Doing `P2PoolIO.read()` anywhere will give you the readout result. You can also do
```
foo = P2PoolIO
data = foo.read()
```

### Possible arguments:
- `path` (default: p2pool.log - must point to p2pool.log)
- `returnLines` (default: False)
- `linelimit` (default: 100)

## Returned data
If you do not specify anything and there was a payout in the last 100 rows, your data may look like this:

```json
{"payout": {"amount": "0.00123456789", "timestamp": 1676707788}, "time": 0.016999244689941406}
```

`time` refers to execution time. `{}` will be returned if there was no payout. Note that only the most recent (=lowest in file) payout will be shown.

If you choose to set `returnLines` to `True`, you will get something similar to this:

```json
{"payout": {}, "time": 0.008997917175292969, "lines": [{"type": "NOTICE", "timestamp": 1676731203, "module": "StratumServer", "payout": {"payout": false}, "content": "SHARE FOUND: mainchain height 2824691, sidechain height 3890718, diff 117341323, client xy user xy, effort 40.795%"}, {}]}
```
Type stands for the message type, for instance NOTICE or WARN. Timestamp is the timestamp the message was logged, exact to the second. Module refers to whatever is the first word (ex. P2Pool, StratumServer). payout indicates whether the line contains a payout, and if yes, will show data about it (`{"amount": "0.00123456789", "timestamp": 1676707788}`).
