import typer
from typing import Annotated

from communex._common import get_node_url  # type: ignore
from communex.client import CommuneClient  # type: ignore
from communex.compat.key import classic_load_key  # type: ignore

from validator.validator import CommunityContributionValidator
from validator._config import ValidatorSettings

app = typer.Typer()

@app.command("serve-subnet")
def serve(
    commune_key: Annotated[
        str, typer.Argument(help="Name of the key present in `~/.commune/key`")
    ],
    call_timeout: int = 65,
):
    keypair = classic_load_key(commune_key)  # type: ignore
    settings = ValidatorSettings()  # type: ignore
    c_client = CommuneClient(get_node_url())
    subnet_uid = get_subnet_netuid(c_client, "Community Contribution Subnet")  # Adjust to your subnet name
    validator = CommunityContributionValidator(keypair, subnet_uid, c_client, call_timeout=call_timeout,)

    # Start validation loop
    validator.validation_loop(settings)

if __name__ == "__main__":
    typer.run(serve)
