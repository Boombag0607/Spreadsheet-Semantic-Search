from pydantic import BaseModel
from typing import List, Optional, Any, Dict

class SearchQuery(BaseModel):
    """Model for search query requests"""
    query: str
    max_results: int = 10
    include_formulas: bool = True
    include_values: bool = True

class SearchResult(BaseModel):
    """Model for individual search results"""
    concept_name: str
    location: str
    formula: Optional[str] = None
    value: Optional[str] = None
    business_context: str
    explanation: str
    relevance_score: float

class SearchResponse(BaseModel):
    """Model for search response"""
    query: str
    results: List[SearchResult]
    total_results: int

class SpreadsheetInfo(BaseModel):
    """Model for spreadsheet information"""
    name: str
    sheets: List[str]
    total_cells: int
    concepts_identified: List[str]

class ConceptSummary(BaseModel):
    """Model for business concept summary"""
    category: str
    concepts: List[str]
    count: int
    examples: List[str]