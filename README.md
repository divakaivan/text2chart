# This is text2chart - transforming natural language to charts
Hosted webapp: https://text2chart.streamlit.app/ 

You will need a *free* [huggingface API key](https://huggingface.co/docs/api-inference/en/quicktour) to execute queries.

There are 2 default datasets loaded in the webapp:
1. Financial Statements of Major Companies(2009-2023) from [Kaggle](https://www.kaggle.com/datasets/rish59/financial-statements-of-major-companies2009-2023)
2. Boston house price data from [Kaggle](https://www.kaggle.com/datasets/arunjathari/bostonhousepricedata)

## How to use

1. Input your HuggingFace API key
<img width="310" alt="image" src="https://github.com/divakaivan/text2chart/assets/54508530/e832127c-f6f3-4e8d-aa63-605decadd38d">

2. Load your CSV data (optional)
<img width="306" alt="image" src="https://github.com/divakaivan/text2chart/assets/54508530/235e7b73-12dc-4ff5-8a35-c2bde1367c51">

3. Select data to visualize (default is the financial statements data)
<img width="310" alt="image" src="https://github.com/divakaivan/text2chart/assets/54508530/bf273df1-1bba-4474-88cc-a2af97ba247c">

4. Enter a query, run and get your chart
<img width="715" alt="image" src="https://github.com/divakaivan/text2chart/assets/54508530/1767fbbd-3a37-4c39-8548-350f4c3b4173">
   
   
## Experiment with different chart types

- Vertical Bar Charts:
`Display the revenue, net income, and EPS of each top company for the latest fiscal year in separate vertical bar charts for easy comparison.`
![image](https://github.com/divakaivan/text2chart/assets/54508530/d4752dd6-81be-4cf8-aec4-05b4cbf474a2)

- Horizontal Bar Charts (Metric Comparison):
`Compare the revenue, net income, and EPS of the top companies for the latest fiscal year using horizontal bar charts.`
![image](https://github.com/divakaivan/text2chart/assets/54508530/b6238cc7-7d57-428e-98b7-ce2891809338)

- Line Charts (Trend Analysis):
`Plot the revenue trend over the past five years for the top companies to visualize growth or decline over time.`
![image](https://github.com/divakaivan/text2chart/assets/54508530/ba5890f5-37cf-480f-8cba-f6a4f8248f5f)
`Show me AAPL's revenue trend over the Years`
![image](https://github.com/divakaivan/text2chart/assets/54508530/cf9a825a-58ff-42c1-88c9-ee65902727e7)

- Pie Charts (Composition Analysis):
`Group by companies in the IT category and create a pie chart showing a breakdown of each company's market share.`
![image](https://github.com/divakaivan/text2chart/assets/54508530/f5c87a83-0fd1-4407-98a5-8b79b07e8523)

- Scatter Plots (Correlation Analysis):
`Explore the correlation between revenue growth and net income growth over the past five years for each top company using scatter plots.`
![image](https://github.com/divakaivan/text2chart/assets/54508530/60f36fa0-190e-4fc9-9fa8-0fce2ae4a455)

- Box Plots (Distribution Analysis):
`Generate a box plot for each top company to show the distribution of net income in the latest year.`
![image](https://github.com/divakaivan/text2chart/assets/54508530/12b23c6f-574b-427a-8d66-80c27a888dcd)

#### Known limitations
- right now it can read columns as either categorial (if dtype is not int/float) or numerical (int/float), so it might have problems with dates (as seen in the Line chart example above)
- might not be able to make a more complicated chart (or may need a more specific query)
