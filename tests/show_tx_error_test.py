import os
import pytest
import subprocess
from click.testing import CliRunner

import show.main as show
from .utils import get_result_and_return_code

root_path = os.path.dirname(os.path.abspath(__file__))
modules_path = os.path.dirname(root_path)
scripts_path = os.path.join(modules_path, "scripts")

show_intf_tx_error_with_ok = """\
Port       status    statistics 
---------  --------  ------------ 
Ethernet0  OK        0 """

show_intf_tx_error_with_not_ok = """\
Port       status    statistics 
---------  --------  ------------ 
Ethernet0  NotOK     1 """


def verify_output(output, expected_output):
    lines = output.splitlines()
    ignored_intfs = ['eth0', 'lo']
    for intf in ignored_intfs:
        # the output should have line to display the ip address of eth0 and lo
        assert len([line for line in lines if line.startswith(intf)]) == 1

    new_output = '\n'.join([line for line in lines if not any(i in line for i in ignored_intfs)])
    print(new_output)
    assert new_output == expected_output

class TestShowTxErrorStatus(object):

    def test_show_tx_error_ok(self):
        return_code, result = get_result_and_return_code(["show interface Ethernet0 tx_error"])
        assert return_code == 0
        verify_output(result, show_intf_tx_error_with_ok)

    def test_show_tx_error_not_ok(self):
        return_code, result = get_result_and_return_code(["show interface Ethernet0 tx_error"])
        assert return_code == 0
        verify_output(result, show_intf_tx_error_with_not_ok)
