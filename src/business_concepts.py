import re
from typing import List, Dict, Any
from dataclasses import dataclass

@dataclass
class BusinessConcept:
    name: str
    synonyms: List[str]
    keywords: List[str]
    description: str
    category: str

class BusinessConceptMapper:
    """Maps spreadsheet content to business concepts"""
    
    def __init__(self):
        self.concepts = self._initialize_business_concepts()
        self.concept_patterns = self._compile_patterns()
    
    def _initialize_business_concepts(self) -> Dict[str, List[BusinessConcept]]:
        """Initialize comprehensive business concept dictionary"""
        concepts = {
            "profitability": [
                BusinessConcept(
                    name="gross profit margin",
                    synonyms=["gross margin", "gross profit %", "gross profitability"],
                    keywords=["gross", "profit", "margin", "revenue", "cogs"],
                    description="Measures profitability after cost of goods sold",
                    category="profitability"
                ),
                BusinessConcept(
                    name="net profit margin", 
                    synonyms=["net margin", "profit margin", "net profitability"],
                    keywords=["net", "profit", "margin", "bottom line"],
                    description="Overall profitability after all expenses",
                    category="profitability"
                ),
                BusinessConcept(
                    name="operating margin",
                    synonyms=["operating profit margin", "EBIT margin"],
                    keywords=["operating", "margin", "ebit"],
                    description="Profitability from core operations",
                    category="profitability"
                ),
                BusinessConcept(
                    name="EBITDA",
                    synonyms=["earnings before interest tax depreciation amortization"],
                    keywords=["ebitda", "earnings", "cash flow proxy"],
                    description="Operating performance measure",
                    category="profitability"
                ),
                BusinessConcept(
                    name="return on investment",
                    synonyms=["ROI", "return on assets", "ROA"],
                    keywords=["roi", "return", "investment", "efficiency"],
                    description="Efficiency of investment returns",
                    category="profitability"
                )
            ],
            
            "revenue": [
                BusinessConcept(
                    name="total revenue",
                    synonyms=["sales", "income", "turnover", "gross sales"],
                    keywords=["revenue", "sales", "income", "total"],
                    description="Total income from business operations",
                    category="revenue"
                ),
                BusinessConcept(
                    name="revenue growth",
                    synonyms=["sales growth", "income growth", "top line growth"],
                    keywords=["growth", "increase", "yoy", "qoq"],
                    description="Rate of revenue increase over time",
                    category="revenue"
                ),
                BusinessConcept(
                    name="recurring revenue",
                    synonyms=["subscription revenue", "monthly recurring revenue", "MRR"],
                    keywords=["recurring", "subscription", "monthly", "mrr"],
                    description="Predictable revenue streams",
                    category="revenue"
                )
            ],
            
            "costs": [
                BusinessConcept(
                    name="cost of goods sold",
                    synonyms=["COGS", "direct costs", "variable costs"],
                    keywords=["cogs", "cost", "goods", "sold", "direct"],
                    description="Direct costs of producing goods/services",
                    category="costs"
                ),
                BusinessConcept(
                    name="operating expenses",
                    synonyms=["OPEX", "operational costs", "overhead"],
                    keywords=["operating", "expenses", "opex", "overhead"],
                    description="Costs of running business operations",
                    category="costs"
                ),
                BusinessConcept(
                    name="marketing spend",
                    synonyms=["marketing costs", "advertising expenses", "marketing investment"],
                    keywords=["marketing", "advertising", "promotion", "spend"],
                    description="Investment in marketing and advertising",
                    category="costs"
                ),
                BusinessConcept(
                    name="total expenses",
                    synonyms=["total costs", "all expenses", "combined costs"],
                    keywords=["total", "expenses", "costs", "all"],
                    description="Sum of all business expenses",
                    category="costs"
                )
            ],
            
            "efficiency": [
                BusinessConcept(
                    name="asset turnover",
                    synonyms=["asset efficiency", "asset utilization"],
                    keywords=["asset", "turnover", "efficiency", "utilization"],
                    description="How efficiently assets generate revenue",
                    category="efficiency"
                ),
                BusinessConcept(
                    name="inventory turnover",
                    synonyms=["inventory efficiency", "stock turnover"],
                    keywords=["inventory", "turnover", "stock", "efficiency"],
                    description="How quickly inventory is sold",
                    category="efficiency"
                ),
                BusinessConcept(
                    name="working capital ratio",
                    synonyms=["current ratio", "liquidity ratio"],
                    keywords=["working", "capital", "ratio", "liquidity"],
                    description="Short-term financial health measure",
                    category="efficiency"
                ),
                BusinessConcept(
                    name="productivity ratio",
                    synonyms=["productivity measure", "efficiency ratio"],
                    keywords=["productivity", "efficiency", "output", "input"],
                    description="Output relative to input measure",
                    category="efficiency"
                )
            ],
            
            "growth": [
                BusinessConcept(
                    name="year over year growth",
                    synonyms=["YoY growth", "annual growth", "yearly growth"],
                    keywords=["yoy", "year", "annual", "growth"],
                    description="Growth compared to same period previous year",
                    category="growth"
                ),
                BusinessConcept(
                    name="quarter over quarter growth",
                    synonyms=["QoQ growth", "quarterly growth"],
                    keywords=["qoq", "quarter", "quarterly", "growth"],
                    description="Growth compared to previous quarter",
                    category="growth"
                ),
                BusinessConcept(
                    name="compound annual growth rate",
                    synonyms=["CAGR", "compound growth"],
                    keywords=["cagr", "compound", "annual", "growth"],
                    description="Average annual growth rate over multiple years",
                    category="growth"
                ),
                BusinessConcept(
                    name="month over month growth",
                    synonyms=["MoM growth", "monthly growth"],
                    keywords=["mom", "month", "monthly", "growth"],
                    description="Growth compared to previous month",
                    category="growth"
                )
            ],
            
            "financial_analysis": [
                BusinessConcept(
                    name="budget vs actual",
                    synonyms=["budget variance", "actual vs budget", "variance analysis"],
                    keywords=["budget", "actual", "variance", "vs", "against"],
                    description="Comparison of planned vs actual performance",
                    category="financial_analysis"
                ),
                BusinessConcept(
                    name="forecast analysis",
                    synonyms=["projection", "prediction", "forecast"],
                    keywords=["forecast", "projection", "prediction", "future"],
                    description="Future performance predictions",
                    category="financial_analysis"
                ),
                BusinessConcept(
                    name="trend analysis",
                    synonyms=["time series", "historical analysis"],
                    keywords=["trend", "time", "series", "historical"],
                    description="Analysis of patterns over time",
                    category="financial_analysis"
                )
            ],
            
            "formulas": [
                BusinessConcept(
                    name="percentage calculation",
                    synonyms=["percent formula", "ratio as percentage"],
                    keywords=["percentage", "percent", "%", "ratio"],
                    description="Calculations expressed as percentages",
                    category="formulas"
                ),
                BusinessConcept(
                    name="average calculation",
                    synonyms=["mean", "avg", "average formula"],
                    keywords=["average", "mean", "avg"],
                    description="Average or mean calculations",
                    category="formulas"
                ),
                BusinessConcept(
                    name="sum calculation",
                    synonyms=["total", "sum formula", "addition"],
                    keywords=["sum", "total", "add", "addition"],
                    description="Sum or total calculations",
                    category="formulas"
                ),
                BusinessConcept(
                    name="conditional calculation",
                    synonyms=["if formula", "conditional logic"],
                    keywords=["if", "conditional", "logic", "condition"],
                    description="Calculations with conditional logic",
                    category="formulas"
                ),
                BusinessConcept(
                    name="lookup formula",
                    synonyms=["vlookup", "index match", "lookup"],
                    keywords=["vlookup", "lookup", "index", "match"],
                    description="Data lookup and retrieval formulas",
                    category="formulas"
                )
            ]
        }
        
        return concepts
    
    def _compile_patterns(self) -> Dict[str, List[re.Pattern]]:
        """Compile regex patterns for concept recognition"""
        patterns = {}
        
        for category, concept_list in self.concepts.items():
            patterns[category] = []
            for concept in concept_list:
                # Create patterns from keywords and synonyms
                all_terms = concept.keywords + concept.synonyms + [concept.name]
                for term in all_terms:
                    # Create flexible pattern that matches variations
                    pattern_str = r'\b' + re.escape(term.lower()).replace(r'\ ', r'\s+') + r'\b'
                    patterns[category].append(re.compile(pattern_str, re.IGNORECASE))
        
        return patterns
    
    def identify_concepts(self, text: str) -> List[str]:
        """Identify business concepts in given text"""
        identified = []
        text_lower = text.lower()
        
        # Direct keyword matching
        for category, concept_list in self.concepts.items():
            for concept in concept_list:
                # Check if concept keywords/synonyms appear in text
                if self._matches_concept(text_lower, concept):
                    identified.append(concept.name)
        
        # Pattern-based identification
        identified.extend(self._identify_patterns(text_lower))
        
        # Formula-specific identification
        identified.extend(self._identify_formula_concepts(text))
        
        return list(set(identified))  # Remove duplicates
    
    def _matches_concept(self, text: str, concept: BusinessConcept) -> bool:
        """Check if text matches a business concept"""
        all_terms = [concept.name] + concept.synonyms + concept.keywords
        
        for term in all_terms:
            term_words = term.lower().split()
            if all(word in text for word in term_words):
                return True
        
        return False
    
    def _identify_patterns(self, text: str) -> List[str]:
        """Identify concepts using regex patterns"""
        identified = []
        
        # Financial ratio patterns
        if re.search(r'\b\w+\s*/\s*\w+\b', text) or '/' in text:
            identified.append('ratio calculation')
        
        # Percentage patterns
        if re.search(r'%|\bpercent\b|\bratio\b|\brate\b', text):
            identified.append('percentage calculation')
        
        # Growth patterns
        if re.search(r'\b(yoy|qoq|mom)\b|\bgrowth\b|\bincrease\b', text):
            identified.append('growth metric')
        
        # Margin patterns
        if re.search(r'\bmargin\b|\bprofit\s+margin\b', text):
            identified.append('profitability metric')
        
        return identified
    
    def _identify_formula_concepts(self, text: str) -> List[str]:
        """Identify concepts specific to formulas"""
        identified = []
        text_lower = text.lower()
        
        if not text.startswith('='):
            return identified
        
        # Sum formulas
        if 'sum(' in text_lower:
            identified.append('sum calculation')
            identified.append('aggregation formula')
        
        # Average formulas
        if any(func in text_lower for func in ['average(', 'avg(']):
            identified.append('average calculation')
        
        # Conditional formulas
        if any(func in text_lower for func in ['if(', 'sumif(', 'countif(', 'averageif(']):
            identified.append('conditional calculation')
        
        # Lookup formulas
        if any(func in text_lower for func in ['vlookup(', 'hlookup(', 'index(', 'match(', 'xlookup(']):
            identified.append('lookup formula')
        
        # Mathematical operations
        if '/' in text and not any(func in text_lower for func in ['sum(', 'average(']):
            identified.append('ratio calculation')
            identified.append('percentage calculation')
        
        return identified
    
    def get_concept_category(self, concept_name: str) -> str:
        """Get the category of a concept"""
        for category, concept_list in self.concepts.items():
            for concept in concept_list:
                if concept.name == concept_name:
                    return category
        return "unknown"
    
    def get_all_concepts(self) -> Dict[str, List[Dict[str, Any]]]:
        """Get all concepts in a dictionary format"""
        result = {}
        for category, concept_list in self.concepts.items():
            result[category] = []
            for concept in concept_list:
                result[category].append({
                    'name': concept.name,
                    'synonyms': concept.synonyms,
                    'keywords': concept.keywords,
                    'description': concept.description
                })
        return result
    
    def get_related_concepts(self, concept_name: str) -> List[str]:
        """Get concepts related to the given concept"""
        related = []
        target_concept = None
        
        # Find the target concept
        for category, concept_list in self.concepts.items():
            for concept in concept_list:
                if concept.name == concept_name:
                    target_concept = concept
                    # Add other concepts in the same category
                    related.extend([c.name for c in concept_list if c.name != concept_name])
                    break
        
        return related