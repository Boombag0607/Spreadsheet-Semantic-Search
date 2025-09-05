# 🚀 How to Run the Spreadsheet Semantic Search Engine Locally

This guide will get you up and running with the semantic search engine in just a few minutes.

## 📋 Prerequisites

- **Python 3.8 or higher** (Check with `python --version`)
- **pip** package manager
- **8GB+ RAM** recommended (for ML models)
- **Internet connection** (for initial model downloads)

## ⚡ Quick Start (5 minutes)

### Step 1: Download and Extract Files
Create a new folder and save all the provided files:

```
spreadsheet-search/
├── main.py
├── cli_demo.py  
├── setup.py
├── requirements.txt
├── README.md
├── DESIGN_DOCUMENT.md
├── HOW_TO_RUN_LOCALLY.md
└── src/
    ├── __init__.py
    ├── semantic_search.py
    ├── business_concepts.py
    ├── spreadsheet_loader.py
    └── models.py
```

### Step 2: Install Dependencies

**Option A: Automatic Setup (Recommended)**
```bash
cd spreadsheet-search
python setup.py
```

**Option B: Manual Setup**
```bash
cd spreadsheet-search
pip install -r requirements.txt
```

### Step 3: Run the System

**Web Interface (Recommended):**
```bash
python main.py
```
Then open: `http://localhost:8000`

**Command Line Interface:**
```bash
python cli_demo.py --mode interactive
```

## 🌐 Using the Web Interface

1. **Start the server**:
   ```bash
   python main.py
   ```

2. **Open your browser** to `http://localhost:8000`

3. **Load sample data**: Click "Load Sample Financial Data"

4. **Try sample queries**:
   - "find profitability metrics"
   - "show cost calculations"  
   - "where are my growth rates"
   - "budget vs actual analysis"

5. **View detailed results** with explanations and relevance scores

## 💻 Using the Command Line Interface

### Interactive Mode
```bash
python cli_demo.py --mode interactive
```
- Enter queries when prompted
- Type 'quit' to exit
- See results with full context

### Batch Mode  
```bash
python cli_demo.py --mode batch --queries "find margins" "show growth rates"
```

## 🧪 Test Queries to Try

### Business Analysis Queries
```
find profitability metrics
show cost calculations
where are my growth rates
find efficiency ratios
budget vs actual analysis
variance analysis
```

### Formula Analysis Queries
```
show percentage calculations  
find average formulas
what conditional calculations exist
show lookup formulas
sum calculations
```

### Comparative Analysis
```
budget vs actual analysis
time series data
YoY growth analysis
margin trends
```

## 🔧 Troubleshooting

### Common Issues and Solutions

**Issue**: `ModuleNotFoundError: No module named 'sentence_transformers'`
```bash
# Solution: Install missing dependencies
pip install sentence-transformers
```

**Issue**: `Port 8000 is already in use`
```bash
# Solution: Use a different port
python main.py --port 8001
# Or kill the process using port 8000
```

**Issue**: Out of memory errors
```bash
# Solution: Use smaller model or reduce max_results
# Edit semantic_search.py line 12:
# self.model = SentenceTransformer('all-MiniLM-L6-v2')  # Smaller model
```

**Issue**: Slow initial startup
```bash
# This is normal - the system downloads ML models on first run
# Subsequent starts will be much faster
```

### Debugging Steps

1. **Check Python version**:
   ```bash
   python --version  # Should be 3.8+
   ```

2. **Verify installation**:
   ```bash
   python -c "import src.semantic_search; print('✅ Import successful')"
   ```

3. **Test basic functionality**:
   ```bash
   python cli_demo.py --mode batch --queries "test query"
   ```

## 🎯 Performance Tips

### For Better Speed
- Keep the web server running (models stay loaded)
- Use shorter queries when possible
- Limit max_results to 5-10 for faster responses

### For Better Results  
- Use business terminology in queries
- Be specific about what you're looking for
- Try different phrasings of the same concept

## 📂 Project Structure

```
spreadsheet-search/
├── main.py                 # FastAPI web server
├── cli_demo.py            # Command line interface  
├── setup.py               # Automated setup script
├── requirements.txt       # Python dependencies
├── README.md             # Full documentation
├── DESIGN_DOCUMENT.md    # Technical design details
└── src/                  # Core engine code
    ├── semantic_search.py    # Main search engine
    ├── business_concepts.py  # Business domain knowledge
    ├── spreadsheet_loader.py # Data loading utilities
    ├── models.py            # Data structures
    └── __init__.py          # Package initialization
```

## 🔍 Understanding the Results

Each search result includes:

- **🏷️ Concept Name**: What business concept this represents
- **📍 Location**: Excel-style cell reference  
- **🧮 Formula**: The actual formula (if applicable)
- **💰 Value**: Current cell value
- **💡 Context**: Business context explanation
- **🔍 Match Explanation**: Why this result matched your query
- **📊 Relevance Score**: Confidence percentage

## 🚀 Advanced Usage

### Custom Queries
The system supports natural language queries. Try:
- Asking questions: "What efficiency ratios do I have?"
- Being specific: "Find quarterly revenue growth rates"  
- Using synonyms: "Show earnings" (finds profit/revenue data)

### Multiple Concepts
- "Find revenue and cost data"
- "Show profitability and efficiency metrics"
- "Budget vs actual revenue analysis"

### Formula Searches
- "Show percentage calculations"
- "Find conditional formulas" 
- "What lookup formulas exist?"

## 📊 Sample Data

The system includes rich sample data with:
- **Financial Statements**: P&L, cash flow, balance sheet data
- **KPI Dashboards**: Performance metrics and ratios  
- **Budget Analysis**: Variance and comparison data
- **Revenue Analysis**: Growth rates and trends
- **Expense Tracking**: Cost breakdown and efficiency

## 🤝 Getting Help

If you encounter issues:

1. **Check the console output** for error messages
2. **Try the CLI mode** if web interface has issues
3. **Use simpler queries** to test basic functionality
4. **Review the sample queries** for proper formatting
5. **Check the design document** for technical details

## 🎯 Next Steps

Once you have it running:

1. **Try the sample queries** to understand capabilities
2. **Experiment with different phrasings** of the same concept
3. **Compare with traditional keyword search** to see the difference
4. **Review the design document** for technical insights
5. **Test with your own spreadsheet data** (coming soon)

---

**🎉 You're Ready!**

The semantic search engine should now be running locally. Enjoy exploring how it understands spreadsheet content conceptually rather than just structurally!

For questions or issues, refer to the README.md and DESIGN_DOCUMENT.md files for comprehensive documentation.