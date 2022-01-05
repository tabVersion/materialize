# Copyright Materialize, Inc. and contributors. All rights reserved.
#
# Use of this software is governed by the Business Source License
# included in the LICENSE file at the root of this repository.
#
# As of the Change Date specified in that file, in accordance with
# the Business Source License, use of this software will be governed
# by the Apache License, Version 2.0.

import time

from materialize.mzcompose import (
    Kafka,
    Materialized,
    SchemaRegistry,
    Testdrive,
    Workflow,
    Zookeeper,
)

services = [
    Zookeeper(),
    Kafka(name="kafka1", broker_id=1, offsets_topic_replication_factor=2),
    Kafka(name="kafka2", broker_id=2, offsets_topic_replication_factor=2),
    Kafka(name="kafka3", broker_id=3, offsets_topic_replication_factor=2),
    SchemaRegistry(kafka_servers=["kafka1", "kafka2", "kafka3"]),
    Materialized(),
    Testdrive(
        entrypoint=[
            "testdrive",
            "--schema-registry-url=http://schema-registry:8081",
            "--materialized-url=postgres://materialize@materialized:6875",
            "--kafka-option=acks=all",
            "--seed=1",
        ]
    ),
]


def workflow_kafka_multi_broker(w: Workflow):
    w.start_and_wait_for_tcp(
        services=[
            "zookeeper",
            "kafka1",
            "kafka2",
            "kafka3",
            "schema-registry",
            "materialized",
        ]
    )
    w.run_service(
        service="testdrive-svc",
        command="--kafka-addr=kafka2 01-init.td",
    )
    time.sleep(10)
    w.kill_services(services=["kafka1"], signal="SIGKILL")
    time.sleep(10)
    w.run_service(
        service="testdrive-svc",
        command="--kafka-addr=kafka2,kafka3 --no-reset 02-after-leave.td",
    )
    w.start_services(services=["kafka1"])
    time.sleep(10)
    w.run_service(
        service="testdrive-svc",
        command="--kafka-addr=kafka1 --no-reset 03-after-join.td",
    )