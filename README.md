# Stock Price Forecasting & Anomaly Detection with Live Trading Bot

## Overview

In this project, I built an integrated system that combines advanced forecasting and anomaly detection with a robust trading framework. The system uses state-of-the-art machine learning techniques to predict stock prices, detect anomalies in price movements, and execute real-time trades based on these insights.

## What It Does

- **Anomaly Detection:**  
  I utilize a Variational Autoencoder (VAE) with an LSTM encoder-decoder architecture to analyze stock price time series and identify anomalies. Dynamic thresholds based on reconstruction error percentiles help flag unusual market behavior.

- **Price Forecasting:**  
  I implement an Enhanced Transformer model—drawing inspiration from "Attention is All You Need"—for multi-step future price forecasting. This model uses positional encoding and multi-head attention layers to effectively capture temporal dependencies.

- **Technical Feature Engineering:**  
  I compute key technical indicators, including the 7-day and 21-day Moving Averages (MA7, MA21) and the 14-day Relative Strength Index (RSI), to enrich the dataset and improve model predictions.

- **Trading Strategy & Automation:**  
  I develop a rule-based trading strategy that generates actionable signals (Buy, Sell, Hold) based on the outputs from the forecasting and anomaly detection models, complemented by risk mitigation measures such as stop-loss recommendations.

- **Live Trading Bot:**  
  I built a live trading bot in Python that leverages multi-threading to stream live prices, process events in real-time, and execute trades automatically. This bot is designed to operate 24/7, ensuring continuous market monitoring and trading.

- **Backtesting Framework:**  
  I developed a comprehensive backtesting system capable of simulating thousands of trades per second. This framework archives historical data over several years, allowing for extensive performance analysis and strategy optimization.

- **Web Scraping & Data Integration:**  
  I use Python-based web scraping to gather live economic data, news headlines, and market sentiments, which are stored in a MongoDB database. This data is then integrated into the trading strategy for enhanced decision-making.

- **Full-Stack Web Application:**  
  I created a full-featured web application using React for the frontend and Flask for the API backend. This application displays real-time technical indicators, sentiments, headlines, price data, and the trading bot’s status.

## Features

- **Advanced Machine Learning Models:**
  - Variational Autoencoder (VAE) with LSTM for anomaly detection.
  - Enhanced Transformer for multi-step forecasting.

- **Technical Indicators:**
  - Calculation of MA7, MA21, and RSI for feature engineering.

- **Real-Time Trading:**
  - Live trading bot with multi-threading.
  - Dynamic, rule-based strategy with risk management.

- **Backtesting:**
  - High-performance simulation of trading strategies.
  - Automated spreadsheet generation for performance analysis.

- **Data Integration:**
  - Web scraping for economic data and news.
  - MongoDB for real-time data storage and retrieval.

- **Web Application:**
  - React frontend for real-time monitoring.
  - Flask API backend for data access.

## Installation & Setup

### Prerequisites

- **Python 3.8+**
- **Node.js & npm** (for the React web application)
- **MongoDB** (for data storage)
- **Oanda API Access** (or another trading API of your choice)

## COSTS MONEY TO RUN BUT IF YOU WANT HELP RUNNING THIS PROJECT PLEASE LET ME KNOW @nicolosicielo@gmail.com


