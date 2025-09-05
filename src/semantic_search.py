import re
import json
from typing import List, Dict, Any, Tuple
from dataclasses import dataclass
import pandas as pd
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
from .business_concepts import BusinessConceptMapper
from .models import SearchResult

@dataclass
class SpreadsheetCell:
    sheet_name: str
    row: int
    col: int
    value: Any
    formula: str = ""
    header_context: str = ""
    business_concepts: List[str] = None
    semantic_embedding: np.ndarray = None

class SemanticSearchEngine:
    def __init__(self):
        # Initialize the sentence transformer for embeddings
        self.model = SentenceTransformer('all-MiniLM-L6-v2')
        
        # Initialize business concept mapper
        self.concept_mapper = BusinessConceptMapper()
        
        # Storage for processed spreadsheet data
        self.cells: List[SpreadsheetCell] = []
        self.sheet_data = {}
        
        # Pre-computed embeddings for business concepts
        self.concept_embeddings = {}
        self._precompute_concept_embeddings()
    
    def _precompute_concept_embeddings(self):
        """Pre-compute embeddings for business concepts"""
        concepts = self.concept_mapper.get_all_concepts()
        for category, concept_list in concepts.items():
            for concept in concept_list:
                # Create rich text for embedding
                concept_text = f"{concept['name']} {' '.join(concept['synonyms'])} {concept['description']}"
                self.concept_embeddings[concept['name']] = self.model.encode([concept_text])[0]
    
    def load_spreadsheet_data(self, spreadsheet_data: Dict[str, Any]):
        """Load and process spreadsheet data for semantic search"""
        self.sheet_data = spreadsheet_data
        self.cells = []
        
        for sheet_name, sheet_info in spreadsheet_data["sheets"].items():
            self._process_sheet(sheet_name, sheet_info["data"])
        
        # Compute embeddings for all cells
        self._compute_cell_embeddings()
        
        print(f"✅ Loaded {len(self.cells)} cells from {len(spreadsheet_data['sheets'])} sheets")
    
    def _process_sheet(self, sheet_name: str, data: List[List[Any]]):
        """Process individual sheet data"""
        if not data or len(data) == 0:
            return
        
        # Convert to pandas for easier processing
        df = pd.DataFrame(data)
        
        # Identify headers (usually first row or first column with strings)
        headers = {}
        if len(data) > 0:
            for col_idx, val in enumerate(data[0]):
                if isinstance(val, str) and val.strip():
                    headers[col_idx] = val.strip()
        
        # Process each cell
        for row_idx, row in enumerate(data):
            for col_idx, value in enumerate(row):
                if value is None or (isinstance(value, str) and not value.strip()):
                    continue
                
                # Determine header context
                header_context = ""
                if col_idx in headers:
                    header_context = headers[col_idx]
                
                # Check if it's a formula
                formula = ""
                if isinstance(value, str) and value.startswith('='):
                    formula = value
                
                # Identify business concepts
                concepts = self._identify_concepts(value, formula, header_context, sheet_name)
                
                cell = SpreadsheetCell(
                    sheet_name=sheet_name,
                    row=row_idx,
                    col=col_idx,
                    value=value,
                    formula=formula,
                    header_context=header_context,
                    business_concepts=concepts
                )
                
                self.cells.append(cell)
    
    def _identify_concepts(self, value: Any, formula: str, header: str, sheet_name: str) -> List[str]:
        """Identify business concepts associated with a cell"""
        concepts = []
        
        # Create context text for concept identification
        context_parts = []
        if header:
            context_parts.append(header)
        if isinstance(value, str):
            context_parts.append(value)
        if formula:
            context_parts.append(formula)
        context_parts.append(sheet_name)
        
        context_text = " ".join(str(part) for part in context_parts).lower()
        
        # Use business concept mapper to identify concepts
        identified_concepts = self.concept_mapper.identify_concepts(context_text)
        
        # Add formula-based concepts
        if formula:
            formula_concepts = self._analyze_formula_concepts(formula, header)
            identified_concepts.extend(formula_concepts)
        
        # Add value-based concepts
        if isinstance(value, (int, float)):
            value_concepts = self._analyze_value_concepts(value, header, context_text)
            identified_concepts.extend(value_concepts)
        
        return list(set(identified_concepts))  # Remove duplicates
    
    def _analyze_formula_concepts(self, formula: str, header: str = "") -> List[str]:
        """Analyze formulas to identify business concepts"""
        concepts = []
        formula_lower = formula.lower()
        header_lower = header.lower()
        
        # Mathematical operation patterns
        if any(op in formula_lower for op in ['/', 'divide']):
            if any(term in header_lower for term in ['margin', 'ratio', 'rate', 'percentage', '%']):
                concepts.append('ratio calculation')
                if 'margin' in header_lower:
                    concepts.append('profitability metric')
        
        # Aggregation functions
        if 'sum(' in formula_lower:
            concepts.append('aggregation formula')
            if any(term in header_lower for term in ['revenue', 'sales', 'income']):
                concepts.append('revenue calculation')
            elif any(term in header_lower for term in ['cost', 'expense']):
                concepts.append('cost calculation')
        
        if 'average(' in formula_lower or 'avg(' in formula_lower:
            concepts.append('average calculation')
        
        # Conditional logic
        if any(func in formula_lower for func in ['if(', 'sumif(', 'countif(']):
            concepts.append('conditional calculation')
        
        # Lookup functions
        if any(func in formula_lower for func in ['vlookup(', 'index(', 'match(']):
            concepts.append('lookup formula')
        
        return concepts
    
    def _analyze_value_concepts(self, value: Any, header: str = "", context: str = "") -> List[str]:
        """Analyze cell values to identify business concepts"""
        concepts = []
        header_lower = header.lower()
        context_lower = context.lower()
        
        # Percentage values
        if isinstance(value, str) and '%' in value:
            concepts.append('percentage value')
            if any(term in header_lower for term in ['margin', 'growth', 'rate']):
                concepts.append('percentage calculation')
        
        # Currency/monetary values
        if isinstance(value, (int, float)) and value > 1000:
            if any(term in context_lower for term in ['revenue', 'sales', 'income', 'profit', 'cost', 'expense']):
                concepts.append('monetary value')
        
        return concepts
    
    def _compute_cell_embeddings(self):
        """Compute semantic embeddings for all cells"""
        for cell in self.cells:
            # Create rich text representation for embedding
            text_parts = []
            
            if cell.header_context:
                text_parts.append(cell.header_context)
            
            text_parts.append(str(cell.value))
            
            if cell.formula:
                text_parts.append(cell.formula)
            
            if cell.business_concepts:
                text_parts.extend(cell.business_concepts)
            
            text_parts.append(cell.sheet_name)
            
            rich_text = " ".join(text_parts)
            cell.semantic_embedding = self.model.encode([rich_text])[0]
    
    def search(self, query: str, max_results: int = 10) -> List[SearchResult]:
        """Perform semantic search on the loaded spreadsheet data"""
        if not self.cells:
            return []
        
        # Process the query
        processed_query = self._process_query(query)
        
        # Get query embedding
        query_embedding = self.model.encode([processed_query])
        
        # Calculate similarities
        results = []
        for cell in self.cells:
            if cell.semantic_embedding is None:
                continue
            
            # Calculate semantic similarity
            similarity = cosine_similarity(query_embedding, [cell.semantic_embedding])[0][0]
            
            # Calculate concept-based relevance
            concept_relevance = self._calculate_concept_relevance(query, cell.business_concepts)
            
            # Calculate contextual relevance
            contextual_relevance = self._calculate_contextual_relevance(query, cell)
            
            # Combined relevance score
            final_score = (similarity * 0.4) + (concept_relevance * 0.4) + (contextual_relevance * 0.2)
            
            if final_score > 0.1:  # Threshold for relevance
                result = SearchResult(
                    concept_name=self._generate_concept_name(cell),
                    location=f"'{cell.sheet_name}'!{self._get_excel_cell_reference(cell.row, cell.col)}",
                    formula=cell.formula if cell.formula else None,
                    value=str(cell.value) if cell.value else None,
                    business_context=self._generate_business_context(cell),
                    explanation=self._generate_explanation(query, cell),
                    relevance_score=float(final_score)
                )
                results.append(result)
        
        # Sort by relevance score
        results.sort(key=lambda x: x.relevance_score, reverse=True)
        
        return results[:max_results]
    
    def _process_query(self, query: str) -> str:
        """Process and enhance the query for better matching"""
        # Expand query with synonyms and related terms
        expanded_terms = [query]
        
        # Add concept-based expansions
        for concept_name, embedding in self.concept_embeddings.items():
            query_embedding = self.model.encode([query])
            similarity = cosine_similarity(query_embedding, [embedding])[0][0]
            if similarity > 0.3:
                expanded_terms.append(concept_name)
        
        return " ".join(expanded_terms)
    
    def _calculate_concept_relevance(self, query: str, cell_concepts: List[str]) -> float:
        """Calculate how well cell concepts match the query"""
        if not cell_concepts:
            return 0.0
        
        query_lower = query.lower()
        relevance_scores = []
        
        # Check direct concept matches
        for concept in cell_concepts:
            concept_lower = concept.lower()
            if concept_lower in query_lower:
                relevance_scores.append(1.0)
            elif any(word in query_lower for word in concept_lower.split()):
                relevance_scores.append(0.7)
        
        # Use concept mapper for semantic matching
        query_concepts = self.concept_mapper.identify_concepts(query_lower)
        common_concepts = set(cell_concepts) & set(query_concepts)
        if common_concepts:
            relevance_scores.append(0.8)
        
        return max(relevance_scores) if relevance_scores else 0.0
    
    def _calculate_contextual_relevance(self, query: str, cell: SpreadsheetCell) -> float:
        """Calculate contextual relevance based on headers, sheet names, etc."""
        relevance = 0.0
        query_lower = query.lower()
        
        # Header context relevance
        if cell.header_context:
            header_words = cell.header_context.lower().split()
            query_words = query_lower.split()
            common_words = set(header_words) & set(query_words)
            if common_words:
                relevance += 0.3 * (len(common_words) / len(query_words))
        
        # Sheet name relevance
        sheet_words = cell.sheet_name.lower().split()
        query_words = query_lower.split()
        common_words = set(sheet_words) & set(query_words)
        if common_words:
            relevance += 0.2 * (len(common_words) / len(query_words))
        
        return min(relevance, 1.0)
    
    def _generate_concept_name(self, cell: SpreadsheetCell) -> str:
        """Generate a meaningful concept name for the cell"""
        if cell.header_context:
            return cell.header_context
        elif cell.business_concepts:
            return cell.business_concepts[0].replace('_', ' ').title()
        else:
            return f"Cell {self._get_excel_cell_reference(cell.row, cell.col)}"
    
    def _generate_business_context(self, cell: SpreadsheetCell) -> str:
        """Generate business context description"""
        contexts = []
        
        if cell.business_concepts:
            primary_concept = cell.business_concepts[0].replace('_', ' ')
            contexts.append(f"This is a {primary_concept}")
        
        if cell.formula:
            contexts.append("calculated using a formula")
        
        contexts.append(f"located in the '{cell.sheet_name}' sheet")
        
        return " ".join(contexts) + "."
    
    def _generate_explanation(self, query: str, cell: SpreadsheetCell) -> str:
        """Generate explanation for why this cell matches the query"""
        explanations = []
        query_lower = query.lower()
        
        # Concept-based matching
        if cell.business_concepts:
            matching_concepts = [concept for concept in cell.business_concepts 
                               if any(word in query_lower for word in concept.lower().split())]
            if matching_concepts:
                explanations.append(f"Contains {', '.join(matching_concepts)}")
        
        # Header matching
        if cell.header_context:
            header_words = set(cell.header_context.lower().split())
            query_words = set(query_lower.split())
            common_words = header_words & query_words
            if common_words:
                explanations.append(f"Header contains: {', '.join(common_words)}")
        
        # Formula matching
        if cell.formula:
            if any(term in query_lower for term in ['formula', 'calculation', 'computed']):
                explanations.append("Contains a formula")
            elif 'average' in query_lower and 'average' in cell.formula.lower():
                explanations.append("Contains average calculation")
            elif any(term in query_lower for term in ['sum', 'total']) and 'sum' in cell.formula.lower():
                explanations.append("Contains sum calculation")
        
        # Sheet context matching
        sheet_words = set(cell.sheet_name.lower().split())
        query_words = set(query_lower.split())
        common_sheet_words = sheet_words & query_words
        if common_sheet_words:
            explanations.append(f"In relevant sheet: {', '.join(common_sheet_words)}")
        
        if not explanations:
            explanations.append("Semantically related to your query")
        
        return "; ".join(explanations)
    
    def _get_excel_cell_reference(self, row: int, col: int) -> str:
        """Convert row/col to Excel-style reference (e.g., A1, B2)"""
        col_letter = ""
        col_num = col + 1  # Convert to 1-based
        while col_num > 0:
            col_num -= 1
            col_letter = chr(col_num % 26 + ord('A')) + col_letter
            col_num //= 26
        return f"{col_letter}{row + 1}"
    
    def has_data(self) -> bool:
        """Check if any spreadsheet data has been loaded"""
        return len(self.cells) > 0