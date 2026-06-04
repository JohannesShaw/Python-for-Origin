import plot
import data_deal as dd
import pyorigin as po

plot.template('time_V_I.csv','1.png')
plot.plot_time_x('time_V_I.csv','2.png','3.png')
plot.plot_two_lines('cleaned.csv','cleaned1.csv','4.png')
plot.plot_two_in_graph('time_V_I.csv','5.png')

# po.clean('raw_data.csv','1.csv')