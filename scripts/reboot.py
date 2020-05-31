
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
    
def make_reboot_tab():
    data=pd.read_csv('~/Logging/LogFiles/CSV/reboot.csv')
    # data.reset_index('Time')
    # data.head()
    
    def make_dataset_table():
        table_data=data
    # table_data['Amplitude'] = table_data['Amplitude'].round(2)
        return ColumnDataSource(table_data)

    # function to plot table
    def make_plot_table(src_table):
        table_columns = [TableColumn(field='Version', title='Version'),TableColumn(field='Start_time', title='Session Start'),TableColumn(field='End_time', title='Session End'),TableColumn(field='Session_duration', title='Duration')]
        peak_table = DataTable(source=src_table, columns=table_columns, width=900)
        return peak_table

    src_table = make_dataset_table()	
    # plot initial table
    peak_table=make_plot_table(src_table)


    layout = row(peak_table)
    
    # Make a tab with the layout 
    tab = Panel(child=layout, title = 'Reboot Details')
    return tab
    # show(layout)
    
    
    
