import streamlit as st
import numpy as np
import pandas as pd

st.title("Force fields!")


def harmonic_potential(x, x0, k):
    return np.power(x - x0, 2.0) * k / 2.0 

def morse_potential(x, x0, k, D):
    return D * np.power(1-np.exp(-k*(x -x0)), 2.0)

def torsion_potential(x, tau, k):

    out = np.zeros_like(x)
    for _, (τ, k_) in enumerate(zip(tau, k)):
        out += (1/2) * k_ * (1 + np.cos(τ * x))
    return out

def vdw_potential(x, radius, ε):

    att = -2 * np.power(radius / x, 6.0)
    rep = np.power(radius/ x, 12.0)
    return (att + rep) * ε

def electrostatic_potential(x, q1, q2, D):
    return 332 * q1 * q2 / (D * x)


def guess_function(x):

    hp = harmonic_potential(x, 2.31, 2.5)
    vdw = vdw_potential(x, 1.75,3.3)
    ep = electrostatic_potential(x, 1.0, -0.25, 1.0)
    return hp + vdw + ep


with st.container(border=True):

    col1, col2 = st.columns(2, vertical_alignment='center')
    with col1.container(border=True):
        st.subheader("Harmonic potential")
        st.latex(
            r"""
            f(x)=\frac{k}{2} (x-x_0)^2
            """
        )

        x = np.arange(0.5, 5.0, 0.01)
        k = st.slider("k", min_value=0.0, max_value=10.0, value=5.0)
        x0 = st.slider("x0", min_value=0.1, max_value=3.0, value=1.5)
        hp = harmonic_potential(x, x0, k)

        px_harmonic = pd.DataFrame.from_dict(dict(x=x, harmonic=hp))
    with col1.container(border=True):
        st.subheader("Morse potential")
        st.latex(
            r"""
            f(x)=D \left(1-e^{µ(x-x_0)}\right)^2
            """
        )
        x = np.arange(0.5, 5.0, 0.01)
        D = st.slider("D", min_value=0.0, max_value=20.0, value=10.0)
        µ = st.slider("µ", min_value=0.0, max_value=1.0, value=0.50)
        x0_morse = st.slider("x0 morse", min_value=0.1, max_value=3.0, value=1.5)
        mp = morse_potential(x, x0_morse, µ, D)

    with col2.container(border=True):
        
        px_morse = pd.DataFrame.from_dict(dict(x=x, morse=mp))
        px = pd.merge(px_harmonic, px_morse, on='x')
        # st.write(px)
        st.line_chart(
            data=px, x='x', y=['harmonic', 'morse'], color=['#f24', '#56f'], width=450, height=600, use_container_width=False,
            x_label="Distance", y_label="Energy"
        )
        

with st.container(border=True):

    col1, col2 = st.columns(2, vertical_alignment='center')
    
    with col1.container(border=True):
        st.subheader("Torsions")
        st.latex(
            r"""
            f(x)=\sum_{i} k_i (1 + \cos(\tau \theta))
            """
        )
        x = np.arange(-np.pi, np.pi, 0.01)
        tau1 = st.slider("tau1", min_value=0.0, max_value=5.0, value=1.0, step=1.0)
        tau2 = st.slider("tau2", min_value=0.0, max_value=5.0, value=2.0, step=1.0)
        tau3 = st.slider("tau3", min_value=0.0, max_value=5.0, value=3.0, step=1.0)
        tau4 = st.slider("tau4", min_value=0.0, max_value=5.0, value=4.0, step=1.0)

        k1 = st.slider("k1", min_value=0.0, max_value=1.0, value=0.125)
        k2 = st.slider("k2", min_value=0.0, max_value=1.0, value=0.125)
        k3 = st.slider("k3", min_value=0.0, max_value=1.0, value=0.125)
        k4 = st.slider("k4", min_value=0.0, max_value=1.0, value=0.125)

        tau = [tau1, tau2, tau3, tau4]
        k_ = [k1, k2, k3, k4]
        
        tp = torsion_potential(x, tau, k_)

    with col2.container(border=True):
        
        tp = pd.DataFrame.from_dict(dict(x=x, torsion=tp))
        
        # st.write(px)
        st.line_chart(
            data=tp, x='x', y=['torsion'], color=['#f24'], width=450, height=600, use_container_width=False,
            x_label="Distance", y_label="Energy"
        )

