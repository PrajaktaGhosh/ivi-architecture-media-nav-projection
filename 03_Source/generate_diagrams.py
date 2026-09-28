import os
import sys
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Circle, Rectangle
from matplotlib.lines import Line2D

plt.rcParams["font.family"] = "DejaVu Sans"
plt.rcParams["svg.fonttype"] = "none"

K = {
    "ink": "#1f2937", "mute": "#6b7280", "line": "#374151",
    "med": "#2563eb", "nav": "#16a34a", "prj": "#9333ea", "ctl": "#64748b", "vid": "#0f766e", "aud": "#d97706",
    "ext": "#f1f5f9", "ext_e": "#475569",
    "con": "#e0f2fe", "con_e": "#0369a1",
    "hu": "#f8fafc", "hu_e": "#1e3a5f",
    "hmi": "#fce7f3", "hmi_e": "#be185d",
    "app": "#ede9fe", "app_e": "#6d28d9",
    "mw": "#ecfdf5", "mw_e": "#047857",
    "os": "#fef3c7", "os_e": "#b45309",
    "hw": "#e2e8f0", "hw_e": "#334155",
    "out": "#fee2e2", "out_e": "#b91c1c",
    "veh": "#f5f5f4", "veh_e": "#57534e",
}


def cv(w, h):
    f, a = plt.subplots(figsize=(w, h))
    a.set_xlim(0, w)
    a.set_ylim(0, h)
    a.set_aspect("equal")
    a.axis("off")
    return f, a


def bx(a, x, y, w, h, t="", fc="#fff", ec="#333", fs=8.5, b=False, r=0.08, lw=1.2, tc=None, ls="-", va="center", z=2, it=False):
    a.add_patch(FancyBboxPatch((x, y), w, h, boxstyle=f"round,pad=0,rounding_size={r}", fc=fc, ec=ec, lw=lw, ls=ls, zorder=z))
    if t:
        ty = y + h / 2 if va == "center" else y + h - 0.14
        a.text(x + w / 2, ty, t, ha="center", va=va, fontsize=fs, color=tc or K["ink"], fontweight="bold" if b else "normal",
               style="italic" if it else "normal", zorder=z + 1, linespacing=1.25)


def ar(a, p, q, c=None, lw=1.5, ls="-", both=False, rad=0.0, ms=11, z=5):
    a.add_patch(FancyArrowPatch(p, q, arrowstyle="<|-|>" if both else "-|>", mutation_scale=ms, color=c or K["line"], lw=lw, ls=ls,
                                connectionstyle=f"arc3,rad={rad}", zorder=z, shrinkA=0, shrinkB=0))


def ln(a, xs, ys, c=None, lw=1.5, ls="-", z=5):
    a.add_line(Line2D(xs, ys, color=c or K["line"], lw=lw, ls=ls, zorder=z))


def tx(a, x, y, t, fs=8, c=None, b=False, ha="center", va="center", rot=0, bg=None, it=False, z=7):
    kw = {"bbox": dict(boxstyle="round,pad=0.18", fc=bg, ec="none")} if bg else {}
    a.text(x, y, t, fontsize=fs, color=c or K["mute"], ha=ha, va=va, rotation=rot, fontweight="bold" if b else "normal",
           style="italic" if it else "normal", zorder=z, linespacing=1.2, **kw)


def tag(a, x, y, n, c):
    a.add_patch(Circle((x, y), 0.2, fc="white", ec=c, lw=1.6, zorder=9))
    a.text(x, y, str(n), fontsize=7.5, color=c, ha="center", va="center", fontweight="bold", zorder=10)


def sv(f, d, n):
    for e in ("png", "svg", "pdf"):
        if e == "png" or n.startswith("D1_"):
            f.savefig(os.path.join(d, f"{n}.{e}"), dpi=220 if e == "png" else None, bbox_inches="tight", pad_inches=0.12, facecolor="white")
    plt.close(f)


