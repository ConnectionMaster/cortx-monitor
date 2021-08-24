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
from common import (
    check_sspl_ll_is_running, get_fru_response, send_enclosure_sensor_request)


def init(args):
    pass

def test_real_stor_fan_module_sensor(args):
    check_sspl_ll_is_running()
    instance_id = "*"
    resource_type = "storage:hw:fan"
    ingress_msg_type = "sensor_response_type"
    send_enclosure_sensor_request(resource_type, instance_id)
    ingressMsg = get_fru_response(
        resource_type, instance_id, ingress_msg_type)
    fan_module_sensor_msg = ingressMsg.get(ingress_msg_type)

    assert(fan_module_sensor_msg is not None)
    assert(fan_module_sensor_msg.get("alert_type") is not None)
    assert(fan_module_sensor_msg.get("alert_id") is not None)
    assert(fan_module_sensor_msg.get("severity") is not None)
    assert(fan_module_sensor_msg.get("host_id") is not None)
    assert(fan_module_sensor_msg.get("info") is not None)

    fan_module_info = fan_module_sensor_msg.get("info")
    assert(fan_module_info.get("site_id") is not None)
    assert(fan_module_info.get("node_id") is not None)
    assert(fan_module_info.get("cluster_id") is not None)
    assert(fan_module_info.get("rack_id") is not None)
    assert(fan_module_info.get("resource_type") is not None)
    assert(fan_module_info.get("event_time") is not None)
    assert(fan_module_info.get("resource_id") is not None)
    assert(fan_module_info.get("description") is not None)

    fru_specific_info = fan_module_sensor_msg.get("specific_info", {})
    if fru_specific_info:
        assert(fru_specific_info.get("durable_id") is not None)
        assert(fru_specific_info.get("status") is not None)
        assert(fru_specific_info.get("name") is not None)
        assert(fru_specific_info.get("enclosure_id") is not None)
        assert(fru_specific_info.get("health") is not None)
        assert(fru_specific_info.get("health_reason") is not None)
        assert(fru_specific_info.get("location") is not None)
        assert(fru_specific_info.get("health_recommendation") is not None)
        assert(fru_specific_info.get("position") is not None)

    fans = fan_module_sensor_msg.get("specific_info").get("fans", [])
    if fans:
        for fan in fans:
            assert(fan.get("durable_id") is not None)
            assert(fan.get("status") is not None)
            assert(fan.get("name") is not None)
            assert(fan.get("speed") is not None)
            assert(fan.get("locator_led") is not None)
            assert(fan.get("position") is not None)
            assert(fan.get("location") is not None)
            assert(fan.get("part_number") is not None)
            assert(fan.get("serial_number") is not None)
            assert(fan.get("fw_revision") is not None)
            assert(fan.get("hw_revision") is not None)
            assert(fan.get("health") is not None)
            assert(fan.get("health_reason") is not None)
            assert(fan.get("health_recommendation") is not None)

test_list = [test_real_stor_fan_module_sensor]
