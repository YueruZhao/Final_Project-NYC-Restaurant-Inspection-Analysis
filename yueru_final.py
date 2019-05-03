import pandas as pd
import numpy as np
import datetime as dt



data = pd.read_csv('/Users/ritazhao/Desktop/Inspection_Results.csv')

def fix_space(data):
    """
    :param data: food inspection dataframe
    :return:food inspection dataframe with non space column name

    >>> df = pd.DataFrame(np.random.randn(3, 2),columns=[' Column A ', ' Column B '], index=range(3))
    >>> print(fix_space(df).columns.values)
    ['Column_A' 'Column_B']
    """
    data.columns = data.columns.str.strip().str.replace(' ', '_')  # change space to '_' in column name
    return data

data=fix_space(data)
# drop rows with missing grade and borough values
pd1=pd.crosstab(data.BORO, data.GRADE)
pd1['Sum']=pd1['A']+pd1['B']+pd1['C']+pd1['G']+pd1['P']+pd1['Z']
pd1=pd1.drop(index='Missing')
pd1=pd1.drop(columns=['Not Yet Graded'])
pd1

def create_grade_percentage_chart(df):
    """
    :param df: grade count per borough dataframe
    :return: grade percentage dataframe

    >>> df = pd.DataFrame({'A':[1,2,3,4],'B':[2,4,6,8],'Sum':[3,6,9,12]})
    >>> create_grade_percentage_chart(df)
          A%     B%
    0  33.33  66.67
    1  33.33  66.67
    2  33.33  66.67
    3  33.33  66.67
    """
    grade=df.columns.values
    chart=pd.DataFrame()
    for value in grade:
        if value !='Sum':
            chart[value+'%']=round(df[value]/df['Sum']*100,2)
    return chart

create_grade_percentage_chart(pd1)


def create_code_chart(data,top_num):
    """
    :param data: food inspection dataframe
    :param top_num: an integer indicates the top number of most frequent violation code
    :return:top number of most frequent violation code for NYC and different borough dataframe

    >>> df = data
    >>> print(create_code_chart(data, 1).values)
    [['10F' '10F' '10F' '10F' '10F' '10F']]
    >>> print(create_code_chart(data, 2).values)
    [['10F' '10F' '10F' '10F' '10F' '10F']
     ['08A' '08A' '08A' '08A' '08A' '08A']]

    """
    pd3 = pd.crosstab(data.VIOLATION_CODE, data.BORO)
    pd3 = fix_space(pd3)

    pd4 = pd.DataFrame()
    for boro in pd3.columns.values:
        if boro != 'Missing':
            pd4[boro] = pd3.nlargest(top_num, [boro])[boro].index
    pd4['NYC'] = data.VIOLATION_CODE.value_counts(dropna=False).head(top_num).index

    return pd4


create_code_chart(data, 10)


def code_count_chart(data, top_num):
    """
    :param data: food inspection dataframe
    :param top_num: an integer indicates the top number of most frequent violation code
    :return:top number of most frequent violation code count for NYC and different borough dataframe

    >>> df = data
    >>> print(code_count_chart(data, 1).values)
    [[ 4885 13667 21259 12252  1858]]
    >>> print(code_count_chart(data, 2).values)
    [[ 4885 13667 21259 12252  1858]
     [ 4289 10706 16042  8832  1216]]
    """
    pd3 = pd.crosstab(data.VIOLATION_CODE, data.BORO)
    pd3 = fix_space(pd3)
    pd3['All'] = pd3['BRONX'] + pd3['BROOKLYN'] + pd3['MANHATTAN'] + pd3['QUEENS'] + pd3['STATEN_ISLAND']
    pd5 = pd3.sort_values(by='All', ascending=0).head(top_num)

    pd6 = pd.DataFrame()
    for boro in pd5.columns.values:
        if boro != 'Missing' and boro != 'All':
            pd6[boro] = pd5[boro]
    return pd6

data = pd.read_csv('/Users/ritazhao/Desktop/Inspection_Results.csv')
data = fix_space(data)

