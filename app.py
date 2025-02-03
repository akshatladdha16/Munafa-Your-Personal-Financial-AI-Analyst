# import streamlit as st
# from phi.agent import Agent ,RunResponse
# from phi.model.groq import Groq
# from phi.tools.duckduckgo import DuckDuckGo
# from phi.tools.yfinance import YFinanceTools
# import openai
# import os
# from dotenv import load_dotenv
# load_dotenv()
# openai.api_key = os.getenv("OPENAI_API_KEY")

# def initialize_session_state():
#     if "messages" not in st.session_state:
#         st.session_state.messages = []

# def get_agents():
#         web_agent = Agent(
#             name="WebSearchAgent",
#             role="Search web for the information",
#             model=Groq(id="llama-3.3-70b-versatile"),
#             tools=[DuckDuckGo()], #used for search engine
#             instructions=["Always include sources"],
#             show_tool_calls=True,
#             markdown=True,
#         )
#         finance_agent = Agent(
#             name="FinanceAgent",
#             model=Groq(id="llama-3.3-70b-versatile"),
#             tools=[YFinanceTools(
#                 stock_price=True,
#                 analyst_recommendations=True,
#                 stock_fundamentals=True,
#             )],
#             # description="You are an investment analyst that researches stock prices, analyst recommendations, and stock fundamentals.",
#             instructions=["Use tables to display the data"],
#             show_tool_calls=True,
#             markdown=True,
#         )
                    
#         return web_agent, finance_agent
# def process_user_query(user_input):
#     # Process user input and return response
#     web_agent, finance_agent = get_agents()
    
#     multimodal_agent = Agent(
#         team=[web_agent, finance_agent],    
#         instructions=["Use the web search agent to find information about the company and the finance agent to find financial data and analyst buy/sell/hold recommendations with valid reasons."],
#         show_tool_calls=True,
#         markdown=True,
#     )
#     try:
#         # Replace print_response with run to capture the response
#         response = multimodal_agent.run(user_input)
#         if isinstance(response, RunResponse):
#             return response.content
#         return str(response)
#     except Exception as e:
#         return "I am sorry, I am still learning. I will get back to you soon with the answer.: " + str(e)

# def main():
#     st.title("Munafa: Your Personal Financial Assistant")
    
#     # Initialize session state
#     initialize_session_state()
    
#     # Display chat messages
#     for message in st.session_state.messages:
#         with st.chat_message(message["role"]):
#             st.markdown(message["content"])
    
#     # Chat input
#     user_input = st.chat_input("Share your financial query. For .e.g. 'What is the current price of AAPL?'")
    
#     if user_input:
#         # Add user message to chat
#         st.session_state.messages.append({"role": "user", "content": user_input})
#         with st.chat_message("user"):
#             st.write(user_input)
            
#         # Show loading spinner while getting response
#         with st.spinner('Processing your request...'):
#             # Get assistant response from function
#             assistant_response = process_user_query(user_input)
            
#         st.session_state.messages.append({"role": "assistant", "content": assistant_response})
#         with st.chat_message("assistant"):
#             st.markdown(assistant_response)

# if __name__ == "__main__":
#     main()
import streamlit as st
from phi.agent import Agent, RunResponse
from phi.model.groq import Groq
from phi.tools.duckduckgo import DuckDuckGo
from phi.tools.yfinance import YFinanceTools
import openai
import os

def initialize_session_state():
    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "openai_api_key" not in st.session_state:
        st.session_state.openai_api_key = None
    if "page" not in st.session_state:
        st.session_state.page = "api_key"

def api_key_page():
    st.title("Welcome to Munafa: Your Personal Financial Assistant")
    api_key = st.text_input("Please enter your OpenAI API Key:", type="password")
    if st.button("Submit"):
        if api_key:
            st.session_state.openai_api_key = api_key
            st.session_state.page = "chat"
            st.rerun()  # Changed from experimental_rerun to rerun
        else:
            st.warning("Please enter a valid API key.")

def get_agents():
    web_agent = Agent(
        name="WebSearchAgent",
        role="Search web for the information",
        model=Groq(id="llama-3.3-70b-versatile"),
        tools=[DuckDuckGo()],
        instructions=["Always include sources"],
        show_tool_calls=True,
        markdown=True,
    )
    finance_agent = Agent(
        name="FinanceAgent",
        model=Groq(id="llama-3.3-70b-versatile"),
        tools=[YFinanceTools(
            stock_price=True,
            analyst_recommendations=True,
            stock_fundamentals=True,
        )],
        instructions=["Use tables to display the data"],
        show_tool_calls=True,
        markdown=True,
    )
    
    return web_agent, finance_agent

def process_user_query(user_input):
    web_agent, finance_agent = get_agents()
    
    multimodal_agent = Agent(
        team=[web_agent, finance_agent],    
        instructions=["Use the web search agent to find information about the company and the finance agent to find financial data and analyst buy/sell/hold recommendations with valid reasons."],
        show_tool_calls=True,
        markdown=True,
    )
    
    try:
        response = multimodal_agent.run(user_input)
        if isinstance(response, RunResponse):
            return response.content
        return str(response)
    except Exception as e:
        return "I am sorry, I am still learning. I will get back to you soon with the answer.: " + str(e)

def chat_page():
    st.title("Munafa: Your Personal Financial Assistant")
    
    # Set OpenAI API key
    openai.api_key = st.session_state.openai_api_key
    
    # Display chat messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    
    # Chat input
    user_input = st.chat_input("Share your financial query. For example, 'What is the current price of AAPL?'")
    
    if user_input:
        # Add user message to chat
        st.session_state.messages.append({"role": "user", "content": user_input})
        with st.chat_message("user"):
            st.write(user_input)
            
        # Show loading spinner while getting response
        with st.spinner('Processing your request...'):
            assistant_response = process_user_query(user_input)
            
        st.session_state.messages.append({"role": "assistant", "content": assistant_response})
        with st.chat_message("assistant"):
            st.markdown(assistant_response)

def main():
    initialize_session_state()
    
    if st.session_state.page == "api_key":
        api_key_page()
    else:
        chat_page()

if __name__ == "__main__":
    main()
