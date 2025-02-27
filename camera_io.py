import requests
from requests.auth import HTTPBasicAuth
from urllib3.exceptions import InsecureRequestWarning
import logging

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

_LOGGER = logging.getLogger(__name__)

class CameraIO:
    def __init__(self, ip, username, password):
        self.ip = ip
        self.username = username
        self.password = password
        self.base_url = f"http://{ip}"
        self.auth = HTTPBasicAuth(username, password)
        self.headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
            'Accept': 'text/plain',
            'User-Agent': 'Mozilla/4.0',
            'Connection': 'Keep-Alive'
        }
        self.param_paths = {
            'set': '/cgi-bin/dido/setdo.cgi',
            'dido_get_out': '/cgi-bin/dido/getdo.cgi',
            'dido_get_in': '/cgi-bin/dido/getdi.cgi'
        }
        self.timeout = 15

    def test_connection(self):
        """Test connection to camera."""
        try:
            response = requests.get(
                self.base_url,
                auth=self.auth,
                headers=self.headers,
                verify=False,
                timeout=self.timeout
            )
            return response.status_code == 200
        except Exception as e:
            _LOGGER.error(f"Connection test failed: {str(e)}")
            return False

    def get_io_status(self):
        """Get digital input and output status."""
        try:
            # Get output status
            out_response = requests.get(
                f"{self.base_url}{self.param_paths['dido_get_out']}",
                auth=self.auth,
                headers=self.headers,
                verify=False,
                timeout=self.timeout
            )
            
            # Get input status
            in_response = requests.get(
                f"{self.base_url}{self.param_paths['dido_get_in']}",
                auth=self.auth,
                headers=self.headers,
                verify=False,
                timeout=self.timeout
            )
            
            result = {'input': 'unknown', 'output': 'unknown'}
            
            if out_response.status_code == 200:
                result['output'] = 'grounded' if 'do0=1' in out_response.text else 'open'
                
            if in_response.status_code == 200:
                result['input'] = 'high' if 'di0=1' in in_response.text else 'low'
                
            return result
            
        except Exception as e:
            _LOGGER.error(f"Error reading I/O status: {str(e)}")
            return {'input': 'unknown', 'output': 'unknown'}

    def set_output(self, state):
        """Set digital output state."""
        try:
            output_state = "1" if state else "0"
            response = requests.get(
                f"{self.base_url}{self.param_paths['set']}?do0={output_state}",
                auth=self.auth,
                headers=self.headers,
                verify=False,
                timeout=self.timeout
            )
            
            if response.status_code == 200:
                # Verify the state change
                status = self.get_io_status()
                current_state = status['output']
                expected_state = 'grounded' if state else 'open'
                return current_state == expected_state
                
            return False
            
        except Exception as e:
            _LOGGER.error(f"Error setting output: {str(e)}")
            return False
