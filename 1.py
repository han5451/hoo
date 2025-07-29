import streamlit as st
import numpy as np
import altair as alt
import pandas as pd

st.header('st write')

#예제 1

st.write('hello,*world!* :sunglasses:' )

#예제2

st.write(1234)


#예제3

df= pd.DataFrame({
    "첫번째 컬럼":[1,2,3,4],
    "두번째 컬럼":[10,20,30,40]
})

st.write(df)

#예제4

st.write('아래는 DataFrame입니다.', df, '위는 dataframe입니다.')

#예제5

df2= pd.DataFrame(
    np.random.randn(200,3),
    columns=['a','b','c'])
c = alt.Chart(df2).mark_circle().encode(
     x='a', y='b', size='c', color='c', tooltip=['a', 'b', 'c'])
st.write(c)