from collections import namedtuple

SourceDestination = namedtuple('SourceDestination', 'source_bucket, destination_bucket, delete_source_file')

source_to_destination_mapping = {
    'dev-datalake-landing': SourceDestination(source_bucket='dev-datalake-landing', destination_bucket='dev-l1-datalake-v1-landing', delete_source_file=True),
    'sandbox-datalake-landing': SourceDestination(source_bucket='sandbox-datalake-landing', destination_bucket='cert-l1-datalake-v1-landing', delete_source_file=True),
    'prod-datalake-landing': SourceDestination(source_bucket='prod-datalake-landing', destination_bucket='prod-l1-datalake-v1-landing', delete_source_file=True),
    'dev-l1-datalake-v1-storage': SourceDestination(source_bucket='dev-l1-datalake-v1-storage', destination_bucket='dev-datalake-storage', delete_source_file=False),
    'cert-l1-datalake-v1-storage': SourceDestination(source_bucket='cert-l1-datalake-v1-storage', destination_bucket='sandbox-datalake-storage', delete_source_file=False),
    'prod-l1-datalake-v1-storage': SourceDestination(source_bucket='prod-l1-datalake-v1-storage', destination_bucket='prod-datalake-storage', delete_source_file=False),
    'dev-l1-datalake-v1-secure-storage': SourceDestination(source_bucket='dev-l1-datalake-v1-secure-storage', destination_bucket='dev-datalake-secure-storage', delete_source_file=False),
    'cert-l1-datalake-v1-secure-storage': SourceDestination(source_bucket='cert-l1-datalake-v1-secure-storage', destination_bucket='sandbox-datalake-secure-storage', delete_source_file=False),
    'prod-l1-datalake-v1-secure-storage': SourceDestination(source_bucket='prod-l1-datalake-v1-secure-storage', destination_bucket='prod-datalake-secure-storage', delete_source_file=False),
    'dev-l1-datalake-v1-derived-storage': SourceDestination(source_bucket='dev-l1-datalake-v1-derived-storage', destination_bucket='dev-datalake-derived-storage', delete_source_file=False),
    'cert-l1-datalake-v1-derived-storage': SourceDestination(source_bucket='cert-l1-datalake-v1-derived-storage', destination_bucket='sandbox-datalake-derived-storage', delete_source_file=False),
    'prod-l1-datalake-v1-derived-storage': SourceDestination(source_bucket='prod-l1-datalake-v1-derived-storage', destination_bucket='prod-datalake-derived-storage', delete_source_file=False)
}