from flask import Flask, render_template, request, send_file
from utils import generate_bits, calculate_ber
from modulation import bpsk_modulate, bpsk_demodulate
from report import generate_report
import os
from ofdm import (
    serial_to_parallel,
    ofdm_modulate,
    add_cyclic_prefix,
    remove_cyclic_prefix,
    ofdm_demodulate
)
from channel import awgn
import plotly.graph_objects as go
import plotly.io as pio

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def home():
    num_bits = 16
    subcarriers = 4
    snr = 20
    modulation = "BPSK"

    if request.method == "POST":
        num_bits = int(request.form["bits"])
        subcarriers = int(request.form["subcarriers"])
        snr = int(request.form["snr"])
        modulation = request.form["modulation"]

    # Generate Random Bits
    bits = generate_bits(num_bits)

    # BPSK Modulation
    symbols = bpsk_modulate(bits)

    # Serial to Parallel
    parallel = serial_to_parallel(symbols, subcarriers)

    # OFDM Modulation (IFFT)
    ofdm_signal = ofdm_modulate(parallel)

    # Add Cyclic Prefix
    cp_signal = add_cyclic_prefix(ofdm_signal, 1)

    # AWGN Channel
    received_signal = awgn(cp_signal, snr)

    # Remove Cyclic Prefix
    received_no_cp = remove_cyclic_prefix(received_signal, 1)

    # OFDM Demodulation (FFT)
    received_symbols = ofdm_demodulate(received_no_cp)

    # BPSK Demodulation
    received_bits = bpsk_demodulate(received_symbols.flatten())

    # Keep only original number of bits
    received_bits = received_bits[:len(bits)]

    # BER Calculation
    ber, errors = calculate_ber(bits, received_bits)

    generate_report(
        bits,
        modulation,
        snr,
        ber,
        errors
    )

    # Input Bits Graph
    bits_fig = go.Figure()

    bits_fig.add_trace(
        go.Scatter(
            y=bits,
            mode='lines+markers',
            name='Bits'
        )
    )

    bits_fig.update_layout(
        title="Input Binary Data",
        xaxis_title="Bit Number",
        yaxis_title="Bit Value"
    )

    bits_graph = pio.to_html(bits_fig, full_html=False)

    # BPSK Graph
    bpsk_fig = go.Figure()

    bpsk_fig.add_trace(
        go.Scatter(
            y=symbols,
            mode='lines+markers',
            name='BPSK'
        )
    )

    bpsk_fig.update_layout(
        title="BPSK Symbols",
        xaxis_title="Symbol",
        yaxis_title="Amplitude"
    )

    bpsk_graph = pio.to_html(bpsk_fig, full_html=False)

    # OFDM Signal Graph
    ofdm_fig = go.Figure()

    ofdm_fig.add_trace(
        go.Scatter(
            y=ofdm_signal.flatten().real,
            mode='lines',
            name='OFDM'
        )
    )

    ofdm_fig.update_layout(
        title="OFDM Time Domain Signal",
        xaxis_title="Sample",
        yaxis_title="Amplitude"
    )

    ofdm_graph = pio.to_html(ofdm_fig, full_html=False)

    # Constellation Diagram
    constellation_fig = go.Figure()

    constellation_fig.add_trace(
        go.Scatter(
            x=received_symbols.flatten().real,
            y=received_symbols.flatten().imag,
            mode="markers",
            name="Received Symbols"
        )
    )

    constellation_fig.update_layout(
        title="Constellation Diagram",
        xaxis_title="In-phase",
        yaxis_title="Quadrature"
    )

    constellation_graph = pio.to_html(
        constellation_fig,
        full_html=False
    )

    return render_template(
        "index.html",
        bits=bits,
        symbols=symbols,
        parallel=parallel,
        ofdm_signal=ofdm_signal,
        cp_signal=cp_signal,
        received_signal=received_signal,
        received_no_cp=received_no_cp,
        received_symbols=received_symbols,
        received_bits=received_bits,
        ber=ber,
        errors=errors,
        bits_graph=bits_graph,
        bpsk_graph=bpsk_graph,
        ofdm_graph=ofdm_graph,
        received_graph=constellation_graph,
        constellation_graph=constellation_graph,
        num_bits=num_bits,
        subcarriers=subcarriers,
        snr=snr,
        modulation=modulation
    )

@app.route("/download_report")
def download_report():

    pdf_path = "OFDM_Report.pdf"

    if os.path.exists(pdf_path):
        return send_file(
            pdf_path,
            as_attachment=True
        )

    return "Report not found!"

if __name__ == "__main__":
    app.run(debug=True)