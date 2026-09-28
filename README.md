# Conceptual Architecture of an In-Vehicle Infotainment (IVI) System

**Author:** Prajakta Ghosh | Enrollment No: 12023002002107 | Reg No: 304202300900494 | Dept: ECE | Sec: 4B | Roll: 34

**Task:** Design a conceptual architecture diagram of an IVI system integrating media, navigation and projection features. Annotate component interfaces and data flow.

## Folder structure

```
Teesta/
├── 01_Diagrams/
│   ├── D1_IVI_Conceptual_Architecture.png / .svg / .pdf   main annotated architecture (14 interfaces, colour-coded data flows)
│   ├── data_flows/
│   │   ├── D2_media_data_flow.png
│   │   ├── D3_navigation_data_flow.png
│   │   ├── D4_projection_data_flow.png
│   │   └── D5_projection_session_sequence.png
│   └── views/
│       └── D6_physical_deployment_view.png
├── 02_Documentation/
│   └── IVI_Architecture_Design_Document.docx / .pdf        component descriptions, interface table, data-flow walkthroughs
└── 03_Source/
    ├── generate_diagrams.py                                regenerates every diagram
    └── requirements.txt
```

## Interface summary (as annotated on D1)

| IF | Interface | Protocol / bus |
|---|---|---|
| 1 | Phone ↔ Bluetooth | HFP, A2DP, AVRCP, PBAP, iAP2 / RFCOMM |
| 2 | Phone ↔ Wi-Fi AP | 802.11ac 5 GHz, TCP/IP (wireless CarPlay / Android Auto) |
| 3 | Phone / USB drive ↔ USB | USB 2.0 HS: iAP2 + NCM, AOA, MSC |
| 4 | Cloud ↔ TCU | LTE / 5G: NDS.Live, TPEG, streaming, OTA |
| 5 | Satellites → GNSS | L1 / L5 |
| 6 | Broadcast → tuner | AM / FM + RDS, DAB+ + DLS |
| 7 | I/O modules ↔ SoC | PCIe, UART, USB, I2S / TDM |
| 8 | Apps ↔ services | Android Car API / Binder IPC |
| 9 | Apps ↔ HMI | Surface composition, input events |
| 10 | Head unit ↔ centre display | GMSL2 / FPD-Link + I2C back-channel |
| 11 | IVI VM → cluster | Inter-VM shared memory |
| 12 | Head unit → HUD | GMSL2 video |
| 13 | Audio DSP → amplifier | A2B |
| 14 | Vehicle network ↔ VHAL | CAN-FD, automotive Ethernet (SOME/IP) |
