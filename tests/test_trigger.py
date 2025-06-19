import importlib.util
import sys
from pathlib import Path
from types import ModuleType
from unittest import mock

# Create a dummy paramiko module since it's not installed
class DummyChannel:
    def __init__(self):
        self.exec_command = mock.Mock()
        self.recv = mock.Mock(return_value=b'out')
        self.recv_stderr = mock.Mock(return_value=b'')

class DummyTransport:
    def __init__(self):
        self.open_session = mock.Mock(return_value=DummyChannel())

class DummySSHClient:
    def __init__(self):
        self.set_missing_host_key_policy = mock.Mock()
        self.connect = mock.Mock()
        self.get_transport = mock.Mock(return_value=DummyTransport())
        self.close = mock.Mock()

class DummyAutoAddPolicy:
    pass

mock_paramiko = ModuleType('paramiko')
mock_paramiko.SSHClient = DummySSHClient
mock_paramiko.AutoAddPolicy = DummyAutoAddPolicy

sys.modules['paramiko'] = mock_paramiko

@mock.patch('socket.gethostname', return_value='acqhost')
@mock.patch('socket.gethostbyname', return_value='1.2.3.4')
def test_trigger_invocation(mock_gethostbyname, mock_gethostname):
    # Reload the module to ensure our dummy paramiko is used
    module_key = 'experiments_nwb.trigger'
    if module_key in sys.modules:
        del sys.modules[module_key]
    trigger_path = Path(__file__).resolve().parents[1] / 'experiments_nwb' / 'trigger.py'
    spec = importlib.util.spec_from_file_location(module_key, trigger_path)
    trigger = importlib.util.module_from_spec(spec)
    sys.modules[module_key] = trigger
    spec.loader.exec_module(trigger)

    ssh = trigger.ssh
    channel = ssh.get_transport.return_value.open_session.return_value

    expected_cmd = "bash ~/post_acquire.sh --host 'acqhost' --ip 1.2.3.4"
    channel.exec_command.assert_called_with(expected_cmd)
    ssh.connect.assert_called_with(hostname=trigger.compute_host, username=trigger.user)
    ssh.close.assert_called()
