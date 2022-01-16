from sentry_sdk.api import flush
from backend_service.api.operation.stats_operation import StatsOperation
from prometheus_client.core import CounterMetricFamily, REGISTRY

class StatsMetricsCollector(object):
    """
    Custom collector that takes the stats dictionary and formats it into prometheus metrics.

    See "Custom Collectors" section
    https://pythonrepo.com/repo/prometheus-client_python-python-monitoring
    """
    def collect(self):
        """
        Executes a StatsOperation to get the most recent stats. Then creates counters from the stats dictionary.
        """
        # Get all Stats
        result = StatsOperation(show_all = all).execute()

        # Remove the "message" key, since it is not a float
        result.pop('message', None)

        stats_counter = CounterMetricFamily("backend_stats", 'Output of /stats as emitted as metric', labels = ["stat"])
        for k, v in result.items():
            stats_counter.add_metric([k], v)
        
        yield stats_counter