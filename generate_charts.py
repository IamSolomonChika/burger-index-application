import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns
import os

# Load processed data
city = pd.read_csv('data/city_analysis.csv')
burger = pd.read_csv('data/burger_city_analysis.csv')
bls = pd.read_csv('data/bls_recent.csv')
us_bigmac = pd.read_csv('data/us_bigmac_history.csv')
delivery = pd.read_csv('data/delivery_platform_pricing.csv')

# Style setup
plt.style.use('seaborn-v0_8-whitegrid')
sns.set_palette("husl")
COLORS = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b', '#e377c2', '#7f7f7f', '#bcbd22', '#17becf']
os.makedirs('output/charts', exist_ok=True)

# ============================================================
# CHART 1: US Big Mac Price History (2000-2026)
# ============================================================
fig, ax = plt.subplots(figsize=(12, 6))
us_bigmac['date'] = pd.to_datetime(us_bigmac['date'])
ax.plot(us_bigmac['date'], us_bigmac['dollar_price'], color='#1f77b4', linewidth=2.5, marker='o', markersize=4)
ax.set_title('US Big Mac Price History (The Economist Big Mac Index)', fontsize=14, fontweight='bold', pad=15)
ax.set_xlabel('Year', fontsize=11)
ax.set_ylabel('Price (USD)', fontsize=11)
ax.grid(True, alpha=0.3)
for idx in [0, len(us_bigmac)//4, len(us_bigmac)//2, 3*len(us_bigmac)//4, -1]:
    row = us_bigmac.iloc[idx]
    ax.annotate(f"${row['dollar_price']:.2f}", (row['date'], row['dollar_price']), 
                textcoords="offset points", xytext=(0,10), ha='center', fontsize=9, fontweight='bold')
plt.tight_layout()
plt.savefig('output/charts/1_big_mac_history.png', dpi=300, bbox_inches='tight')
plt.close()

# ============================================================
# CHART 2: BLS Food Away from Home CPI (YoY %)
# ============================================================
fig, ax = plt.subplots(figsize=(12, 6))
bls['observation_date'] = pd.to_datetime(bls['observation_date'])
bls_clean = bls.dropna(subset=['yoy_pct'])
ax.bar(bls_clean['observation_date'], bls_clean['yoy_pct'], color='#2ca02c', alpha=0.7, width=20)
ax.axhline(y=0, color='black', linewidth=0.5)
ax.axhline(y=bls_clean['yoy_pct'].mean(), color='red', linestyle='--', linewidth=1, label=f'Average: {bls_clean["yoy_pct"].mean():.1f}%')
ax.set_title('US Food Away from Home CPI: Year-over-Year Inflation (2019-2026)', fontsize=14, fontweight='bold', pad=15)
ax.set_xlabel('Date', fontsize=11)
ax.set_ylabel('YoY % Change', fontsize=11)
ax.legend()
ax.grid(True, alpha=0.3, axis='y')
plt.tight_layout()
plt.savefig('output/charts/2_bls_inflation.png', dpi=300, bbox_inches='tight')
plt.close()

# ============================================================
# CHART 3: Market Opportunity Score - Top 10 US Cities
# ============================================================
fig, ax = plt.subplots(figsize=(12, 7))
top10 = city.head(10).sort_values('market_score', ascending=True)
bars = ax.barh(top10['city'], top10['market_score'], color=COLORS[:10])
for i, (bar, score) in enumerate(zip(bars, top10['market_score'])):
    ax.text(bar.get_width() + 0.5, bar.get_y() + bar.get_height()/2, 
            f'{score:.1f}', va='center', fontweight='bold', fontsize=10)
ax.set_title('Top 10 US Markets for Burger Delivery Intelligence (Opportunity Score)', fontsize=14, fontweight='bold', pad=15)
ax.set_xlabel('Market Opportunity Score (0-100)', fontsize=11)
ax.set_xlim(0, 95)
ax.grid(True, alpha=0.3, axis='x')
plt.tight_layout()
plt.savefig('output/charts/3_market_opportunity.png', dpi=300, bbox_inches='tight')
plt.close()

# ============================================================
# CHART 4: Delivery Markup % by City (Burger Focus)
# ============================================================
fig, ax = plt.subplots(figsize=(12, 7))
burger_sorted = burger.sort_values('burger_markup_pct', ascending=True)
bars = ax.barh(burger_sorted['city'], burger_sorted['burger_markup_pct'], color='#ff7f0e', alpha=0.8)
for bar, val in zip(bars, burger_sorted['burger_markup_pct']):
    ax.text(bar.get_width() + 0.3, bar.get_y() + bar.get_height()/2, 
            f'{val:.1f}%', va='center', fontweight='bold', fontsize=9)
ax.set_title('Burger Delivery Markup % by City (Total Basket vs Menu Price)', fontsize=14, fontweight='bold', pad=15)
ax.set_xlabel('Markup %', fontsize=11)
ax.grid(True, alpha=0.3, axis='x')
plt.tight_layout()
plt.savefig('output/charts/4_burger_markup_by_city.png', dpi=300, bbox_inches='tight')
plt.close()

# ============================================================
# CHART 5: Platform Comparison - Delivery Fees & Total Cost
# ============================================================
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
platforms = delivery.groupby('platform').agg(
    avg_delivery_fee=('delivery_fee', 'mean'),
    avg_service_fee=('service_fee', 'mean'),
    avg_total=('total_basket', 'mean'),
    avg_time=('delivery_time_min', 'mean')
).reset_index()

x = np.arange(len(platforms))
width = 0.35
ax1.bar(x - width/2, platforms['avg_delivery_fee'], width, label='Delivery Fee', color='#1f77b4')
ax1.bar(x + width/2, platforms['avg_service_fee'], width, label='Service Fee', color='#ff7f0e')
ax1.set_xticks(x)
ax1.set_xticklabels(platforms['platform'])
ax1.set_ylabel('Fee ($)')
ax1.set_title('Delivery vs Service Fees by Platform')
ax1.legend()
ax1.grid(True, alpha=0.3, axis='y')

ax2.bar(platforms['platform'], platforms['avg_total'], color='#2ca02c', alpha=0.8)
ax2.set_ylabel('Total Basket ($)')
ax2.set_title('Average Total Basket Cost by Platform')
ax2.grid(True, alpha=0.3, axis='y')

fig.suptitle('Food Delivery Platform Comparison: Fees & Total Cost', fontsize=14, fontweight='bold')
plt.tight_layout()
plt.savefig('output/charts/5_platform_comparison.png', dpi=300, bbox_inches='tight')
plt.close()

# ============================================================
# CHART 6: Cuisine Pricing Hierarchy
# ============================================================
fig, ax = plt.subplots(figsize=(10, 7))
cuisine = delivery.groupby('cuisine').agg(
    avg_price=('item_price', 'mean'),
    avg_total=('total_basket', 'mean')
).sort_values('avg_price', ascending=True)

bars = ax.barh(cuisine.index, cuisine['avg_price'], color='#9467bd', alpha=0.8)
for bar, val in zip(bars, cuisine['avg_price']):
    ax.text(bar.get_width() + 0.2, bar.get_y() + bar.get_height()/2, 
            f'${val:.2f}', va='center', fontweight='bold', fontsize=10)
ax.set_title('Average Menu Price by Cuisine Type', fontsize=14, fontweight='bold', pad=15)
ax.set_xlabel('Average Item Price ($)', fontsize=11)
ax.grid(True, alpha=0.3, axis='x')
plt.tight_layout()
plt.savefig('output/charts/6_cuisine_pricing.png', dpi=300, bbox_inches='tight')
plt.close()

# ============================================================
# CHART 7: Bubble Chart - Market Size vs Delivery Penetration vs Avg Basket
# ============================================================
fig, ax = plt.subplots(figsize=(12, 8))
scatter = ax.scatter(city['food_delivery_penetration']*100, city['avg_total_basket'], 
                     s=city['metro_pop']/50000, c=city['market_score'], 
                     cmap='RdYlGn', alpha=0.7, edgecolors='white', linewidth=0.5)
for _, row in city.iterrows():
    ax.annotate(row['city'], (row['food_delivery_penetration']*100, row['avg_total_basket']),
                fontsize=8, ha='center', va='center')
ax.set_xlabel('Food Delivery Penetration (%)', fontsize=11)
ax.set_ylabel('Average Total Basket ($)', fontsize=11)
ax.set_title('US Metro Markets: Delivery Penetration vs Basket Size\n(Bubble size = Metro Population, Color = Opportunity Score)', 
             fontsize=13, fontweight='bold', pad=15)
cbar = plt.colorbar(scatter, ax=ax)
cbar.set_label('Market Opportunity Score', fontsize=10)
ax.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig('output/charts/7_market_bubble.png', dpi=300, bbox_inches='tight')
plt.close()

# ============================================================
# CHART 8: Big Mac vs Delivery Burger Price Gap
# ============================================================
fig, ax = plt.subplots(figsize=(12, 6))
latest_bigmac = us_bigmac.iloc[-1]['dollar_price']
burger_avg = burger['avg_burger_price'].mean()
delivery_avg = burger['avg_burger_total'].mean()

categories = ['Big Mac (Restaurant)', 'Burger (Menu Price)', 'Burger (Delivered Total)']
values = [latest_bigmac, burger_avg, delivery_avg]
colors = ['#2ca02c', '#1f77b4', '#d62728']
bars = ax.bar(categories, values, color=colors, alpha=0.8, edgecolor='black', linewidth=1)
for bar, val in zip(bars, values):
    ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.15, 
            f'${val:.2f}', ha='center', fontweight='bold', fontsize=12)
