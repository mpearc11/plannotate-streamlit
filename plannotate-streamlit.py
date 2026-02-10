from plannotate.annotate import annotate
from plannotate.bokeh_plot import get_bokeh
from plannotate.resources import get_seq_record
from bokeh.io import show
from streamlit_bokeh import streamlit_bokeh
import streamlit as st
from Bio.Seq import Seq
from Bio import SeqIO
from Bio import Align
from io import StringIO

aligner = Align.PairwiseAligner()
aligner.mode = 'local'

uploaded_file = st.file_uploader('',type='fasta',key=1)

if uploaded_file is not None:
    st.success('nanopore sequence file uploaded')
else:
    st.info('please upload your nanopore sequence file')

if st.button('annotate sequence'):
    stringio = StringIO(uploaded_file.getvalue().decode('utf-8'))
    record = SeqIO.read(stringio, 'fasta')
    npseq = str(record.seq)
    #st.write(npseq)

    hits = annotate(npseq, is_detailed = True, linear = True)
    st.write(hits)
    p = get_bokeh(hits, linear = True)
    #show(p)
    streamlit_bokeh(p, use_container_width=True)

@st.fragment()
def alignseqs():
    uploaded_file2 = st.file_uploader('',type='fasta',key=2)

    if uploaded_file2 is not None:
        st.success('original target sequence file uploaded')
    else:
        st.info('please upload your target sequence file')

    if st.button('align sequences'):
        stringio = StringIO(uploaded_file2.getvalue().decode('utf-8'))
        record = SeqIO.read(stringio,'fasta')
        ogseq = str(record.seq)

        #create var for qseq of pckA feature
        for idx, i in enumerate(hits['Feature']):
            if i == 'pckA':
                pckAseq = hits.loc[idx,'qseq']
                #st.write(i)
                #st.write(pckAseq)
        alignment = aligner.align(pckAseq,ogseq)
        st.write(alignment[0])
alignseqs()
