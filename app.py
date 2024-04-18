import streamlit as st
import pandas as pd
from langchain.chains import LLMChain
from langchain_core.prompts import PromptTemplate
from langchain_community.llms.huggingface_endpoint import HuggingFaceEndpoint

# disable warning from pyplot
st.set_option('deprecation.showPyplotGlobalUse', False)

def get_response(prompt, api_key):
    """Get response from the LLM given a prompt and huggingface api key."""
    llm = HuggingFaceEndpoint(huggingfacehub_api_token=api_key, repo_id='codellama/CodeLlama-34b-Instruct-hf', temperature=0.1) 
    prompt = PromptTemplate.from_template(prompt)
    llm_chain = LLMChain(llm=llm, prompt=prompt)
    response = llm_chain.predict()
    return response


def setup_code_query(df, selected_df):
    """
    Set up the table description and initial code for the prompt.

    Parameters:
    df: pd.DataFrame
    selected_df: str in the format 'dfs["'+selected_df+'"]'

    Returns:
    table_instruct:
        Prompt telling the model to read a df, describing its columns, and instructions on formatting a chart.
    chart_code:
        Prompt containing code for creating a chart.
    """
    table_instruct = f"Use a dataframe called {selected_df} from data_file.csv with columns {', '.join(map(str, df.columns))}."
    for col in df.columns:
        # if col.lower() in ['year', 'date', 'years', 'dates', 'month']:
            # table_instruct += f"The column '{col}' has date values."
        if len(df[col].unique()) < 10 and df.dtypes[col] == '0':
            table_instruct += f"\nThe column '{col}' has categorical values '{', '.join(map(str, df[col].unique()))}'."
        elif df.dtypes[col] == 'int64' or df.dtypes[col] == 'float64':
            table_instruct += f"\nThe column '{col}' is type {df.dtypes[col]} and contains numerical values."
    table_instruct += """
    Add a title.
    Label the x and y axes appropriately.
    Do not use the 'c' argument in the plot function, instead use 'color' and only pass color names like 'green', 'red', 'yellow', 'blue', 'purple'.
    Use Python version 3.10 and generate a script using the dataframe {} to graph the following: 
    """.format(selected_df)
    chart_code = f"import pandas as pd\nimport matplotlib.pyplot as plt\nfig, ax = plt.subplots(1, 1, figsize=(10,4))\nax.spines['right'].set_visible(False)\nax.spines['top'].set_visible(False)\ndf={selected_df}.copy()"
    return table_instruct, chart_code


if 'dfs' not in st.session_state:
    dfs = {}
    dfs['fin_statements'] = pd.read_csv('fin_statements.csv') 
    dfs['boston_house_prices'] = pd.read_csv('boston_house_prices.csv')
    st.session_state['dfs'] = dfs
else:
    dfs = st.session_state['dfs']

with st.sidebar:
    api_key = st.text_input(label = ':hugging_face: HuggingFace API key:', type='password')
    uploaded_df = st.file_uploader('Load your CSV file', type='csv')
    upload_btn = st.button('Load CSV')
    if uploaded_df:
        if upload_btn:
            dfs[uploaded_df.name[:-4]] = pd.read_csv(uploaded_df) # remove .csv
    selectbox_df = st.selectbox(
        label='Which dataset would you like to use?',
        options=dfs.keys(),
        index=None,
        placeholder='Select a dataset...'
    )
    selected_df = 'fin_statements' # set fin_statements as default choice
    if selectbox_df:
        selected_df = selectbox_df
    st.write('Selected:', selected_df)

query = st.text_area(f'What chart would you like to make? (Active dataset: {selected_df})', placeholder='Before you run queries, add your HuggingFace API key in the sidebar')
run_btn = st.button('Run')

if run_btn and query is not False:
    api_key_entered = True
    if not api_key.startswith('hf'): # simple check
        st.error('Please, check your HuggingFace API key')
        api_key_entered = False

    if api_key_entered:
        plot = st.container()
        table_instruct, chart_code = setup_code_query(dfs[selected_df], 'dfs["'+selected_df+'"]')

        with plot:
            try:
                prompt = '"""\n' + table_instruct + query + '\n"""\n' + chart_code
                response = get_response(prompt, api_key)
                answer = chart_code + response
                plt_area = st.empty()
                plt_area.pyplot(exec(answer))
                st.code(response)
            except Exception as e:
                st.error(f'Oops! :sweat: There was an error: {e}')

df_shot_tabs = st.tabs(dfs.keys())
for i, tab in enumerate(df_shot_tabs): 
    with tab:
        df_name = list(dfs.keys())[i]
        st.subheader(df_name)
        st.dataframe(dfs[df_name], hide_index=True)
