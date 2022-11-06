from collections import defaultdict

import altair as alt
import streamlit as st

import ReferenceRate as rr


def render_df(container, df):
    float_column = list(df.drop('Bank', axis=1, inplace=False))
    container.dataframe(df.set_index('Bank', inplace=False).style.format(
        subset=float_column, formatter="{:.2f}"), use_container_width=True)
    container.write("\n")


def valid_input(expire, selected_bank, rates, periods, pv, fv, pmt):
    if len(selected_bank) == 0:
        return 'Please Choose At Least A Bank'
    dup_bank_index = list_duplicates(selected_bank)
    for bank_name, index_list in dup_bank_index:
        for index in index_list:
            if periods.count(periods[index]) > 1:
                return 'Please Choose The Different Period For The Same Bank'

    if fv is None and pv == 0 and pmt == 0:
        return 'Present value and Payment cannot be Zero at the similiar time'
    elif pmt is None and pv is not None and fv is not None:
        if pv == 0 and fv == 0:
            return 'Present Value and Future Value cannot be Zero at the similiar time'
        elif fv < pv:
            return 'Future Value must be greater than Present Value'
    elif pv is None and fv == 0 and pmt == 0:
        return 'Future value and Payment cannot be Zero at the similiar time'

    return None


def list_duplicates(seq):
    tally = defaultdict(list)
    for i, item in enumerate(seq):
        tally[item].append(i)
    return sorted((key, locs) for key, locs in tally.items()
                  if len(locs) > 1)

def get_dup_index(key, seq):
    dup_list = list_duplicates(seq)
    for bank_name, index_list in dup_list:
        if key == bank_name:
            return list(index_list)
        else:
            return None


@st.experimental_memo
def generate_fv_chart(df, expired):
    line = alt.Chart(df.reset_index().melt('index')).mark_line(interpolate='step-after', point=True).encode(
        alt.X('index:Q', title="Months", scale=alt.Scale(
            domain=[0, expired]), axis=alt.Axis(tickMinStep=1)),
        alt.Y('value', title='Value', scale=alt.Scale(zero=False)),
        color=alt.Color('variable', title='Bank')
    ).properties(
        height=500, width=750,
        title='Reference Saving Rate'
    ).configure_title(
        fontSize=24
    ).configure_axis(
        titleFontSize=14,
        labelFontSize=12
    )
    return line


def generate_pmt_chart(df):
    bar = alt.Chart(df.melt('Bank')).mark_bar().encode(
        x=alt.X('variable', axis=alt.Axis(title=None)) if len(df.index) == 1 else
        alt.X('Bank', axis=alt.Axis(title=None)),
        y=alt.Y('value:Q',stack=None),
        color=alt.Color('variable', title=None),
        # column=alt.Column('Bank', header=alt.Header(
        #     titleOrient='bottom', labelOrient='bottom'), title=None)
    ).properties(
        height=500, width=450,
        title='Reference Saving Rate'
    ).configure_title(
        fontSize=24
    ).configure_axis(
        titleFontSize=14,
        labelFontSize=15
    )

    return bar
