"""
Entry point for the Algorand XSS Scanner application.
"""
from src.scanner.xss_scanner import AlgorandXSSScanner
from src.reports.report_generator import ReportGenerator
from config.settings import ALGOD_ADDRESS, ALGOD_TOKEN

def main():
    """Main execution function."""
    # Initialize scanner
    scanner = AlgorandXSSScanner(ALGOD_ADDRESS, ALGOD_TOKEN)
    
    # Get application ID from user or configuration
    app_id = input("Enter Algorand application ID to scan: ")
    
    try:
        # Perform scan
        scan_results = scanner.scan_contract(int(app_id))
        
        # Generate report
        report_generator = ReportGenerator()
        report = report_generator.generate_json_report(scan_results)
        
        # Save report to file
        with open(f"scan_report_{app_id}.json", "w") as f:
            f.write(report)
            
        print(f"Scan complete. Report saved to scan_report_{app_id}.json")
        
    except Exception as e:
        print(f"Error during scan: {e}")

if __name__ == "__main__":
    main()