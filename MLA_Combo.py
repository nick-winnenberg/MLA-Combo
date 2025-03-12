import streamlit as st
import pandas as pd
from fuzzywuzzy import process
from pathlib import Path


## Similar Names
def combine_similar_names(df, column_name):
    unique_names = df[column_name].unique()
    combined_names = {}
    
    for name in unique_names:
        matches = process.extract(name, unique_names, limit=len(unique_names))
        for match in matches:
            if match[1] >= 90:  # Threshold for similarity
                combined_names[match[0]] = name
    
    df[column_name] = df[column_name].apply(lambda x: combined_names[x])
    return df

"Welcome to the MLA Combo Quick Tool. If you're with the company, you know what to do! If you have issues with this, send Nick Winnenberg an email."
"Reminder to GET OWNER PERMISSION before merging their files. This is and should continue to be an opt-in excersize."

files_dict = {}

# Streamlit file uploader
uploaded_files = st.file_uploader("Upload your files", accept_multiple_files=True)

if uploaded_files:
    for uploaded_file in uploaded_files:
        filename = Path(uploaded_file.name).stem  # Get filename without extension
        
        try:
            # Load file based on extension
            if uploaded_file.name.endswith('.csv'):
                files_dict[filename] = pd.read_csv(uploaded_file, encoding='cp1252')
            elif uploaded_file.name.endswith(('.xls', '.xlsx')):
                files_dict[filename] = pd.read_excel(uploaded_file)
            elif uploaded_file.name.endswith('.txt'):
                files_dict[filename] = pd.read_csv(uploaded_file, delimiter='\t', encoding='cp1252')
            elif uploaded_file.name.endswith('.json'):
                files_dict[filename] = pd.read_json(uploaded_file)
            else:
                st.warning(f"Unsupported file type for {uploaded_file.name}")
                continue
                
            st.success(f"Successfully loaded: {filename}")
            
        except Exception as e:
            st.error(f"Error loading {filename}: {str(e)}")

# Display the loaded dataframes
for name, df in files_dict.items():
    st.write(f"### {name}")
    st.dataframe(df)


scrubbed = {}
for key, value in files_dict.items():
    grouped = value.groupby(["Company Name"]).agg(Date_Completed_Count=("Date Completed", "count"))
    grouped = grouped.rename(columns={"Date_Completed_Count": key})
    scrubbed[key] = grouped

dfs = []
for key, value in scrubbed.items():
    dfs.append(value)

df = dfs[0]

for i in dfs[1:]:
    df = pd.merge(df,i,on="Company Name", how="outer")

df = df.reset_index()

print("Processing Combined Names")
st.write("Combining similar names. No big deal. It takes a minute, so go grab a cup of coffee... Seriously, it takes forever. Feel free to open a different tab and browse Creeds Greatest Hits. If your computer catches fire or anything, SOAK Zone is not liable.")
df_combined = combine_similar_names(df, 'Company Name')

print("Processing Finished")
df_combined=df_combined.groupby('Company Name').sum()

df_combined["Offices Contacted"] = df_combined.apply(lambda row: (row > 0).sum(), axis=1)

df_combined = df_combined.sort_values(by=["Offices Contacted"], ascending=False)

df_combined

"Press the download button over the above card and it should pull in everyone. GLHF! If it works, it was Nick Winnenberg. If it's broken, it's Chris's fault."