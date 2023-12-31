import streamlit as st
from beambending import Beam, DistributedLoadV, PointLoadV
import matplotlib.pyplot as plt
from io import BytesIO

calculate = st.button('Calculate')


def calculator(beam_length, pinned_support, rolling_support, point_loads, distributed_loads):
    beam = Beam(beam_length)
    beam.pinned_support = pinned_support
    beam.rolling_support = rolling_support

    for point_load in point_loads:
        beam.add_loads([PointLoadV(float(point_load['magnitude']), float(point_load['position']))])

    for dist_load in distributed_loads:
        beam.add_loads(
            [DistributedLoadV(float(dist_load['magnitude']), (float(dist_load['start']), float(dist_load['end'])))])

    plt.subplots()
    beam.plot()
    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)

    return buffer


def main():
    st.title("Moment Calculator")

    beam_length = st.number_input("Enter beam length:", min_value=1.0, value=10.0, step=1.0)
    pinned_support = st.number_input("Enter pinned support position:", min_value=0.0, value=0.0, step=1.0)
    rolling_support = st.number_input("Enter rolling support position:", min_value=0.0, value=10.0, step=1.0)

    point_loads = []
    st.subheader("Point Loads")
    num_point_loads = st.number_input("Enter the number of point loads:", min_value=0, value=2)
    for i in range(num_point_loads):
        magnitude = st.number_input(f"Enter magnitude of Point Load {i + 1}:", value=1.0)
        position = st.number_input(f"Enter position of Point Load {i + 1}:", value=1.0)
        point_loads.append({'magnitude': magnitude, 'position': position})

    distributed_loads = []
    st.subheader("Distributed Loads")
    num_distributed_loads = st.number_input("Enter the number of distributed loads:", min_value=0, value=2)
    for i in range(num_distributed_loads):
        magnitude = st.number_input(f"Enter magnitude of Distributed Load {i + 1}:", value=1.0)
        start = st.number_input(f"Enter start position of Distributed Load {i + 1}:", value=1.0)
        end = st.number_input(f"Enter end position of Distributed Load {i + 1}:", value=2.0)
        distributed_loads.append({'magnitude': magnitude, 'start': start, 'end': end})

    if calculate:
        plot_buffer = calculator(beam_length, pinned_support, rolling_support, point_loads, distributed_loads)

        st.image(plot_buffer, use_column_width=True)


if __name__ == "__main__":
    main()
