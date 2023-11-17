import yfinance as yf
import pandas as pd

def change_date(df):
    df.columns = [pd.to_datetime(col, errors='ignore').strftime('%d-%m-%Y') for col in df.columns]
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
    
    return fin_table


if __name__ == '__main__':
    company = input('Type a ticker: ')
    table = get_data(company)
    print(table)