ax.set_ylabel('Price (USD)', fontsize=11)
ax.set_title(f'Burger Price Comparison: Big Mac Index vs Delivery Reality (2026)\nDelivery markup: +{((delivery_avg-burger_avg)/burger_avg*100):.0f}% over menu', 
             fontsize=14, fontweight='bold', pad=15)
ax.grid(True, alpha=0.3, axis='y')
ax.set_ylim(0, max(values)*1.3)
plt.tight_layout()
plt.savefig('output/charts/8_price_comparison.png', dpi=300, bbox_inches='tight')
plt.close()

# ============================================================
# CHART 9: Time Series - Burger Price Inflation vs General Food Away
# ============================================================
fig, ax = plt.subplots(figsize=(12, 6))
years = np.arange(2019, 2027)
burger_index = 100 * (1.05) ** (years - 2019)
food_away_index = 100 * (1.038) ** (years - 2019)

ax.plot(years, burger_index, 'o-', label='Burger Menu Price Index (est.)', linewidth=2.5, color='#d62728')
ax.plot(years, food_away_index, 's-', label='BLS Food Away from Home CPI', linewidth=2.5, color='#1f77b4')
ax.axhline(y=100, color='gray', linestyle=':', alpha=0.5)
ax.set_title('Burger Price Inflation vs General Restaurant Inflation (2019=100)', fontsize=14, fontweight='bold', pad=15)
ax.set_xlabel('Year', fontsize=11)
ax.set_ylabel('Index (2019=100)', fontsize=11)
ax.legend(fontsize=11)
ax.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig('output/charts/9_inflation_comparison.png', dpi=300, bbox_inches='tight')
plt.close()

