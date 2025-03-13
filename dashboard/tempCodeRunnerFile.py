st.header('Bike Sharing Dashboard :sparkles:')
st.subheader('Hourly Rentals')

col1, col2 = st.columns(2)
with col1 :
    total_rentals = hourly_rentals_df.rental_totals.sum()
    st.metric('Total Rentals', value=total_rentals)
with col2 :
    st.text('Siuu')
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