def main_diagram(d):
    W, H = 22.0, 19.4
    f, a = cv(W, H)
    tx(a, W / 2, H - 0.35, "Conceptual Architecture of an In-Vehicle Infotainment (IVI) System", fs=17, c=K["ink"], b=True)
    tx(a, W / 2, H - 0.85, "Integrated media, navigation and smartphone projection (Apple CarPlay / Android Auto) on a cockpit domain controller", fs=10.5, c=K["mute"], it=True)

    y0, y1 = 4.95, 17.7
    bx(a, 0.2, y0, 3.0, y1 - y0, "", fc=K["ext"], ec=K["ext_e"], lw=1.5, r=0.15)
    tx(a, 1.7, y1 - 0.3, "EXTERNAL\nSOURCES", fs=10, c=K["ext_e"], b=True)
    E = {"ph": (15.0, 1.9, "Smartphone\niPhone / Android"), "usb": (13.1, 1.0, "USB storage\n(media files)"),
         "cl": (11.0, 1.4, "Cloud services\nmaps, traffic,\nstreaming, OTA"), "gn": (9.1, 1.0, "GNSS satellites\n(GPS, NavIC,\nGalileo)"),
         "bc": (7.5, 1.0, "Broadcast\nAM / FM / DAB+"), "us": (5.6, 1.2, "Driver &\npassengers")}
    for k, (y, h, t) in E.items():
        bx(a, 0.4, y, 2.6, h, t, fc="white", ec=K["ext_e"], fs=8.5)

    bx(a, 3.7, y0, 3.2, y1 - y0, "", fc=K["con"], ec=K["con_e"], lw=1.5, r=0.15)
    tx(a, 5.3, y1 - 0.3, "CONNECTIVITY &\nI/O MODULES", fs=10, c=K["con_e"], b=True)
    Cn = {"bt": (15.9, "Bluetooth 5.x\n(HFP, A2DP, AVRCP, PBAP)"), "wf": (14.85, "Wi-Fi access point\n802.11ac/ax, 5 GHz"),
          "ub": (13.8, "USB host / hub\n(Type-C, power delivery)"), "tc": (11.7, "Telematics unit\n4G / 5G modem, eSIM"),
          "gr": (9.55, "GNSS receiver\n+ 6-axis IMU (DR)"), "tu": (7.75, "AM / FM / DAB+\ntuner"),
          "mi": (6.7, "Microphone array"), "in": (5.55, "Touch panel, rotary\nknob, hard keys")}
    for k, (y, t) in Cn.items():
        bx(a, 3.9, y, 2.8, 0.88 if k not in ("mi",) else 0.7, t, fc="white", ec=K["con_e"], fs=8)

    ar(a, (3.0, 16.3), (3.9, 16.35), c=K["prj"], both=True); tag(a, 3.45, 16.62, 1, K["prj"])
    ar(a, (3.0, 15.6), (3.9, 15.3), c=K["prj"], both=True); tag(a, 3.45, 15.72, 2, K["prj"])
    ar(a, (3.0, 15.15), (3.9, 14.2), c=K["prj"], both=True); tag(a, 3.3, 14.72, 3, K["prj"])
    ar(a, (3.0, 13.6), (3.9, 14.05), c=K["med"]);
    ar(a, (3.0, 11.7), (3.9, 12.1), c=K["nav"], both=True); tag(a, 3.45, 12.2, 4, K["nav"])
    ar(a, (3.0, 9.6), (3.9, 9.95), c=K["nav"]); tag(a, 3.45, 10.1, 5, K["nav"])
    ar(a, (3.0, 8.0), (3.9, 8.15), c=K["med"]); tag(a, 3.45, 8.35, 6, K["med"])
    ar(a, (3.0, 6.3), (3.9, 7.0), c=K["ctl"]); ar(a, (3.0, 6.0), (3.9, 6.0), c=K["ctl"])

    ox_ = 18.5
    hx, hw = 7.6, 10.4
    L = hx + 0.55
    iw = hw - 0.8
    bx(a, hx, y0, hw, y1 - y0, "", fc=K["hu"], ec=K["hu_e"], lw=2.2, r=0.2)
    tx(a, hx + hw / 2, y1 - 0.3, "IVI HEAD UNIT  /  COCKPIT DOMAIN CONTROLLER", fs=11, c=K["hu_e"], b=True)
    for yy, t, c in [(16.42, "HMI", K["hmi_e"]), (14.75, "APPS", K["app_e"]), (11.9, "SERVICES", K["mw_e"]), (9.2, "OS / VM", K["os_e"]), (6.15, "HARDWARE", K["hw_e"])]:
        tx(a, hx + 0.28, yy, t, fs=7.5, c=c, b=True, rot=90)
    bx(a, L, 15.9, iw, 1.05, "HMI FRAMEWORK & WINDOW MANAGER\nhome screen, split-screen layout, notifications, day / night theme, input focus, surface composition",
       fc=K["hmi"], ec=K["hmi_e"], fs=8.5)
    aw = (iw - 0.4) / 3
    apps = [("MEDIA APP\nsources, browse, now playing,\nqueue, radio presets", K["med"]),
            ("NAVIGATION APP\ndestination search, map view,\nroute options, guidance UI", K["nav"]),
            ("PROJECTION RECEIVER\nApple CarPlay / Android Auto\nfull-screen or split view", K["prj"])]
    for i, (t, c) in enumerate(apps):
        bx(a, L + i * (aw + 0.2), 14.05, aw, 1.4, t, fc=K["app"], ec=c, fs=8.3, lw=1.6)
    sw = (iw - 0.6) / 4
    R1, R2, RH = 12.15, 10.35, 1.25
    mw = [[("Media framework\ndecode, demux, library,\nmetadata (ID3, RDS)", K["med"]), ("Positioning engine\nGNSS + dead reckoning\n+ map matching", K["nav"]),
           ("Map & routing engine\nNDS map DB, route calc,\nguidance, traffic", K["nav"]), ("Projection session mgr\niAP2 / AAP, MFi auth,\nvideo decode, channels", K["prj"])],
          [("Audio manager\nfocus, routing, ducking,\nmixing, volume", K["aud"]), ("Speech services\nTTS, ASR, wake-word,\necho cancellation", K["aud"]),
           ("Connectivity manager\nBT profiles, Wi-Fi,\nTCU data, phone link", K["con_e"]), ("Vehicle data service\n(Vehicle HAL) speed, gear,\nlights, keys, camera", K["ctl"])]]
    for r, row in enumerate(mw):
        for i, (t, c) in enumerate(row):
            bx(a, L + i * (sw + 0.2), (R1, R2)[r], sw, RH, t, fc=K["mw"], ec=c, fs=7.8, lw=1.4)
    m = [L + i * (sw + 0.2) + sw / 2 for i in range(4)]
    ml = [L + i * (sw + 0.2) for i in range(4)]
    ob = 7.4
    bx(a, L, 9.05, ob, 0.9, "Android Automotive OS  (IVI virtual machine)\nLinux kernel, audio / camera / display HALs, Car services, SELinux", fc=K["os"], ec=K["os_e"], fs=8.0)
    bx(a, L + ob + 0.2, 9.05, iw - ob - 0.2, 0.9, "RTOS / QNX VM\ncluster & HUD\nrendering (ASIL-B)", fc=K["os"], ec=K["os_e"], fs=7.3)
    bx(a, L, 8.4, iw, 0.5, "Type-1 hypervisor: CPU / memory partitioning, shared GPU & display controller, inter-VM shared memory", fc="#fde68a", ec=K["os_e"], fs=8)
    tx(a, hx + hw / 2, 7.75, "Drivers expose Wi-Fi (PCIe), Bluetooth (UART), USB, GNSS (UART), tuner and microphones (I2S / TDM) to the IVI VM", fs=7.3, c=K["hw_e"], it=True)
    hwb = ["Audio DSP\nEQ, mixing,\nAEC, zones", "Multi-core SoC\nCPU / GPU /\nNPU", "HW video codec\nH.264 / H.265", "Security\nHSM + MFi\nauth chip", "Vehicle MCU\n(AUTOSAR)\nCAN-FD / Eth", "Storage (UFS)\nmaps, media,\napps"]
    hw_w = (iw - 1.0) / 6
    hxs = [L + i * (hw_w + 0.2) for i in range(6)]
    for i, t in enumerate(hwb):
        bx(a, hxs[i], 5.55, hw_w, 1.2, t, fc=K["hw"], ec=K["hw_e"], fs=7.5)
    hmx = hxs[4] + hw_w / 2
    vxl = L + ob + 0.1
    ar(a, (vxl, 6.75), (vxl, R2), c=K["ctl"], lw=1.5, both=True)
    tx(a, vxl, 7.3, "VHAL", fs=7, c=K["ctl"], b=True, bg="white")
    ar(a, (hmx, 3.75 + 0.85), (hmx, 5.55), c=K["ctl"], lw=1.8, both=True); tag(a, hmx - 0.38, 4.8, 14, K["ctl"])
    dxx = hxs[0] + hw_w / 2
    ar(a, (dxx, R2), (dxx, 6.75), c=K["aud"], lw=1.8)
    tx(a, dxx, 7.3, "PCM", fs=7, c=K["aud"], b=True, bg="white")
    ln(a, [dxx, dxx, 18.2], [5.55, 5.2, 5.2], c=K["aud"], lw=2.2)
    ar(a, (18.2, 5.2), (ox_ + 0.2, 6.6), c=K["aud"], lw=2.2)
    tag(a, 17.2, 5.2, 13, K["aud"])
    for cc, mm, c in [(L + aw / 2, m[0], K["med"]), (L + aw + 0.2 + aw / 2 - 0.55, m[1], K["nav"]), (L + aw + 0.2 + aw / 2 + 0.55, m[2], K["nav"]), (L + 2 * (aw + 0.2) + aw / 2, m[3], K["prj"])]:
        ar(a, (cc, 14.05), (mm, R1 + RH), c=c, lw=1.5, both=True)
    tag(a, (L + aw / 2 + m[0]) / 2 + 0.32, 13.72, 8, K["app_e"])
    tx(a, L + iw, 13.72, "Android Car API / Binder IPC", fs=7.3, c=K["app_e"], ha="right", it=True, bg=K["hu"])
    for i in range(3):
        cc = L + i * (aw + 0.2) + aw / 2
        ar(a, (cc, 15.45), (cc, 15.9), c=K["hmi_e"], lw=1.3, both=True)
    tag(a, L + aw / 2 + 0.35, 15.68, 9, K["hmi_e"])
    ar(a, (ml[1] + sw, R1 + RH / 2), (ml[2], R1 + RH / 2), c=K["nav"], lw=1.6)
    ar(a, (m[0] - 0.5, R1), (m[0] - 0.5, R2 + RH), c=K["med"], lw=1.6)
    ln(a, [m[3], m[3], m[0] + 0.45], [R1, 11.875, 11.875], c=K["prj"], lw=1.5)
    ar(a, (m[0] + 0.45, 11.875), (m[0] + 0.45, R2 + RH), c=K["prj"], lw=1.5)
    tx(a, (m[1] + m[2]) / 2 + 0.6, 11.875, "projection audio: media, nav prompts, voice", fs=6.8, c=K["prj"], bg=K["hu"])
    ar(a, (ml[1], R2 + RH / 2), (ml[0] + sw, R2 + RH / 2), c=K["aud"], lw=1.6)
    ar(a, (m[2] - 0.7, R1), (m[1] + 0.7, R2 + RH), c=K["nav"], lw=1.2, ls="--")
    ar(a, (6.9, 11.2), (hx, 11.2), c=K["line"], lw=3.0, ms=16, both=True)
    tag(a, 7.25, 11.6, 7, K["line"])

    ox, owd = ox_, 3.3
    bx(a, ox, y0, owd, y1 - y0, "", fc=K["out"], ec=K["out_e"], lw=1.5, r=0.15)
    tx(a, ox + owd / 2, y1 - 0.3, "OUTPUT\nDEVICES", fs=10, c=K["out_e"], b=True)
    O = {"cd": (14.6, 1.6, "Centre touchscreen\n12-15 in, 1920x720+\n(touch via I2C back-channel)"), "ic": (12.4, 1.5, "Digital instrument\ncluster 12.3 in"),
         "hud": (10.3, 1.5, "Head-up display\n(AR-HUD optional)"), "amp": (6.0, 2.2, "External amplifier\n+ speakers\n(multi-zone, 8-16 ch)")}
    for k, (y, h, t) in O.items():
        bx(a, ox + 0.2, y, owd - 0.4, h, t, fc="white", ec=K["out_e"], fs=8.3)

    ar(a, (hx + hw, 16.4), (ox + 0.2, 15.4), c=K["vid"], lw=1.8); tag(a, 18.25, 16.1, 10, K["vid"])
    ar(a, (ox + 0.2, 14.9), (hx + hw, 15.2), c=K["ctl"], lw=1.2, ls="--")
    ar(a, (hx + hw, 9.6), (ox + 0.2, 13.1), c=K["nav"], lw=1.8); tag(a, 18.25, 12.3, 11, K["nav"])
    ar(a, (hx + hw, 9.3), (ox + 0.2, 11.0), c=K["nav"], lw=1.8); tag(a, 18.25, 10.4, 12, K["nav"])
    bx(a, 3.7, 3.75, 18.1, 0.85, "VEHICLE NETWORK  |  central gateway, CAN-FD and 100/1000BASE-T1 automotive Ethernet (SOME/IP)  |  vehicle speed, gear, wheel ticks, lights, steering-wheel keys, reverse camera, climate",
       fc=K["veh"], ec=K["veh_e"], fs=8.8, lw=1.5)
    ar(a, (5.3, 4.6), (5.3, 5.55), c=K["ctl"], lw=1.2, ls="--")
    fl = [("Media / audio source data", K["med"]), ("Navigation data", K["nav"]), ("Projection session", K["prj"]),
          ("Audio output", K["aud"]), ("Video / display", K["vid"]), ("Control & vehicle data", K["ctl"])]
    tx(a, 0.3, 3.3, "DATA-FLOW KEY", fs=9, c=K["ink"], b=True, ha="left")
    for i, (t, c) in enumerate(fl):
        yy = 2.85 - i * 0.42
        ln(a, [0.35, 0.95], [yy, yy], c=c, lw=2.4)
        tx(a, 1.1, yy, t, fs=8.2, c=K["ink"], ha="left")
    IF = [(1, "Bluetooth: pairing, iAP2 / RFCOMM session start, HFP calls, A2DP audio, AVRCP control, PBAP contacts"),
          (2, "Wi-Fi 5 GHz (802.11ac): wireless CarPlay / Android Auto video, audio and control over TCP/IP"),
          (3, "USB 2.0 HS: iAP2 + CDC-NCM (wired CarPlay), AOA (wired Android Auto), MSC (USB media), charging"),
          (4, "LTE / 5G: online map tiles and updates (NDS.Live), live traffic (TPEG), streaming, OTA software"),
          (5, "GNSS L1 / L5 signals: raw position and time; IMU and wheel ticks add dead reckoning in tunnels"),
          (6, "RF broadcast: AM / FM with RDS, DAB+ with DLS metadata and slideshow images"),
          (7, "Internal I/O: PCIe (Wi-Fi), UART / USB (BT), USB, UART (GNSS), I2S / TDM (tuner audio, microphones)"),
          (8, "Android Car API / Binder IPC between apps and services: commands down, state and data up"),
          (9, "Surface composition and input events between apps and the HMI / window manager"),
          (10, "GMSL2 / FPD-Link serial video to centre display, touch data returned over the link's I2C back-channel"),
          (11, "Inter-VM shared memory: turn-by-turn, media and phone info rendered by RTOS on the cluster"),
          (12, "Maneuver arrow, distance, lane guidance and speed limit to HUD over serial video link"),
          (13, "A2B (Automotive Audio Bus): multichannel PCM from audio DSP to amplifier, volume and zone control"),
          (14, "CAN-FD / SOME/IP via vehicle MCU into Vehicle HAL: speed, gear, lights, steering-wheel keys, camera")]
    tx(a, 4.2, 3.3, "INTERFACE ANNOTATIONS", fs=9, c=K["ink"], b=True, ha="left")
    for i, (n, t) in enumerate(IF):
        col, row = divmod(i, 7)
        xx, yy = 4.35 + col * 8.9, 2.85 - row * 0.42
        tag(a, xx, yy, n, K["ink"])
        tx(a, xx + 0.32, yy, t, fs=7.7, c=K["ink"], ha="left")
    tx(a, 20.9, 0.02, "Dashed arrows: control / feedback", fs=7.5, ha="right", it=True)
    sv(f, d, "D1_IVI_Conceptual_Architecture")


