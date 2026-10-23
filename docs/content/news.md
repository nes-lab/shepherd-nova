# News and upcoming Events

## October 2026

Release of two QoL-Updates!
Both updates fix a lot of the bug-sources seen in recently failed experiments.
Also, the performance of the observers was improved.
There should be no harm in activating power-tracing and gpio-tracing at the same time anymore.
Because of that the server now accepts experiments with custom samplerates in PowerTracing().
See newly added [benchmark-results for more](/content/infrastructure.md#benchmarks).

```{attention}
Experiments that fail because of a high sync-offset are likely caused by too much traffic on the network.
Reducing data-rates could circumvent that.
Users can disable power-tracing or use it with lower sample-rates or only record power instead of IV-values.
As the testbed is embedded into the infrastructure of the university, the issue can also be caused by external factors.
So rescheduling a failed experiment once or twice is encouraged!
This is an ongoing issue and will hopefully be fixed in the near future.
```

## Past Events

- our [extension of deployment](/content/deployment.md) is finished. A total of 24 nodes are now selectable for experiments. (March 2026)
- the capes of the current observers got replaced with v2.5, so the number of observable GPIO increased and the target can receive two power good signals, [see here for more info](/content/deployment.md) (March 2026)
- the Launch of public access is in January 2026
- [Our Paper introducing Shepherd Nova](https://dl.acm.org/doi/10.1145/3711875.3729146) got accepted and published at [MobiSys 2025](https://www.sigmobile.org/mobisys/2025/)
- In the second half of 2023 a semi-open instance of the Shepherd testbed went live.
