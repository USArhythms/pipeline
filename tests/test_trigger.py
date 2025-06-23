"""
Test Suite for Trigger Module

This test module validates the functionality of the trigger.py script which
is responsible for triggering post-acquisition processing on a remote compute server.

The tests use mocking to simulate the SSH connection and remote server interaction,
avoiding the need for an actual network connection during testing.

Test Coverage:
- Command line argument parsing with different input methods
  - Default values
  - Command line arguments
  - Environment variables
- Trigger invocation with correct parameter passing 
- Main function execution flow

Dependencies:
- unittest: Standard Python testing framework
- unittest.mock: For creating mock objects and patching functions
- importlib.util: For dynamically loading the trigger module

No external dependencies required as paramiko is mocked.
"""

import importlib.util
import sys
import unittest
from pathlib import Path
from types import ModuleType
from unittest import mock

# Create a dummy paramiko module since it's not installed
# This approach allows testing code that requires paramiko without actually installing it
# Each class simulates a component of the paramiko library with appropriate mock methods

class DummyChannel:
    """Mock for paramiko.Channel - simulates the SSH channel for command execution"""
    def __init__(self):
        self.exec_command = mock.Mock()
        self.recv = mock.Mock(return_value=b'out')  # Simulates stdout output
        self.recv_stderr = mock.Mock(return_value=b'')  # Simulates stderr output (empty)

class DummyTransport:
    """Mock for paramiko.Transport - simulates the SSH transport layer"""
    def __init__(self):
        self.open_session = mock.Mock(return_value=DummyChannel())

class DummySSHClient:
    """Mock for paramiko.SSHClient - simulates the SSH client connection"""
    def __init__(self):
        self.set_missing_host_key_policy = mock.Mock()
        self.connect = mock.Mock()
        self.get_transport = mock.Mock(return_value=DummyTransport())
        self.close = mock.Mock()

class DummyAutoAddPolicy:
    """Mock for paramiko.AutoAddPolicy - simulates the SSH host key policy"""
    pass

mock_paramiko = ModuleType('paramiko')
mock_paramiko.SSHClient = DummySSHClient
mock_paramiko.AutoAddPolicy = DummyAutoAddPolicy

sys.modules['paramiko'] = mock_paramiko

