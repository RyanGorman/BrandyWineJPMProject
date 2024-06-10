import pandas as pd
import numpy as np
import yfinance as yf
from statsmodels.regression.linear_model import OLS
from statsmodels.tools.tools import add_constant
import statsmodels.stats.api as sms
import statsmodels.api as sm

def get_stock_data(symbol, start, end):
    df = yf.download(symbol, start=start, end=end)
    df['Return'] = df['Adj Close'].pct_change()
    return df

def get_ff_factors(file_path):
    ff_factors = pd.read_csv(file_path)
    ff_factors.columns = ff_factors.columns.str.strip()
    if 'Date' not in ff_factors.columns:
        raise KeyError("Expected column 'Date' not found in the CSV file. Columns found: " + ", ".join(ff_factors.columns))
    ff_factors['Date'] = pd.to_datetime(ff_factors['Date'], format='%Y%m%d')
    ff_factors.set_index('Date', inplace=True)
    ff_factors = ff_factors.apply(lambda x: x / 100 if x.name != 'RF' else x)
    return ff_factors

def perform_regression(jpm_data, ff_factors):
    data = pd.merge(jpm_data, ff_factors, on='Date', how='inner')
    data.dropna(subset=['Return'], inplace=True)
    
    X = data[['Mkt-RF', 'SMB', 'HML', 'RMW', 'CMA']]
    X = add_constant(X)
    y = data['Return'] - data['RF']
    
    model = OLS(y, X).fit()
    
    dw_test = sms.durbin_watson(model.resid)
    
    bp_test = sms.het_breuschpagan(model.resid, model.model.exog)
    labels = ['Lagrange multiplier statistic', 'p-value', 'f-value', 'f p-value']
    bp_test_result = dict(zip(labels, bp_test))
    
    return model, dw_test, bp_test_result

def main():
    symbol = 'JPM'
    start_date = '1999-12-31'
    end_date = '2024-04-30'
    file_path = 'C:\\Users\\Ryan Gorman\\Downloads\\JPMProject.csv'
    
    jpm_data = get_stock_data(symbol, start_date, end_date)
    ff_factors = get_ff_factors(file_path)
    
    model, dw_test, bp_test_result = perform_regression(jpm_data, ff_factors)
    
    print("Regression Analysis Results:")
    print(model.summary())
    
    print("\nDurbin-Watson Test for Autocorrelation:")
    print(f'Durbin-Watson statistic: {dw_test}')
    
    print("\nBreusch-Pagan Test for Heteroscedasticity:")
    for key, value in bp_test_result.items():
        print(f'{key}: {value}')

if __name__ == '__main__':
    main()
