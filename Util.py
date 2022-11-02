import streamlit as st
import altair as alt
from collections import defaultdict
import ReferenceRate as rr


def render_df(container, df):
    float_column = list(df.drop('Bank', axis=1, inplace=False))
    container.dataframe(df.set_index('Bank', inplace=False).style.format(
        subset=float_column, formatter="{:.2f}"))
    container.write("\n")


def valid_input(expire, selected_bank, rates, periods, pv, fv, pmt):
    if len(selected_bank) == 0:
        rr.reload_page = True
        return 'Please choose another period or another bank'
    dup_bank_index = list_duplicates(selected_bank)
    for bank_name, index_list in dup_bank_index:
        for index in index_list:
            if periods.count(periods[index]) > 1:
                return 'Please Choose The Different Period For The Same Bank'

    if fv is None and pv == 0 and pmt == 0:
        return 'Present value and Payment cannot be Zero at the similiar time'
    elif pv is None and fv == 0 and pmt == 0:
        return 'Future value and Payment cannot be Zero at the similiar time'

    return None


def list_duplicates(seq):
    tally = defaultdict(list)
    for i, item in enumerate(seq):
        tally[item].append(i)
    return sorted((key, locs) for key, locs in tally.items()
                  if len(locs) > 1)


def render_chart(df, expired):
    line = alt.Chart(df.reset_index().melt('index')).mark_line(interpolate='step-after', point=True).encode(
        alt.X('index:Q', title="Months", scale=alt.Scale(domain=[0,expired])),
        alt.Y('value', title='Value', scale=alt.Scale(zero=False)),
        color='variable'
    ).properties(
        height=400, width=650,
        title='Reference Saving Rate'
    ).configure_title(
        fontSize=16
    ).configure_axis(
        titleFontSize=14,
        labelFontSize=12
    )
    st.altair_chart(line)
