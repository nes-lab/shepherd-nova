# Instance at TU Dresden

For now (February 2026) the testbed is reshaped to mimic an elongated multihop mesh-network on the lower part of the office-map.

The initial deployment covered the ring of offices around the buildings ventilation system.
The inner structure mostly blocks RF due to lots of metal vents.
10 - 14 shepherd observers were used for the testrun.
Unfortunately the RF-Performance of the nodes was not strong enough to close the gap between II62 and II75 (left side of plan).

## Deployment

Below is a screenshot of the [Campus-Navigator](https://navigator.tu-dresden.de/etplan/bar/02) with marked node-positions.

```{figure} /media/cfaed_floorplan_current.png
:align: center
:alt: CFAED floor with marked node-positions

**CFAED floor with marked node-positions**.
Most horizontal walls are concrete, while the walls between offices are drywall.
```

## Link-Matrix

The link-matrix of the testbed is currently measured mostly after changes in deployment.
It is planned to offer weekly scans in the future while also keeping the history available.

```{code-block}
:caption: [TrafficBench](https://github.com/nes-lab/TrafficBench) RF-survey from 2026-02-07, all nodes, values in dBm
Tx⟍Rx     1     2     3     4     5     6     7     8     9    10    11
     +-----------------------------------------------------------------
   1 |        -36   -57   -64   -67   -73   -84   -81
   2 |  -37         -49   -65   -64   -69         -83
   3 |  -57   -49         -56   -49   -60   -86   -76
   4 |  -63   -64   -55         -44   -49   -70   -60
   5 |  -67   -63   -48   -44         -53   -68   -70
   6 |  -73   -68   -59   -49   -53         -59   -64   -80   -78
   7 |  -83         -85   -70   -67   -58         -53   -76   -61   -77
   8 |  -82   -82   -76   -61   -71   -65   -54         -85   -73
   9 |                                -80   -77   -84         -40   -74
  10 |                                -79   -62   -73   -41         -82
  11 |                                      -78         -74   -82
```

## Changes in near Future

Currently new hardware is manufactured, validated and calibrated.

With the official public release of the testbed in January 2026 it is planned to roll out an extended layout:

```{figure} /media/cfaed_floorplan_with_nodes.png
:align: center
:alt: CFAED floor with marked future node-positions

**floor with marked future node-positions**.
Most horizontal walls are concrete, while the walls between offices are drywall.
```

### What does that mean for the user?

- number of observable GPIO from the target increases from 9 to 12, [see table here](https://github.com/nes-lab/shepherd-targets/tree/main/hardware/shepherd_nRF_FRAM_Target_v1.3)
- two power good signals to communicate current state of the virtual source to the target ([similar to Riotee](https://www.riotee.nessie-circuits.de/docs/latest/hardware/module.html)) for more advanced intermittent computing algorithms
- usable node-count increases from 11 to 20+ for enabling more complex scenarios and a wider range of topologies
