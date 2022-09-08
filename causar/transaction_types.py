from enum import IntEnum


class TransactionTypes(IntEnum):
    INTERACTION_RESPONSE_SENT = 1
    INTERACTION_FOLLOWUP_SENT = 2