class TestTrigger(unittest.TestCase):
    """
    Test cases for the trigger.py script functionality
    
    This test suite uses dynamic module loading to test the trigger.py script
    without directly importing it, allowing us to mock its dependencies like paramiko
    before they are imported by the script.
    """
    
    @mock.patch('socket.gethostname', return_value='acqhost')
    @mock.patch('socket.gethostbyname', return_value='1.2.3.4')    
    def test_trigger_invocation(self, mock_gethostbyname, mock_gethostname):
        """Test that the trigger function works correctly"""
        # Reload the module to ensure our dummy paramiko is used
        module_key = 'processing.Remote.trigger'
        if module_key in sys.modules:
            del sys.modules[module_key]
        trigger_path = Path(__file__).resolve().parents[1] / 'processing' / 'Remote' / 'trigger.py'
        spec = importlib.util.spec_from_file_location(module_key, trigger_path)
        trigger = importlib.util.module_from_spec(spec)
        sys.modules[module_key] = trigger
        spec.loader.exec_module(trigger)

        # Test with custom values
        test_host = 'test.compute.host'
        test_user = 'testuser'
        test_script = '~/custom_script.sh'
        
        # Create an instance of SSHClient that will be returned by mock
        ssh_client_instance = mock.Mock()
        transport = mock.Mock()
        channel = mock.Mock()
        
        # Configure the mocks
        ssh_client_instance.get_transport.return_value = transport
        transport.open_session.return_value = channel
        channel.recv.return_value = b'out'
        channel.recv_stderr.return_value = b''
        
        # Replace the SSHClient class with a mock that returns our instance
        original_ssh_client = trigger.paramiko.SSHClient
        trigger.paramiko.SSHClient = mock.Mock(return_value=ssh_client_instance)
        
        try:
            # Run the trigger function from our module
            std_out, std_err = trigger.run_trigger(test_host, test_user, test_script)
            
            # Verify the expected command was executed
            expected_cmd = f"bash {test_script} --host 'acqhost' --ip 1.2.3.4"
            channel.exec_command.assert_called_with(expected_cmd)
            ssh_client_instance.connect.assert_called_with(hostname=test_host, username=test_user)
            ssh_client_instance.close.assert_called()
            
            # Verify default parameters
            self.assertEqual(std_out, 'out')
            self.assertEqual(std_err, '')
        finally:
            # Restore the original SSHClient class
            trigger.paramiko.SSHClient = original_ssh_client    
    def test_get_args(self):
        """Test that argument parsing works correctly"""
        import os
        
        # Import the trigger module
        module_key = 'processing.Remote.trigger'
        if module_key in sys.modules:
            del sys.modules[module_key]
        trigger_path = Path(__file__).resolve().parents[1] / 'processing' / 'Remote' / 'trigger.py'
        spec = importlib.util.spec_from_file_location(module_key, trigger_path)
        trigger_module = importlib.util.module_from_spec(spec)
        sys.modules[module_key] = trigger_module
        spec.loader.exec_module(trigger_module)
        
        # Test default values
        with mock.patch('sys.argv', ['trigger.py']):
            args = trigger_module.get_args()
            self.assertEqual(args.host, trigger_module.DEFAULT_COMPUTE_HOST)
            self.assertEqual(args.user, trigger_module.DEFAULT_USER)
            self.assertEqual(args.script, trigger_module.DEFAULT_REMOTE_SCRIPT)
        
        # Test command line arguments
        with mock.patch('sys.argv', ['trigger.py', '--host', 'cmdhost', '--user', 'cmduser', '--script', 'cmdscript']):
            args = trigger_module.get_args()
            self.assertEqual(args.host, 'cmdhost')
            self.assertEqual(args.user, 'cmduser')
            self.assertEqual(args.script, 'cmdscript')
        
        # Test environment variables
        with mock.patch.dict(os.environ, {'COMPUTE_HOST': 'envhost', 'COMPUTE_USER': 'envuser', 'REMOTE_SCRIPT': 'envscript'}):
            with mock.patch('sys.argv', ['trigger.py']):
                args = trigger_module.get_args()
                self.assertEqual(args.host, 'envhost')
                self.assertEqual(args.user, 'envuser')
                self.assertEqual(args.script, 'envscript')    
    @mock.patch('socket.gethostname', return_value='acqhost')
    @mock.patch('socket.gethostbyname', return_value='1.2.3.4')
    def test_main_function(self, mock_gethostbyname, mock_gethostname):
        """Test that the main function works correctly"""
        # Reload the module to ensure our dummy paramiko is used
        module_key = 'processing.Remote.trigger'
        if module_key in sys.modules:
            del sys.modules[module_key]
        trigger_path = Path(__file__).resolve().parents[1] / 'processing' / 'Remote' / 'trigger.py'
        spec = importlib.util.spec_from_file_location(module_key, trigger_path)
        trigger_module = importlib.util.module_from_spec(spec)
        sys.modules[module_key] = trigger_module
        spec.loader.exec_module(trigger_module)
        
        # Mock the run_trigger function to check if it's called with correct args
        with mock.patch.object(trigger_module, 'run_trigger') as mock_run_trigger:
            mock_run_trigger.return_value = ('success', '')
            with mock.patch('sys.argv', ['trigger.py', '--host', 'test.host', '--user', 'testuser']):
                # Call the main function
                with mock.patch('builtins.print') as mock_print:
                    trigger_module.main()
                    
                    # Verify run_trigger was called with correct arguments
                    mock_run_trigger.assert_called_once_with('test.host', 'testuser', trigger_module.DEFAULT_REMOTE_SCRIPT)
                    # Verify output was printed
                    mock_print.assert_called_once_with('success', '', sep='\n')


if __name__ == '__main__':
    unittest.main()
