from taipy.gui import Gui, notify
import pandas as pd
import webbrowser
import datetime

section_1="""
<center>
<|navbar|lov={[("https://educatcode.github.io/website-Information/", "Home"), ("https://shopee.tw/shop/1080106867", "Shopee"), ("https://github.com/EduCatCode", "GitHub")]}|>
</center>

Data Dashboard with EduCatCode
=========================
<|layout|columns=1 3|
<|
### Let's upload the data set to instantly display the data dashboard!
<br/> 
<center>
<|{content}|file_selector|label=Upload Dataset|on_action=get_data|>
</center>
|>
<|
<center>
<|{logo}|image|height=250px|width=250px|on_action=image_action|>
</center>
|>
|>
"""

section_2 = """
## RealTime Data Visualization
<|{dataset}|chart|mode=lines|x=Time|y[1]=X-axis Angular Velocity|y[2]=Y-axis Angular Velocity|y[3]=Z-axis Angular Velocity|color[1]=blue|color[2]=red|color[3]=green|>
"""

section_3 = """
<|layout|columns= 1 5|
<|
## Custom Date
**Starting Date**\n\n<|{start_date}|date|not with_time|on_change=start_date_onchange|>
<br/><br/>
**Ending Date**\n\n<|{end_date}|date|not with_time|on_change=end_date_onchange|>
<br/>
<br/>
<|button|label=GO|on_action=button_action|>
|>
<|
<center> <h2>Dataset</h2><|{download_data}|file_download|on_action=download|>
</center>
<center>
<|{dataset}|table|page_size=10|height=500px|width=65%|>
</center>
|>
|>
"""


def image_action(state):
    webbrowser.open("https://educatcode.github.io/website-Information/")

def get_data(path: str):
    dataset = pd.read_csv(path)
    dataset["Date"] = pd.to_datetime(dataset["Date"]).dt.date
    return dataset

def start_date_onchange(state, var_name, value):
    state.start_date = value.date()

def end_date_onchange(state, var_name, value):
    state.end_date = value.date()

def filter_by_date_range(dataset, start_date, end_date):
    mask = (dataset['Date'] > start_date) & (dataset['Date'] <= end_date)
    return dataset.loc[mask], mask

def button_action(state):
    state.dataset, mask = filter_by_date_range(dataset, state.start_date, state.end_date)
    notify(state, "info", "Updated date range from {} to {}.".format(state.start_date.strftime("%m/%d/%Y"), state.end_date.strftime("%m/%d/%Y")))
    return mask

def download(state, mask):
    state.dataset.loc[mask].to_csv('Download.csv')
    

global mask 
global content
global download_data

content = None
download_data = 'Download.csv'
logo = "EduCatCode_Logo.png"
dataset = get_data("Train_Label_v2.csv")
start_date = datetime.date(2023, 4, 17)
end_date = datetime.date(2023, 4, 17)


Gui(page=section_1+section_2+section_3).run(dark_mode=False)