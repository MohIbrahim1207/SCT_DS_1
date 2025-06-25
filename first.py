# WORLD BANK POPULATION DATA ANALYSIS - COMPLETE SCRIPT
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# ======================
# 1. DATA LOADING & CLEANING
# ======================
def load_data():
    # Load main population data (skip metadata rows)
    df = pd.read_csv('API_SP.POP.TOTL_DS2_en_csv_v2_2590.csv', skiprows=4)
    
    # Load metadata
    country_meta = pd.read_csv('Metadata_Country_API_SP.POP.TOTL_DS2_en_csv_v2_2590.csv')
    indicator_meta = pd.read_csv('Metadata_Indicator_API_SP.POP.TOTL_DS2_en_csv_v2_2590.csv')
    
    # Clean main dataframe
    df = df.drop(['Country Code', 'Indicator Name', 'Indicator Code', 'Unnamed: 66'], axis=1, errors='ignore')
    df = df.rename(columns={'Country Name': 'Country'})
    
    # Convert to long format
    years = [str(year) for year in range(1960, 2024)]
    df_melted = pd.melt(df, id_vars=['Country'], value_vars=years, 
                       var_name='Year', value_name='Population')
    df_melted['Year'] = df_melted['Year'].astype(int)
    
    return df_melted, country_meta, indicator_meta


# 2. BASIC ANALYSIS

def basic_analysis(df):
    print("\n=== BASIC STATISTICS ===")
    latest_year = df['Year'].max()
    
    # Latest year stats
    latest_data = df[df['Year'] == latest_year]
    print(f"\nLatest year available: {latest_year}")
    print(f"Total countries: {len(latest_data)}")
    print(f"Global population: {latest_data['Population'].sum()/1e9:.2f} billion")
    
    # Top 10 countries
    top10 = latest_data.nlargest(10, 'Population')
    print("\nTop 10 Countries:")
    print(top10[['Country', 'Population']].to_string(index=False))
    
    return latest_year


# 3. VISUALIZATIONS

def create_visualizations(df, latest_year):
    plt.style.use('seaborn-v0_8') 
    
    # Visualization 1: Population Trends
    plt.figure(figsize=(12, 6))
    for country in ['India', 'China', 'United States', 'Nigeria']:
     data = df[df['Country'] == country]
    plt.plot(data['Year'], data['Population']/1e6, label=country, linewidth=2)
    
    plt.title('Population Trends (1960-2023)', fontsize=14)
    plt.xlabel('Year', fontsize=12)
    plt.ylabel('Population (Millions)', fontsize=12)
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig('population_trends.png')
    plt.show()
    
    # Visualization 2: Latest Year Comparison
    plt.figure(figsize=(10, 8))
    latest_data = df[df['Year'] == latest_year].nlargest(15, 'Population')
    sns.barplot(x='Population', y='Country', data=latest_data, palette='viridis')
    plt.title(f'Top 15 Countries by Population ({latest_year})', fontsize=14)
    plt.xlabel('Population', fontsize=12)
    plt.ylabel('')
    plt.tight_layout()
    plt.savefig('top_countries.png')
    plt.show()
    
    # Visualization 3: Growth Rate Analysis
    df['Growth Rate'] = df.groupby('Country')['Population'].pct_change() * 100
    plt.figure(figsize=(12, 6))
    for country in ['India', 'China']:
        data = df[df['Country'] == country]
        plt.plot(data['Year'], data['Growth Rate'], label=country, alpha=0.8)
    
    plt.title('Annual Population Growth Rate (%)', fontsize=14)
    plt.xlabel('Year', fontsize=12)
    plt.ylabel('Growth Rate %', fontsize=12)
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig('growth_rates.png')
    plt.show()

# ======================
# 4. MAIN EXECUTION
# ======================
if __name__ == '__main__':
    print("WORLD BANK POPULATION DATA ANALYSIS")
    print("==================================")
    
    # Load data
    df, country_meta, indicator_meta = load_data()
    
    # Basic analysis
    latest_year = basic_analysis(df)
    
    # Create visualizations
    create_visualizations(df, latest_year)
    
    # Save processed data
    df.to_csv('processed_population_data.csv', index=False)
    print("\nAnalysis complete! Results saved to:")
    print("- population_trends.png")
    print("- top_countries.png")
    print("- growth_rates.png")
    print("- processed_population_data.csv")