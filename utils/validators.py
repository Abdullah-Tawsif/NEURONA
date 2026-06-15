from config.settings import ALLOWED_EMAIL_DOMAINS


def is_email_domain_allowed(email: str) -> bool:
    domain = email.split("@")[-1].lower()
    return domain in ALLOWED_EMAIL_DOMAINS