def hdr(a, W, H, t, st):
    tx(a, W / 2, H - 0.35, t, fs=15, c=K["ink"], b=True)
    tx(a, W / 2, H - 0.8, st, fs=9.5, c=K["mute"], it=True)


def grp(a, x, y, w, h, t, items, fc, ec, fs=7.9, ih=None, top=0.62):
    bx(a, x, y, w, h, "", fc=fc, ec=ec, lw=1.6, r=0.15)
    tx(a, x + w / 2, y + h - 0.3, t, fs=9, c=ec, b=True)
    n = len(items)
    av = h - top - 0.15
    ih = ih or min(1.0, (av - 0.12 * (n - 1)) / n)
    g = (av - n * ih) / max(n - 1, 1)
    ys = []
    for i, it in enumerate(items):
        yy = y + h - top - ih - i * (ih + g)
        bx(a, x + 0.15, yy, w - 0.3, ih, it, fc="white", ec=ec, fs=fs, lw=0.9, r=0.06)
        ys.append(yy + ih / 2)
    return ys


def media_flow(d):
    W, H = 20.0, 13.0
    f, a = cv(W, H)
    hdr(a, W, H, "Media Data Flow", "From audio sources through decoding, focus arbitration and DSP to the speakers, with metadata to the HMI and cluster")
    sy = grp(a, 0.3, 2.3, 3.4, 8.6, "AUDIO SOURCES", ["USB drive\nMSC: MP3, AAC, FLAC", "Bluetooth phone\nA2DP (SBC / AAC)\n+ AVRCP control", "AM / FM / DAB+ tuner\nI2S PCM + RDS / DLS",
                                                  "Streaming app\nHTTPS via TCU (AAC / Opus)", "Projection audio\nCarPlay / Android Auto"], K["ext"], K["ext_e"], ih=1.2)
    my = grp(a, 4.5, 4.0, 3.6, 6.9, "MEDIA FRAMEWORK", ["Source plug-ins\n(USB, A2DP, tuner, stream)", "Demux + decoder\n(SW / DSP offload)", "Metadata extractor\nID3, AVRCP, RDS, DLS", "Media library index\n(USB scan, artwork cache)"],
             K["mw"], K["med"], ih=1.1)
    for i in range(4):
        ar(a, (3.55, sy[i]), (4.65, min(max(sy[i], my[-1]), my[0])), c=K["med"], lw=1.6)
    tx(a, 4.1, sy[0] + 0.25, "files", fs=7, c=K["med"], b=True)
    tx(a, 4.1, sy[1] + 0.25, "SBC / AAC", fs=7, c=K["med"], b=True)
    tx(a, 4.1, sy[2] + 0.25, "PCM", fs=7, c=K["med"], b=True)
    tx(a, 4.1, sy[3] - 0.25, "AAC / Opus", fs=7, c=K["med"], b=True)
    amy = grp(a, 9.0, 2.3, 3.5, 8.6, "AUDIO MANAGER", ["Audio focus arbitration\n(priority rules)", "Ducking / muting of\nlower-priority streams", "Routing to zones\n(front, rear, headrest)", "Volume curves &\nuser settings"],
              K["mw"], K["aud"], ih=1.2)
    ar(a, (8.1, 8.0), (9.15, 8.0), c=K["aud"], lw=2)
    tx(a, 8.55, 8.55, "decoded PCM\n48 kHz", fs=7, c=K["aud"], b=True)
    ar(a, (3.55, sy[4]), (9.15, sy[4]), c=K["prj"], lw=1.8)
    tx(a, 6.3, sy[4] + 0.25, "PCM streams: media, nav prompt, assistant", fs=7, c=K["prj"], b=True, bg="white")
    for i, (t, c) in enumerate([("Nav prompt\n(TTS)", K["nav"]), ("Phone call\n(HFP)", K["prj"]), ("Safety chime\n(vehicle)", K["out_e"])]):
        xx = 9.0 + i * 1.2
        bx(a, xx, 11.05, 1.1, 0.65, t, fc="white", ec=c, fs=6.8)
        ar(a, (xx + 0.55, 11.05), (xx + 0.55, 10.9), c=c, lw=1.4)
    dy = grp(a, 13.3, 4.0, 3.2, 6.9, "AUDIO DSP", ["Mixer (per zone)", "EQ + loudness", "Speed-dependent volume\n(speed from VHAL)", "Delay alignment,\nsound zones, AEC"], K["hw"], K["hw_e"], ih=1.05)
    ar(a, (12.5, 8.0), (13.45, 8.0), c=K["aud"], lw=2)
    tx(a, 12.95, 8.35, "TDM\nstreams", fs=7, c=K["aud"], b=True)
    bx(a, 17.3, 6.2, 2.4, 2.8, "External amplifier\n(A2B main node)\n\n8-16 speakers\n(tweeter, mid,\nwoofer, sub)", fc="white", ec=K["out_e"], fs=8)
    ar(a, (16.5, 7.6), (17.3, 7.6), c=K["aud"], lw=2.4)
    tx(a, 16.9, 7.95, "A2B", fs=7.5, c=K["aud"], b=True)
    bx(a, 4.5, 0.5, 3.6, 1.5, "Media app / HMI\nnow playing: title, artist,\nalbum art, progress, queue", fc=K["app"], ec=K["med"], fs=7.8)
    ar(a, (5.1, 4.0), (5.1, 2.0), c=K["med"], lw=1.4, both=True)
    tx(a, 5.25, 2.45, "metadata up / commands down", fs=6.8, c=K["med"], b=True, ha="left", bg="white")
    bx(a, 9.0, 0.5, 3.5, 1.5, "Centre display +\ncluster media widget\n(inter-VM shared memory)", fc="white", ec=K["vid"], fs=7.8)
    ar(a, (8.1, 1.25), (9.0, 1.25), c=K["vid"], lw=1.6)
    bx(a, 0.3, 0.5, 3.4, 1.5, "Driver input\ntouch, SWC keys, voice\n(play, pause, skip)", fc="white", ec=K["ctl"], fs=7.8)
    ar(a, (3.7, 1.25), (4.5, 1.25), c=K["ctl"], lw=1.3, ls="--")
    ar(a, (4.65, sy[1] - 0.35), (3.55, sy[1] - 0.35), c=K["ctl"], lw=1.2, ls="--")
    tx(a, 4.1, sy[1] - 0.6, "AVRCP", fs=6.8, c=K["ctl"], b=True)
    bx(a, 13.3, 0.3, 6.4, 3.3, "", fc="#fffbeb", ec=K["aud"], lw=1.2)
    tx(a, 16.5, 3.3, "AUDIO FOCUS PRIORITY (highest first)", fs=8.5, c=K["aud"], b=True)
    for i, t in enumerate(["1. Safety chimes and warnings (always audible)", "2. Phone call (HFP) - media paused", "3. Voice assistant / ASR session", "4. Navigation prompt - media ducked, not paused", "5. Media: radio, USB, Bluetooth, streaming, projection"]):
        tx(a, 13.55, 2.85 - i * 0.5, t, fs=7.8, c=K["ink"], ha="left")
    sv(f, d, "D2_media_data_flow")


