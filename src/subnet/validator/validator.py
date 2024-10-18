import asyncio
import time

from communex.client import CommuneClient  # type: ignore
from communex.module.module import Module  # type: ignore
from substrateinterface import Keypair  # type: ignore

from ._config import ValidatorSettings
from ..utils import log

def set_weights(
    settings: ValidatorSettings,
    score_dict: dict[
        int, float
    ],  # implemented as a float score from 0 to 1, one being the best
    # you can implement your custom logic for scoring
    netuid: int,
    client: CommuneClient,
    key: Keypair,
) -> None:
    """
    Set weights for miners based on their scores.

    Args:
        score_dict: A dictionary mapping miner UIDs to their scores.
        netuid: The network UID.
        client: The CommuneX client.
        key: The keypair for signing transactions.
    """

    # you can replace with `max_allowed_weights` with the amount your subnet allows
    score_dict = cut_to_max_allowed_weights(score_dict, settings.max_allowed_weights)

    # Create a new dictionary to store the weighted scores
    weighted_scores: dict[int, int] = {}

    # Calculate the sum of all inverted scores
    scores = sum(score_dict.values())

    # process the scores into weights of type dict[int, int] 
    # Iterate over the items in the score_dict
    for uid, score in score_dict.items():
        # Calculate the normalized weight as an integer
        weight = int(score * 1000 / scores)

        # Add the weighted score to the new dictionary
        weighted_scores[uid] = weight


    # filter out 0 weights
    weighted_scores = {k: v for k, v in weighted_scores.items() if v != 0}

    uids = list(weighted_scores.keys())
    weights = list(weighted_scores.values())
    # send the blockchain call
    client.vote(key=key, uids=uids, weights=weights, netuid=netuid)

def cut_to_max_allowed_weights(
    score_dict: dict[int, float], max_allowed_weights: int
) -> dict[int, float]:
    """
    Cut the scores to the maximum allowed weights.

    Args:
        score_dict: A dictionary mapping miner UIDs to their scores.
        max_allowed_weights: The maximum allowed weights (default: 420).

    Returns:
        A dictionary mapping miner UIDs to their scores, where the scores have been cut to the maximum allowed weights.
    """
    # sort the score by highest to lowest
    sorted_scores = sorted(score_dict.items(), key=lambda x: x[1], reverse=True)

    # cut to max_allowed_weights
    cut_scores = sorted_scores[:max_allowed_weights]

    return dict(cut_scores)

class CommunityContributionValidator(Module):
    """
    A class for validating community contributions in a subnet.
    """

    def __init__(
        self,
        key: Keypair,
        netuid: int,
        client: CommuneClient,
        call_timeout: int = 60,
    ) -> None:
        super().__init__()
        self.client = client
        self.key = key
        self.netuid = netuid
        self.call_timeout = call_timeout

    def get_addresses(self, client: CommuneClient, netuid: int) -> dict[int, str]:
        """
        Retrieve all module addresses from the subnet.
        """
        return client.query_map_address(netuid)

    def _score_contribution(self, contribution: dict) -> float:
        """
        Score the contribution based on its quality and engagement metrics.

        Args:
            contribution: A dictionary representing a community contribution.

        Returns:
            The score assigned to the contribution.
        """
        quality_score = contribution.get('quality_rating', 0)
        engagement_score = contribution.get('engagement_metrics', 0)
        # Weighted scoring: 70% quality and 30% engagement
        return (quality_score * 0.7) + (engagement_score * 0.3)

    async def validate_step(self, settings: ValidatorSettings) -> None:
        """
        Perform a validation step by fetching contributions and scoring them.
        """
        contributions = self.client.query_contributions(self.netuid)  # Adjust to your API
        score_dict: dict[int, float] = {}

        for contribution in contributions:
            score = self._score_contribution(contribution)
            uid = contribution['author_uid']  # Assuming contributions have an author UID
            score_dict[uid] = score

        if not score_dict:
            log("No contributions to validate")
            return None

        # Call to set the weights based on scores
        set_weights(settings, score_dict, self.netuid, self.client, self.key)

    def validation_loop(self, settings: ValidatorSettings) -> None:
        """
        Run the validation loop continuously based on the provided settings.
        """
        while True:
            start_time = time.time()
            asyncio.run(self.validate_step(settings))

            elapsed = time.time() - start_time
            if elapsed < settings.iteration_interval:
                sleep_time = settings.iteration_interval - elapsed
                log(f"Sleeping for {sleep_time}")
                time.sleep(sleep_time)
