import pandas as pd
from matplotlib import pyplot as plt
import seaborn as sns
import streamlit as st
import os
sns.set(style='dark')

# Helper function untuk berbagai DataFrame

def create_hourly_rentals_df (df) :
    hourly_rentals_df = df.groupby(by='hr')[['weekday', 'dteday', 'cnt']].first()
    hourly_rentals_df = hourly_rentals_df.reset_index()
    hourly_rentals_df.rename(columns={
        'hr' : 'hourly_record',
        'cnt' : 'rental_totals'
    }, inplace=True)

    return hourly_rentals_df

def create_monthly_rentals_df (df) :
    monthly_rentals_df = df.groupby(by=['yr', 'mnth']).agg({
        'cnt' : 'sum'
    })
    monthly_rentals_df = monthly_rentals_df.reset_index()
    monthly_rentals_df.rename(columns={
        'mnth' : 'bulan',
        'cnt' : 'rentals_total'
    }, inplace=True)

    return monthly_rentals_df

def create_weekly_rentals_by_temp_hum_df (df) :
    rentals_by_temp_df = df.resample(
        rule='W', on='dteday')['temp_group'].value_counts().unstack().fillna(0).reset_index()
    rentals_by_hum_df = df.resample(
        rule='W', on='dteday')['hum_group'].value_counts().unstack().fillna(0).reset_index()
    date_period = pd.date_range(start=date_picked, freq='D', periods=7)
    for date_day in rentals_by_temp_df['dteday'] :
        if date_day in date_period:
            rentals_by_temp_df = rentals_by_temp_df[rentals_by_temp_df['dteday'] == date_day]
            rentals_by_hum_df = rentals_by_hum_df[rentals_by_hum_df['dteday'] == date_day]
    weekly_rentals_by_temp_df = rentals_by_temp_df.melt(id_vars=['dteday'], var_name='temp', value_name='user_total')
    weekly_rentals_by_hum_df = rentals_by_hum_df.melt(id_vars=['dteday'], var_name='hum', value_name='user_total')

    return {'temp':weekly_rentals_by_temp_df, 'hum':weekly_rentals_by_hum_df}

# Load Data yang sudah diproses
path_file = os.path.join(os.path.dirname(__file__), "all_data.csv")
all_df = pd.read_csv(path_file)

all_df.sort_values(by='dteday', inplace=True)
all_df.reset_index(inplace=True)
all_df['dteday'] = pd.to_datetime(all_df.dteday)

# Filter Data
min_date = all_df.dteday.min()
max_date = all_df.dteday.max()
with st.sidebar :
    # Menambahkan gambar log
    st.image('https://github.com/dicodingacademy/assets/raw/main/logo.png')

    # Mengambil data hari
    date_picked = st.date_input(
        label='Pilih Hari',
        max_value=max_date, min_value=min_date,
        value='today'
    )
main_df = all_df[all_df.dteday == str(date_picked)]
tahun_df = int(date_picked.strftime('%Y'))
main_df2 = all_df[all_df.yr == tahun_df]

# Menyiapkan berbagai DataFrame
hourly_rentals_df = create_hourly_rentals_df(main_df)
monthly_rentals_df = create_monthly_rentals_df(main_df2)
weekly_rentals_by_temp_hum_df = create_weekly_rentals_by_temp_hum_df(main_df2)

# Plot Number dari Hourly Rentals
st.header('Bike Sharing Dashboard :sparkles:')
st.subheader('Hourly Rentals')

col1, col2 = st.columns(2)
with col1 :
    total_rentals = hourly_rentals_df.rental_totals.sum()
    st.metric('Total Rentals', value=total_rentals)
with col2 :
    st.text(f'Hari : {hourly_rentals_df.weekday[0]}')
    str_time = hourly_rentals_df.dteday[0].strftime('%Y-%m-%d')
    st.write(f'Tanggal : {str_time}')
    # (label='Tanggal' ,height=100, value=)
fig, ax = plt.subplots(figsize=(16, 8))
ax.plot(
    hourly_rentals_df['hourly_record'],
    hourly_rentals_df['rental_totals'],
    marker='o',
    linewidth=2,
    color='#80ABD9'
)
ax.tick_params(axis='y', labelsize=20)
ax.tick_params(axis='x', labelsize=15)
st.pyplot(fig)

# Plot Number Monthly Rentals
st.subheader(f'Monthly Rentals by {monthly_rentals_df.yr[0]}')

fig, ax = plt.subplots(figsize=(16, 8))
max_user = monthly_rentals_df.rentals_total.max()
colors = ["#08ED00" if cnt == max_user else "#78C9FF" for cnt in monthly_rentals_df.rentals_total]
sns.barplot(
    x='bulan',
    y='rentals_total',
    data=monthly_rentals_df.sort_values(by='rentals_total', ascending=False),
    palette=colors,
    ax=ax
)
ax.set_title('Bike Sharing Log in {}'.format(monthly_rentals_df.yr[0]), fontsize=20)
ax.set_ylabel('Total User Rental')
ax.set_xlabel('Bulan Dalam Angka')
st.pyplot(fig)

# Plot Number User Interest by Temperature n Humidity
st.subheader('Rental User Interest This Week')
st.write('Based On Temperature And Humidity')

fig, ax = plt.subplots(nrows=1, ncols=2, figsize=(24,12))

temp_max = weekly_rentals_by_temp_hum_df['temp']['user_total'].max()
hum_max = weekly_rentals_by_temp_hum_df['hum']['user_total'].max()

temp_colors = ['#12BCD4' if cnt == temp_max else '#D3D3D3' for cnt in weekly_rentals_by_temp_hum_df['temp']['user_total']]
hum_colors = ['#FF3B3E' if cnt == hum_max else '#D3D3D3' for cnt in weekly_rentals_by_temp_hum_df['hum']['user_total']]

sns.barplot(data=weekly_rentals_by_temp_hum_df['temp'], x='temp', y='user_total', palette=temp_colors, ax=ax[0])
ax[0].set_ylabel(None)
ax[0].set_xlabel(None)
ax[0].set_title('Minat Rental dengan Faktor Suhu', loc='center', fontsize=30)
ax[0].tick_params(axis='y', labelsize=30)
ax[0].tick_params(axis='x', labelsize=30)

sns.barplot(data=weekly_rentals_by_temp_hum_df['hum'], x='hum', y='user_total', palette=hum_colors, ax=ax[1])
ax[1].set_ylabel(None)
ax[1].set_xlabel(None)
ax[1].invert_xaxis()
ax[1].yaxis.set_label_position("right")
ax[1].yaxis.tick_right()
ax[1].set_title('Minat Rental dengan Faktor Kelembapan', loc='center', fontsize=30)
ax[1].tick_params(axis='y', labelsize=30)
ax[1].tick_params(axis='x', labelsize=30)

plt.suptitle('Minat User Rental dengan Faktor Suhu dan Kelembapan', fontsize=40)
st.pyplot(fig)