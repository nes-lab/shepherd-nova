# Account & Access

## Getting an Account

If you are interested in trying out the testbed please contact us via mail: <testbed@nes-lab.org>.
We will provide you an access-token in time.

```{note}
1) Your e-mail address is acting as your account name and is needed on the server for sending you updates on i.e. finished experiments.
2) To comply with [privacy law](/about/privacy.md) we will disable accounts that have been inactive for 18 month and delete the account in the following clean-up-cycle, no later than 6 months after deactivation.
3) The testbed is a best-effort service. Availability and functionality [is not guaranteed](/about/disclaimer.md).
```

## Quota

To ensure a good experience for every user we will start with the following fair-use quotas:

- **Duration** of an experiment is limited to 60 minutes. Submissions to the testbed must have a valid duration specified.
- **Storage** of each user is limited to 200 GiB. Users being over quota won't be able to schedule new experiments. Old data must be deleted first.

It's by no means a one-size-fits-all.
If your setup requires temporary customization of quotas, feel free to contact us.

Let's look at some numbers to bring the storage quota into perspective.
Depending on the use-case the 200 GiB can either hold 1 hour or several hundred.
`GPIOTraces` produce 10 bytes per sample (2 byte value, 8 byte timestamp).
So the sample-stream of continuous UART with 115 kBaud from the target results in roughly 1.2 MB/s.
`PowerTraces` are in a similar ballpark with 16 bytes per sample (2*4 byte value, 8 byte timestamp).
The sampling-rate of 100 kHz produces 1.6 MB/s data per node.

```{tip}
How to get by with storage quotas:

- GPIO- and Power-tracers can be limited to a specific timeframe, or be disabled completely
- a UART-tracer can directly decode the GPIO-stream and only timestamps a line of text
- data can be deleted, even without downloading it
```

## Access via Token

To access the testbed with your token you just add it to your config:

```{attention}
TODO: show how to use a token safely via

- env-var,
- separate file,
- config in xdg-path
```
