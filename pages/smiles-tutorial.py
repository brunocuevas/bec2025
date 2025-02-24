import streamlit as st
import rdkit.Chem as chem
from rdkit.Chem import Draw
import time

st.title("Learning SMILES representation")


if 'targets' not in st.session_state:
    st.session_state['targets'] = [
        ("Butane", "CCCC"),
        ("Acetate", "CC(=O)O"),
        ("Acetamide", "CC(=O)N"),
        ("Thioacetamide", "CC(=S)N"),
        ("Malate", "C(C(C(=O)O)O)C(=O)O"),
        ("Cyclo Hexane", "C1CCCCC1"),
        ("Benzene", "c1ccccc1"),
        ("Napthalene", "C1=CC=C2C=CC=CC2=C1"),
        ("Caffeine", "CN1C=NC2=C1C(=O)N(C(=O)N2C)C"),
        ("Indole-3-acetic acid", "C1=CC=C2C(=C1)C(=CN2)CC(=O)O"),
        ("Capsaicin", "CC(C)C=CCCCCC(=O)NCC1=CC(=C(C=C1)O)OC")
    ]

if 'current_molecule' not in st.session_state:
    st.session_state['current_molecule'] = st.session_state['targets'].pop(0)


u = st.session_state['current_molecule']
mol = chem.MolFromSmiles(u[1])
left, right = st.columns(2)
left.image(Draw.MolToImage(mol))
smiles = st.text_area("write your smiles")
if st.button("submit"):
    newmol = chem.MolFromSmiles(smiles)
    right.image(Draw.MolToImage(newmol))
    if chem.MolToInchiKey(newmol) == chem.MolToInchiKey(mol):
        # 
        # st.write(targets)
        
        st.balloons()
        time.sleep(3)
        try:
            st.session_state["current_molecule"] = st.session_state['targets'].pop(0)
            st.rerun()
        except IndexError:
            st.info("congrats!!")
            
if st.button("next"):
    time.sleep(3)
    try:
        st.session_state["current_molecule"] = st.session_state['targets'].pop(0)
        st.rerun()
    except IndexError:
        st.info("congrats!!")