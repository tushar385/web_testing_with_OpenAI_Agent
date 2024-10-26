import sys
import os
# Open AI imports
import openai
from langchain.agents import initialize_agent, AgentType
from langchain.chat_models import ChatOpenAI
from langchain.chains.conversation.memory import ConversationBufferWindowMemory
from config.models.cost import openai_api_calculate_cost
# code functions imports
from config.logs.logger import *
from config.tools.browser_control_methods import *
from config.tools.website_url import redirect_to_website
from config.tools.page_scrap import *
from config.tools.interacting_element import *
##ai
##ai2

initialize_logs()

def get_completion(prompt):
    model = "gpt-4o-mini" 
    
    tools = [start_chrome_driver, redirect_to_website, sleep_driver, stop_chrome_driver, fetch_html, input_element, click_element, is_page_loaded]

    memory = ConversationBufferWindowMemory(k=5, return_messages=True)

    system_prompt = """
    You are an AI assistant designed to help with web automation tasks using Selenium WebDriver.
    You will be given a task to run using the tools provided to you.

    Follow these steps for every task:
    1. Start with starting the chrome driver.
    2. After navigating to url first time & EVERY other navigation action, ALWAYS use the fetch_html tool to get the current page HTML.
    3. Analyze the fetched HTML to determine your next action.
    4. Always close the chrome driver before you finish the task.

    When using tools, always format your response as a JSON object with 'action' and 'action_input' keys.

    Note: 
    1) If user gives wrong url or website name or ip address, return an error message to the user and stop the execution.
    2) If any error occurs, close the driver.
    3) If you fail to execute any step of the prompt, tell the user which task gave an issue in the output.
    4) ALWAYS fetch and analyze the HTML after EACH action to keep track of the current page state.
    """
    try:
        log_message(f"Received prompt")
        
        turbo_llm = ChatOpenAI(model_name=model, temperature=0.2)

        agent = initialize_agent(
            tools=tools,
            llm=turbo_llm,
            agent=AgentType.STRUCTURED_CHAT_ZERO_SHOT_REACT_DESCRIPTION,
            verbose=True,
            max_iterations=20,
            early_stopping_method="generate",
            memory=memory,
            # handle_parsing_errors="Retry once if failed"
        )

        response = agent.run(input=f"{system_prompt}\n\nTask: {prompt}")

        ai_response = response.strip() if isinstance(response, str) else str(response)

        user_prompt_tokens = len(prompt) // 4
        system_prompt_tokens = len(system_prompt) // 4
        completion_tokens = len(ai_response) // 4
        memory_tokens = sum(len(msg.content) // 4 for msg in memory.chat_memory.messages)

        cost_info = openai_api_calculate_cost(
            user_prompt_tokens=user_prompt_tokens,
            system_prompt_tokens=system_prompt_tokens,
            completion_tokens=completion_tokens,
            model=model,
            memory_tokens=memory_tokens
        )
        
        return ai_response, cost_info
    
    except Exception as e:
        error_message = f"Error: Failed to execute task. Details: {str(e)}"
        log_message(error_message)
        stop_chrome_driver("")
        return error_message, None





