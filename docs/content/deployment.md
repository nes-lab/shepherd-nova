# Instance at TU Dresden

Welcome to the first public deployment of the [Shepherd Nova](https://nes-lab.github.io/shepherd-nova/) testbed!
It is available for experiments all around the clock (24/7).
This page describes the physical layout and wireless connectivity between nodes.

## Physical Deployment

Our testbed is located in the cfaed offices of the Barkhausen Bau at TU Dresden.
It consists of **24 observer nodes** that form a ring‑shaped network, largely determined by the building’s ventilation system.
The many metal vents inside the ventilation system block radio signals, creating a realistic and challenging wireless environment.

### Key Topological Features

In addition to that ring-network, you can find or create the following topological features.

- **Dense cluster** on the south side of the office-map - ideal for experiments that require many nodes with direct links
- **Bottleneck** between offices II62 and II75 on the west side - useful for testing multi-hop routing
- (elongated) **U-shaped network** can be created by disabling certain nodes or reducing transmit power

### Floor Plan

The map below from the [Campus-Navigator](https://navigator.tu-dresden.de/etplan/bar/02) shows the exact positions of the nodes.

```{figure} /media/cfaed_floorplan_with_nodes.png
:align: center
:alt: CFAED floor with marked node-positions

**CFAED floor with marked node-positions**.
Most horizontal walls are concrete, while the walls between offices are drywall.
```

## Link-Matrix

The link-matrix shows the measured **RSSI (Received Signal Strength Indicator) values in dBm** between every pair of nodes.

```{code-block}
:caption: [TrafficBench](https://github.com/nes-lab/TrafficBench) RF-survey via [example-script](https://github.com/nes-lab/shepherd-webapi/blob/main/shepherd_client/examples/e3_experiment_create_and_schedule.py) from 2026-04-07, values in dBm
Tx⟍Rx     1     2     3     4     5     6     7     8     9    10    11    12    13    14    15    16    17    18    19    20    21    22    23    24
     +-----------------------------------------------------------------------------------------------------------------------------------------------
   1 |        -35   -52   -78   -61   -61   -73   -73   -80   -83   -77                                                                     -73   -69
   2 |  -35         -54   -60   -63   -63   -77   -67   -70   -85   -78                                                               -81   -61   -68
   3 |  -53   -54         -43   -40   -47   -60   -61   -73   -67   -65                                                                     -48   -48
   4 |  -76   -59   -43         -36   -42   -48   -42   -60   -66   -62                           -88                                       -37   -40
   5 |  -61   -63   -39   -37         -38   -53   -53   -55   -74   -61         -87                                                         -43   -32
   6 |  -61   -62   -46   -43   -38         -43   -47   -60   -64   -52   -86                                                               -43   -39
   7 |  -74   -77   -61   -50   -54   -44         -41   -47   -54   -63   -83   -81                                                         -52   -60
   8 |  -72   -67   -59   -43   -53   -47   -40         -54   -49   -51   -82   -83                                                         -39   -43
   9 |  -81   -72   -73   -61   -56   -61   -47   -55         -40   -48   -73   -71               -87                                       -63   -60
  10 |  -82   -83   -65   -65   -72   -63   -51   -48   -37         -44   -70   -69   -83   -86   -81   -88                                 -72   -68
  11 |  -78   -78   -65   -63   -62   -53   -63   -52   -48   -46         -77   -68         -84   -87                                       -65   -61
  12 |                    -88         -86   -81   -82   -71   -71   -76         -50   -80   -70   -65   -74   -74         -83               -86
  13 |                          -88         -80   -83   -70   -72   -68   -51         -74   -74   -71   -86                                 -88
  14 |                                                        -84         -80   -73         -77   -74   -84
  15 |                                                        -89   -84   -73   -74   -79         -53   -59   -65   -72   -75
  16 |                                                  -88   -83   -87   -65   -70   -75   -52         -50   -63   -78   -72   -84   -86
  17 |                                                        -89         -76         -84   -57   -49         -46   -66   -64   -77   -84
  18 |                                                                    -74               -63   -62   -45         -58   -60   -62   -78
  19 |                                                                    -90               -70   -78   -65   -57         -50   -53   -62
  20 |                                                                    -83               -74   -71   -64   -61   -51         -52   -78
  21 |                                                                                            -83   -78   -63   -54   -52         -50
  22 |        -81                                                                                 -86   -84   -79   -62   -78   -49
  23 |  -73   -61   -47   -37   -42   -42   -50   -38   -61   -73   -64   -85   -87                                                               -40
  24 |  -68   -66   -47   -39   -31   -38   -58   -42   -57   -69   -60                                                                     -39
```

This data helps you understand the network and configure custom topologies.

- **Rows (Tx)** represent the transmitter
- **Columns (Rx)** represent the receiver
- **Empty cells** have no direct link
- `dBm` is a logarithmic unit of power - higher values (closer to 0) are stronger links (e.g. -30 dBm is very strong, -90 dBm is very weak)

Updates are currently done manually - mainly after changes in deployment.
It is planned to offer weekly scans in the future while also keeping the history available.
A collection of past measurements and network-layouts is available [here](https://github.com/nes-lab/shepherd-nova/tree/main/docs/link_matrix).

## Impressions

```{figure} /media/deployment_conference_room.jpg
:align: center
:alt: Observer node deployed in conference room II62

Observer node deployed in conference room II62. It is mounted under the ceiling-duct and connected and powered via ethernet.
```

```{figure} /media/deployment_pre-assembly.jpg
:align: center
:alt: Observer nodes assembled - before deployment

Observer nodes are assembled and tested - right before deployment.
```
