import json
from openai import OpenAI
from typing import List, Dict

class BaristaAgent:
    def __init__(self, api_key: str, menu: List[Dict]):
        self.client = OpenAI(
            api_key=api_key,
            base_url="https://openrouter.ai/api/v1"
        )
        self.menu = menu
        self.system_prompt = f"""You are an experienced barista at ☕ Coffee Shop. You're knowledgeable, friendly, and passionate about the drinks you serve.

YOUR MENU (8 items - you know these inside and out):
{self._format_menu_detailed()}

YOUR EXPERTISE:
- You know the ingredients, taste profiles, and preparation for each item
- You can explain what makes each drink special (flavor notes, texture, serving style)
- You understand dietary needs (dairy-free, vegan, allergen concerns)
- You're warm, welcoming, and love helping customers find their perfect drink

YOUR BOUNDARIES:
- You can ONLY recommend items from the 8-item menu above
- If asked about items not on the menu, acknowledge kindly: "We don't carry that, but let me suggest something similar from what we have!"
- Keep descriptions accurate to the actual menu items

CART ACTIONS:
When a customer wants to add an item to their cart (e.g., "add that to my cart", "I'll take one", "give me the cold brew"), respond with:
[CART_ADD:<item_id>] <friendly confirmation message>

Examples:
- User: "Tell me about the cold brew"
  You: "Our Cold Brew Coffee is smooth and bold - we slow-steep it for 12+ hours to bring out rich, low-acid flavors. It's served ice-cold and completely dairy-free. Would you like to try it?"
  
- User: "Add that to my cart"
  You: "[CART_ADD:3] Perfect! I've added Cold Brew Coffee ($4.00) to your cart. Anything else I can get you?"

- User: "I want the oat milk honey latte"
  You: "[CART_ADD:2] Great choice! Our Oat Milk Honey Latte ($5.00) is in your cart - it's creamy, naturally sweet, and dairy-free. What else sounds good?"

CONVERSATION CONTEXT:
- Track recently mentioned items in conversation
- "That", "it", "one of those" refers to the last item discussed
- If ambiguous, ask: "Just to confirm - did you mean the Cold Brew or the Nitro Cold Brew?"

CHECKOUT ACTIONS:
When a customer wants to complete their order (e.g., "proceed with checkout", "I'm ready to order", "checkout please"), respond with:
[CHECKOUT] <friendly confirmation message>

Example:
- User: "Proceed with checkout"
  You: "[CHECKOUT] Perfect! Your order is confirmed. Thank you for choosing ☕ Coffee Shop!"

Only use [CHECKOUT] if the cart has items. If cart is empty, say: "Your cart is empty! Would you like me to recommend something?"

Be natural, knowledgeable, and helpful. You're a real barista who happens to work through chat.
"""
    
    def _format_menu_detailed(self) -> str:
        lines = []
        
        ingredient_notes = {
            1: "Single shot of dark-roasted espresso - bold, intense, pure coffee flavor",
            2: "Espresso + steamed oat milk + honey drizzle - creamy, naturally sweet, plant-based",
            3: "Slow-steeped coffee served over ice - smooth, low-acid, refreshing",
            4: "Espresso + steamed milk + pumpkin spice + whipped cream - seasonal, warming, indulgent",
            5: "Traditional French pastry with butter layers - flaky, rich, buttery",
            6: "Plant-based muffin with fresh blueberries - soft, sweet, vegan-friendly",
            7: "Cold brew infused with nitrogen gas - ultra-smooth, creamy head, no dairy needed",
            8: "Vanilla syrup + milk over ice + espresso shots + caramel drizzle - sweet, cold, layered"
        }
        
        for item in self.menu:
            allergen_note = f" • Allergens: {', '.join(item['allergens'])}" if item['allergens'] else " • No major allergens"
            tags_note = f" • Tags: {', '.join(item['tags'])}"
            
            lines.append(f"\n{item['id']}. {item['name']} - ${item['price']:.2f}")
            lines.append(f"   Description: {item['description']}")
            lines.append(f"   Ingredients: {ingredient_notes.get(item['id'], 'See description')}")
            lines.append(f"   {allergen_note}{tags_note}")
        
        return "\n".join(lines)

    def get_response(self, user_message: str, conversation_history: List[Dict]) -> str:
        messages = [{"role": "system", "content": self.system_prompt}]
        messages.extend(conversation_history[-10:])
        messages.append({"role": "user", "content": user_message})
        
        try:
            response = self.client.chat.completions.create(
                model="nvidia/nemotron-3.5-lightning:free",
                messages=messages,
                temperature=0.5,
                max_tokens=500
            )
            raw_response = response.choices[0].message.content
            
            validated_response = self._validate_response(raw_response)
            return validated_response
            
        except Exception as e:
            return f"I apologize, I'm having trouble connecting right now. Please try again. (Error: {str(e)})"
    
    def _validate_response(self, response: str) -> str:
        response_lower = response.lower()
        valid_item_names = {item['name'].lower() for item in self.menu}
        
        hallucination_terms = [
            'cappuccino', 'americano', 'mocha', 'frappuccino', 
            'flat white', 'cortado', 'affogato',
            'bagel', 'sandwich', 'cookie', 'brownie'
        ]
        
        for term in hallucination_terms:
            if term in response_lower:
                is_valid = any(term in valid_name for valid_name in valid_item_names)
                if not is_valid:
                    return (
                        f"I'd love to help, but we don't carry {term} right now. "
                        f"Let me show you what we do have - I think you'll find something you'll love! "
                        f"We've got {', '.join([item['name'] for item in self.menu[:3]])} and more. What sounds good?"
                    )
        
        return response


