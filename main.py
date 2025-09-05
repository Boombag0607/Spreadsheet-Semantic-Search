from fastapi import FastAPI, HTTPException, UploadFile, File, Form
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, FileResponse
import uvicorn
import os
from pathlib import Path

# Import our custom modules
from src.semantic_search import SemanticSearchEngine
from src.spreadsheet_loader import SpreadsheetLoader
from src.models import SearchQuery, SearchResponse

# Create FastAPI app
app = FastAPI(title="Spreadsheet Semantic Search Engine", version="1.0.0")

# Mount static files
static_dir = Path("static")
static_dir.mkdir(exist_ok=True)
app.mount("/static", StaticFiles(directory="static"), name="static")

# Initialize the search engine
search_engine = SemanticSearchEngine()
loader = SpreadsheetLoader()

# Global storage for loaded spreadsheets
loaded_spreadsheets = {}

@app.get("/", response_class=HTMLResponse)
async def get_demo_interface():
    """Serve the demo web interface"""
    html_content = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Spreadsheet Semantic Search</title>
        <style>
    body {
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        max-width: 1200px;
        margin: 0 auto;
        padding: 20px;
        background: #000; /* Black background */
        color: #fff; /* White text */
        min-height: 100vh;
    }
    .container {
        background: #2b2b2b; /* Dark gray container */
        border-radius: 15px;
        padding: 30px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.6);
    }
    h1 {
        color: #fff;
        text-align: center;
        margin-bottom: 30px;
        font-size: 2.5em;
    }
    .upload-section, .sample-section, .search-section {
        margin-bottom: 30px;
        padding: 20px;
        border: 2px dashed #555; /* darker gray borders */
        border-radius: 10px;
        background: #1e1e1e; /* darker background */
    }
    .upload-section h2, .sample-section h2, .search-section h2 {
        color: #ccc;
        margin-bottom: 15px;
    }
    input, button, select {
        padding: 12px;
        border: 1px solid #555;
        border-radius: 5px;
        font-size: 16px;
        background: #111;
        color: #fff;
    }
    button {
        background: #6b46c1; /* Purple button */
        color: white;
        border: none;
        cursor: pointer;
        transition: all 0.3s ease;
        margin: 5px;
    }
    button:hover {
        transform: translateY(-2px);
        box-shadow: 0 5px 15px rgba(0,0,0,0.5);
        background: #805ad5; /* lighter purple on hover */
    }
    button:disabled {
        opacity: 0.6;
        cursor: not-allowed;
        transform: none;
    }
    .file-input {
        display: none;
    }
    .file-input-label {
        display: inline-block;
        padding: 12px 20px;
        background: #6b46c1; /* Purple button */
        color: white;
        border-radius: 5px;
        cursor: pointer;
        transition: all 0.3s ease;
    }
    .file-input-label:hover {
        transform: translateY(-2px);
        box-shadow: 0 5px 15px rgba(0,0,0,0.5);
        background: #805ad5;
    }
    .file-name {
        margin-top: 10px;
        color: #aaa;
        font-style: italic;
    }
    .upload-btn {
        background: #6b46c1;
    }
    .search-input {
        width: 70%;
        margin-right: 10px;
    }
    .search-button {
        width: 25%;
    }
    .results {
        margin-top: 30px;
    }
    .result-item {
        background: #2d2d2d;
        border-left: 4px solid #6b46c1;
        padding: 20px;
        margin-bottom: 20px;
        border-radius: 5px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.4);
    }
    .result-header {
        font-weight: bold;
        color: #fff;
        font-size: 18px;
        margin-bottom: 10px;
    }
    .result-details {
        color: #bbb;
        line-height: 1.6;
    }
    .relevance-score {
        background: #6b46c1;
        color: white;
        padding: 5px 10px;
        border-radius: 15px;
        font-size: 12px;
        float: right;
    }
    .demo-queries {
        margin-top: 20px;
        padding: 15px;
        background: #1a1a1a;
        border-radius: 5px;
    }
    .demo-queries h3 {
        color: #fff;
        margin-bottom: 10px;
    }
    .demo-query {
        display: inline-block;
        background: #6b46c1;
        color: white;
        padding: 5px 10px;
        margin: 3px;
        border-radius: 15px;
        cursor: pointer;
        font-size: 12px;
        transition: all 0.3s ease;
    }
    .demo-query:hover {
        background: #805ad5;
        transform: scale(1.05);
    }
    .loading {
        text-align: center;
        color: #6b46c1;
        font-style: italic;
    }
    .spinner {
        display: inline-block;
        width: 16px;
        height: 16px;
        border: 2px solid #333;
        border-top: 2px solid #6b46c1;
        border-radius: 50%;
        animation: spin 1s linear infinite;
        margin-right: 8px;
    }
    @keyframes spin {
        0% { transform: rotate(0deg); }
        100% { transform: rotate(360deg); }
    }
    .error {
        color: #e53e3e;
        background: #331111;
        padding: 10px;
        border-radius: 5px;
        margin: 10px 0;
    }
    .success {
        color: #38a169;
        background: #13331d;
        padding: 10px;
        border-radius: 5px;
        margin: 10px 0;
    }
    .info {
        color: #63b3ed;
        background: #112233;
        padding: 10px;
        border-radius: 5px;
        margin: 10px 0;
    }
    .file-summary {
        background: #1e1e1e;
        border: 1px solid #333;
        border-radius: 8px;
        padding: 15px;
        margin-top: 15px;
    }
    .file-summary h3 {
        color: #fff;
        margin-bottom: 10px;
    }
    .summary-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
        gap: 10px;
        margin-top: 10px;
    }
    .summary-item {
        background: #2b2b2b;
        padding: 10px;
        border-radius: 5px;
        border-left: 3px solid #6b46c1;
    }
    .summary-label {
        font-size: 12px;
        color: #aaa;
        margin-bottom: 3px;
    }
    .summary-value {
        font-weight: bold;
        color: #fff;
    }
