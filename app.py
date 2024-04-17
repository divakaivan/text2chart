import streamlit as st
import pandas as pd
from langchain.chains import LLMChain
from langchain_core.prompts import PromptTemplate
from langchain_community.llms.huggingface_endpoint import HuggingFaceEndpoint

st.set_option('deprecation.showPyplotGlobalUse', False)

api_key = st.text_input(label = ':hugging_face: HuggingFace API key:', type='password')

def get_response(prompt, api_key):
    llm = HuggingFaceEndpoint(huggingfacehub_api_token=api_key, repo_id='codellama/CodeLlama-34b-Instruct-hf', temperature=0.1, max_new_tokens=512) 
    prompt = PromptTemplate.from_template(prompt)
    llm_chain = LLMChain(llm=llm, prompt=prompt)
    response = llm_chain.predict()
    print(f'{response=}')
    # response = format_response(response)
    return response

def format_response(response):
    csv_line = response.find('read_csv')
    if csv_line:
        return_before_csv_line = response[0:csv_line].rfind('\n')
        if return_before_csv_line == -1:
            response_before = ''
        else:
            response_before = response[0:return_before_csv_line]
        response_after = response[csv_line:]
        return_after_csv_line = response_after.find('\n')
        if return_after_csv_line == -1:
            response_after = ''
        else:
            response_after = response_after[return_after_csv_line:]
        response = response_before+response_after
    return response

def setup_code_query(df, selected_df):
    table_instruct = f"Use a dataframe called {selected_df} from data_file.csv with columns {', '.join(map(str, df.columns))}."
    for col in df.columns:
        if len(df[col].drop_duplicates()) < 20 and df.dtypes[col] == '0':
            table_instruct += f"\nThe column '{col}' has categorical values '{', '.join(map(str, df[col].drop_duplicates()))}'."
        elif df.dtypes[col] == 'int64' or df.dtypes[col] == 'float64':
            table_instruct += f"\nThe column '{col}' is type {df.dtypes[col]} and contains numeric values."
    table_instruct += """
    Label the x and y axes appropriately.
    Add a title.
    Do not use the 'c' argument in the plot function, use 'color' instead and only pass color names like 'green', 'red', 'blue'.
    Using Python version 3.10, create a script using the dataframe {} to graph the following: 
    """.format(selected_df)
    chart_code = f"import pandas as pd\nimport matplotlib.pyplot as plt\nfig, ax = plt.subplots(1, 1, figsize=(10,4))\nax.spines['top'].set_visible(False)\nax.spines['right'].set_visible(False)\ndf={selected_df}.copy()"
    return table_instruct, chart_code


if 'dfs' not in st.session_state:
    dfs = {}
    dfs['fin_statements'] = pd.read_csv('fin_statements.csv') 
    dfs['boston_house_prices'] = pd.read_csv('boston_house_prices.csv')
    st.session_state['dfs'] = dfs
else:
    dfs = st.session_state['dfs']

with st.sidebar:
    uploaded_df = st.file_uploader('Load your CSV file', type='csv')
    upload_btn = st.button('Load CSV')
    if uploaded_df:
        if upload_btn:
            dfs[uploaded_df.name[:-4]] = pd.read_csv(uploaded_df)
    selectbox_df = st.selectbox(
        'Which dataset would you like to use?',
        dfs.keys(),
        index=None,
        placeholder='Select a dataset...'
    )
    selected_df = 'fin_statements'
    if selectbox_df:
        selected_df = selectbox_df
    st.write('Selected:', selected_df)

query = st.text_area(f'What chart would you like to make? (Active dataset: {selected_df})')
run_btn = st.button('Run')

if run_btn and query is not False:
    api_key_entered = True
    if not api_key.startswith('hf_'):
        st.error('Please, check your HuggingFace API key')
        api_key_entered = False

    if api_key_entered:
        plots = st.columns(1)
        table_instruct, chart_code = setup_code_query(dfs[selected_df], 'dfs["'+selected_df+'"]')

        for plot in plots:
            with plot:
                try:
                    prompt = '"""\n' + table_instruct + query + '\n"""\n' + chart_code
                    response = get_response(prompt, api_key)
                    answer = chart_code + response
                    print(f'{answer=}')
                    plt_area = st.empty()
                    plt_area.pyplot(exec(answer))
                except Exception as e:
                    st.error(f'Oops! :sweat: There was an error: {e}')

df_tabs = st.tabs(dfs.keys())
for i, tab in enumerate(df_tabs): 
    with tab:
        df_name = list(dfs.keys())[i]
        st.subheader(df_name)
        st.dataframe(dfs[df_name], hide_index=True)