with st.container(border=True):

    col1, col2 = st.columns(2, vertical_alignment='center')
    
    with col1.container(border=True):
        st.subheader("Van Der Waals")
        st.latex(
            r"""
            f(x)=\epsilon \left(\left(\frac{r}{x}\right)^{12} - 2 \left(\frac{r}{x}\right)^{6}\right)
            """
        )
        x = np.arange(0.5, 5.0, 0.01)
        radius = st.slider("radius", min_value=0.0, max_value=5.0, value=1.0)
        epsilon = st.slider("epsilon", min_value=0.0, max_value=5.0, value=2.0)
        
        
        vp = vdw_potential(x, radius, epsilon)
        vp = np.clip(vp, a_max=10.0, a_min=None)

    with col2.container(border=True):
        
        vp = pd.DataFrame.from_dict(dict(x=x, vdw=vp))
        
        # st.write(px)
        st.line_chart(
            data=vp, x='x', y=['vdw'], color=['#f24'], width=450, height=600, use_container_width=False,
            x_label="Distance", y_label="Energy"
        )

    

with st.container(border=True):

    col1, col2 = st.columns(2, vertical_alignment='center')
    
    with col1.container(border=True):
        st.subheader("Electrostatic")
        st.latex(
            r"""
            f(x)=\frac{332}{D} \frac{q_1·q_2}{x}
            """
        )
        x = np.arange(0.5, 5.0, 0.01)
        q1 = st.slider("q1", min_value=-5.0, max_value=5.0, value=1.0)
        q2 = st.slider("q2", min_value=-5.0, max_value=5.0, value=-2.0)
        D = st.slider("D", min_value=0.0, max_value=5.0, value=2.0)
        
        ep = electrostatic_potential(x, q1, q2, D)
        

    with col2.container(border=True):
        
        ep = pd.DataFrame.from_dict(dict(x=x, ep=ep))
        
        # st.write(px)
        st.line_chart(
            data=ep, x='x', y=['ep'], color=['#f24'], width=450, height=600, use_container_width=False,
            x_label="Distance", y_label="Energy"
        )

with st.container(border=True):

    st.header("exercise")

    """
    Use the sliders below to match the following curve
    """

    x = np.arange(0.5, 5.0, 0.01)
    y = guess_function(x)

    x = x[y < 100.0]
    y = y[y < 100.0]

    

    col1, col2 = st.columns(2)
    with col1.container():
        k_test = st.slider("k_test_test", min_value=0.0, max_value=10.0, value=5.0)
        x0_test = st.slider("x0_test_test", min_value=0.1, max_value=3.0, value=1.5)
        radius_test = st.slider("radius_test", min_value=0.0, max_value=5.0, value=1.0)
        epsilon_test = st.slider("epsilon_test", min_value=0.0, max_value=5.0, value=2.0)
        q1_test = st.slider("q1_test", min_value=-5.0, max_value=5.0, value=1.0)
        q2_test = st.slider("q2_test", min_value=-5.0, max_value=5.0, value=-2.0)
        D_test = st.slider("D_test", min_value=0.0, max_value=5.0, value=2.0)

        u = harmonic_potential(x, x0_test, k_test) + vdw_potential(x, radius_test, epsilon_test) + electrostatic_potential(x, q1_test, q2_test, D_test)


    with col2.container():



        u = pd.DataFrame.from_dict(dict(x=x, y=y, model = u))
        st.line_chart(u, x='x', y=['y', 'model'], color=['#f24', '#56f'], width=450, height=600, use_container_width=False,
            x_label="Distance", y_label="Energy")

    
    


        