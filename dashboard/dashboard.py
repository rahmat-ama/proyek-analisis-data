import pandas as pd
from matplotlib import pyplot as plt
import seaborn as sns
import streamlit as st
import datetime as dt
import os
sns.set(style='dark')

# Helper function untuk berbagai DataFrame

def create_rentals_season_df (df) :
    rentals_season_df = df.groupby(['yr', 'season']).cnt.sum()
    rentals_season_df = rentals_season_df.reset_index()
    rentals_season_df.rename(columns={
        'yr' : 'tahun',
        'season' : 'musim',
        'cnt' : 'total_rental'
    }, inplace=True)

    return rentals_season_df

    
def create_hour_rentals_df (df) :
    df['tanggal'] = df.dteday.dt.date
    hour_rentals_df = df.loc[df.groupby('tanggal')['cnt'].idxmax(),
                             ['tanggal', 'hr', 'cnt']]
    hour_rentals_df = hour_rentals_df.reset_index(drop=True)
    hour_rentals_df['tanggal'] = pd.to_datetime(hour_rentals_df.tanggal)
    hour_rentals_df.rename(columns={
        'hr' : 'jam',
        'cnt' : 'total_user'
    }, inplace=True)

    return hour_rentals_df

def create_monthly_rentals_df (df) :
    monthly_rentals_df = df.groupby(by=['yr', 'mnth']).agg({
        'cnt' : 'sum'
    })
    monthly_rentals_df = monthly_rentals_df.reset_index()
    monthly_rentals_df.rename(columns={
        'mnth' : 'bulan',
        'cnt' : 'total_rental'
    }, inplace=True)

    return monthly_rentals_df

def create_rentals_by_temp_hum_df (df) :
    df.rename(columns={
        'cnt' : 'user_total'
    }, inplace=True)
    rentals_by_temp_df = df.groupby('temp_group').user_total.sum().sort_values(ascending=False)
    rentals_by_hum_df = df.groupby('hum_group').user_total.sum().sort_values(ascending=False)
    rentals_by_temp_df = rentals_by_temp_df.reset_index()
    rentals_by_hum_df = rentals_by_hum_df.reset_index()


    return {'temp':rentals_by_temp_df, 'hum':rentals_by_hum_df}

# Load Data yang sudah diproses
path_file = os.path.join(os.path.dirname(__file__), "all_data.csv")
all_df = pd.read_csv(path_file)

all_df.sort_values(by='dteday', inplace=True)
all_df.reset_index(inplace=True)
all_df['dteday'] = pd.to_datetime(all_df.dteday)

# Filter Data
min_date = all_df.dteday.min()
max_date = all_df.dteday.max()
median_date = all_df.dteday.median()
end_median_date = median_date + pd.Timedelta(days=7)
with st.sidebar :
    # Menambahkan gambar log
    st.image('https://github.com/dicodingacademy/assets/raw/main/logo.png')

    # Mengambil data hari
    start_date, end_date = st.date_input(
        label='Rentang Waktu',
        max_value=max_date, min_value=min_date,
        value=[median_date, end_median_date]
    )
    st.caption('Pilih Rentang Waktu Awal dan Akhir Data yang ingin ditampilkan')
main_df = all_df[(all_df.dteday >= str(start_date)) & 
                  (all_df.dteday <= str(end_date))]

# Menyiapkan berbagai DataFrame
season_rentals_df = create_rentals_season_df(main_df)
hour_rentals_df = create_hour_rentals_df(main_df)
monthly_rentals_df = create_monthly_rentals_df(main_df)
rentals_by_temp_hum_df = create_rentals_by_temp_hum_df(main_df)

st.header('Bike Sharing Dashboard :sparkles:')

# Season Rentals
st.subheader('Total Rental Berdasarkan Musim')
season_color = ['#ffc72e', '#389fff']
fig, ax1 = plt.subplots(figsize=(20, 10))
sns.barplot(data=season_rentals_df, x='musim', y='total_rental',
            hue='tahun', errorbar=None, ax=ax1, palette=season_color)
ax1.set_title('Total Rental Bike Berdasarkan Musim', fontsize=30)
ax1.set_xlabel('Musim Dalam Satu Tahun', fontsize=25)
ax1.set_ylabel('Total Rental Bike', fontsize=25)
ax1.tick_params(axis='y', labelsize=20)
ax1.tick_params(axis='x', labelsize=20)
ax1.legend(title='Tahun', fontsize=20)
st.pyplot(fig)


