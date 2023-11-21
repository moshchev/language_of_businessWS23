import yfinance as yf
import pandas as pd
import numpy as np

def change_date(df):
    df.columns = [pd.to_datetime(col, errors='ignore').strftime('%d-%m-%Y') for col in df.columns]
    return df


def substraction_of_metrics(df, first_summand, second_summand, name_of_new_metric):
    assets = df.loc[df['Financial Indicators'] == first_summand].iloc[0]
    debt = df.loc[df['Financial Indicators'] == second_summand].iloc[0]
    na = assets.iloc[2:] - debt.iloc[2:]
    new_row = pd.DataFrame([[name_of_new_metric, 'bs' ] + list(na)], columns=df.columns)
    df = pd.concat([df, new_row], ignore_index=False)

    return df


def year_averages(df, financial_indicator):
    # get the data of the indicator so to calc average
    indicator_data = df.loc[df['Financial Indicators'] == financial_indicator, df.columns[2:]]

    # calculate moving average
    avg_balances = [
        np.nanmean(indicator_data.iloc[:, col -2:col].values)
        for col in range(2, len(df.columns)) 
        ]
    # create new row
    new_row_data = pd.DataFrame([[financial_indicator + ' MA', 'bs'] + avg_balances], columns=df.columns)
 
    # insert the new rows into the original df
    df = pd.concat([df, pd.DataFrame(new_row_data, columns=df.columns)], ignore_index=True)

    return df


def get_data(ticker):
    # call data
    company = yf.Ticker(ticker=ticker)
    bs, income, cf = company.balance_sheet, company.income_stmt, company.cash_flow
    
    # adjust datetype for columns
    bs = change_date(bs)
    income = change_date(income)
    cf = change_date(cf)

    #add data source
    bs.insert(0, 'Data Source', 'bs')
    income.insert(0, 'Data Source', 'is')
    cf.insert(0, 'Data Source', 'cf')

    # produce final table
    fin_table = pd.concat([bs, income, cf])
    fin_table = fin_table.reset_index().rename(columns={'index': 'Financial Indicators'})
    
    # add net assets
    fin_table = substraction_of_metrics(fin_table, 'Total Assets', 'Total Debt', 'Net Assets')

    # add year averages for 
    fin_table = year_averages(fin_table, 'Total Assets')
    fin_table = year_averages(fin_table, 'Accounts Receivable')
    fin_table = year_averages(fin_table, 'Inventory')
    
    return fin_table


def get_rate(df, nom, denom, nom_source, denom_source ,year = False):

    nom_data = df[(df['Financial Indicators'] == nom) & (df['Data Source'] == nom_source)]
    denom_data = df[(df['Financial Indicators'] == denom) & (df['Data Source'] == denom_source)]
    
    nom_values=nom_data.iloc[:,2:].values
    denom_values=denom_data.iloc[:,2:].values
    
    rate=nom_values/denom_values
    if year:
        rate = rate * 365
   
    calc = pd.DataFrame(rate, columns=df.columns[2:])
    
    return calc

if __name__ == '__main__':
    #company = input('Type a ticker: ')
    table = get_data('PEP')
    print(table.tail(15))
    some_metric = get_rate(table, 'Total Assets', 'Total Debt', 'bs', 'bs' )
    year_mult = get_rate(table, 'Total Assets', 'Total Debt', 'bs', 'bs', year=True)
    print(f'Here is normal metric {some_metric}')
    print(f'multiplied with 360 {year_mult}')