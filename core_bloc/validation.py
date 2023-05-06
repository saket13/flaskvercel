import constants

def validate_ticker(ticker: str):
    return True if ticker in constants.VALID_TICKERS else False