# Hourly Rentals
st.subheader('Most Rental Berdasarkan Jam Setiap Hari')
col1, col2 = st.columns(2)
with col1 :
    total_rentals = hour_rentals_df.total_user.sum()
    st.metric('Total Rentals', value=total_rentals)
with col2 :
    st.metric('Waktu Dengan User Terbanyak Pukul', value=hour_rentals_df.jam.mode().values[0])
fig, ax2 = plt.subplots(figsize=(20, 12))
bar_container = ax2.bar(
    hour_rentals_df['tanggal'],
    hour_rentals_df['total_user'],
    width=0.6
)
ax2.set_title('Waktu/Jam Yang Memiliki User Paling Banyak Setiap Hari', fontsize=30)
ax2.set_ylabel('Total User (Dengan Tambahan Label Waktu)', fontsize=25)
ax2.bar_label(container=bar_container, 
              labels=[f'{user}\n{jam}' for user, jam in zip(hour_rentals_df['total_user'], hour_rentals_df['jam'])], 
                      fontsize=18, padding=4)
ax2.tick_params(axis='y', labelsize=20)
ax2.tick_params(axis='x', labelsize=20)
str_tanggal = [date.strftime('%m\n%d\n%Y') for date in hour_rentals_df['tanggal']]
ax2.set_xticks(hour_rentals_df.tanggal, labels=str_tanggal, fontsize=15)
ax2.legend(labels=['User\nJam'], loc='upper right', fontsize=18)
st.pyplot(fig)

# Plot Number Monthly Rentals
st.subheader('Monthly Rental')
fig, ax = plt.subplots(figsize=(16, 8))
max_user = monthly_rentals_df.total_rental.max()
colors = ["#08ED00" if cnt == max_user else "#78C9FF" for cnt in monthly_rentals_df.total_rental]
sns.lineplot(
    x='bulan',
    y='total_rental',
    data=monthly_rentals_df,
    ax=ax
)
ax.set_title('Monthly Bike Sharing Log', fontsize=30)
ax.set_ylabel('Total User Rental', fontsize=20)
ax.set_xlabel('Bulan Dalam Angka', fontsize=20)
ax.tick_params(axis='x', labelsize=18)
ax.tick_params(axis='y', labelsize=18)
st.pyplot(fig)

# Plot Number User Interest by Temperature n Humidity
st.subheader('Rental User Interest')
st.write('Based On Temperature And Humidity')

fig, ax = plt.subplots(nrows=1, ncols=2, figsize=(24,12))

temp_max = rentals_by_temp_hum_df['temp']['user_total'].max()
hum_max = rentals_by_temp_hum_df['hum']['user_total'].max()

temp_colors = ['#12BCD4' if cnt == temp_max else '#D3D3D3' for cnt in rentals_by_temp_hum_df['temp']['user_total']]
hum_colors = ['#FF3B3E' if cnt == hum_max else '#D3D3D3' for cnt in rentals_by_temp_hum_df['hum']['user_total']]

sns.barplot(data=rentals_by_temp_hum_df['temp'], x='temp_group', y='user_total', palette=temp_colors, ax=ax[0])
ax[0].set_ylabel(None)
ax[0].set_xlabel(None)
ax[0].set_title('Minat Rental dengan Faktor Suhu', loc='center', fontsize=30)
ax[0].tick_params(axis='y', labelsize=20)
ax[0].tick_params(axis='x', labelsize=20)

sns.barplot(data=rentals_by_temp_hum_df['hum'], x='hum_group', y='user_total', palette=hum_colors, order=rentals_by_temp_hum_df['hum']['hum_group'].unique(), ax=ax[1])
ax[1].set_ylabel(None)
ax[1].set_xlabel(None)
ax[1].invert_xaxis()
ax[1].yaxis.set_label_position("right")
ax[1].yaxis.tick_right()
ax[1].set_title('Minat Rental dengan Faktor Kelembapan', loc='center', fontsize=30)
ax[1].tick_params(axis='y', labelsize=20)
ax[1].tick_params(axis='x', labelsize=20)

plt.suptitle('Minat User Rental dengan Faktor Suhu dan Kelembapan', fontsize=40)
st.pyplot(fig)