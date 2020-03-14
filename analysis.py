'''Analysis of simulation data and creation of graphical output

'''
import pandas as pd
import numpy as np
from bokeh.models import ColumnDataSource, Legend, LinearAxis, SingleIntervalTicker
from bokeh.plotting import figure, show
from bokeh.layouts import column
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

def property_count_progression(growth_file, property_label):
    '''Construct property count progression data

    '''
    def _true_counter(x):
        return x.loc[x == 'True'].count()

    def _false_counter(x):
        return x.loc[x == 'False'].count()

    df = pd.read_csv(growth_file)

    df_state = df.loc[df['property'].isin(['contagious','infected','dead','immune','quarantined','revealed'])]
    gg = df_state.groupby(['time_coordinate','property'])['0'].agg([_true_counter, _false_counter])
    df_state_agg = gg.rename(columns={'_true_counter' : 'N_people_Yes', '_false_counter' : 'N_people_No'}).reset_index()
    df_property_progression = df_state_agg.loc[df_state_agg['property'] == property_label]

    return df_property_progression[['time_coordinate', 'property', 'N_people_Yes']]

def state_analysis_main(state_files, slice_name='infected', data_names=None,
                        shifter_key=None, shifter_kwargs={},
                        group_indeces=None, agg_func=None):
    '''Main analysis function for the state progression data

    '''
    if data_names is None:
        data_names = state_files

    dfs_process = []
    for k, file in enumerate(state_files):
        df_file = property_count_progression(file, slice_name)

        # Align property count progression data
        if shifter_key is None:
            pass

        elif shifter_key == 'first_above_thrs':
            try:
                day_shift = df_file.loc[df_file['N_people_Yes'] > shifter_kwargs['thrs']].iloc[0]['time_coordinate']
            except IndexError:
                raise RuntimeError('The count value {} never exceeded for data in file {}'.format(shifter_kwargs['thrs'], file))

            df_file['time_coordinate'] = df_file['time_coordinate'] - day_shift

        elif shifter_key == 'max':
            idx_max = df_file['N_people_Yes'].idxmax()
            day_shift = df_file['time_coordinate'][idx_max]
            df_file['time_coordinate'] = df_file['time_coordinate'] - day_shift

        else:
            raise ValueError('Unknown shifter_key value: {}'.format(shifter_key))

        dfs_process.append(df_file)

    # Aggregate data groups
    if not group_indeces is None:
        dfs_groups = []
        for group_df in [[dfs_process[k] for k in group] for group in group_indeces]:
            df_new = pd.concat(group_df)
            df_gg = df_new.groupby(['time_coordinate', 'property']).agg(agg_func).reset_index()
            dfs_groups.append(df_gg)
    else:
        dfs_groups = dfs_process

    source_to_plot = [ColumnDataSource(df) for df in dfs_groups]

    colors = brewer['PRGn'][max(4, len(source_to_plot))]
    if len(source_to_plot) == 3:
        colors = [colors[k] for k in [0,1,3]]
    elif len(source_to_plot) == 2:
        colors = [colors[k] for k in [0,3]]

    p = figure(plot_width=650, plot_height=500, toolbar_location='above')
    for k, source in enumerate(source_to_plot):

        p.line(x='time_coordinate', y='N_people_Yes', source=source, line_width=3,
               color=colors[k], line_dash='solid')

    sims_renders = [(x, [g]) for (x, g) in zip(data_names, p.renderers)]
    legend = Legend(items=sims_renders,
                    location="bottom_left")
    p.add_layout(legend, "below")
    p.yaxis.axis_label = 'Number of {}'.format(slice_name)
    if not shifter_key is None:
        p.xaxis.axis_label = 'Days since N > {}'.format(shifter_kwargs['thrs'])
    else:
        p.xaxis.axis_label = 'Days since start'

    #show(p)

