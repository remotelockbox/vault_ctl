# Command Line Control for PiVault

PiVault is located at https://pishock.com

This project is not affiliated with PiShock or PiVault.

## Setup

You will need your account API key and a specific device API key to allow this
program to control a vault (either yours or someone else's).

First, copy the file `vault_credentials_example.ini` to `vault_credentials.ini`.
Then update it with your user name and account API key (called `user_key`).

You can generate an API key for your account by going to `Menu -> Account`
and clicking "Generate API Key".

Have the owner of the box provide an API key with appropriate permissions.
They can do this by clicking the API button and creating a key. 
The API link may not show up if the user is already in a session.

Set `box_key` to device key.

## Usage

Run `./vault_ctl.py` or `python3 vaul_ctl.py` to run the program.

These are the supported commands:

```
  --status         prints lock and session status
  --add-minutes N  minutes to add to the lock time. If not already locked, creates a new sessions
  --show-status    show the release time at the end of the command
  --unlock         unlock the lockbox
  --silent         require manual unlocking by pressing the physical button
  --clear          clear any ongoing session
```
