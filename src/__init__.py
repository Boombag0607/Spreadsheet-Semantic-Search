# Semantic Search Engine for Spreadsheets
# Built for Superjoin Hiring Assignment

from .semantic_search import SemanticSearchEngine
from .business_concepts import BusinessConceptMapper
from .spreadsheet_loader import SpreadsheetLoader
from .models import SearchQuery, SearchResult, SearchResponse

__version__ = "1.0.0"
__author__ = "Claude AI"
__description__ = "Semantic search engine for spreadsheets that understands business concepts"

__all__ = [
    'SemanticSearchEngine',
    'BusinessConceptMapper', 
    'SpreadsheetLoader',
    'SearchQuery',
    'SearchResult', 
    'SearchResponse'
]