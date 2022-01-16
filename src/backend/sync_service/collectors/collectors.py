from datetime import datetime, timedelta
from sync_service.api.routers.sync_stats import get_last_sync as stats_get_last_sync
from sync_service.api.routers.sync_stats import get_last_sync as users_get_last_sync
from prometheus_client.core import GaugeMetricFamily

class TimeSinceSyncMetricsCollector(object):
    """
    Custom collector that emits info the time since the last sync operation

    See "Custom Collectors" section
    https://pythonrepo.com/repo/prometheus-client_python-python-monitoring
    """
    def collect(self):
        """
        """

        time_since_gauge = GaugeMetricFamily("sync_time_since_last", 'Time since the last sync operation occurred', labels = ["sync"])
        now = datetime.now()

        # Stats
        stats_sync = stats_get_last_sync()
        time_since = (now - datetime.fromtimestamp(stats_sync.sync_timestamp)).total_seconds()
        time_since_gauge.add_metric(labels = ["stats", stats_sync.who_updated], value = time_since)

        # Users
        users_sync = users_get_last_sync()
        time_since = (now - datetime.fromtimestamp(users_sync.sync_timestamp)).total_seconds()
        time_since_gauge.add_metric(labels = ["users", users_sync.who_updated], value = time_since)

        yield time_since_gauge

class CompletedSuccesfullyMetricsCollector(object):
    """
    Custom collector that emits if the last sync operaiton was successful.

    See "Custom Collectors" section
    https://pythonrepo.com/repo/prometheus-client_python-python-monitoring
    """
    def collect(self):
        """
        """

        # Stats
        stats_sync = stats_get_last_sync()
        completed_successfully_gauge = GaugeMetricFamily("sync_completed_sucessfully", 'If the last sync operation was successful', labels = ["sync"])
        completed_successfully_gauge.add_metric(labels = ["stats", stats_sync.who_updated], value = float(stats_sync.completed_successfully))

        # Users
        users_sync = users_get_last_sync()
        completed_successfully_gauge.add_metric(labels = ["users", stats_sync.who_updated], value = float(users_sync.completed_successfully))

        yield completed_successfully_gauge