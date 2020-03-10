import pandas as pd
import networkx as nx
import bokeh
from bokeh.models import ColumnDataSource

def _bool_to_int(row):
    if row['0'] == 'True':
        ret_int = 1
    elif row['0'] == 'False':
        ret_int = 0
    else:
        raise ValueError('Invalid state variable value: {}'.format(row['0']))
    row['0'] = ret_int
    return row

def _true_counter(x):
    return x.loc[x == 'True'].count()

def _false_counter(x):
    return x.loc[x == 'False'].count()

def growth_analysis(growth_file):

    df = pd.read_csv(growth_file)

    df_state = df.loc[df['property'].isin(['contagious','infected','dead','immune','quarantined','revealed'])]
    gg = df_state.groupby(['time_coordinate','property'])['0'].agg([_true_counter, _false_counter])
    df_state_agg = gg.rename(columns={'_true_counter' : 'N_people_Yes', '_false_counter' : 'N_people_No'})


if __name__ == '__main__':

    growth_analysis(growth_file='test_run_1_1_data.csv')