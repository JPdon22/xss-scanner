import unittest
from unittest.mock import patch, MagicMock
from src.scanner.xss_scanner import AlgorandXSSScanner, ScanResult

class TestAlgorandXSSScanner(unittest.TestCase):

    def setUp(self):
        self.algod_address = "http://localhost:4001"
        self.algod_token = "test-token"
        self.scanner = AlgorandXSSScanner(self.algod_address, self.algod_token)

    @patch('algosdk.v2client.algod.AlgodClient.application_info')
    def test_scan_contract_success(self, mock_application_info):
        # Mock the contract info response
        mock_application_info.return_value = {
            'params': {
                'approval-program': 'sample_teal_code',
            }
        }

        # Mock the vulnerability scanning functions
        with patch.object(self.scanner, '_scan_teal_code', return_value=['XSS vulnerability found']), \
             patch.object(self.scanner, '_scan_application_state', return_value=['State vulnerability found']):

            scan_result = self.scanner.scan_contract(app_id=1010)

            self.assertIsInstance(scan_result, ScanResult)
            self.assertEqual(scan_result.app_id, 1010)
            self.assertIn('XSS vulnerability found', scan_result.vulnerabilities)
            self.assertIn('State vulnerability found', scan_result.vulnerabilities)
            self.assertIsNotNone(scan_result.risk_level)
            self.assertIsNotNone(scan_result.recommendations)

    @patch('algosdk.v2client.algod.AlgodClient.application_info')
    def test_scan_contract_no_vulnerabilities(self, mock_application_info):
        # Mock the contract info response
        mock_application_info.return_value = {
            'params': {
                'approval-program': 'sample_teal_code',
            }
        }

        # Mock the vulnerability scanning functions to return empty lists
        with patch.object(self.scanner, '_scan_teal_code', return_value=[]), \
             patch.object(self.scanner, '_scan_application_state', return_value=[]):

            scan_result = self.scanner.scan_contract(app_id=1010)

            self.assertIsInstance(scan_result, ScanResult)
            self.assertEqual(scan_result.app_id, 1010)
            self.assertEqual(scan_result.vulnerabilities, [])
            self.assertIsNotNone(scan_result.risk_level)
            self.assertIsNotNone(scan_result.recommendations)

    @patch('algosdk.v2client.algod.AlgodClient.application_info')
    def test_get_contract_info_error(self, mock_application_info):
        # Simulate an error when retrieving contract info
        mock_application_info.side_effect = Exception("Connection error")

        contract_info = self.scanner._get_contract_info(app_id=1010)

        self.assertIsNone(contract_info)

    @patch('algosdk.v2client.algod.AlgodClient.application_info')
    def test_get_application_state_success(self, mock_application_info):
        # Mock the application state response
        mock_application_info.return_value = {
            'params': {
                'global-state': [{'key': 'some_key', 'value': 'some_value'}]
            }
        }

        app_state = self.scanner._get_application_state(app_id=1010)

        self.assertIsNotNone(app_state)
        self.assertEqual(app_state, {'some_key': 'some_value'})

    @patch('algosdk.v2client.algod.AlgodClient.application_info')
    def test_get_application_state_no_global_state(self, mock_application_info):
        # Mock the application state response without global state
        mock_application_info.return_value = {
            'params': {}
        }

        app_state = self.scanner._get_application_state(app_id=1010)

        self.assertIsNone(app_state)

if __name__ == '__main__':
    unittest.main()

#python -m unittest src/tests/test_xss_scanner.py
