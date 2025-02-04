"""Criteo Authentication."""

from __future__ import annotations

from singer_sdk import RESTStream
from singer_sdk.authenticators import OAuthAuthenticator


class CriteoAuthenticator(OAuthAuthenticator):
    """Authenticator class for Criteo."""

    @property
    def oauth_request_body(self) -> dict:
        """Define the OAuth request body for the Criteo API.

        Returns:
            A dictionary with the request body for authentication.
        """
        return {
            "client_id": self.config["client_id"],
            "client_secret": self.config["client_secret"],
            "grant_type": "client_credentials",
        }

    @classmethod
    def create_for_stream(
        cls: type[CriteoAuthenticator], stream: RESTStream
    ) -> CriteoAuthenticator:
        """Initialize authenticator from Singer stream instance.

        Args:
            stream: Stream instance.

        Returns:
            An authenticator object.
        """
        return cls(stream=stream, auth_endpoint="https://api.criteo.com/oauth2/token")

    def update_access_token(self) -> None:
        ret = OAuthAuthenticator.update_access_token(self)
        # self.logger.info("***********ACCESS TOKEN: %s", self.access_token)
        return ret