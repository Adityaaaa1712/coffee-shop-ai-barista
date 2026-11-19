import json
from pathlib import Path
from typing import List, Dict, Optional

def load_menu() -> List[Dict]:
    menu_path = Path(__file__).parent / "data" / "menu.json"
    with open(menu_path, "r", encoding="utf-8") as f:
        return json.load(f)

def search_menu(query: str, menu: List[Dict]) -> List[Dict]:
    if not query:
        return menu
    
    query_lower = query.lower()
    results = []
    
    for item in menu:
        score = 0
        name_lower = item["name"].lower()
        desc_lower = item["description"].lower()
        tags_lower = [tag.lower() for tag in item.get("tags", [])]
        category_lower = item.get("category", "").lower()
        
        if query_lower == name_lower:
            score += 100
        elif query_lower in name_lower:
            score += 50
        
        if query_lower in desc_lower:
            score += 30
        
        if query_lower in tags_lower:
            score += 40
        elif any(query_lower in tag for tag in tags_lower):
            score += 20
        
        if query_lower == category_lower:
            score += 35
        elif query_lower in category_lower:
            score += 15
        
        if score > 0:
            results.append((score, item))
    
    results.sort(key=lambda x: x[0], reverse=True)
    return [item for score, item in results]

def filter_by_preferences(
    menu: List[Dict],
    hot_cold: Optional[str] = None,
    sweet_strong: Optional[str] = None,
    dietary: Optional[List[str]] = None
) -> List[Dict]:
    filtered = menu
    
    if hot_cold:
        hot_cold_lower = hot_cold.lower()
        filtered = [item for item in filtered if hot_cold_lower in [tag.lower() for tag in item.get("tags", [])]]
    
    if sweet_strong:
        sweet_strong_lower = sweet_strong.lower()
        filtered = [item for item in filtered if sweet_strong_lower in [tag.lower() for tag in item.get("tags", [])]]
    
    if dietary:
        dietary_lower = [d.lower() for d in dietary]
        filtered = [
            item for item in filtered
            if any(d in [tag.lower() for tag in item.get("tags", [])] for d in dietary_lower)
            and not any(d in [a.lower() for a in item.get("allergens", [])] for d in dietary_lower)
        ]
    
    return filtered

def get_recommendations(preferences: Dict, menu: List[Dict], limit: int = 3) -> List[Dict]:
    query = preferences.get("query", "")
    hot_cold = preferences.get("hot_cold")
    sweet_strong = preferences.get("sweet_strong")
    dietary = preferences.get("dietary")
    
    if query:
        results = search_menu(query, menu)
    else:
        results = menu
    
    results = filter_by_preferences(results, hot_cold, sweet_strong, dietary)
    
    return results[:limit]