def nav_flow(d):
    W, H = 20.0, 12.0
    f, a = cv(W, H)
    hdr(a, W, H, "Navigation Data Flow", "Sensor fusion, map matching, routing and guidance, with outputs to the display, cluster, HUD and voice prompts")
    iy = grp(a, 0.3, 0.4, 3.5, 10.4, "INPUTS", ["GNSS receiver\nposition, time (1-10 Hz)", "IMU\ngyro + accel (100 Hz)", "Vehicle HAL\nwheel ticks, speed, gear", "Destination input\ntouch search, voice, phone", "Cloud via TCU\nlive traffic (TPEG),\nmap updates, online POI"],
             K["ext"], K["ext_e"], ih=1.35)
    py = grp(a, 4.7, 5.4, 3.5, 5.4, "POSITIONING ENGINE", ["Sensor fusion (EKF)", "Dead reckoning\n(tunnels, parking)", "Map matching to\nroad segment"], K["mw"], K["nav"], ih=1.1)
    for i in range(3):
        ar(a, (3.65, iy[i]), (4.85, py[min(i, 2)]), c=K["nav"], lw=1.5)
    bx(a, 4.7, 2.2, 3.5, 2.2, "MAP DATABASE (NDS)\nroad graph, lanes, POIs,\nspeed limits, 3D landmarks\n(on UFS storage)", fc=K["hw"], ec=K["hw_e"], fs=7.8)
    ar(a, (6.45, 4.4), (6.45, 5.4), c=K["hw_e"], lw=1.3)
    ry = grp(a, 9.1, 4.3, 3.5, 6.5, "ROUTE ENGINE", ["Route calculation\n(A* on road graph)", "Traffic-aware\ncost function", "Alternative routes,\nEV range (if EV)", "Off-route detection\n& re-routing"], K["mw"], K["nav"], ih=1.05)
    ar(a, (8.2, 8.9), (9.25, 8.9), c=K["nav"], lw=2)
    tx(a, 8.65, 9.3, "matched\nposition", fs=7, c=K["nav"], b=True)
    ar(a, (8.2, 3.3), (9.9, 4.3), c=K["hw_e"], lw=1.3)
    tx(a, 8.7, 3.95, "road graph", fs=7, c=K["hw_e"], b=True)
    ln(a, [3.65, 4.25, 4.25, 10.3], [iy[3], iy[3], 1.85, 1.85], c=K["ctl"], lw=1.3, ls="--")
    ar(a, (10.3, 1.85), (10.3, 4.3), c=K["ctl"], lw=1.3, ls="--")
    tx(a, 7.3, 1.85, "destination", fs=7, c=K["ctl"], b=True, bg="white")
    ln(a, [3.65, 11.7], [iy[4], iy[4]], c=K["nav"], lw=1.3)
    ar(a, (11.7, iy[4]), (11.7, 4.3), c=K["nav"], lw=1.3)
    tx(a, 7.3, iy[4], "live traffic, map updates", fs=7, c=K["nav"], b=True, bg="white")
    gy = grp(a, 13.4, 4.3, 3.3, 6.5, "GUIDANCE ENGINE", ["Maneuver generation\n(turn, exit, roundabout)", "Distance-to-maneuver,\nETA", "Lane guidance,\nspeed limit", "Prompt scheduling\n(e.g. 500 m, 100 m)"], K["mw"], K["nav"], ih=1.05)
    ar(a, (12.6, 8.9), (13.55, 8.9), c=K["nav"], lw=2)
    tx(a, 13.05, 9.3, "route", fs=7, c=K["nav"], b=True)
    ar(a, (13.55, gy[3]), (12.45, ry[3]), c=K["nav"], lw=1.2, ls="--")
    tx(a, 13.0, gy[3] - 0.45, "off route", fs=6.8, c=K["nav"], b=True)
    oy = [9.6, 7.6, 5.6, 3.35]
    ot = [("Navigation app map renderer\n(GPU) on centre display", K["vid"]), ("Instrument cluster\nturn-by-turn (inter-VM)", K["vid"]), ("Head-up display\nmaneuver arrow, lane,\nspeed limit", K["vid"]),
          ("TTS voice prompt\n-> audio manager ducks media\n-> DSP -> speakers", K["aud"])]
    for yy, (t, c) in zip(oy, ot):
        bx(a, 17.3, yy - 0.7, 2.5, 1.4, t, fc="white", ec=c, fs=7.4)
        ar(a, (16.7, max(min(yy, 10.3), 4.6)), (17.3, yy), c=c, lw=1.5)
    tx(a, 18.55, 10.75, "OUTPUTS", fs=9, c=K["out_e"], b=True)
    bx(a, 13.4, 0.4, 6.4, 1.85, "When projection navigation is active (e.g. Google Maps or Apple Maps on\nthe phone), the phone computes the route. The head unit only supplies\nGNSS / speed data upstream and receives turn-by-turn metadata for the\ncluster and HUD (see Projection Data Flow).", fc="#f5f3ff", ec=K["prj"], fs=7.4)
    sv(f, d, "D3_navigation_data_flow")


