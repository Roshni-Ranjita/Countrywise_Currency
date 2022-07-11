# Importing Libraries
from queue import Full
import streamlit as st
import numpy as np
import pandas as pd
from datetime import date


#Headding
st.set_page_config(
    page_title= "Currency conversion and PPP",
    page_icon= '🤑',
    layout= "wide"
)
st.markdown(f"<h2 style= 'text-align: center;'> Currency converter and PPP predictor </h2>", unsafe_allow_html=True)
today = date.today() # Returns the current local date
st.write('Last Updated date:', today)

# Currency Converter
st.markdown(f"<h4 style= 'text-align: left;'> Convertion Rate </h4>", unsafe_allow_html=True)
st.write('The Exchange rate is the ratio between the currency of one country\'s currency vs the value of another country\'s  currency. \n For example, if 1 USD = 79 INR, then the exchange rate from USD to INR is 79. ')

def rate_usd(curr,Exchange_Rate):
    er= Exchange_Rate.set_index('Currency').Exchange_Rate.to_dict()
    return er[curr]

def prepare_exchange_rate_table(Exchange_Rate, curr):
    Exchange_Rate=Exchange_Rate[['Currency', 'Exchange_Rate']]
    rate= rate_usd(curr,Exchange_Rate)
    s= 'Exchange_Rate_'+curr+'(1'+curr+' = X unit)'
    Exchange_Rate[s]= Exchange_Rate['Exchange_Rate']/rate
    Exchange_Rate.rename(columns = {'Exchange_Rate':'Exchange_Rate_USD(1 USD = X unit)'}, inplace = True)
    return Exchange_Rate
def currency_converter_rate(exchange_rate, currency_to,  currency_from='INR'):
    er= exchange_rate.set_index('Currency').Exchange_Rate.to_dict()
    return  er[currency_from]/er[currency_to]

def currency_converter(exchange_rate, currency_to,  currency_from='INR', amount=1):
    rate= currency_converter_rate(exchange_rate, currency_to,  currency_from)
    return amount/rate

col1, col2 = st.columns(2)

with col1:
    st.markdown(f"<h6 style= 'text-align: left;'> Curent Convertion Rate </h6>", unsafe_allow_html=True)
    Exchange_Rate= pd.read_csv('Exchange_Rate.csv')
    li= Exchange_Rate.Currency.to_list()
    curr=st.selectbox('Pick a currency', li)
    Exchange_Rate_table= prepare_exchange_rate_table(Exchange_Rate, curr)
    st.dataframe(Exchange_Rate_table, width= None)

with col2:
    st.markdown(f"<h6 style= 'text-align: left;'> Curency Convertion Calculator </h6>", unsafe_allow_html=True)
    currency_from =st.selectbox('currency_from', li)
    currency_to =st.selectbox('currency_to', li)
    amount= st.number_input('Enter an amount')
    value= currency_converter(Exchange_Rate, currency_to,  currency_from, amount)
    st.write('Converted: '+ str(amount) +' '+ currency_from + ' = '+ str(value) + ' ' + currency_to)



# PPP Converter
st.markdown(f"<h4 style= 'text-align: left;'> Purchase Power Parity(PPP) </h4>", unsafe_allow_html=True)
st.write('Purchase Power Parity is the ratio of cost of good x in currency 1 to cost of good x in currency 2.')

def get_year_range_filtered(year_range, PPP_Rate):
    mn_year, mx_year= year_range
    PPP_Rate['TIME'] = PPP_Rate['TIME'].astype(int)
    PPP_Rate= PPP_Rate[PPP_Rate['TIME']>=mn_year]
    PPP_Rate= PPP_Rate[PPP_Rate['TIME']<=mx_year]
    return PPP_Rate

def prepare_ppp_rate_table(ppp):
    ppp=pd.crosstab(index = ppp.LOCATION, columns = ppp.TIME, values = ppp.Value, aggfunc = 'mean').reset_index()
    return ppp

def reading_ppp_file(ppp):
    ppp=pd.crosstab(index = ppp.LOCATION, columns = ppp.TIME, values = ppp.Value, aggfunc = 'mean').reset_index()
    return ppp


def ppp_convertion_rate(ppp, currency_to, currency_from='IND'):
    ppp_dict= ppp.set_index('LOCATION')[ppp.columns[-1]].to_dict()
    return ppp_dict[currency_to]/ppp_dict[currency_from]


def ppp_converter(ppp,currency_to,  currency_from='IND', amount=1):
    ppp= reading_ppp_file(ppp)
    rate= ppp_convertion_rate(ppp, currency_to,  currency_from)
    return amount * rate

col1, col2 = st.columns(2)
with col1:
    st.markdown(f"<h6 style= 'text-align: left;'> PPP Values Yearwise </h6>", unsafe_allow_html=True)
    PPP_Rate= pd.read_csv('PurchasePowerParity.csv')
    mini= PPP_Rate['TIME'].min()
    maxi= PPP_Rate['TIME'].max()
    year_range= st.select_slider('Year Range', range(mini, maxi+1), (2010,2021))
    st.write('Following table shows the PPP rate for the year: ' ,year_range)
    PPP_Rate_table= get_year_range_filtered(year_range, PPP_Rate)
    PPP_Rate_table= prepare_ppp_rate_table(PPP_Rate_table)
    st.dataframe(PPP_Rate_table)

with col2:
    st.markdown(f"<h6 style= 'text-align: left;'> Country wise money calculation </h6>", unsafe_allow_html=True)
    li= PPP_Rate_table.LOCATION.tolist()
    currency_from =st.selectbox('currency_from', li)
    currency_to =st.selectbox('currency_to', li)
    amount= st.number_input('Enter an amount for ppp')
    value= ppp_converter(PPP_Rate, currency_to,  currency_from, amount)
    st.write('PPP: '+ str(amount) +' '+ currency_from + ' = '+ str(value) + ' ' + currency_to)