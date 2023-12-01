import os
import sys
import pytest
import mock
from importlib import reload

from click.testing import CliRunner

from utilities_common.db import Db

modules_path = os.path.join(os.path.dirname(__file__), "..")
test_path = os.path.join(modules_path, "tests")
sys.path.insert(0, modules_path)
sys.path.insert(0, test_path)
mock_db_path = os.path.join(test_path, "int_ip_input")

class TestIntTx(object):
    @pytest.fixture(scope="class", autouse=True)
    def setup_class(cls):
        print("SETUP")
        os.environ['UTILITIES_UNIT_TESTING'] = "1"
        import config.main as config
        reload(config)
        yield
        print("TEARDOWN")
        os.environ["UTILITIES_UNIT_TESTING"] = "0"
        from .mock_tables import dbconnector
        dbconnector.dedicated_dbs = {}    


    def test_interface_tx_error_threshold_set(
            self,
            get_cmd_module):
        (config, show) = get_cmd_module
        jsonfile_config = os.path.join(mock_db_path, "config_db.json")
        from .mock_tables import dbconnector
        dbconnector.dedicated_dbs['CONFIG_DB'] = jsonfile_config

        runner = CliRunner()
        db = Db()
        obj = {'config_db': db.cfgdb}

        # set a new threshold
        with mock.patch('utilities_common.cli.run_command') as mock_run_command:
            result = runner.invoke(config.config.commands["interface"].commands["tx-error-threshold"].commands["set"],
                                   ["Ethernet2", "10"], obj=obj)
            print(result.exit_code, result.output)
            assert result.exit_code == 0
            assert mock_run_command.call_count == 1