# FAQ

## Maintenance

For validating and updating the infrastructure a fixed timeslot is reserved every week, monday 8 PM CET, for 4 hours.
If needed, the scheduler will be paused during that time period.
Changes in the deployment will be announced in the [news-section](./news) ahead of time.

If critical work has to be done, we reserve the right to cancel currently active experiments at any time.

## Limitations

Beside [maintenance](#maintenance) and [quota](/content/access.md#quota) there are no further limitations.
The testbed is usable 24-7 and a scheduled task has exclusive access to all observers.

## Trusting the Results

We don't expect you to trust the testbed right away.
Create an account, do some experiments, get some impressions.
We tried to document our view and measures concerning trust in the [section about infrastructure](/content/infrastructure.md#building-a-chain-of-trust).

## Lifetime of Data

We aim to offer a guaranteed storage for the result data of at least 15 days.
The maximum storage duration is currently set to 6 month.
Depending on the capacity of the file-server, old results will be deleted similar to a FIFO.

## Web-API

The API is based on [fastapi](https://github.com/fastapi/fastapi) and is publicly available.
In addition to the available sources it documents itself.
So writing your own tooling is generally possible.

We'd also like to point out, that the included redoc-website is interactive.
It allows to log in and interact with actual data.

Redoc-Documentation: <https://shepherd.cfaed.tu-dresden.de:8000/>

Sources: <https://github.com/nes-lab/shepherd-webapi>

## Contributions

Feedback is more than welcome during that initial phase. Reusable & useful scripts or firmware you developed and want to donate is also welcome.
