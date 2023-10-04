import streamlit as st
import pandas as pd

def paginate_data(df, page_number, page_size):
    start_index = (page_number - 1) * page_size
    end_index = min(page_number * page_size, len(df))
    return df[start_index:end_index]

def main():
    # Example DataFrame (replace this with your actual DataFrame)
    data = {'Column1': range(1, 101), 'Column2': range(101, 201)}
    df = pd.DataFrame(data)

    page_size = 10
    page_number = st.session_state.get('page_number', 1)



    col1, col2, col3 = st.columns(3)
    
    if col1.button('Previous') and page_number > 1:
        page_number -= 1
    col2.write(f'Page {page_number}')
    if col3.button('Next') and page_number < (len(df) // page_size) + 1:
        page_number += 1

    st.session_state.page_number = page_number
    paginated_df = paginate_data(df, page_number, page_size)

    st.table(paginated_df)

if __name__ == '__main__':
    main()
