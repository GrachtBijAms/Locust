from __future__ import annotations

import csv
import os
import statistics
import threading
from collections import defaultdict
from datetime import datetime
from locust import events


class StepReportCollector:
    def __init__(self):
        self.lock = threading.Lock()
        self.rows = []
        self.started_at = None
        self.output_dir = os.path.join(os.getcwd(), "reports")

    def on_test_start(self, environment, **kwargs):
        with self.lock:
            self.rows = []
            self.started_at = datetime.utcnow()
            os.makedirs(self.output_dir, exist_ok=True)

    def on_request(self, request_type, name, response_time, response_length, exception, **kwargs):
        with self.lock:
            self.rows.append(
                {
                    "request_type": request_type,
                    "name": name,
                    "response_time": float(response_time or 0),
                    "response_length": int(response_length or 0),
                    "success": exception is None,
                    "error": "" if exception is None else str(exception),
                    "timestamp": datetime.utcnow().isoformat(timespec="seconds"),
                }
            )

    def percentile(self, values, pct):
        if not values:
            return 0.0
        if len(values) == 1:
            return float(values[0])
        values = sorted(values)
        idx = (len(values) - 1) * pct
        lower = int(idx)
        upper = min(lower + 1, len(values) - 1)
        if lower == upper:
            return float(values[lower])
        fraction = idx - lower
        return float(values[lower] + (values[upper] - values[lower]) * fraction)

    def build_summary(self):
        grouped = defaultdict(list)
        for row in self.rows:
            grouped[(row["request_type"], row["name"])].append(row)

        summary = []
        for (request_type, name), entries in grouped.items():
            times = [r["response_time"] for r in entries]
            failures = [r for r in entries if not r["success"]]
            summary.append(
                {
                    "request_type": request_type,
                    "name": name,
                    "count": len(entries),
                    "failures": len(failures),
                    "failure_pct": round((len(failures) / len(entries)) * 100, 2) if entries else 0.0,
                    "min_ms": round(min(times), 2) if times else 0.0,
                    "avg_ms": round(statistics.mean(times), 2) if times else 0.0,
                    "p50_ms": round(self.percentile(times, 0.50), 2) if times else 0.0,
                    "p95_ms": round(self.percentile(times, 0.95), 2) if times else 0.0,
                    "p99_ms": round(self.percentile(times, 0.99), 2) if times else 0.0,
                    "max_ms": round(max(times), 2) if times else 0.0,
                }
            )

        summary.sort(key=lambda x: (x["request_type"], x["name"]))
        return summary

    def write_csv(self):
        raw_path = os.path.join(self.output_dir, "step_raw_results.csv")
        summary_path = os.path.join(self.output_dir, "step_summary.csv")

        with open(raw_path, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(
                f,
                fieldnames=[
                    "timestamp",
                    "request_type",
                    "name",
                    "response_time",
                    "response_length",
                    "success",
                    "error",
                ],
            )
            writer.writeheader()
            writer.writerows(self.rows)

        with open(summary_path, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(
                f,
                fieldnames=[
                    "request_type",
                    "name",
                    "count",
                    "failures",
                    "failure_pct",
                    "min_ms",
                    "avg_ms",
                    "p50_ms",
                    "p95_ms",
                    "p99_ms",
                    "max_ms",
                ],
            )
            writer.writeheader()
            writer.writerows(self.build_summary())

        return raw_path, summary_path

    def write_markdown(self, environment):
        md_path = os.path.join(self.output_dir, "step_summary.md")
        summary = self.build_summary()
        started = self.started_at.isoformat(timespec="seconds") if self.started_at else ""
        finished = datetime.utcnow().isoformat(timespec="seconds")
        total = environment.stats.total

        with open(md_path, "w", encoding="utf-8") as f:
            f.write("# Locust Step Summary\n\n")
            f.write(f"- Started: {started}\n")
            f.write(f"- Finished: {finished}\n")
            f.write(f"- Total requests/events: {total.num_requests}\n")
            f.write(f"- Total failures: {total.num_failures}\n\n")
            f.write("## Step Metrics\n\n")
            f.write("| Type | Name | Count | Failures | Failure % | Min ms | Avg ms | P50 ms | P95 ms | P99 ms | Max ms |\n")
            f.write("|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|\n")
            for row in summary:
                f.write(
                    f"| {row['request_type']} | {row['name']} | {row['count']} | {row['failures']} | {row['failure_pct']} | {row['min_ms']} | {row['avg_ms']} | {row['p50_ms']} | {row['p95_ms']} | {row['p99_ms']} | {row['max_ms']} |\n"
                )

        return md_path

    def on_test_stop(self, environment, **kwargs):
        with self.lock:
            self.write_csv()
            self.write_markdown(environment)


collector = StepReportCollector()
events.test_start.add_listener(collector.on_test_start)
events.request.add_listener(collector.on_request)
events.test_stop.add_listener(collector.on_test_stop)
