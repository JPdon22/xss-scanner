from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from src.scanner.xss_scanner import AlgorandXSSScanner
from config.settings import ALGOD_ADDRESS, ALGOD_TOKEN

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ScanRequest(BaseModel):
    contract_url: str

@app.post("/api/scan")
async def scan_contract(request: ScanRequest):
    try:
        # Extract app_id from URL or use directly if it's just an ID
        app_id = request.contract_url.split('/')[-1]
        app_id = int(app_id)

        # Initialize scanner
        scanner = AlgorandXSSScanner(ALGOD_ADDRESS, ALGOD_TOKEN)

        # Perform scan
        results = scanner.scan_contract(app_id)

        return results
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid application ID")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="localhost", port=8000)
