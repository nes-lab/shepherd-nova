# Account & Access

## Getting an Account

If you are interested in trying out the testbed, please contact us via mail: <testbed@nes-lab.org>.
We will provide you a registration-token in time.
This token is bound to the e-mail address and allows creating an account.
Please read through the [disclaimer](/about/disclaimer.md) and [privacy policy](/about/privacy.md) prior to registration.

```{note}
1) Your e-mail address is acting as your account name and is needed on the server for sending updates on i.e. finished experiments.
2) To comply with [privacy law](/about/privacy.md), we will disable accounts that have been inactive for 18 month and delete the account in the following clean-up-cycle, no later than 6 months after deactivation.
3) The testbed is a best-effort service. Availability and functionality [is not guaranteed](/about/disclaimer.md).
```

## Quota

To ensure a good user-experience for everyone we will start with the following fair-use quotas:

- **Duration** of an experiment is limited to 60 minutes. Submissions to the testbed must have a valid duration specified.
- **Storage** of each user is limited to 200 GiB. Users being over quota won't be able to schedule new experiments. Old data must be deleted first from the testbed-server.

It's by no means a one-size-fits-all.
If your setup requires temporary customization of quotas, feel free to contact us.

```{tip}
The [getting started guide](/content/getting_started.md#reduce-size-of-result-files) includes a section that highlights options to reduce the size of result-files.
```

## Registration & Access

To access the testbed, you will need the webclient written in Python.
You can install the client by using the package-manager of your choice.
In the following case we use pip:

```Shell
pip3 install shepherd-client -U
```

With it, you can manage your account and experiments.
You have the option to save your credentials in your `XDG-config`-directory (i.e. `$HOME/.config/shepherd`).
That way you can safely host your later scripts in public repositories without leaking data.
For registering an account you can fill out & run the following snippet once:

```{literalinclude} access_registration.py
:language: python
:start-after: start example
:end-before: end example
```

A few notes to explain the behavior:

- registration is possible as soon as you receive a custom token via mail
- passwords need to be between 10 and 64 characters (all printable ASCII)
- if you omit the password, the client will create a custom one for you
- it is possible to trigger a forgot-password-routine (you can also back up the config-file)
- choosing `save_credentials` will overwrite the local config (or create a new one)

Once saved, you can omit the credentials, as shown here:

```{literalinclude} access_user.py
:language: python
:start-after: start example
:end-before: end example
```

The next steps are explained in the [getting started guide](/content/getting_started.md)
