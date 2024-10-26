import openai, os, json, datetime, pytz


def openai_api_calculate_cost(user_prompt_tokens, system_prompt_tokens, completion_tokens, model="gpt-4o-mini", memory_tokens=0):
    pricing = {
        'gpt-3.5-turbo': {
            'prompt': 0.0015,
            'completion': 0.002,
        },
        'gpt-4': {
            'prompt': 0.03, 
            'completion': 0.06,  
        },
        'gpt-4o-mini': {
            'prompt': 0.00015,
            'completion': 0.0006,
        }
    }

    try:
        model_pricing = pricing[model]
    except KeyError:
        model_pricing = {'prompt': 0, 'completion': 0}
        print(f"Warning: Invalid model specified: {model}")

    input_prompt_tokens = user_prompt_tokens + system_prompt_tokens
    input_prompt_cost = input_prompt_tokens * model_pricing['prompt'] / 1000

    system_prompt_cost = system_prompt_tokens * model_pricing['prompt'] / 1000
    user_prompt_cost = user_prompt_tokens * model_pricing['prompt'] / 1000
    memory_cost = memory_tokens * model_pricing['prompt'] / 1000
    output_cost = completion_tokens * model_pricing['completion'] / 1000

    total_tokens = input_prompt_tokens + memory_tokens + completion_tokens
    total_cost_usd = input_prompt_cost + memory_cost + output_cost

    token_consumption_dict = {
        'model': model,
        'input_prompt_tokens': input_prompt_tokens,
        'input_prompt_cost_usd': round(input_prompt_cost, 6),
        'system_prompt_tokens': system_prompt_tokens,
        'system_prompt_cost_usd': round(system_prompt_cost, 6),
        'user_prompt_tokens': user_prompt_tokens,
        'user_prompt_cost_usd': round(user_prompt_cost, 6),
        'memory_tokens': memory_tokens,
        'memory_cost_usd': round(memory_cost, 6),
        'output_tokens': completion_tokens,
        'output_cost_usd': round(output_cost, 6),
        'total_tokens': total_tokens,
        'total_cost_usd': round(total_cost_usd, 6)
    }

    return token_consumption_dict


