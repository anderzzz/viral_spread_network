import pandas as pd
from bokeh.models import ColumnDataSource, Legend
from bokeh.plotting import figure, show
from bokeh.palettes import brewer

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

def growth_analysis(growth_file, property_label):

    df = pd.read_csv(growth_file)

    df_state = df.loc[df['property'].isin(['contagious','infected','dead','immune','quarantined','revealed'])]
    gg = df_state.groupby(['time_coordinate','property'])['0'].agg([_true_counter, _false_counter])
    df_state_agg = gg.rename(columns={'_true_counter' : 'N_people_Yes', '_false_counter' : 'N_people_No'}).reset_index()
    df_infected = df_state_agg.loc[df_state_agg['property'] == property_label]

    return df_infected[['time_coordinate', 'property', 'N_people_Yes']]

def growth_analysis_main(growth_files):

    p = figure(plot_width=650, plot_height=500, toolbar_location='above')
    colors = brewer['Set3'][len(growth_files)]
    for file, color in zip(growth_files, colors):
        df_file = growth_analysis(file, 'infected')

        source = ColumnDataSource(df_file)
        p.line(x='time_coordinate', y='N_people_Yes', source=source, line_width=3, color=color)

    sims_renders = [(x, [g]) for (x, g) in zip(growth_files, p.renderers)]
    legend = Legend(items=sims_renders,
                    location="center",
                    title="Number Infected", title_text_font_style="bold")
    p.add_layout(legend, "right")

    show(p)
    raise RuntimeError

if __name__ == '__main__':

    sim_out_files = ['test_run_1_1_data.csv', 'test_run_1_2_data.csv', 'test_run_1_3_data.csv',
                     'test_run_2_1_data.csv', 'test_run_2_2_data.csv', 'test_run_2_3_data.csv',
                     'test_run_3_1_data.csv', 'test_run_3_2_data.csv', 'test_run_3_3_data.csv',
                     'test_run_4_1_data.csv', 'test_run_4_2_data.csv', 'test_run_4_3_data.csv']
    growth_analysis_main(sim_out_files)
