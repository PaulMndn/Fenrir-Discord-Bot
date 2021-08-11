# What's this?
Before the develop branch can merge into the main branch, it needs to go throu a release workflow using the `release/`_`releaseNo.`_ branch.

# Release workflow
The release workflow includes the following steps:

## Changes in `bot.py`
* change `client.run(DEV_TOKEN)` to `client.run(TOKEN)`
* remove the check for Bot-test-channel --> Bot should answer to all messages in guild
* set logging level to `logging.INFO`

## Changes in `cfg.py`
* change Prefix to `"!"`
