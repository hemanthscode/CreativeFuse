import requests
from app.config import OPENROUTER_API_KEY

OPENROUTER_API_URL = "https://openrouter.ai/api/v1/chat/completions"

def boost_idea(idea: str) -> str:
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json"
    }
    
    system_prompt = (
        "You are an expert idea catalyst and innovation consultant with 15+ years of experience across "
        "business, social impact, creative projects, and personal development. Your expertise spans "
        "Indian and global markets, understanding cultural nuances, resource constraints, and practical implementation. "
        "You help transform ANY type of idea - business, creative, social, personal, or technical - into "
        "actionable plans with realistic steps. You balance encouragement with brutal honesty, "
        "always concluding your responses completely without cutting off mid-sentence."
    )
    
    user_prompt = (
        f"Enhance and transform this idea: {idea}\n\n"
        "Please provide a comprehensive analysis that MUST be concluded completely. Structure your response as follows:\n\n"
        "🎯 **IDEA ASSESSMENT**\n"
        "- Core strengths and unique value proposition\n"
        "- Market/audience potential and timing analysis\n"
        "- Realistic viability score (1-10 with reasoning)\n\n"
        "✅ **VALIDATION ROADMAP**\n"
        "- 3 specific ways to test this idea within 2 weeks\n"
        "- Key questions to answer before investing time/money\n"
        "- Success indicators to look for\n\n"
        "🚀 **IMPLEMENTATION BLUEPRINT**\n"
        "- Phase 1: Immediate next steps (Week 1-4)\n"
        "- Phase 2: Building momentum (Month 2-6)\n"
        "- Phase 3: Scaling/expanding (Month 6+)\n"
        "- Budget estimates in INR where applicable\n\n"
        "⚠️ **REALITY CHECK**\n"
        "- Top 3 challenges that will definitely arise\n"
        "- Common failure points and prevention strategies\n"
        "- Honest timeline expectations\n\n"
        "📈 **GROWTH STRATEGY**\n"
        "- How to scale from prototype to impact\n"
        "- Revenue models or sustainability approaches\n"
        "- Strategic partnerships or resources in India\n\n"
        "🎯 **SUCCESS METRICS**\n"
        "- Key performance indicators to track\n"
        "- Milestones for first 6 months\n"
        "- When to pivot vs when to persist\n\n"
        "CRITICAL: End with a compelling 2-line conclusion that motivates action while being realistic. "
        "Ensure your response is COMPLETE and doesn't cut off. Include specific Indian context, "
        "government schemes, local resources, and culturally relevant examples."
    )
    
    payload = {
        "model": "x-ai/grok-4-fast:free",
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        "temperature": 0.75,
        "max_tokens": 2000,  # Significantly increased for complete responses
        "n": 1,
        "stop": None,  # Don't stop early
    }

    try:
        response = requests.post(OPENROUTER_API_URL, json=payload, headers=headers, timeout=30)
        if response.status_code != 200:
            raise RuntimeError(f"OpenRouter request failed: {response.status_code} {response.text}")

        res_json = response.json()
        enhanced_idea = res_json['choices'][0]['message']['content'].strip()
        
        # Ensure response is complete by checking if it ends mid-sentence
        if not enhanced_idea.endswith(('.', '!', '?', ':', '"')):
            enhanced_idea += "\n\n**Ready to Begin?** Take the first validation step this week and remember - every successful idea started as just a thought. The difference is taking action."
        
        return enhanced_idea
        
    except requests.exceptions.Timeout:
        raise RuntimeError("AI service timeout - please try again")
    except requests.exceptions.RequestException as e:
        raise RuntimeError(f"Network error: {str(e)}")
    except KeyError:
        raise RuntimeError("Invalid response format from AI service")
    except Exception as e:
        raise RuntimeError(f"AI service error: {str(e)}")

def categorize_idea_type(idea: str) -> str:
    """
    Determine the type of idea to provide more targeted advice
    """
    idea_lower = idea.lower()
    
    if any(word in idea_lower for word in ['business', 'startup', 'company', 'revenue', 'profit', 'customers', 'market']):
        return 'business'
    elif any(word in idea_lower for word in ['ngo', 'social', 'community', 'help', 'volunteer', 'charity', 'society']):
        return 'social_impact'
    elif any(word in idea_lower for word in ['app', 'software', 'website', 'platform', 'ai', 'tech', 'digital']):
        return 'technology'
    elif any(word in idea_lower for word in ['art', 'music', 'design', 'creative', 'content', 'video', 'blog']):
        return 'creative'
    elif any(word in idea_lower for word in ['learn', 'skill', 'course', 'education', 'training', 'personal']):
        return 'personal_development'
    else:
        return 'general'