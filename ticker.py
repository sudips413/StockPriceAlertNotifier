import yahoo_fin.stock_info as si
dow_list = si.tickers_dow()
print("Tickers in Dow Jones:", len(dow_list))
# create a dictionary of the dataframes
dow_dict={}
for i in range(0, len(dow_list)):
    dow_dict[i]= dow_list[i]


print(dow_dict)

