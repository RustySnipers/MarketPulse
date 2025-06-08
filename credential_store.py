"""Helpers for securely storing credentials using keyring."""
import keyring

APP_NAME = "MarketPulse"


def save_password(service: str, username: str, password: str) -> None:
    """Save password for given service and username."""
    keyring.set_password(f"{APP_NAME}:{service}", username, password)


def get_password(service: str, username: str) -> str | None:
    """Retrieve password for given service and username."""
    try:
        return keyring.get_password(f"{APP_NAME}:{service}", username)
    except keyring.errors.KeyringError:
        return None


def delete_password(service: str, username: str) -> None:
    """Delete stored password."""
    try:
        keyring.delete_password(f"{APP_NAME}:{service}", username)
    except keyring.errors.KeyringError:
        pass
