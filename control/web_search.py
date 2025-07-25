#!/usr/bin/env python3
"""
Quick Web Search Module for Shadow AI
Provides web search capabilities and information retrieval
"""

import requests
import webbrowser
import json
import logging
from typing import List, Dict, Optional
from urllib.parse import quote_plus
import time

class QuickWebSearch:
    """Quick web search and information retrieval"""
    
    def __init__(self):
        self.search_engines = {
            'google': 'https://www.google.com/search?q={}',
            'bing': 'https://www.bing.com/search?q={}',
            'duckduckgo': 'https://duckduckgo.com/?q={}',
            'youtube': 'https://www.youtube.com/results?search_query={}',
            'wikipedia': 'https://en.wikipedia.org/wiki/Special:Search?search={}',
            'stackoverflow': 'https://stackoverflow.com/search?q={}',
            'github': 'https://github.com/search?q={}',
            'reddit': 'https://www.reddit.com/search/?q={}',
            'amazon': 'https://www.amazon.com/s?k={}',
            'flipkart': 'https://www.flipkart.com/search?q={}'
        }
        
        self.news_sources = {
            'bbc': 'https://www.bbc.com/search?q={}',
            'cnn': 'https://www.cnn.com/search?q={}',
            'reuters': 'https://www.reuters.com/search/news?blob={}',
            'techcrunch': 'https://techcrunch.com/?s={}'
        }
    
    def search_web(self, query: str, engine: str = 'google', open_browser: bool = True) -> bool:
        """Search the web using specified search engine"""
        try:
            if engine.lower() not in self.search_engines:
                logging.error(f"Unknown search engine: {engine}")
                return False
            
            search_url = self.search_engines[engine.lower()].format(quote_plus(query))
            
            if open_browser:
                webbrowser.open(search_url)
                logging.info(f"Opened {engine} search for: {query}")
                return True
            else:
                return search_url
                
        except Exception as e:
            logging.error(f"Error searching web: {e}")
            return False
    
    def search_news(self, query: str, source: str = 'bbc', open_browser: bool = True) -> bool:
        """Search news sources"""
        try:
            if source.lower() not in self.news_sources:
                logging.error(f"Unknown news source: {source}")
                return False
            
            news_url = self.news_sources[source.lower()].format(quote_plus(query))
            
            if open_browser:
                webbrowser.open(news_url)
                logging.info(f"Opened {source} news search for: {query}")
                return True
            else:
                return news_url
                
        except Exception as e:
            logging.error(f"Error searching news: {e}")
            return False
    
    def search_multiple_engines(self, query: str, engines: List[str] = None) -> bool:
        """Search multiple engines simultaneously"""
        try:
            if engines is None:
                engines = ['google', 'bing', 'duckduckgo']
            
            for engine in engines:
                if engine in self.search_engines:
                    search_url = self.search_engines[engine].format(quote_plus(query))
                    webbrowser.open(search_url)
                    time.sleep(1)  # Delay to avoid overwhelming the browser
            
            logging.info(f"Opened search in {len(engines)} engines for: {query}")
            return True
            
        except Exception as e:
            logging.error(f"Error in multi-engine search: {e}")
            return False
    
    def get_weather_info(self, city: str) -> str:
        """Get weather information for a city"""
        try:
            # Use a simple weather API or web search
            weather_query = f"weather in {city} today"
            weather_url = self.search_engines['google'].format(quote_plus(weather_query))
            webbrowser.open(weather_url)
            return f"Weather search opened for {city}"
            
        except Exception as e:
            logging.error(f"Error getting weather: {e}")
            return f"Error getting weather for {city}"
    
    def search_product_prices(self, product: str, sites: List[str] = None) -> bool:
        """Search product prices across multiple sites"""
        try:
            if sites is None:
                sites = ['amazon', 'flipkart', 'google']
            
            for site in sites:
                if site in self.search_engines:
                    if site == 'google':
                        query = f"{product} price comparison"
                    else:
                        query = product
                    
                    search_url = self.search_engines[site].format(quote_plus(query))
                    webbrowser.open(search_url)
                    time.sleep(1)
            
            logging.info(f"Product price search opened for: {product}")
            return True
            
        except Exception as e:
            logging.error(f"Error searching product prices: {e}")
            return False
    
    def quick_definition(self, term: str) -> bool:
        """Get quick definition of a term"""
        try:
            definition_query = f"define {term}"
            search_url = self.search_engines['google'].format(quote_plus(definition_query))
            webbrowser.open(search_url)
            logging.info(f"Definition search opened for: {term}")
            return True
            
        except Exception as e:
            logging.error(f"Error getting definition: {e}")
            return False
    
    def search_tutorials(self, topic: str, platform: str = 'youtube') -> bool:
        """Search for tutorials on specified topic"""
        try:
            if platform == 'youtube':
                query = f"{topic} tutorial"
                search_url = self.search_engines['youtube'].format(quote_plus(query))
            else:
                query = f"{topic} tutorial guide"
                search_url = self.search_engines['google'].format(quote_plus(query))
            
            webbrowser.open(search_url)
            logging.info(f"Tutorial search opened for: {topic}")
            return True
            
        except Exception as e:
            logging.error(f"Error searching tutorials: {e}")
            return False
    
    def search_code_examples(self, programming_query: str) -> bool:
        """Search for code examples"""
        try:
            # Search on Stack Overflow and GitHub
            stackoverflow_url = self.search_engines['stackoverflow'].format(quote_plus(programming_query))
            github_url = self.search_engines['github'].format(quote_plus(programming_query))
            
            webbrowser.open(stackoverflow_url)
            time.sleep(1)
            webbrowser.open(github_url)
            
            logging.info(f"Code examples search opened for: {programming_query}")
            return True
            
        except Exception as e:
            logging.error(f"Error searching code examples: {e}")
            return False
    
    def search_academic(self, research_query: str) -> bool:
        """Search for academic/research content"""
        try:
            # Search Google Scholar and Wikipedia
            scholar_url = f"https://scholar.google.com/scholar?q={quote_plus(research_query)}"
            wiki_url = self.search_engines['wikipedia'].format(quote_plus(research_query))
            
            webbrowser.open(scholar_url)
            time.sleep(1)
            webbrowser.open(wiki_url)
            
            logging.info(f"Academic search opened for: {research_query}")
            return True
            
        except Exception as e:
            logging.error(f"Error searching academic content: {e}")
            return False

# Global instance
web_search = QuickWebSearch()
