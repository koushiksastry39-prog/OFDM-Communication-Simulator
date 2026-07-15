from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet


def generate_report(bits, modulation, snr, ber, errors):

    doc = SimpleDocTemplate("OFDM_Report.pdf")

    styles = getSampleStyleSheet()

    story = []

    story.append(
        Paragraph(
            "OFDM Communication Simulator Report",
            styles["Title"]
        )
    )

    story.append(
        Paragraph(
            f"Modulation : {modulation}",
            styles["Normal"]
        )
    )

    story.append(
        Paragraph(
            f"SNR : {snr} dB",
            styles["Normal"]
        )
    )

    story.append(
        Paragraph(
            f"BER : {ber:.6f}",
            styles["Normal"]
        )
    )

    story.append(
        Paragraph(
            f"Errors : {errors}",
            styles["Normal"]
        )
    )

    story.append(
        Paragraph(
            f"Total Bits : {len(bits)}",
            styles["Normal"]
        )
    )

    story.append(
        Paragraph(
            "Simulation completed successfully.",
            styles["Normal"]
        )
    )

    doc.build(story)