import React, { useState } from 'react';
import { AlertCircle, CheckCircle, Search } from 'lucide-react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Alert, AlertDescription, AlertTitle } from '@/components/ui/alert';

const XSSScanner = () => {
  const [contractUrl, setContractUrl] = useState('');
  const [scanning, setScanning] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState(null);

  const handleScan = async (e) => {
    e.preventDefault();
    setScanning(true);
    setError(null);
    setResult(null);

    try {
      const response = await fetch('http://localhost:8000/api/scan', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ contract_url: contractUrl }),
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.detail || 'Scan failed');
      }

      setResult(data);
    } catch (err) {
      setError(err.message);
    } finally {
      setScanning(false);
    }
  };

  return (
    <div className="container mx-auto px-4 py-8 max-w-2xl">
      <Card>
        <CardHeader>
          <CardTitle>Algorand XSS Vulnerability Scanner</CardTitle>
          <CardDescription>
            Enter the Algorand smart contract URL to scan for XSS vulnerabilities
          </CardDescription>
        </CardHeader>
        <CardContent>
          <form onSubmit={handleScan} className="space-y-4">
            <div className="flex gap-2">
              <input
                type="text"
                value={contractUrl}
                onChange={(e) => setContractUrl(e.target.value)}
                placeholder="Enter contract URL or App ID"
                className="flex-1 px-3 py-2 border rounded-md"
                disabled={scanning}
              />
              <button
                type="submit"
                disabled={scanning || !contractUrl}
                className="px-4 py-2 bg-blue-600 text-white rounded-md disabled:bg-blue-400"
              >
                {scanning ? (
                  <div className="flex items-center gap-2">
                    <div className="animate-spin">
                      <Search className="w-5 h-5" />
                    </div>
                    Scanning...
                  </div>
                ) : (
                  'Scan'
                )}
              </button>
            </div>
          </form>

          {error && (
            <Alert variant="destructive" className="mt-4">
              <AlertCircle className="h-4 w-4" />
              <AlertTitle>Error</AlertTitle>
              <AlertDescription>{error}</AlertDescription>
            </Alert>
          )}

          {result && (
            <Alert
              variant={result.vulnerabilities_found ? "destructive" : "default"}
              className="mt-4"
            >
              {result.vulnerabilities_found ? (
                <AlertCircle className="h-4 w-4" />
              ) : (
                <CheckCircle className="h-4 w-4" />
              )}
              <AlertTitle>
                {result.vulnerabilities_found
                  ? "XSS Vulnerabilities Found!"
                  : "No XSS Vulnerabilities Detected"}
              </AlertTitle>
              <AlertDescription>
                Risk Level: {result.details.risk_level}
              </AlertDescription>
            </Alert>
          )}

          {result && result.vulnerabilities_found && (
            <div className="mt-4 space-y-2">
              <h3 className="font-semibold">Vulnerability Details:</h3>
              <pre className="bg-gray-100 p-4 rounded-md overflow-auto">
                {JSON.stringify(result.details, null, 2)}
              </pre>
            </div>
          )}
        </CardContent>
      </Card>
    </div>
  );
};

export default XSSScanner;