def grade_trend_chart(data):
    """
    :param data: food inspection dataframe
    :return: grade trend from 2012-2019 dataframe

    >>> data = pd.read_csv('/Users/ritazhao/Desktop/Inspection_Results.csv')
    >>> df=fix_space(data)
    >>> print(grade_trend_chart(df).values[0])
    [100.   0.   0.   0.   0.   0.]

    """
    pd7=pd.DataFrame()
    data['GRADE_DATE'] = pd.to_datetime(data['GRADE_DATE']).dt.year

    pd7['BORO']=data['BORO']
    pd7['GRADE']=data['GRADE']
    pd7['GRADE_YEAR']=data['GRADE_DATE']
    pd7=pd7.dropna()
    pd8=pd7.groupby(['BORO','GRADE','GRADE_YEAR']).size()
    pd8=pd.crosstab(pd7.GRADE_YEAR,pd7.GRADE)
    pd8=pd8.drop(columns=['Not Yet Graded'])
    pd8['Total'] = pd8.sum(axis=1)

    chart=pd.DataFrame()
    for grade in pd8.columns.values:
        if grade !='Total':
            chart[grade+'%']=round(pd8[grade]/pd8['Total']*100,2)
    return chart


pd9 = pd.DataFrame()

pd9['DBA'] = data['DBA']
pd9['GRADE_YEAR'] = data['GRADE_DATE']
pd9['STREET'] = data['STREET']
pd9 = pd9.dropna()
pd10 = pd9.groupby(['DBA', 'STREET']).count()

chain_list = []
non_chain = []
dba_list = pd9['DBA'].unique()
for value in dba_list:
    if pd10.loc[value].count().values[0] > 1:
        chain_list.append(value)
    else:
        non_chain.append(value)


def grade_for_chain(data):
    """
    :param data: food inspection dataframe
    :return: grade count for all chain resturants dataframe

    >>> print(grade_for_chain(data).loc[['10 BELOW ICE CREAM'],['A']].values)
    [[17]]

    """
    pd11 = pd.DataFrame()
    pd11['DBA'] = data['DBA']
    pd11['GRADE'] = data['GRADE']
    pd11 = pd11.dropna()

    pd11 = pd.crosstab(pd11.DBA, pd11.GRADE)
    pd11 = pd11.drop(columns=['Not Yet Graded'])

    pd12 = pd11

    # get a grade table for all chain resturants
    for index1, row in pd12.iterrows():
        if index1 in non_chain:
            pd12 = pd12.drop(index=index1)
    pd12['Total'] = pd12.sum(axis=1)

    return pd12


def grade_for_non_chain(data):
    """
    :param data: food inspection dataframe
    :return: grade count for all non chain resturants dataframe

    >>> print(grade_for_non_chain(data).loc[['ZURILEE'],['A']].values)
    [[7]]

    """
    pd11 = pd.DataFrame()
    pd11['DBA'] = data['DBA']
    pd11['GRADE'] = data['GRADE']
    pd11 = pd11.dropna()

    pd11 = pd.crosstab(pd11.DBA, pd11.GRADE)
    pd11 = pd11.drop(columns=['Not Yet Graded'])

    # get a grade table for all non chain resturants
    for index1, row in pd11.iterrows():
        if index1 in chain_list:
            pd11 = pd11.drop(index1)
    pd11['Total'] = pd11.sum(axis=1)

    return pd11


def chain_non_chain_compare(data):
    """
    :param data: food inspection dataframe
    :return: grade count percentage for non chain and chain resturants dataframe

    >>> print(chain_non_chain_compare(data).loc[['A%'],['Chain']].values)
    [[85.84]]

    """
    pd_non_chain = grade_for_non_chain(data)
    pd_chain = grade_for_chain(data)

    non_chain_grade_list = []
    chain_grade_list = []

    for grade in pd_non_chain.columns.values:
        if grade != 'Total':
            non_chain_grade_list.append(round(pd_non_chain[grade].sum() / pd_non_chain['Total'].sum() * 100, 2))
            chain_grade_list.append(round(pd_chain[grade].sum() / pd_chain['Total'].sum() * 100, 2))

    df_chain_nonchain = pd.DataFrame(np.array([chain_grade_list, non_chain_grade_list]),
                                     columns=['A%', 'B%', 'C%', 'G%', 'P%', 'Z%'])

    plot = df_chain_nonchain.T
    plot.columns = ['Chain', 'Non Chain']

    return plot


