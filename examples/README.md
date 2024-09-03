# Examples

We have a few examples to help you get started. You can find them in the [examples]
directory. Please be sure to adjust these examples to suit your purposes.

[examples]: ./

## Before you start

To run the existing example you will need to do a few things.

1. You will need an EMOTIV headset. You can purchase a headset in an [online store][emotiv]

2. Next, [download and install][developer] the Cortex service. Please note that
currently, the Cortex service is only available for Windows and macOS.

3. We have updated our Terms of Use, Privacy Policy and EULA to comply with GDPR.
Please login via the EMOTIV Launcher to read and accept our latest policies in
order to proceed using the following examples.

4. Next, to get a client id and a client secret, you must connect to your Emotiv
account on [emotiv.com][emotiv-account] and create a Cortex app. If you don't
have a EmotivID, you can [register here].

5. Then, if you have not already, you will need to login with your Emotiv id in
the EMOTIV Launcher.

6. Finally, the first time you run these examples, you also need to authorize
them in the EMOTIV Launcher.

[emotiv]: https://www.emotiv.com/
[developer]: https://www.emotiv.com/developer/
[emotiv-account]: https://www.emotiv.com/my-account/cortex-apps/
[register here]: https://id.emotivcloud.com/eoidc/account/registration/

## Samples

Here are some examples to get you started. Please be sure to refer to the
[documentation][docs] for more information.

[docs]: https://emotiv.gitbook.io/cortex-api/

### Subscribe Data

- [`subscribe.py`] shows data stream from `Headset`: EEG, Motion, Performance Metrics
and Band Power.
- For more details, please refer to the [documentation][subscribe].

[`subscribe.py`]: ./subscribe.py
[subscribe]: https://emotiv.gitbook.io/cortex-api/data-subscription

### BCI

- [`facial_expression.py`] shows facial expression training.
- [`mental_command.py`] shows mental command training.
- For more details, please refer to the [documentation][bci].

[`facial_expression.py`]: ./train/facial_expression.py
[`mental_command.py`]: ./train/mental_command.py
[bci]: https://emotiv.gitbook.io/cortex-api/bci

### Advanced BCI

- [`live_advance.py`] shows the ability to get and set sensitivity of mental command
action in live mode.
- For more details, please refer to the [documentation][advanced-bci].

[`live_advance.py`]: ./live_advance.py
[advanced-bci]: https://emotiv.gitbook.io/cortex-api/advanced-bci

### Create record and export to file

- [`record.py`] shows how to crate a record and export data to CSV or EDF format.
- For more details, please refer to the [documentation][records].

[`record.py`]: ./record.py
[records]: https://emotiv.gitbook.io/cortex-api/records

### Inject Marker while Recording

- [`marker.py`] shows how to inject marker during a recording.
- For more details, please refer to the [documentation][markers].

[`marker.py`]: ./marker.py
[markers]: https://emotiv.gitbook.io/cortex-api/markers