def proj_flow(d):
    W, H = 20.0, 12.4
    f, a = cv(W, H)
    hdr(a, W, H, "Smartphone Projection Data Flow (Apple CarPlay / Android Auto)", "The phone runs the apps and renders the UI; the head unit displays video, plays audio and returns input and vehicle data")
    grp(a, 0.3, 0.8, 3.4, 10.3, "SMARTPHONE", ["CarPlay / Android Auto\nphone-side stack", "UI rendering +\nH.264 encoder", "Apps: maps, music,\nmessages, calls", "Voice assistant\n(Siri / Google Assistant)"], K["ext"], K["ext_e"], ih=1.5)
    tv = [(8.2, "USB 2.0 HS\niAP2 + NCM (CarPlay)\nAOA (Android Auto)"), (5.3, "Wi-Fi 5 GHz\nTCP/IP session\n(wireless mode)"), (2.4, "Bluetooth\nsession bootstrap,\nHFP call audio")]
    bx(a, 4.4, 0.8, 2.9, 10.3, "", fc=K["con"], ec=K["con_e"], lw=1.6, r=0.15)
    tx(a, 5.85, 10.8, "TRANSPORT", fs=9, c=K["con_e"], b=True)
    for yy, t in tv:
        bx(a, 4.55, yy, 2.6, 1.9, t, fc="white", ec=K["con_e"], fs=7.8)
        ar(a, (3.55, yy + 0.95), (4.55, yy + 0.95), c=K["prj"], lw=1.8, both=True)
        ar(a, (7.15, yy + 0.95), (8.1, yy + 0.95), c=K["prj"], lw=1.8, both=True)
    tx(a, 4.05, 0.45, "wired OR wireless", fs=7.2, c=K["prj"], b=True)
    grp(a, 7.95, 0.8, 3.5, 10.3, "PROJECTION SESSION MGR", ["Authentication\n(MFi chip / AA certificate)", "Capability exchange\n(display, codecs, inputs)", "Channel mux / demux", "Resource arbitration\n(screen, main audio)"],
        K["mw"], K["prj"], ih=1.5)
    tx(a, 14.3, 10.75, "DOWNSTREAM   phone  ->  car", fs=9, c=K["prj"], b=True)
    tx(a, 14.3, 5.75, "UPSTREAM   car  ->  phone", fs=9, c=K["ctl"], b=True)
    rows = [(9.8, "Video: H.264 encoded UI\n(e.g. 1920x720, 30-60 fps)", "HW decoder -> projection\nsurface -> HMI compositor\n-> centre display", K["vid"], False),
            (8.3, "Audio: media, nav prompts,\nassistant, alerts (PCM / AAC)", "Audio manager\n(focus, ducking)\n-> DSP -> speakers", K["aud"], False),
            (6.8, "Metadata: turn-by-turn,\nETA, now playing", "Cluster / HUD\n(inter-VM)", K["nav"], False),
            (4.8, "Input: touch, rotary,\nsteering-wheel keys", "HMI input service\n+ Vehicle HAL", K["ctl"], True),
            (3.3, "Microphone audio\n(assistant, calls)", "Mic array + AEC\n(audio DSP)", K["aud"], True),
            (1.8, "Vehicle data: GNSS location,\nspeed, night mode, gear", "Positioning engine\n+ Vehicle HAL", K["ctl"], True)]
    for yy, lab, dst, c, up in rows:
        bx(a, 16.4, yy - 0.62, 3.3, 1.24, dst, fc="white", ec=c, fs=7.3)
        if up:
            ar(a, (16.4, yy), (11.45, yy), c=c, lw=1.8)
        else:
            ar(a, (11.45, yy), (16.4, yy), c=c, lw=1.8)
        tx(a, 13.92, yy + 0.02, lab, fs=7.2, c=K["ink"], bg="white")
    ln(a, [11.7, 19.7], [5.55, 5.55], c=K["mute"], lw=0.8, ls=":")
    sv(f, d, "D4_projection_data_flow")