</style>

    </head>
    <body>
        <div class="container">
            <h1>🔍 Spreadsheet Semantic Search</h1>
            
            <!-- File Upload Section -->
            <div class="upload-section">
                <h2>📁 Upload Your Spreadsheet</h2>
                <form id="uploadForm">
                    <label for="fileInput" class="file-input-label">
                        Choose File (Excel/CSV)
                    </label>
                    <input type="file" id="fileInput" class="file-input" accept=".xlsx,.xls,.csv">
                    <div class="file-name" id="fileName"></div>
                    <button type="submit" class="upload-btn" id="uploadBtn" disabled>
                        Upload & Process
                    </button>
                </form>
                <div id="upload-status"></div>
                <div id="file-summary"></div>
            </div>

            <!-- Sample Data Section -->
            <div class="sample-section">
                <h2>📊 Or Try Sample Data</h2>
                <button onclick="loadTestData()">Load Sample Financial Data</button>
                <div id="load-status"></div>
            </div>

            <div class="search-section">
                <h2>🤖 Semantic Search</h2>
                <div>
                    <input type="text" id="searchQuery" class="search-input" 
                           placeholder="Try: 'find profitability metrics' or 'show cost calculations'"
                           disabled>
                    <button class="search-button" id="searchButton" onclick="performSearch()" disabled>Search</button>
                </div>
                
                <div class="demo-queries">
                    <h3>💡 Try these sample queries:</h3>
                    <div class="demo-query" onclick="setQuery('find profitability metrics')">find profitability metrics</div>
                    <div class="demo-query" onclick="setQuery('show cost calculations')">show cost calculations</div>
                    <div class="demo-query" onclick="setQuery('where are my growth rates')">where are my growth rates</div>
                    <div class="demo-query" onclick="setQuery('find efficiency ratios')">find efficiency ratios</div>
                    <div class="demo-query" onclick="setQuery('show percentage calculations')">show percentage calculations</div>
                    <div class="demo-query" onclick="setQuery('budget vs actual analysis')">budget vs actual analysis</div>
                    <div class="demo-query" onclick="setQuery('find average formulas')">find average formulas</div>
                    <div class="demo-query" onclick="setQuery('what conditional calculations exist')">what conditional calculations exist</div>
                </div>
            </div>

            <div id="results" class="results"></div>
            <div>Made with ❤️ by &#169; Ananya Gautam, 2025</div>
        </div>

        <script>
            const fileInput = document.getElementById('fileInput');
            const fileName = document.getElementById('fileName');
            const uploadBtn = document.getElementById('uploadBtn');
            const uploadForm = document.getElementById('uploadForm');
            const uploadStatus = document.getElementById('upload-status');
            const fileSummary = document.getElementById('file-summary');
            const searchQuery = document.getElementById('searchQuery');
            const searchButton = document.getElementById('searchButton');

            // File input change handler
            fileInput.addEventListener('change', function(e) {
                const file = e.target.files[0];
                if (file) {
                    fileName.innerHTML = `Selected: <strong>${file.name}</strong> (${(file.size / 1024 / 1024).toFixed(2)} MB)`;
                    uploadBtn.disabled = false;
                } else {
                    fileName.innerHTML = '';
                    uploadBtn.disabled = true;
                }
            });

            // Upload form handler
            uploadForm.addEventListener('submit', async function(e) {
                e.preventDefault();
                
                const file = fileInput.files[0];
                if (!file) {
                    showStatus(uploadStatus, 'Please select a file first.', 'error');
                    return;
                }

                const formData = new FormData();
                formData.append('file', file);

                uploadBtn.disabled = true;
                uploadBtn.innerHTML = '<span class="spinner"></span>Uploading...';
                showStatus(uploadStatus, 'Uploading and processing file...', 'info');

                try {
                    const response = await fetch('/load_file', {
                        method: 'POST',
                        body: formData
                    });

                    const data = await response.json();

                    if (response.ok) {
                        showStatus(uploadStatus, data.message, 'success');
                        displayFileSummary(data.summary);
                        enableSearch();
                    } else {
                        showStatus(uploadStatus, `Error: ${data.detail}`, 'error');
                    }
                } catch (error) {
                    showStatus(uploadStatus, `Upload failed: ${error.message}`, 'error');
                } finally {
                    uploadBtn.disabled = false;
                    uploadBtn.innerHTML = 'Upload & Process';
                }
            });

            function setQuery(query) {
                document.getElementById('searchQuery').value = query;
            }

            async function loadTestData() {
                const statusDiv = document.getElementById('load-status');
                statusDiv.innerHTML = '<div class="loading"><span class="spinner"></span>Loading test data...</div>';
                
                try {
                    const response = await fetch('/load_test_data', {
                        method: 'POST'
                    });
                    const result = await response.json();
                    
                    if (response.ok) {
                        statusDiv.innerHTML = `<div class="success">${result.message}</div>`;
                        enableSearch();
                    } else {
                        statusDiv.innerHTML = `<div class="error">Error: ${result.detail}</div>`;
                    }
                } catch (error) {
                    statusDiv.innerHTML = `<div class="error">Error loading data: ${error.message}</div>`;
                }
            }

            async function performSearch() {
                const query = document.getElementById('searchQuery').value;
                if (!query.trim()) return;
                
                const resultsDiv = document.getElementById('results');
                resultsDiv.innerHTML = '<div class="loading"><span class="spinner"></span>Searching...</div>';
                
                try {
                    const response = await fetch('/search', {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json'
                        },
                        body: JSON.stringify({
                            query: query,
                            max_results: 10
                        })
                    });
                    
                    const data = await response.json();
                    
                    if (response.ok) {
                        displayResults(data);
                    } else {
                        resultsDiv.innerHTML = `<div class="error">Search error: ${data.detail}</div>`;
                    }
                } catch (error) {
                    resultsDiv.innerHTML = `<div class="error">Error: ${error.message}</div>`;
                }
            }

            function displayResults(searchResponse) {
                const resultsDiv = document.getElementById('results');
                
                if (!searchResponse.results || searchResponse.results.length === 0) {
                    resultsDiv.innerHTML = '<div class="result-item">No results found. Try a different query.</div>';
                    return;
                }

                let html = `<h2>🎯 Search Results (${searchResponse.results.length} found)</h2>`;
                
                searchResponse.results.forEach((result, index) => {
                    html += `
                        <div class="result-item">
                            <div class="result-header">
                                <span class="relevance-score">${(result.relevance_score * 100).toFixed(1)}% match</span>
                                ${result.concept_name}
                            </div>
                            <div class="result-details">
                                <strong>📍 Location:</strong> ${result.location}<br>
                                <strong>💡 Concept:</strong> ${result.business_context}<br>
                                ${result.formula ? `<strong>🧮 Formula:</strong> <code>${result.formula}</code><br>` : ''}
                                ${result.value ? `<strong>💰 Value:</strong> ${result.value}<br>` : ''}
                                <strong>🔍 Why it matched:</strong> ${result.explanation}
                            </div>
                        </div>
                    `;
                });
                
                resultsDiv.innerHTML = html;
            }

            function showStatus(element, message, type) {
                element.innerHTML = `<div class="${type}">${message}</div>`;
            }

            function displayFileSummary(summary) {
                let html = `
                    <div class="file-summary">
                        <h3>📋 File Summary</h3>
                        <div class="summary-grid">
                            <div class="summary-item">
                                <div class="summary-label">Filename</div>
                                <div class="summary-value">${summary.filename}</div>
                            </div>
                            <div class="summary-item">
                                <div class="summary-label">Sheets</div>
                                <div class="summary-value">${summary.total_sheets}</div>
                            </div>
                            <div class="summary-item">
                                <div class="summary-label">Total Rows</div>
                                <div class="summary-value">${summary.total_rows || 'N/A'}</div>
                            </div>
                            <div class="summary-item">
                                <div class="summary-label">Data Cells</div>
                                <div class="summary-value">${summary.total_cells}</div>
                            </div>
                        </div>
                `;

                if (summary.sheet_names && summary.sheet_names.length > 0) {
                    html += `
                        <div style="margin-top: 15px;">
                            <div class="summary-label">Sheet Names:</div>
                            <div class="summary-value">${summary.sheet_names.join(', ')}</div>
                        </div>
                    `;
                }

                html += '</div>';
                fileSummary.innerHTML = html;
            }

            function enableSearch() {
                searchQuery.disabled = false;
                searchButton.disabled = false;
            }

            // Allow Enter key to trigger search
            document.getElementById('searchQuery').addEventListener('keypress', function(e) {
                if (e.key === 'Enter' && !searchQuery.disabled) {
                    performSearch();
                }
            });
        </script>
    </body>
    </html>
    """
    return HTMLResponse(content=html_content)

@app.post("/load_file")
async def load_file(file: UploadFile = File(...)):
    """Load spreadsheet data from uploaded file"""
    try:
        # Validate file type
        if not file.filename:
            raise HTTPException(status_code=400, detail="No file provided")
        
        # Check if file extension is supported
        file_extension = file.filename.lower().split('.')[-1]
        supported_extensions = ['xlsx', 'xls', 'csv']
        
        if file_extension not in supported_extensions:
            raise HTTPException(
                status_code=400, 
                detail=f"Unsupported file type. Supported formats: {', '.join(supported_extensions)}"
            )
        
        # Check file size (50MB limit)
        MAX_FILE_SIZE = 50 * 1024 * 1024  # 50MB
        file_content = await file.read()
        
        if len(file_content) > MAX_FILE_SIZE:
            raise HTTPException(
                status_code=413, 
                detail="File too large. Maximum size is 50MB"
            )
        
        # Load the spreadsheet data
        spreadsheet_data = loader.load_from_bytes(file_content, file.filename)
        
        # Validate the loaded data
        if not loader.validate_spreadsheet_data(spreadsheet_data):
            raise HTTPException(status_code=400, detail="Invalid spreadsheet data format")
        
        # Load the data into the search engine
        search_engine.load_spreadsheet_data(spreadsheet_data)
        
        # Get summary information
        summary = loader.get_spreadsheet_summary(spreadsheet_data)
        
        return {
            "message": f"File '{file.filename}' loaded successfully! You can now perform semantic searches.",
            "summary": {
                "filename": file.filename,
                "total_sheets": summary.get("total_sheets", 0),
                "sheet_names": summary.get("sheet_names", []),
                "total_rows": summary.get("total_rows", 0),
                "total_cells": summary.get("total_cells", 0)
            }
        }
        
    except HTTPException:
        # Re-raise HTTP exceptions
        raise
    except Exception as e:
        # Handle any other errors
        raise HTTPException(status_code=500, detail=f"Error loading file: {str(e)}")

@app.post("/load_test_data")
async def load_test_data():
    """Load sample spreadsheet data for testing"""
    try:
        # Create sample data
        sample_data = {
            "financial_model": {
                "sheets": {
                    "Revenue Analysis": {
                        "data": [
                            ["", "Q1 2024", "Q2 2024", "Q3 2024", "Q4 2024"],
                            ["Total Revenue", 150000, 165000, 175000, 190000],
                            ["Product A Sales", 90000, 95000, 100000, 110000],
                            ["Product B Sales", 60000, 70000, 75000, 80000],
                            ["Gross Revenue", "=B2+C2+D2+E2", "", "", ""],
                            ["", "", "", "", ""],
                            ["Cost of Goods Sold", 75000, 82500, 87500, 95000],
                            ["Gross Profit", "=B2-B7", "=C2-C7", "=D2-D7", "=E2-E7"],
                            ["Gross Profit Margin", "=B8/B2", "=C8/C2", "=D8/D2", "=E8/E2"]
                        ]
                    },
                    "Expenses": {
                        "data": [
                            ["", "Q1 2024", "Q2 2024", "Q3 2024", "Q4 2024"],
                            ["Marketing Spend", 25000, 27000, 30000, 35000],
                            ["Marketing ROI", "=RevAnalysis!B8/B2", "=RevAnalysis!C8/C2", "", ""],
                            ["Operating Expenses", 45000, 48000, 52000, 58000],
                            ["Total Expenses", "=B2+B4", "=C2+C4", "=D2+D4", "=E2+E4"],
                            ["", "", "", "", ""],
                            ["Efficiency Ratio", "=RevAnalysis!B2/B4", "", "", ""],
                            ["Expense Growth Rate", "", "=C4/B4-1", "=D4/C4-1", "=E4/D4-1"]
                        ]
                    },
                    "KPI Dashboard": {
                        "data": [
                            ["Key Performance Indicators", "", "", ""],
                            ["", "Current", "Target", "Variance"],
                            ["Revenue Growth YoY", "15%", "12%", "25%"],
                            ["Profit Margin", "45%", "40%", "12.5%"],
                            ["Customer Acquisition Cost", "$150", "$200", "-25%"],
                            ["Return on Investment", "3.2x", "2.5x", "28%"],
                            ["Asset Turnover", "1.8", "1.5", "20%"],
                            ["Budget vs Actual Revenue", "102%", "100%", "2%"],
                            ["EBITDA Margin", "35%", "30%", "16.7%"],
                            ["Working Capital Ratio", "2.1", "2.0", "5%"]
                        ]
                    }
                }
            }
        }
        
        # Load the sample data into the search engine
        search_engine.load_spreadsheet_data(sample_data["financial_model"])
        
        return {"message": "Sample financial data loaded successfully! You can now perform semantic searches."}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error loading test data: {str(e)}")

@app.post("/search", response_model=SearchResponse)
async def search_spreadsheets(query: SearchQuery):
    """Perform semantic search on loaded spreadsheets"""
    try:
        if not search_engine.has_data():
            raise HTTPException(status_code=400, detail="No spreadsheet data loaded. Please load a file or sample data first.")
        
        results = search_engine.search(query.query, query.max_results)
        
        return SearchResponse(
            query=query.query,
            results=results,
            total_results=len(results)
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Search error: {str(e)}")

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "message": "Spreadsheet Semantic Search API is running"}

if __name__ == "__main__":
    print("🚀 Starting Spreadsheet Semantic Search Engine...")
    print("📊 Loading components...")
    
    # Create necessary directories
    os.makedirs("data", exist_ok=True)
    os.makedirs("static", exist_ok=True)
    
    print("✅ Ready! Visit http://localhost:8000 to try the demo")
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)