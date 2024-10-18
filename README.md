# Community Contribution Subnet

This subnet is built on top of [CommuneX](https://github.com/agicommies/communex) and is designed to validate and incentivize community contributions through a scoring mechanism.

## Overview

The Community Contribution Subnet consists of two main components: a **Validator** and a **Miner**. The Validator assesses contributions based on quality and engagement metrics, while the Miner processes the contributions.

## Dependencies

This subnet is built on the [CommuneX library / SDK](https://github.com/agicommies/communex), which is the primary dependency. Additional libraries used can be found in the [requirements.txt](./requirements.txt) file:

```txt
communex
typer
uvicorn
keylimiter
pydantic-settings
```

## Validator

To run the validator, just call the file in which you are executing `validator.validate_loop()`. For example:

```sh
python3 -m community_contribution_subnet.subnet.validator <name-of-your-com-key>
```

## Validation Process

1. Fetch Contributions: The Validator retrieves contributions from the subnet.
2. Score Contributions: Contributions are scored based on quality and engagement metrics.
3. Set Weights: The Validator updates the weights for miners based on their scores.

## Miner

From the root of your project, you can just call **comx module serve**. For example:

```sh
comx module serve community_contribution_subnet.subnet.miner.model.ContributionMiner <name-of-your-com-key> [--subnets-whitelist <your-subnet-netuid>] [--ip <text>] [--port <number>]
```

## Contribution Processing

The Miner processes incoming contributions and performs the necessary handling as defined in its logic.

## Further Reading

For full documentation of the Commune AI ecosystem, please visit the [Official Commune Page](https://communeai.org/), and it's developer documentation. There you can learn about all subnet details, deployment, and more!
