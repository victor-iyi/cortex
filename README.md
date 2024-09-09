# Cortex

[![CI](https://github.com/victor-iyi/cortex/actions/workflows/ci.yaml/badge.svg)](https://github.com/victor-iyi/cortex/actions/workflows/ci.yaml)
[![pytest](https://github.com/victor-iyi/cortex/actions/workflows/tests.yml/badge.svg)](https://github.com/victor-iyi/cortex/actions/workflows/tests.yml)
[![pre-commit.ci status](https://results.pre-commit.ci/badge/github/victor-iyi/cortex/main.svg)](https://results.pre-commit.ci/latest/github/victor-iyi/cortex/main)
[![formatter | docformatter](https://img.shields.io/badge/%20formatter-docformatter-fedcba.svg)](https://github.com/PyCQA/docformatter)
[![style | google](https://img.shields.io/badge/%20style-google-3666d6.svg)](https://google.github.io/styleguide/pyguide.html#s3.8-comments-and-docstrings)

`cortex` is an API for communicating with your Emotiv EEG device via websockets.

[![Emotiv Insight Headset](images/insight-2021.png)][insight]
*Source: [Emotiv][insight]*

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
[insight]: https://www.emotiv.com/insight/

## Getting Started

To get started, you will need to install the `cortex` package. You should check out
some [examples] to get you started.

```sh
poetry install
```

For testing and development, you can install the package with the `test` and `dev`
flags respectively.

```sh
poetry install --with test,dev
```

You'll also need to set your client id and client secret as environment variables.

```sh
export EMOTIV_CLIENT_ID="your-client-id"
export EMOTIV_CLIENT_SECRET="your-client-secret"
```

[examples]: ./examples/

## Contribution

You are very welcome to modify and use them in your own projects.

Please keep a link to the [original repository]. If you have made a fork with
substantial modifications that you feel may be useful, then please [open a new
issue on GitHub][issues] with a link and short description.

## License (MIT)

This project is opened under the [MIT][license] which allows very
broad use for both private and commercial purposes.

A few of the images used for demonstration purposes may be under copyright.
These images are included under the "fair usage" laws.

[original repository]: https://github.com/victor-iyi/cortex
[issues]: https://github.com/victor-iyi/cortex/issues
[license]: ./LICENSE
