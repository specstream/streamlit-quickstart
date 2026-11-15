import requests
import streamlit as st

API = "https://api.specstream.ai/v1"

st.set_page_config(page_title="SpecStream live web search")
st.title("SpecStream live web search")
st.markdown(
    "[SpecStream](https://specstream.ai) is the live web data engine. "
    "This small app asks the Search API a question and reads the top result with the Extract API. "
    "The Search API scores 97.9 F-score on all 1,000 SimpleQA Verified questions "
    "([benchmarks](https://specstream.ai/benchmarks)). "
    "For complete tables with a source on every value, use Deep Search at [specstream.ai](https://specstream.ai)."
)

key = st.text_input("Your SpecStream API key", type="password", help="New accounts start with $10 of credit at specstream.ai")
question = st.text_input("Question", "When was the Python programming language first released?")

if st.button("Search") and key and question:
    headers = {"Authorization": f"Bearer {key}"}
    search = requests.get(f"{API}/web-search", params={"q": question}, headers=headers, timeout=60)
    if not search.ok:
        st.error(f"Search failed: {search.status_code} {search.text[:300]}")
        st.stop()
    found = search.json()["data"]
    if found.get("answer"):
        st.subheader("Answer")
        st.write(found["answer"]["value"])
        st.caption(f"Read from {found['answer']['page']}")
    st.subheader("Sources")
    for source in found.get("sources", []):
        st.markdown(f"- [{source['title']}]({source['url']})")
    if found.get("sources"):
        top = found["sources"][0]["url"]
        extract = requests.post(f"{API}/extract", json={"urls": [top], "format": "markdown"}, headers=headers, timeout=60)
        if extract.ok:
            page = extract.json()["data"]["results"][0]
            st.subheader("Top result, read with the Extract API")
            st.markdown((page.get("text") or "")[:3000])

st.divider()
st.markdown("Docs: [specstream.ai/docs](https://specstream.ai/docs). Prices: Search API $5 per 1,000 searches, Extract API $0.80 per 1,000 pages.")
