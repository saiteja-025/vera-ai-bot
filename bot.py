def get_greeting(category_slug: str, merchant_name: str) -> str:
    """Returns a tailored greeting based on category tone."""
    if category_slug == "dentists":
        return f"Dear {merchant_name},"
    elif category_slug == "retail":
        return f"Hey {merchant_name}!"
    else:
        return f"Hi {merchant_name},"

def compose(category: dict, merchant: dict, trigger: dict, customer: dict | None = None) -> dict:
    """
    Core logic to compose a personalized, engaging message based on business rules.
    """
    merchant_name = merchant.get("identity", {}).get("name", "Merchant")
    category_slug = category.get("slug", "")
    trigger_kind = trigger.get("kind")
    
    # Advanced logic: if customer exists -> send_as = "merchant_on_behalf"
    send_as = "merchant_on_behalf" if customer else "vera"
    
    body = ""
    cta = ""
    suppression_key = f"suppress_{trigger.get('id', 'default_trigger')}"
    rationale = f"Action triggered by {trigger_kind}"

    greeting = get_greeting(category_slug, merchant_name)

    if trigger_kind == "perf_dip":
        ctr = merchant.get("performance", {}).get("ctr", 0.0)
        avg_ctr = category.get("peer_stats", {}).get("avg_ctr", 0.0)
        body = f"{greeting} your visibility has dropped recently. Your click-through rate is {ctr*100:.1f}%, while peers average {avg_ctr*100:.1f}%. You're missing out on potential customers! Let's apply a quick fix to boost your profile."
        cta = "Apply Quick Fix"
        rationale = "Performance drop detected; highlighting lost potential against peer average."
        
    elif trigger_kind == "research_digest":
        top_item = trigger.get("payload", {}).get("top_item", "new industry trends")
        body = f"{greeting} here's a useful insight: engaging with '{top_item}' can significantly improve your customer reach. Stay ahead of the curve!"
        cta = "View Full Insight"
        rationale = f"Sharing research digest on {top_item}."
        
    elif trigger_kind == "festival_upcoming":
        offers = category.get("offer_catalog", [])
        offer_text = offers[0] if offers else "a festive discount"
        body = f"{greeting} the festive season is almost here! Capture the holiday crowd by running our recommended '{offer_text}' campaign."
        cta = "Launch Offer Now"
        rationale = "Festival preparation using top catalog offer."
        
    elif trigger_kind == "recall_due" and customer:
        customer_name = customer.get("identity", {}).get("name", "Valued Customer")
        body = f"Hi {customer_name}, we've missed seeing you at {merchant_name}! It's been a while since your last visit. We'd love to welcome you back soon."
        cta = "Book an Appointment"
        rationale = "Customer recall due; sending friendly reminder."
        
    else:
        body = f"{greeting} we have some exciting new updates to share with you!"
        cta = "Check Updates"
        rationale = "General communication."

    return {
        "body": body,
        "cta": cta,
        "send_as": send_as,
        "suppression_key": suppression_key,
        "rationale": rationale
    }

def handle_reply(reply_text: str, state: dict) -> dict:
    """
    Multi-turn handling for merchant replies.
    """
    reply_lower = reply_text.strip().lower()
    history = state.get("history", [])
    
    # Detect auto-replies: if the same message repeats consecutively
    if history and history[-1] == reply_lower:
        return {
            "response": "Auto-reply pattern detected. Ending conversation gracefully.",
            "state": state
        }
        
    history.append(reply_lower)
    state["history"] = history
    
    # Intent matching based on new rules
    if reply_lower in ["yes", "ok", "go ahead"]:
        return {
            "response": "Great! We will proceed with the action right away.",
            "state": state
        }
    elif reply_lower in ["no", "not interested"]:
        return {
            "response": "Understood, we won't bother you with this. Let us know if you need anything else.",
            "state": state
        }
    else:
        return {
            "response": "I didn't quite catch that. Please reply with 'yes' to proceed or 'no' to cancel.",
            "state": state
        }
