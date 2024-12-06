from prometheus_api import *
# from prometheus_api_client import *


class PrometheusHandler:
    def __init__(self, logger, PROMETHEUS_URL="http://localhost:9090") -> None:
        self.prom = PrometheusConnect(url=PROMETHEUS_URL)
        self.logger = logger
        self.all_metrics_full = []
        self.all_metrics_name = []

    def get_all_metrics(self):
        self.all_metrics_full = self.prom.all_metric_meta()
        return self.all_metrics_full

    def get_range_data(self, metric_name, range=None,include_index=False):
        metric_data = self.prom.get_metric_range_data(metric_name=metric_name)

        range_data = []
        metric_object_list = MetricsList(metric_data)
        for metric in metric_object_list:
            values = []
            for index, row in metric.metric_values.iterrows():
                timestamp = row['ds']
                value = row['y']
                
                data_row = (timestamp, value)
                if include_index:
                    data_row = (index, timestamp, value)
                values.append(data_row)
                range_data.append(values)
        return range_data

    def test_prometheus(self, metric_name="go_gc_duration_seconds"):
        my_label_config = {'instance': 'instance_id', 'job': 'job_id', 'quantile': 'quantile_value'}
        metric_data = self.prom.get_metric_range_data(metric_name=metric_name)

        metric_object_list = MetricsList(metric_data)
        for metric in metric_object_list:
            self.logger.info(metric.label_config)