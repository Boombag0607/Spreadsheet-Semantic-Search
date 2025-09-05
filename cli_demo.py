#!/usr/bin/env python3
"""
Command Line Interface for Spreadsheet Semantic Search Engine
Superjoin Hiring Assignment

This CLI provides an alternative way to test the semantic search functionality
without running the web server.
"""

import argparse
import json
import sys
import os
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from semantic_search import SemanticSearchEngine
from spreadsheet_loader import SpreadsheetLoader
from models import SearchQuery

class CLIDemo:
    def __init__(self):
        self.search_engine = SemanticSearchEngine()
        self.loader = SpreadsheetLoader()
        self.data_loaded = False
    
    def load_sample_data(self):
        """Load sample financial data"""
        print("🔄 Loading sample financial data...")
        
        # Create comprehensive sample data
        sample_data = {
            "name": "Financial Analysis Demo",
            "sheets": {
                "Revenue Analysis": {
                    "data": [
                        ["", "Q1 2024", "Q2 2024", "Q3 2024", "Q4 2024", "Total"],
                        ["Product A Revenue", 150000, 165000, 175000, 190000, "=SUM(B2:E2)"],
                        ["Product B Revenue", 120000, 135000, 145000, 160000, "=SUM(B3:E3)"],
                        ["Service Revenue", 85000, 95000, 105000, 115000, "=SUM(B4:E4)"],
                        ["Total Revenue", "=SUM(B2:B4)", "=SUM(C2:C4)", "=SUM(D2:D4)", "=SUM(E2:E4)", "=SUM(B5:E5)"],
                        ["", "", "", "", "", ""],
                        ["Revenue Growth Rates", "", "", "", "", ""],
                        ["QoQ Growth Rate", "", "=C5/B5-1", "=D5/C5-1", "=E5/D5-1", ""],
                        ["YoY Growth Rate", "15%", "18%", "22%", "25%", ""],
                        ["", "", "", "", "", ""],
                        ["Cost Analysis", "", "", "", "", ""],
                        ["Cost of Goods Sold", 195000, 218000, 235000, 260000, "=SUM(B11:E11)"],
                        ["Gross Profit", "=B5-B11", "=C5-C11", "=D5-D11", "=E5-E11", "=SUM(B12:E12)"],
                        ["Gross Profit Margin", "=B12/B5", "=C12/C5", "=D12/D5", "=E12/E5", "=F12/F5"]
                    ]
                },
                "Expense Dashboard": {
                    "data": [
                        ["Operating Expenses", "Q1 2024", "Q2 2024", "Q3 2024", "Q4 2024"],
                        ["", "", "", "", ""],
                        ["Sales & Marketing", 75000, 82000, 88000, 95000],
                        ["Marketing ROI", "=RevAnalysis!B5/B3", "=RevAnalysis!C5/C3", "=RevAnalysis!D5/D3", "=RevAnalysis!E5/E3"],
                        ["General & Admin", 45000, 48000, 52000, 58000],
                        ["R&D Expenses", 65000, 72000, 78000, 85000],
                        ["Total OpEx", "=SUM(B3:B6)", "=SUM(C3:C6)", "=SUM(D3:D6)", "=SUM(E3:E6)"],
                        ["", "", "", "", ""],
                        ["Efficiency Metrics", "", "", "", ""],
                        ["OpEx as % of Revenue", "=B7/RevAnalysis!B5", "=C7/RevAnalysis!C5", "=D7/RevAnalysis!D5", "=E7/RevAnalysis!E5"],
                        ["Expense Growth Rate", "", "=C7/B7-1", "=D7/C7-1", "=E7/D7-1"],
                        ["Cost per Employee", "=B7/125", "=C7/132", "=D7/138", "=E7/145"]
                    ]
                },
                "KPI Scorecard": {
                    "data": [
                        ["Key Performance Indicators", "Current", "Target", "Variance", "Performance"],
                        ["", "", "", "", ""],
                        ["Financial Metrics", "", "", "", ""],
                        ["Revenue Growth (YoY)", "22%", "18%", "4%", "Above Target"],
                        ["Gross Profit Margin", "45%", "42%", "3%", "Above Target"],
                        ["EBITDA Margin", "28%", "25%", "3%", "Above Target"],
                        ["Operating Margin", "18%", "15%", "3%", "Above Target"],
                        ["", "", "", "", ""],
                        ["Efficiency Ratios", "", "", "", ""],
                        ["Asset Turnover Ratio", "1.8x", "1.5x", "0.3x", "Above Target"],
                        ["Return on Assets", "15%", "12%", "3%", "Above Target"],
                        ["Return on Equity", "22%", "18%", "4%", "Above Target"],
                        ["Working Capital Ratio", "2.1", "2.0", "0.1", "Above Target"],
                        ["", "", "", "", ""],
                        ["Growth Metrics", "", "", "", ""],
                        ["Customer Growth Rate", "12%", "10%", "2%", "Above Target"],
                        ["Market Share Growth", "8%", "6%", "2%", "Above Target"],
                        ["Product Line Growth", "25%", "20%", "5%", "Above Target"]
                    ]
                },
                "Budget vs Actual": {
                    "data": [
                        ["Budget vs Actual Analysis", "Budget", "Actual", "Variance", "Variance %"],
                        ["", "", "", "", ""],
                        ["Revenue Items", "", "", "", ""],
                        ["Product Sales Budget", 600000, 630000, 30000, "=D4/B4"],
                        ["Service Revenue Budget", 300000, 315000, 15000, "=D5/B5"],
                        ["Total Revenue Budget", "=B4+B5", "=C4+C5", "=C6-B6", "=D6/B6"],
                        ["", "", "", "", ""],
                        ["Expense Items", "", "", "", ""],
                        ["Marketing Budget", 280000, 295000, 15000, "=D9/B9"],
                        ["Operations Budget", 180000, 175000, -5000, "=D10/B10"],
                        ["Total Expense Budget", "=B9+B10", "=C9+C10", "=C11-B11", "=D11/B11"],
                        ["", "", "", "", ""],
                        ["Profitability Analysis", "", "", "", ""],
                        ["Planned Profit", "=B6-B11", "=C6-C11", "=C13-B13", "=D13/B13"],
                        ["Profit Margin Plan", "=B13/B6", "=C13/C6", "", ""]
                    ]
                }
            }
        }
        
        self.search_engine.load_spreadsheet_data(sample_data)
        self.data_loaded = True
        print("✅ Sample data loaded successfully!")
        print(f"📊 Loaded {len(sample_data['sheets'])} sheets with business data")
    
    def run_interactive_demo(self):
        """Run interactive CLI demo"""
        print("\n" + "="*60)
        print("🔍 SPREADSHEET SEMANTIC SEARCH ENGINE")
        print("   Superjoin Hiring Assignment Demo")
        print("="*60)
        
        if not self.data_loaded:
            self.load_sample_data()
        
        print("\n💡 Try these sample queries:")
        sample_queries = [
            "find profitability metrics",
            "show cost calculations", 
            "where are my growth rates",
            "find efficiency ratios",
            "show percentage calculations",
            "budget vs actual analysis",
            "find average formulas",
            "what conditional calculations exist",
            "show revenue trends",
            "margin analysis"
        ]
        
        for i, query in enumerate(sample_queries, 1):
            print(f"  {i:2d}. {query}")
        
        print("\n" + "-"*60)
        
        while True:
            try:
                query = input("\n🔍 Enter your search query (or 'quit' to exit): ").strip()
                
                if query.lower() in ['quit', 'exit', 'q']:
                    print("👋 Thank you for trying the Semantic Search Engine!")
                    break
                
                if not query:
                    print("⚠️  Please enter a search query.")
                    continue
                
                print(f"\n🔄 Searching for: '{query}'")
                print("-" * 40)
                
                # Perform search
                results = self.search_engine.search(query, max_results=8)
                
                if not results:
                    print("❌ No results found. Try a different query.")
                    continue
                
                # Display results
                print(f"🎯 Found {len(results)} results:\n")
                
                for i, result in enumerate(results, 1):
                    print(f"📍 Result {i}:")
                    print(f"   🏷️  Concept: {result.concept_name}")
                    print(f"   📍 Location: {result.location}")
                    print(f"   💡 Context: {result.business_context}")
                    if result.formula:
                        print(f"   🧮 Formula: {result.formula}")
                    if result.value:
                        print(f"   💰 Value: {result.value}")
                    print(f"   🔍 Match: {result.explanation}")
                    print(f"   📊 Relevance: {result.relevance_score:.1%}")
                    print()
                
            except KeyboardInterrupt:
                print("\n\n👋 Goodbye!")
                break
            except Exception as e:
                print(f"❌ Error: {str(e)}")
    
    def run_batch_demo(self, queries: list):
        """Run batch demo with predefined queries"""
        if not self.data_loaded:
            self.load_sample_data()
        
        print("\n🚀 Running Batch Demo with Sample Queries")
        print("="*50)
        
        for i, query in enumerate(queries, 1):
            print(f"\n📝 Query {i}: '{query}'")
            print("-" * 30)
            
            results = self.search_engine.search(query, max_results=3)
            
            if results:
                for j, result in enumerate(results, 1):
                    print(f"  {j}. {result.concept_name} ({result.relevance_score:.1%} match)")
                    print(f"     📍 {result.location}")
                    print(f"     💡 {result.explanation}")
            else:
                print("  ❌ No results found")

def main():
    parser = argparse.ArgumentParser(
        description="Spreadsheet Semantic Search Engine - CLI Demo"
    )
    
    parser.add_argument(
        '--mode', 
        choices=['interactive', 'batch'],
        default='interactive',
        help='Demo mode: interactive or batch'
    )
    
    parser.add_argument(
        '--queries',
        nargs='+',
        help='Custom queries for batch mode'
    )
    
    args = parser.parse_args()
    
    demo = CLIDemo()
    
    if args.mode == 'interactive':
        demo.run_interactive_demo()
    else:
        # Batch mode
        if args.queries:
            queries = args.queries
        else:
            # Default batch queries
            queries = [
                "find profitability metrics",
                "show cost calculations", 
                "where are my growth rates",
                "find efficiency ratios",
                "budget vs actual analysis"
            ]
        
        demo.run_batch_demo(queries)

if __name__ == "__main__":
    main()