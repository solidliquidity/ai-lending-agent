from langchain_openai import ChatOpenAI
from browser_use import Agent, Controller
import asyncio, time
from dotenv import load_dotenv
load_dotenv()

timestamp = int(time.time())

interactive_brokers_scanner_prompt = """
Go to http://localhost:5056/ - visit the scanner in the nav bar.
In the Sort By dropdown of the scanner page, select the Most Active option. Then click the Scan button and wait for the new scan to run. You should do this each time you visit the scanner page.
Find the top 3 stocks that are NOT ETF's, ultra longs, or ultra shorts. Click on the stock symbol to go to the order screen. 
If you can't find a particular stock symbol, there is a stock lookup tool in the top navbar. 
Place a buy order for 2 shares of each of the top 3 stocks from the scanner. You should use a price of 20% below the most recent high.
"""

stocktwits_prompt = f"""
Go to StockTwits account at https://stocktwits.com/ripster47, find the first 3 stock symbols in his feed. Be sure to exclude the leading $ sign.
Then go to http://localhost:5056/watchlists and create a watchlist named "Twitter Picks {timestamp}" and paste a comma separated list of the 5 stock symbols into the symbols text area. Create the watchlist.
Wait until the modal disappears, then reload the page every 2 seconds until you see the Twitter Picks {timestamp} watchlist. 
When you see it, visit the watchlist, then visit each symbol in the watchlist and buy 2 shares for 5 dollars a share.
"""

perplexity_prompt = f"""
Go to https://www.perplexity.ai/finance/TSLA and extract information about their most recent earnings.
"""


async def main():
    agent = Agent(
        task=perplexity_prompt,
        llm=ChatOpenAI(model="gpt-4o")
    )
    result = await agent.run()
    
    print(result)
		
asyncio.run(main())