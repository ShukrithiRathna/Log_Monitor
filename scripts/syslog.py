
from bokeh.models import ColumnDataSource, HoverTool, RangeSlider, CheckboxGroup, Select, CategoricalColorMapper, Range1d
from bokeh.plotting import figure
from bokeh.io import show,curdoc
from bokeh.layouts import column, row
from bokeh.models.widgets import Tabs
from bokeh.models.widgets import RadioButtonGroup

from bokeh.models import ColumnDataSource, Panel
from bokeh.models.widgets import TableColumn, DataTable
import pandas as pd
import seaborn as sns
    
def make_syslog_tab():
    error=pd.read_csv('~/Logging/LogFiles/syslog/error.csv')
    system=pd.read_csv('~/Logging/LogFiles/syslog/system.csv')
    log=pd.read_csv('~/Logging/LogFiles/syslog/sys_log.csv')
    # data.reset_index('Time')
    # data.head()
    

    def make_dataset_table(user_list):  
        if user_list ==0:
            table_data=error
        elif user_list == 1:
            table_data=system 
        else:
            table_data=log 
         # table_data['Amplitude'] = table_data['Amplitude'].round(2)
        return ColumnDataSource(table_data)

    # function to plot table
    def make_plot_table(src_table):
        table_columns = [TableColumn(field='Time', title='Timestamp'),TableColumn(field='User', title='User'),TableColumn(field='Key/Agent', title='Key/Agent'),TableColumn(field='Message', title='Message')]
        peak_table = DataTable(source=src_table, columns=table_columns, width=900)
        return peak_table


    def update_table(attr, old, new):
        	users_to_show = user_selection.active

        # get new data for table 
        	new_src_table = make_dataset_table(users_to_show)
        # update data source with new values
        	src_table.data.update(new_src_table.data)

    labels = ['Error Messages','Systemd Messages','All']
    user_selection = RadioButtonGroup(labels=labels, active = 0)
    user_selection.on_change('active', update_table)

    # get initial data for table
    initial_users = user_selection.active
    src_table = make_dataset_table(initial_users)	

    # plot initial table
    peak_table=make_plot_table(src_table)


    layout = row(peak_table,user_selection)
    # Make a tab with the layout 
    # tab = Panel(child=layout, title = 'Peak Summary')
    # show(layout)
    
    # Make a tab with the layout 
    tab = Panel(child=layout, title = 'System Log Details')
    return tab
    # show(layout)
    
    
    
