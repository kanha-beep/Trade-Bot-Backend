from server.vcp.nse_symbols import get_all_nse_symbols
from server.vcp.debug_vcp_stocks import scan_vcp_stocks

if __name__ == "__main__":
    symbols = get_all_nse_symbols()
    print("Total NSE Stocks in other folder:", len(symbols))

    vcp = scan_vcp_stocks(symbols)
    print("\n🔥 FINAL VCP STOCKS 🔥")
    print(vcp)