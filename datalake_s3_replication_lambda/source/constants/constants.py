from enum import Enum

class DeletionStatus(Enum):
    ABORT = 'Abort'
    SUCCESS = 'Success'
    FAIL = 'Fail'

class EventType(Enum):
    S3_NOTIFICATION = 's3_notification'
    SNS_NOTIFICATION = 'sns_notification'