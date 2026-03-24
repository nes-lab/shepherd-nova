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
It is planned to offer weekly scans in the future while also keeping the history available. A collection of past measurements is available [here](https://github.com/nes-lab/shepherd-nova/tree/main/docs/link_matrix).

```{code-block}
:caption: [TrafficBench](https://github.com/nes-lab/TrafficBench) RF-survey from 2026-03-23, all nodes, values in dBm
Tx⟍Rx     1     2     3     4     5     6     7     8     9    10    11
     +-----------------------------------------------------------------
   1 |        -33   -58   -59   -57   -71   -87   -79
   2 |  -32         -45   -60   -56   -75   -78   -78
   3 |  -59   -46         -39   -50   -52   -66   -67
   4 |  -59   -60   -38         -44   -44   -61   -62
   5 |  -57   -56   -50   -44         -52   -61   -65
   6 |  -70   -75   -52   -44   -52         -57   -60   -81   -73
   7 |  -85   -77   -64   -60   -60   -55         -42   -76   -65   -84
   8 |  -79   -79   -67   -63   -66   -61   -44         -76   -67   -88
   9 |                                -81   -77   -76         -46   -82
  10 |                                -73   -67   -67   -46         -73
  11 |                                      -85         -82   -73
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

- (done) number of observable GPIO from the target increases from 9 to 12, [see table here](https://github.com/nes-lab/shepherd-targets/tree/main/hardware/shepherd_nRF_FRAM_Target_v1.3)
- (done) two power good signals to communicate current state of the virtual source to the target ([similar to Riotee](https://www.riotee.nessie-circuits.de/docs/latest/hardware/module.html)) for more advanced intermittent computing algorithms
- usable node-count increases from 11 to 20+ for enabling more complex scenarios and a wider range of topologies