def proj_seq(d):
    W, H = 19.0, 12.8
    f, a = cv(W, H)
    hdr(a, W, H, "Wireless Projection Session Set-up (Sequence View)", "Typical order of events when a paired phone connects to the head unit for wireless CarPlay or Android Auto")
    L = [("Driver", 1.4, K["ctl"]), ("HMI", 4.7, K["hmi_e"]), ("Connectivity\nmanager", 8.2, K["con_e"]), ("Projection\nsession mgr", 11.9, K["prj"]), ("Smartphone", 16.0, K["ext_e"])]
    for n, x, c in L:
        bx(a, x - 1.2, 10.6, 2.4, 0.9, n, fc="white", ec=c, fs=8.8, b=True, lw=1.6)
        ln(a, [x, x], [0.4, 10.6], c=c, lw=1.0, ls="--", z=1)
    X = {n.split("\n")[0]: x for n, x, _ in L}
    M = [("Smartphone", "Connectivity", "Bluetooth pairing (first time only); head unit advertises CarPlay / Android Auto support in BT EIR", K["prj"], True),
         ("Connectivity", "Smartphone", "iAP2 over BT (CarPlay) or RFCOMM (Android Auto): share Wi-Fi SSID, passphrase, 5 GHz channel", K["prj"], False),
         ("Smartphone", "Connectivity", "Phone joins the head unit's Wi-Fi access point (WPA2 / WPA3), gets IP address via DHCP", K["prj"], False),
         ("Connectivity", "Projection", "Link up: service discovery (mDNS / Bonjour) and TCP session opened", K["con_e"], False),
         ("Projection", "Smartphone", "Authentication: MFi challenge-response (CarPlay) or TLS certificate check (Android Auto)", K["prj"], True),
         ("Projection", "Smartphone", "Capability exchange: screen size, codecs, input types, audio channels, supported vehicle data", K["prj"], True),
         ("Smartphone", "Projection", "Video stream (H.264) and audio channels start", K["vid"], False),
         ("Projection", "HMI", "Request screen and main-audio ownership; HMI shows projection surface", K["hmi_e"], False),
         ("Driver", "HMI", "Touch / rotary / steering-wheel input", K["ctl"], False),
         ("HMI", "Smartphone", "Input events forwarded through session manager", K["ctl"], False),
         ("Projection", "Smartphone", "Vehicle data (location, speed, night mode) sent periodically", K["ctl"], False),
         ("Connectivity", "Projection", "Wi-Fi lost or phone leaves: session ends, HMI returns to native UI; calls continue on BT HFP", K["out_e"], False)]
    y = 9.95
    for i, (p, q, t, c, both) in enumerate(M):
        x1, x2 = X[p], X[q]
        ar(a, (x1, y), (x2, y), c=c, lw=1.5, both=both, z=6)
        xm = (x1 + x2) / 2
        tx(a, xm, y + 0.22, f"{i + 1}. {t}", fs=7.2, c=K["ink"], bg="white")
        y -= 0.8
    sv(f, d, "D5_projection_session_sequence")


