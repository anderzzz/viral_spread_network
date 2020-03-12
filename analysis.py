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

def growth_analysis_main(growth_files, slice_name='infected', data_names=None,
                         shifter_key=None, shifter_kwargs={}):

    if data_names is None:
        data_names = growth_files
    colors = brewer['PRGn'][max(3, len(growth_files))]

    p = figure(plot_width=650, plot_height=500, toolbar_location='above')
    for k, file in enumerate(growth_files):
        df_file = growth_analysis(file, slice_name)
        if shifter_key is None:
            pass
        elif shifter_key == 'first_above_thrs':
            day_shift = df_file.loc[df_file['N_people_Yes'] > shifter_kwargs['thrs']].iloc[0]['time_coordinate']
            df_file['time_coordinate'] = df_file['time_coordinate'] - day_shift
        elif shifter_key == 'max':
            idx_max = df_file['N_people_Yes'].idxmax()
            day_shift = df_file['time_coordinate'][idx_max]
            df_file['time_coordinate'] = df_file['time_coordinate'] - day_shift

        source = ColumnDataSource(df_file)

        line_dash = 'solid'
        color = colors[k]

        p.line(x='time_coordinate', y='N_people_Yes', source=source, line_width=3,
               color=color, line_dash=line_dash)

    sims_renders = [(x, [g]) for (x, g) in zip(data_names, p.renderers)]
    legend = Legend(items=sims_renders,
                    location="bottom_left")
    p.add_layout(legend, "below")
    p.xaxis.axis_label = 'Days since N > 50'
    p.yaxis.axis_label = 'N infected'

    show(p)

if __name__ == '__main__':

    #cc_1 = [0,1]
    #cc_2 = [0,1,2]
    #inp = []
    #for c_1 in cc_1:
    #    for c_2 in cc_2:
    #        name = 'sim_out_{}_{}_data.csv'.format(c_1, c_2)
    #        inp.append(name)
    #growth_analysis_main(inp, 'infected')

    inp = ['baseline_complete_q_00_data.csv', 'sim_out_4_1_data.csv']
    root = 'impimmun_complete_q_0'
    for kk in range(2, 3):
        inp.append('{}{}_data.csv'.format(root, kk))
    growth_analysis_main(inp, 'infected', None, 'first_above_thrs', shifter_kwargs={'thrs':50})

    #inp = ['baseline_complete_00_data.csv', 'baseline_complete_q_00_data.csv', 'hightransmit_complete_q_00_data.csv',
    #       'hightransmit_complete_00_data.csv']
    #growth_analysis_main(inp, 'infected',
    #                     ['complete graph', 'complete graph w. reactive quarantine policy',
    #                      'complete graph w. double transmitter rate & reactive quarantine policy',
    #                      'complete graph w. double transmitter rate'],
    #                     'first_above_thrs', {'thrs':50})