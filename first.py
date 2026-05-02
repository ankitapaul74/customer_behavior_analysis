import pandas as pd
df=pd.read_csv('C:\\Users\\Ankita Pual\\Desktop\\customer_shopping_behavior.csv')
df.head()
df.describe(include='all')
df['Review Rating']=df.groupby('Category')['Review Rating'].transform(lambda x: x.fillna(x.median()))
print(df.isnull().sum())
df.columns=df.columns.str.lower()
df.columns=df.columns.str.replace(' ','_')
df=df.rename(columns={'purchase_amount_(usd)':'purchase_amount'})
#create a column age_group
labels=['Young Adult','Adult','Middle Aged','Senior']
df['age_group']=pd.qcut(df['age'] ,q=4, labels=labels)
print(df.columns)
print(df[['age','age_group']].head())
#create column purchase_frequency_days

frequency_mapping={
    'Fortnightly':14,
    'Monthly':30,
    'Quarterly':90,
    'Bi-Weekly':14,
    'Annually':365,
    'Every 3 Months':180,
    'Weekly':7
}

df['purchase_frequency_days']=df['frequency_of_purchases'].map(frequency_mapping)
print(df[['purchase_frequency_days','frequency_of_purchases']].head())
print((df['discount_applied']==df['promo_code_used']).all()) #both columns have same information ,so we can drop one of these two,we are dropping promo_code_used
df=df.drop('promo_code_used',axis=1)

from sqlalchemy import create_engine
engine=create_engine('mysql+mysqlconnector://root:Ap032005#@localhost:3306/da_project')
df.to_sql('customer_shopping_behavior', con=engine, if_exists='replace', index=False)
print('Data uploaded successfully to MySQL database.')