def trajectory_analysis_main(traj_files, group_indeces=None, nth_infected=200):
    '''Main analysis function for the trajectory data

    '''
    dfs_transmit_events = []
    dfs_transmit_lags = []
    for k, file in enumerate(traj_files):
        df = pd.read_csv(file)

        # Select the earliest infections
        df_early = df.iloc[:nth_infected]

        # Determine cases infected but never transmitting
        s_receive = set(df_early['receiver'].array)
        s_transmit_all = set(df['transmitter'].array)
        receive_never_transmit = s_receive - s_transmit_all
        df_index = pd.Index(receive_never_transmit, name='receiver')
        df_0_count = pd.DataFrame(data=[0] * len(df_index), index=df_index, columns=['day counter'])
        n_0_count = len(df_0_count)

        # Determine cases infected and transmitting and how many times
        df_transmits = df.loc[df['transmitter'].isin(df_early['receiver'])]
        df_transmits_per_transmitter = df_transmits.groupby(['transmitter']).count()
        df_transmits_count = df_transmits_per_transmitter.groupby('receiver').count()
        df_transmits_count.loc[0] = n_0_count

        # Normalize so empirical frequency of number of infection transmits is obtained
        total_count = df_transmits_count['day counter'].sum()
        df_transmits_count['empirical frequency'] = df_transmits_count['day counter'].div(total_count)
        dfs_transmit_events.append(df_transmits_count.drop(['time since transmitter infected', 'day counter'], axis=1))

        # Compute empirical frequency of lag between infection transmits
        df_transmits_lag = df_transmits.groupby('time since transmitter infected').count()
        total_count = df_transmits_lag['day counter'].sum()
        df_transmits_lag['empirical frequency'] = df_transmits_lag['day counter'].div(total_count)
        dfs_transmit_lags.append(df_transmits_lag.drop(['transmitter', 'receiver', 'day counter'], axis=1))

    # Aggregate data groups
    if not group_indeces is None:
        dfs_groups1 = []
        for group_df in [[dfs_transmit_events[k] for k in group] for group in group_indeces]:
            df_mean_freq1 = pd.concat(group_df).groupby('receiver').mean()
            dfs_groups1.append(df_mean_freq1)

        dfs_groups2 = []
        for group_df in [[dfs_transmit_lags[k] for k in group] for group in group_indeces]:
            df_mean_freq2 = pd.concat(group_df).groupby('time since transmitter infected').mean()
            dfs_groups2.append(df_mean_freq2)

    else:
        raise NotImplementedError('Trajectory analysis without grouper not implemented')

    source1_to_plot = [ColumnDataSource(df) for df in dfs_groups1]
    source2_to_plot = [ColumnDataSource(df) for df in dfs_groups2]

    colors = brewer['PRGn'][max(4, len(source1_to_plot))]
    if len(source1_to_plot) == 3:
        colors = [colors[k] for k in [0,1,3]]
    elif len(source1_to_plot) == 2:
        colors = [colors[k] for k in [0,3]]

    p1 = figure(plot_width=650, plot_height=500, toolbar_location='above')
    for k, source in enumerate(source1_to_plot):

        p1.circle(x='receiver', y='empirical frequency', source=source, line_width=3,
                color=colors[k], line_dash='solid', size=10)
        p1.line(x='receiver', y='empirical frequency', source=source, line_width=1,
                 color=colors[k], line_dash='dotted')

    p1.xaxis.axis_label = 'Number of transmissions to other persons'
    p1.yaxis.axis_label = 'Normalized Frequency'
    p1.xaxis.ticker = SingleIntervalTicker(interval=1)
    p1.xaxis.minor_tick_line_color = None

    p2 = figure(plot_width=650, plot_height=500, toolbar_location='above')
    for k, source in enumerate(source2_to_plot):

        p2.circle(x='time since transmitter infected', y='empirical frequency', source=source, line_width=3,
               color=colors[k], line_dash='solid', size=10)
        p2.line(x='time since transmitter infected', y='empirical frequency', source=source, line_width=1,
                  color=colors[k], line_dash='dotted')

    p2.xaxis.axis_label = 'Days after transmitter was infected'
    p2.yaxis.axis_label = 'Normalized Frequency'
    p2.xaxis.ticker = SingleIntervalTicker(interval=1)
    p2.xaxis.minor_tick_line_color = None

    show(column(p1,p2))

if __name__ == '__main__':

    #cc_1 = [0,1]
    #cc_2 = [0,1,2]
    #inp = []
    #for c_1 in cc_1:
    #    for c_2 in cc_2:
    #        name = 'sim_out_{}_{}_data.csv'.format(c_1, c_2)
    #        inp.append(name)
    #growth_analysis_main(inp, 'infected')

