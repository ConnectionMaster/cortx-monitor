# Copyright (c) 2020 Seagate Technology LLC and/or its Affiliates
#
# This program is free software: you can redistribute it and/or modify it under the
# terms of the GNU Affero General Public License as published by the Free Software
# Foundation, either version 3 of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful, but WITHOUT ANY
# WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A
# PARTICULAR PURPOSE. See the GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License along
# with this program. If not, see <https://www.gnu.org/licenses/>. For any questions
# about this software or licensing, please email opensource@seagate.com or
# cortx-questions@seagate.com.

# -*- coding: utf-8 -*-
import json
import os
import psutil
import time
import sys

from default import world
from messaging.ingress_processor_tests import IngressProcessorTests
from messaging.egress_processor_tests import EgressProcessorTests


resource_type = "node:os:disk_space"

def init(args):
    pass

def test_disk_space_alert(agrs):
    check_sspl_ll_is_running()
    disk_space_data_sensor_request(resource_type)
    disk_space_sensor_msg = None
    # Wait untill expected resource type found in RMQ ingress processor msgQ.
    start_time = time.time()
    max_wait_time = 60
    while not disk_space_sensor_msg:
        if not world.sspl_modules[IngressProcessorTests.name()]._is_my_msgQ_empty():
            ingressMsg = world.sspl_modules[IngressProcessorTests.name()]._read_my_msgQ()
            print("Received: {0}".format(ingressMsg))
            try:
                # Make sure we get back the message type that matches the request
                msg_type = ingressMsg.get("sensor_response_type")
                if msg_type["info"]["resource_type"] == resource_type:
                    disk_space_sensor_msg = msg_type
            except Exception as exception:
                print(exception)
        if (time.time()-start_time) > max_wait_time:
            break

    assert(disk_space_sensor_msg is not None)
    assert(disk_space_sensor_msg.get("alert_type") is not None)
    assert(disk_space_sensor_msg.get("alert_id") is not None)
    assert(disk_space_sensor_msg.get("severity") is not None)
    assert(disk_space_sensor_msg.get("host_id") is not None)
    assert(disk_space_sensor_msg.get("info") is not None)
    assert(disk_space_sensor_msg.get("specific_info") is not None)

    disk_space_info = disk_space_sensor_msg.get("info")
    assert(disk_space_info.get("site_id") is not None)
    assert(disk_space_info.get("node_id") is not None)
    assert(disk_space_info.get("cluster_id") is not None)
    assert(disk_space_info.get("rack_id") is not None)
    assert(disk_space_info.get("resource_type") == resource_type)
    assert(disk_space_info.get("event_time") is not None)
    assert(disk_space_info.get("resource_id") is not None)
    assert(disk_space_info.get("description") is not None)

    disk_space_specific_info = disk_space_sensor_msg.get("specific_info")
    assert(disk_space_specific_info is not None)
    assert(disk_space_specific_info.get("freeSpace") is not None)
    assert(disk_space_specific_info.get("totalSpace") is not None)
    assert(disk_space_specific_info.get("diskUsedPercentage") is not None)

def check_sspl_ll_is_running():
    # Check that the state for sspl_ll service is active
    found = False

    # Support for python-psutil < 2.1.3
    for proc in psutil.process_iter():
        if proc.name == "sspld" and \
           proc.status in (psutil.STATUS_RUNNING, psutil.STATUS_SLEEPING):
               found = True

    # Support for python-psutil 2.1.3+
    if found == False:
        for proc in psutil.process_iter():
            pinfo = proc.as_dict(attrs=['cmdline', 'status'])
            if "sspld" in str(pinfo['cmdline']) and \
                pinfo['status'] in (psutil.STATUS_RUNNING, psutil.STATUS_SLEEPING):
                    found = True

    assert found == True

    # Clear the message queue buffer out
    while not world.sspl_modules[IngressProcessorTests.name()]._is_my_msgQ_empty():
        world.sspl_modules[IngressProcessorTests.name()]._read_my_msgQ()


def disk_space_data_sensor_request(sensor_type):
    egressMsg = {
        "title": "SSPL Actuator Request",
        "description": "Seagate Storage Platform Library - Actuator Request",

        "username" : "JohnDoe",
        "signature" : "None",
        "time" : "2015-05-29 14:28:30.974749",
        "expires" : 500,

        "message" : {
            "sspl_ll_msg_header": {
                "schema_version": "1.0.0",
                "sspl_version": "1.0.0",
                "msg_version": "1.0.0"
            },
             "sspl_ll_debug": {
                "debug_component" : "sensor",
                "debug_enabled" : True
            },
            "sensor_request_type": {
                "node_data": {
                    "sensor_type": sensor_type
                }
            }
        }
    }
    world.sspl_modules[EgressProcessorTests.name()]._write_internal_msgQ(EgressProcessorTests.name(), egressMsg)

test_list = [test_disk_space_alert]