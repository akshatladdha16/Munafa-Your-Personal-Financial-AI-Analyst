import streamlit as st
from phi.agent import Agent, RunResponse
from phi.model.groq import Groq
from phi.tools.duckduckgo import DuckDuckGo
from phi.tools.yfinance import YFinanceTools
from dotenv import load_dotenv
load_dotenv()

# GROQ_API_KEY = os.getenv("GROQ_API_KEY")

def initialize_session_state():
    if "messages" not in st.session_state:
        st.session_state.messages = []

GROQ_API_KEY = st.secrets["GROQ_API_KEY"]
def get_agents():
    web_agent = Agent(
        name="WebSearchAgent",
        role="Search web for the information",
        model=Groq(id="llama-3.3-70b-versatile"),
        tools=[DuckDuckGo()], # used for search engine
        description="You are a web search agent that only helps in financial queries. You can search the web for the latest financial news and information.",
        instructions=["Always include source/article links."],
        show_tool_calls=False,  # Set to False to hide logs
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
        description="""
        Act as a financial analysis assistant. Provide a detailed financial overview of the given stock in a structured format with the following sections:

        Key Financial Ratios (present in a table format)

        Price-to-Earnings (P/E) Ratio
        Price-to-Book (P/B) Ratio
        Sector P/E Ratio
        Return on Equity (ROE)
        Return on Capital Employed (ROCE)
        Debt-to-Equity Ratio
        Earnings Per Share (EPS)
        Free Cash Flow (FCF)
        Latest News & Updates (List the most recent and relevant news about the stock, with direct links to sources.)

        Analyst Recommendations (Summarize expert opinions with a rating such as Buy, Hold, or Sell. Provide a table with analysts' names, recommendations, and direct source links.)

        Ensure that all information is well-formatted, using tables where necessary for easy readability. If any data is unavailable, mention it explicitly instead of providing estimates or assumptions. Keep responses clear, concise, and data-driven.
        """,
        # description="You are an investment analyst that researches stock prices, analyst recommendations, and stock fundamentals.",
        instructions=["Always include source/article links and use tables to display the numerical data and analyst recommendations."],
        show_tool_calls=False,  # Set to False to hide logs
        markdown=True,
    )
    return web_agent, finance_agent

def process_user_query(user_input):
    # Process user input and return response
    web_agent, finance_agent = get_agents()
    
    multimodal_agent = Agent(
        # need to give model here as by default any agent takes up Open AI key as it's model
        model=Groq(id="llama-3.3-70b-versatile"),
        team=[web_agent, finance_agent],    
        instructions=["Use the web agent to search internet sources and the finance agent to find financial data and analyst buy/sell/hold recommendations with valid reasons."],
        show_tool_calls=False,  # Set to False to hide logs
        # debug_mode=True,
        markdown=True,
    )
    try:
        # Replace print_response with run to capture the response
        response = multimodal_agent.run(user_input)
        if isinstance(response, RunResponse):
            return response.content
        return str(response)
    except Exception as e:
        return "I am sorry, I am still learning. I will get back to you soon with the answer.: " + str(e)

def main():
    st.title("Munafa: Your Personal AI Financial Assistant")
    st.markdown("Welcome to Munafa, your personal AI financial assistant. Ask me anything related to finance, stocks, buy/sell/hold recommendations, and the latest news. I will try to help you out to my level best.")
    
    # Initialize session state
    initialize_session_state()
    
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
            # Get assistant response from function
            assistant_response = process_user_query(user_input)
            
        st.session_state.messages.append({"role": "assistant", "content": assistant_response})
        with st.chat_message("assistant"):
            st.markdown(assistant_response)

if __name__ == "__main__":
    main()