#    state_analysis_main(['simfile_baseline_complete_0_data.csv', 'simfile_baseline_complete_1_data.csv',
#                         'simfile_baseline_complete_2_data.csv', 'simfile_baseline_complete_3_data.csv',
#                         'simfile_baseline_complete_4_data.csv', 'simfile_baseline_completeC50200_0_data.csv',
#                         'simfile_baseline_completeC50200_1_data.csv', 'simfile_baseline_completeC50200_2_data.csv',
#                         'simfile_baseline_completeC50200_3_data.csv', 'simfile_baseline_completeC50200_4_data.csv',
#                         'simfile_baseline_completeC50100_0_data.csv', 'simfile_baseline_completeC50100_1_data.csv',
#                         'simfile_baseline_completeC50100_2_data.csv', 'simfile_baseline_completeC50100_3_data.csv',
#                         'simfile_baseline_completeC50100_4_data.csv', 'simfile_baseline_completeC25200_0_data.csv',
#                         'simfile_baseline_completeC25200_1_data.csv', 'simfile_baseline_completeC25200_2_data.csv',
#                         'simfile_baseline_completeC25200_3_data.csv', 'simfile_baseline_completeC25200_4_data.csv',
#                         'simfile_baseline_completeC25100_0_data.csv',
#                         'simfile_baseline_completeC25100_1_data.csv', 'simfile_baseline_completeC25100_2_data.csv',
#                         'simfile_baseline_completeC25100_3_data.csv', 'simfile_baseline_completeC25100_4_data.csv'],
#    slice_name='infected',
#                        data_names=None,
#                        shifter_key='first_above_thrs',
#                        shifter_kwargs={'thrs':50},
#                        group_indeces=[[0,1,2,3,4],[5,6,7,8,9],[10,11,12,13,14],[15,16,17,18,19],[20,21,22,23,24]],
#                        agg_func=np.mean)

    state_analysis_main(['simfile_baseline_complete_0_data.csv', 'simfile_baseline_complete_1_data.csv',
                         'simfile_baseline_complete_2_data.csv', 'simfile_baseline_complete_3_data.csv',
                         'simfile_baseline_complete_4_data.csv', 'simfile_baseline_completeQ_0_data.csv',
                         'simfile_baseline_completeQ_1_data.csv', 'simfile_baseline_completeQ_2_data.csv',
                         'simfile_baseline_completeQ_3_data.csv', 'simfile_baseline_completeQ_4_data.csv'],
                         slice_name='infected',
                         data_names=None,
                         shifter_key='first_above_thrs',
                         shifter_kwargs={'thrs':50},
                         group_indeces=[[0,1,2,3,4],[5,6,7,8,9]],
                         agg_func=np.mean)

    #state_analysis_main(['ddww_0_0_data.csv', 'ddww_0_1_data.csv', 'ddww_0_2_data.csv',
    #                     'ddww_0_5_data.csv', 'ddww_0_6_data.csv', 'ddww_0_7_data.csv', 'ddww_0_8_data.csv', 'ddww_0_9_data.csv',
    #                     'ddww_0_10_data.csv', 'ddww_0_11_data.csv', 'ddww_0_3_data.csv'],
    #                     'infected', None, 'first_above_thrs', shifter_kwargs={'thrs':50})

    trajectory_analysis_main(['simfile_baseline_complete_0_traj.csv','simfile_baseline_complete_1_traj.csv',
                              'simfile_baseline_complete_2_traj.csv','simfile_baseline_complete_3_traj.csv',
                              'simfile_baseline_complete_4_traj.csv','simfile_baseline_completeC50200_0_traj.csv',
                              'simfile_baseline_completeC50200_1_traj.csv','simfile_baseline_completeC50200_2_traj.csv',
                              'simfile_baseline_completeC50200_3_traj.csv','simfile_baseline_completeC50200_4_traj.csv',
                              'simfile_baseline_completeC50100_0_traj.csv','simfile_baseline_completeC50100_1_traj.csv',
                              'simfile_baseline_completeC50100_2_traj.csv','simfile_baseline_completeC50100_3_traj.csv',
                              'simfile_baseline_completeC50100_4_traj.csv','simfile_baseline_completeC25200_0_traj.csv',
                              'simfile_baseline_completeC25200_1_traj.csv','simfile_baseline_completeC25200_2_traj.csv',
                              'simfile_baseline_completeC25200_3_traj.csv','simfile_baseline_completeC25200_4_traj.csv',
                              'simfile_baseline_completeC25100_0_traj.csv','simfile_baseline_completeC25100_1_traj.csv',
                              'simfile_baseline_completeC25100_2_traj.csv','simfile_baseline_completeC25100_3_traj.csv',
                              'simfile_baseline_completeC25100_4_traj.csv'],
                             group_indeces=[[0, 1, 2, 3, 4], [5, 6, 7, 8, 9], [10, 11, 12, 13, 14],
                                            [15, 16, 17, 18, 19], [20, 21, 22, 23, 24]],
                             nth_infected=200)
#    trajectory_analysis_main(['simfile_baseline_complete_0_traj.csv','simfile_baseline_complete_1_traj.csv',
#                              'simfile_baseline_complete_2_traj.csv','simfile_baseline_complete_3_traj.csv',
#                              'simfile_baseline_complete_4_traj.csv','simfile_baseline_completeQ_0_traj.csv',
#                              'simfile_baseline_completeQ_1_traj.csv','simfile_baseline_completeQ_2_traj.csv',
#                              'simfile_baseline_completeQ_3_traj.csv','simfile_baseline_completeQ_4_traj.csv'],
#                               group_indeces=[[0, 1, 2, 3, 4], [5, 6, 7, 8, 9]])

    #inp = ['baseline_complete_q_00_data.csv', 'sim_out_4_1_data.csv']
    #root = 'impimmun_complete_q_0'
    #for kk in range(2, 3):
    #    inp.append('{}{}_data.csv'.format(root, kk))
    #growth_analysis_main(inp, 'infected', None, 'first_above_thrs', shifter_kwargs={'thrs':50})

    #inp = ['baseline_complete_00_data.csv', 'baseline_complete_q_00_data.csv', 'hightransmit_complete_q_00_data.csv',
    #       'hightransmit_complete_00_data.csv']
    #growth_analysis_main(inp, 'infected',
    #                     ['complete graph', 'complete graph w. reactive quarantine policy',
    #                      'complete graph w. double transmitter rate & reactive quarantine policy',
    #                      'complete graph w. double transmitter rate'],
    #                     'first_above_thrs', {'thrs':50})