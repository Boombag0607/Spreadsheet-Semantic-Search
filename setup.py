#!/usr/bin/env python3
"""
Setup and Installation Script
Spreadsheet Semantic Search Engine
"""

import os
import sys
import subprocess
from pathlib import Path

def print_header():
    print("=" * 60)
    print("🔍 SPREADSHEET SEMANTIC SEARCH ENGINE")
    print("   Superjoin Hiring Assignment")
    print("   Setup and Installation")
    print("=" * 60)

def check_python_version():
    """Check if Python version is compatible"""
    print("\n📋 Checking Python version...")
    
    if sys.version_info < (3, 8):
        print("❌ Python 3.8 or higher is required")
        print(f"   Current version: {sys.version}")
        return False
    
    print(f"✅ Python {sys.version.split()[0]} detected")
    return True

def create_directories():
    """Create necessary directories"""
    print("\n📁 Creating directories...")
    
    directories = [
        "src",
        "data", 
        "static",
        "tests"
    ]
    
    for dir_name in directories:
        Path(dir_name).mkdir(exist_ok=True)
        print(f"   ✅ {dir_name}/")

def install_dependencies():
    """Install required Python packages"""
    print("\n📦 Installing dependencies...")
    
    try:
        # Upgrade pip first
        subprocess.run([sys.executable, "-m", "pip", "install", "--upgrade", "pip"], 
                      check=True, capture_output=True)
        
        # Install requirements
        subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"], 
                      check=True, capture_output=True)
        
        print("   ✅ All dependencies installed successfully")
        return True
        
    except subprocess.CalledProcessError as e:
        print("   ❌ Error installing dependencies:")
        print(f"      {e}")
        return False
    except FileNotFoundError:
        print("   ❌ requirements.txt not found")
        return False

def download_models():
    """Download required ML models"""
    print("\n🤖 Downloading semantic models...")
    
    try:
        # Import after installation to ensure packages are available
        from sentence_transformers import SentenceTransformer
        
        # Download the model (will cache automatically)
        model = SentenceTransformer('all-MiniLM-L6-v2')
        print("   ✅ Sentence transformer model downloaded")
        
        return True
        
    except ImportError:
        print("   ❌ sentence-transformers not properly installed")
        return False
    except Exception as e:
        print(f"   ❌ Error downloading models: {e}")
        return False

def run_quick_test():
    """Run a quick test to verify installation"""
    print("\n🧪 Running quick test...")
    
    try:
        # Import core modules
        sys.path.insert(0, "src")
        from semantic_search import SemanticSearchEngine
        from business_concepts import BusinessConceptMapper
        
        # Quick functionality test
        search_engine = SemanticSearchEngine()
        concept_mapper = BusinessConceptMapper()
        
        # Test concept identification
        concepts = concept_mapper.identify_concepts("revenue growth margin")
        
        if len(concepts) > 0:
            print("   ✅ Core functionality working")
            print(f"   📊 Identified concepts: {', '.join(concepts[:3])}")
            return True
        else:
            print("   ⚠️  Core functionality test failed")
            return False
            
    except ImportError as e:
        print(f"   ❌ Import error: {e}")
        return False
    except Exception as e:
        print(f"   ❌ Test error: {e}")
        return False

def print_usage_instructions():
    """Print how to use the system"""
    print("\n🚀 INSTALLATION COMPLETE!")
    print("\n" + "=" * 40)
    print("HOW TO RUN:")
    print("=" * 40)
    
    print("\n1️⃣ WEB INTERFACE (Recommended):")
    print("   python main.py")
    print("   Then open: http://localhost:8000")
    
    print("\n2️⃣ COMMAND LINE INTERFACE:")
    print("   python cli_demo.py --mode interactive")
    
    print("\n3️⃣ BATCH TESTING:")
    print("   python cli_demo.py --mode batch")
    
    print("\n" + "=" * 40)
    print("SAMPLE QUERIES TO TRY:")
    print("=" * 40)
    
    queries = [
        "find profitability metrics",
        "show cost calculations", 
        "where are my growth rates",
        "find efficiency ratios",
        "show percentage calculations",
        "budget vs actual analysis"
    ]
    
    for i, query in enumerate(queries, 1):
        print(f"   {i}. {query}")
    
    print("\n📚 For more details, see README.md")
    print("📋 For technical details, see DESIGN_DOCUMENT.md")

def main():
    """Main setup function"""
    print_header()
    
    # Check prerequisites
    if not check_python_version():
        return False
    
    # Setup steps
    create_directories()
    
    if not install_dependencies():
        print("\n❌ Setup failed at dependency installation")
        return False
    
    if not download_models():
        print("\n⚠️  Model download failed, but basic functionality should work")
    
    if not run_quick_test():
        print("\n⚠️  Quick test failed, but you can still try running the system")
    
    print_usage_instructions()
    return True

if __name__ == "__main__":
    success = main()
    if not success:
        print("\n❌ Setup encountered errors. Please check the output above.")
        sys.exit(1)
    else:
        print("\n✅ Setup completed successfully!")
        sys.exit(0)