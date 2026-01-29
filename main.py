import streamlit as st

from rag import process_urls, generate_amswer



st.title("Real Estate Research Tool")

url1=st.sidebar.text_input("Enter URLs 1 (comma separated):",key="url1")
url2=st.sidebar.text_input("Enter URLs 2 (comma separated):",key="url2")
url3=st.sidebar.text_input("Enter URLs 3 (comma separated):",key="url3")

process_url_botton=st.sidebar.button("Process URLs")
if process_url_botton:
    urls=[url for url in (url1, url2, url3) if url != ""]
    if len(urls)==0:
        st.warning("Please enter at least one URL.")
    else:
        for status in process_urls(urls):
            st.info(status)

query=st.text_input("Enter your query:",key="query")
if query:
    try:
       answer, sources=generate_amswer(query)
       st.header("Answer:")
       st.write(answer)

       if sources:
           st.subheader("Sources:")
           for source in sources.split("\n"):
            st.write(source)
    except RuntimeError as e:
        st.error(str(e))
        st.text("Please process URLs first before asking a query.")