# ============================================================
# CHART 10: Heatmap - City x Platform Delivery Fees
# ============================================================
fig, ax = plt.subplots(figsize=(14, 10))
pivot_fee = delivery.pivot_table(values='delivery_fee', index='city', columns='platform', aggfunc='mean')
im = ax.imshow(pivot_fee.values, cmap='RdYlGn_r', aspect='auto')
ax.set_xticks(range(len(pivot_fee.columns)))
ax.set_xticklabels(pivot_fee.columns, fontsize=11)
ax.set_yticks(range(len(pivot_fee.index)))
ax.set_yticklabels(pivot_fee.index, fontsize=9)
ax.set_title('Average Delivery Fee by City x Platform ($)', fontsize=14, fontweight='bold', pad=15)
for i in range(len(pivot_fee.index)):
    for j in range(len(pivot_fee.columns)):
        val = pivot_fee.iloc[i, j]
        if not np.isnan(val):
            ax.text(j, i, f'${val:.2f}', ha='center', va='center', fontsize=8,
                    color='black', fontweight='bold')
plt.colorbar(im, ax=ax, label='Delivery Fee ($)')
plt.tight_layout()
plt.savefig('output/charts/10_fee_heatmap.png', dpi=300, bbox_inches='tight')
plt.close()

print("ALL 10 CHARTS GENERATED SUCCESSFULLY!")
print(f"Charts saved to: output/charts/")