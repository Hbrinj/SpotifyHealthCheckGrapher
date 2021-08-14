
import sys
sys.path.append(".")
from HealthCheckParser import HealthCheckParser
import plotly.express as px
import pandas as pd
import configparser
import distutils.util

class Config:
    def __init__(self):
        config = configparser.ConfigParser()
        config.read('config.ini')

        self.api_key = config['DEFAULT']['api_key']
        self.username = config['DEFAULT']['username']
        self.parent_page_id = config['DEFAULT']['parent_page_id']
        self.plotOutputDir = config['DEFAULT']['plotOutputDir']
        self.confluenceURL = config['DEFAULT']['confluenceURL']
        self.cloud = bool(distutils.util.strtobool(config['DEFAULT']['cloud']))

def plotHealthChecks(healthChecks, plotOutputDir):
    currentScores = healthChecks[0].getScores()
    previousScores = currentScores
    currentTimestamp = healthChecks[0].getTimestamp().strftime("%Y-%m-%d")
    previousTimestamp = currentTimestamp
    if(len(healthChecks) > 1 ):
        previousScores = healthChecks[1].getScores()
        previousTimestamp = healthChecks[1].getTimestamp().strftime("%Y-%m-%d")

    title = f"The health check for {currentTimestamp} as compared to the previous health check on {previousTimestamp}"
    df = pd.DataFrame({'Current Rating': currentScores, 'Previous Rating': previousScores, 'questions': healthChecks[0].getQuestions()})
    fig = px.scatter(df, x='Current Rating', y='Previous Rating', text='questions', color="Current Rating", color_continuous_scale=["red","yellow","green"], title=title)
    fig.update_traces(textposition='top center', marker=dict(size=40), textfont=dict(color="white"))
    fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor='rgb(100,100,100)', zerolinecolor='rgb(150,150,150)', tickfont=dict(color="white"), range=[-1.25,1.25])
    fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor='rgb(100,100,100)', zerolinecolor='rgb(150,150,150)', tickfont=dict(color="white"), range=[-1.25,1.25])
    fig.update_layout(plot_bgcolor="rgb(42,44,43)", paper_bgcolor="rgb(42,44,43)", legend_title_font_color="white", font_color="white", title_font_color="white")
    fig.write_image(f"{plotOutputDir}/{title}.png", width=1920, height=1080)


def main():
    config = Config()
    parser = HealthCheckParser(config)
    healthChecks = parser.getHealthChecks()
    healthChecks.sort(key=lambda x: x.getTimestamp(), reverse=True)
    plotHealthChecks(healthChecks, config.plotOutputDir)


# Get a confluence object that logs into confluence with an API Key
# Get all sub pages under a page
# Use confluence to create a Health Check Table for each page
# have some options like
# generate trajectory Graph
# which then lets us either pick the latest or a previous date to generat it for

if __name__ == "__main__":
    # execute only if run as a script
    main()