def phys_view(d):
    W, H = 20.0, 12.0
    f, a = cv(W, H)
    hdr(a, W, H, "Physical Deployment View: ECUs and In-Vehicle Links", "How the functional blocks map onto hardware units and which physical interfaces connect them")
    bx(a, 7.2, 4.0, 5.6, 4.2, "COCKPIT DOMAIN CONTROLLER\n\nSoC (CPU / GPU / NPU / video codec)\nType-1 hypervisor: IVI VM + cluster RTOS VM\nWi-Fi + BT combo (PCIe / UART)\nGNSS receiver + IMU, AM / FM / DAB+ tuner\nAudio DSP, HSM, MFi auth chip, UFS storage\nVehicle MCU (AUTOSAR)", fc=K["hu"], ec=K["hu_e"], fs=8.2, lw=2.2)
    T = [(1.6, "Centre touchscreen", "GMSL2 / FPD-Link\n(up to 6 Gbit/s) + touch\nover I2C back-channel"), (7.2, "Instrument cluster", "GMSL2 / LVDS\ncluster video"), (12.8, "Head-up display", "GMSL2\nHUD video")]
    for x, n, l in T:
        bx(a, x, 9.6, 3.6, 1.0, n, fc="white", ec=K["out_e"], fs=8.5, b=True)
        ar(a, (min(max(x + 1.8, 7.6), 12.4), 8.2), (x + 1.8, 9.6), c=K["vid"], lw=1.8)
        tx(a, (min(max(x + 1.8, 7.6), 12.4) + x + 1.8) / 2, 8.9, l, fs=7, c=K["vid"], b=True, bg="white")
    Lf = [(7.4, "Roof antenna module\nGNSS, AM/FM/DAB+,\nLTE/5G, Wi-Fi/BT", "coax (FAKRA)\nRF feeds", K["nav"]), (5.2, "Telematics unit\n4G / 5G, eSIM", "100BASE-T1\nEthernet", K["nav"]), (3.0, "USB-C ports\n(console, rear)", "USB 2.0 HS\n480 Mbit/s via hub", K["prj"])]
    for y, n, l, c in Lf:
        bx(a, 0.3, y - 0.6, 3.4, 1.3, n, fc="white", ec=K["con_e"], fs=7.8)
        ar(a, (3.7, y + 0.05), (7.2, min(max(y + 0.05, 4.3), 7.9)), c=c, lw=1.6, both=True)
        tx(a, 5.45, (y + min(max(y + 0.05, 4.3), 7.9)) / 2 + 0.35, l, fs=7, c=c, b=True, bg="white")
    ar(a, (2.0, 6.8), (2.0, 5.85), c=K["nav"], lw=1.2, ls="--")
    Rt = [(7.3, "Amplifier\n(A2B main node)\n+ speakers", "A2B, 50 Mbit/s\naudio out", K["aud"]), (5.1, "Roof microphones\n(A2B sub-nodes)", "A2B daisy chain\nmic audio in", K["aud"]), (2.9, "Reverse / surround\ncamera", "GMSL2\ncamera video", K["vid"])]
    for y, n, l, c in Rt:
        bx(a, 16.3, y - 0.65, 3.4, 1.3, n, fc="white", ec=K["out_e"], fs=7.8)
        yy = min(max(y, 4.3), 7.9)
        ar(a, (12.8, yy), (16.3, y), c=c, lw=1.6, both=(y != 7.3 and y != 2.9) or False)
        tx(a, 14.55, (y + yy) / 2 + 0.35, l, fs=7, c=c, b=True, bg="white")
    ar(a, (18.0, 6.65), (18.0, 5.75), c=K["aud"], lw=1.2, ls="--")
    bx(a, 7.2, 0.4, 5.6, 1.4, "CENTRAL GATEWAY\nCAN-FD, LIN, 1000BASE-T1 Ethernet", fc=K["veh"], ec=K["veh_e"], fs=8.5, b=True)
    ar(a, (10.0, 1.8), (10.0, 4.0), c=K["ctl"], lw=1.8, both=True)
    tx(a, 10.1, 2.9, "1000BASE-T1 (SOME/IP)\n+ CAN-FD (2-5 Mbit/s data)", fs=7, c=K["ctl"], b=True, ha="left", bg="white")
    bx(a, 1.6, 0.4, 3.6, 1.4, "Steering-wheel controls\n(LIN)", fc="white", ec=K["veh_e"], fs=7.8)
    ar(a, (5.2, 1.1), (7.2, 1.1), c=K["ctl"], lw=1.4)
    bx(a, 14.8, 0.4, 3.6, 1.4, "Other ECUs\nbody, ADAS, powertrain,\nclimate", fc="white", ec=K["veh_e"], fs=7.8)
    ar(a, (12.8, 1.1), (14.8, 1.1), c=K["ctl"], lw=1.4, both=True)
    sv(f, d, "D6_physical_deployment_view")


if __name__ == "__main__":
    o = sys.argv[1] if len(sys.argv) > 1 else "."
    main_diagram(o)
    media_flow(os.path.join(o, "data_flows"))
    nav_flow(os.path.join(o, "data_flows"))
    proj_flow(os.path.join(o, "data_flows"))
    proj_seq(os.path.join(o, "data_flows"))
    phys_view(os.path.join(o, "views"))
    print("done")
