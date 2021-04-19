# YubiKey AWS Helper
This utility will help you configure your YubiKey as a virutal MFA device to use in AWS and refresh your local session token to interact with the API using MFA where required.  Requires `ykman` to be in your PATH prior to running, as well as boto3 to be available. **Note: when setting up the YubiKey in the AWS console, you do NOT use it as a u2f device!  We're leveraging the otp functionality baked into the YubiKey 4/5 series keys to instead generate OTP codes.  At this time, u2f is NOT supported for generating session tokens programmatically.**

## Usage
I recommend creating bash or zsh aliases for these functions - use whatever makes sense to you

`yubaws.py configure` will help you setup a new MFA device on the YubiKey and in AWS

`yubaws.py session` will get you a new session token associated with the MFA device for use with boto or awscli.  Automatically updates your `~/.aws/credentials`

`yubaws.py otp` will print an MFA code for logging into the AWS console, so you don't have to memorize the command to use `ykman`

## Known Issues
* The calls to subprocess are due to an issue with using the native Yubico Python API and macOS at the time of writing
* If you already have a file called `.mfa_device` in your `.aws` config dir, it's going to get overwritten with any new devices created using `yubaws.py configure`
* Unexpected things may happen if you have more than 1 yubikey inserted while using this utility (read: it's untested, but it might be fine?)
