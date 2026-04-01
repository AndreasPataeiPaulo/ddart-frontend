"""
DDART AI – Tutorial video generator
Produces tutorial_el.mp4 with Greek narration text overlays.
"""

from PIL import Image, ImageDraw, ImageFont
from moviepy import ImageSequenceClip
import numpy as np
import math, os, textwrap

# ── Config ────────────────────────────────────────────────────────────────────
W, H   = 1280, 720
FPS    = 30
OUT    = os.path.join(os.path.dirname(__file__), "tutorial_el.mp4")

FONT_PATH = "/System/Library/Fonts/Supplemental/Arial Unicode.ttf"

# Palette
BG        = (15,  20,  30)
CARD      = (30,  40,  58)
CARD2     = (38,  50,  72)
ACCENT    = (66, 153, 225)
ACCENT_L  = (99, 179, 237)
GREEN     = (72, 187, 120)
RED       = (252, 129, 129)
ORANGE    = (237, 137,  54)
TXT1      = (226, 232, 240)
TXT2      = (160, 174, 192)
BORDER    = ( 74,  85, 104)
WHITE     = (255, 255, 255)
BLACK     = (  0,   0,   0)
OVERLAY_C = (10,  14,  22, 220)   # semi-transparent dark

def font(size, bold=False):
    return ImageFont.truetype(FONT_PATH, size)

# ── Drawing helpers ────────────────────────────────────────────────────────────

def new_frame():
    img = Image.new("RGB", (W, H), BG)
    return img, ImageDraw.Draw(img)

def rounded_rect(draw, x, y, w, h, r, fill, outline=None, lw=1):
    draw.rounded_rectangle([x, y, x+w, y+h], radius=r, fill=fill,
                           outline=outline, width=lw)

def text_center(draw, text, y, size, color=TXT1, bold=False):
    f = font(size, bold)
    bb = draw.textbbox((0, 0), text, font=f)
    tw = bb[2] - bb[0]
    draw.text(((W - tw) // 2, y), text, font=f, fill=color)

def text_at(draw, text, x, y, size, color=TXT1, anchor="la"):
    f = font(size)
    draw.text((x, y), text, font=f, fill=color, anchor=anchor)

def cursor(draw, cx, cy, clicking=False):
    r = 14 if not clicking else 10
    alpha_ring = ACCENT if not clicking else GREEN
    draw.ellipse([cx-r, cy-r, cx+r, cy+r], outline=alpha_ring, width=3)
    draw.ellipse([cx-5, cy-5, cx+5, cy+5], fill=WHITE)

def ease(t):
    """Smooth-step easing 0→1"""
    t = max(0, min(1, t))
    return t * t * (3 - 2 * t)

def lerp(a, b, t):
    return a + (b - a) * ease(t)

def lerp_pt(p1, p2, t):
    return (lerp(p1[0], p2[0], t), lerp(p1[1], p2[1], t))

def wrap(draw, text, x, y, w, size, color=TXT2, line_gap=6):
    f = font(size)
    chars_per_line = max(1, int(w / (size * 0.55)))
    lines = textwrap.wrap(text, chars_per_line)
    lh = size + line_gap
    for i, line in enumerate(lines):
        draw.text((x, y + i * lh), line, font=f, fill=color)
    return y + len(lines) * lh

# ── UI component helpers ──────────────────────────────────────────────────────

def input_field(draw, x, y, w, label, value="", focused=False):
    h = 44
    border = ACCENT if focused else BORDER
    rounded_rect(draw, x, y, w, h, 8, CARD2, outline=border, lw=2 if focused else 1)
    f_lbl = font(11)
    draw.text((x+12, y-17), label, font=f_lbl, fill=TXT2)
    if value:
        f_val = font(15)
        draw.text((x+12, y+12), value, font=f_val, fill=TXT1)
    if focused:
        f_val = font(15)
        bb = draw.textbbox((0,0), value, font=f_val) if value else (0,0,0,0)
        cx = x + 12 + (bb[2]-bb[0]) + 2
        draw.line([(cx, y+10), (cx, y+34)], fill=ACCENT, width=2)

def button(draw, x, y, w, label, h=46, color=ACCENT, txt_color=WHITE, outline=None):
    rounded_rect(draw, x, y, w, h, 10, color, outline=outline, lw=2)
    f = font(15)
    bb = draw.textbbox((0,0), label, font=f)
    tw, th = bb[2]-bb[0], bb[3]-bb[1]
    draw.text((x + (w-tw)//2, y + (h-th)//2 - 2), label, font=f, fill=txt_color)

def tab_bar(draw, x, y, w, tabs, active, tab_w=None):
    tw = tab_w or w // len(tabs)
    rounded_rect(draw, x, y, w, 42, 10, CARD2)
    for i, tab in enumerate(tabs):
        tx = x + i * tw
        if i == active:
            rounded_rect(draw, tx+2, y+2, tw-4, 38, 8, ACCENT)
            tcol = WHITE
        else:
            tcol = TXT2
        f = font(14)
        bb = draw.textbbox((0,0), tab, font=f)
        tw2 = bb[2]-bb[0]
        draw.text((tx + (tw-tw2)//2, y+12), tab, font=f, fill=tcol)

def badge(draw, x, y, label, color=ACCENT):
    f = font(12)
    bb = draw.textbbox((0,0), label, font=f)
    pw = bb[2]-bb[0]+20
    ph = 24
    rounded_rect(draw, x, y, pw, ph, 12, (*color, 30), outline=color, lw=1)
    draw.text((x+10, y+5), label, font=f, fill=color)

def annotation_box(draw, text, y, icon="ℹ"):
    """Full-width blue annotation bar at bottom of screen"""
    bh = 52
    by = y
    draw.rectangle([0, by, W, by+bh], fill=(20, 40, 70))
    draw.rectangle([0, by, W, by+2], fill=ACCENT)
    f = font(16)
    draw.text((40, by + 16), f"{icon}  {text}", font=f, fill=TXT1)

def step_indicator(draw, current, total):
    """Small dots at top showing progress"""
    dot_r = 5
    spacing = 22
    total_w = (total - 1) * spacing
    sx = (W - total_w) // 2
    for i in range(total):
        cx = sx + i * spacing
        cy = 22
        col = ACCENT if i <= current else BORDER
        draw.ellipse([cx-dot_r, cy-dot_r, cx+dot_r, cy+dot_r], fill=col)

def header_bar(draw, title, subtitle=""):
    draw.rectangle([0, 0, W, 60], fill=(18, 25, 40))
    f = font(20)
    draw.text((24, 18), title, font=f, fill=TXT1)
    if subtitle:
        f2 = font(12)
        draw.text((24, 42), subtitle, font=f2, fill=TXT2)
    # DDART logo text on right
    f3 = font(18)
    draw.text((W-120, 20), "DDART AI", font=f3, fill=ACCENT)

# ── Annotation label for highlighting ─────────────────────────────────────────

def highlight_box(draw, x, y, w, h, label="", color=ACCENT):
    for offset in range(3, 0, -1):
        draw.rounded_rectangle(
            [x-offset, y-offset, x+w+offset, y+h+offset],
            radius=10+offset,
            outline=(*color, 80 - offset*20),
            width=1
        )
    draw.rounded_rectangle([x-2, y-2, x+w+2, y+h+2], radius=10,
                           outline=color, width=2)
    if label:
        f = font(12)
        bb = draw.textbbox((0,0), label, font=f)
        tw = bb[2]-bb[0]
        lx = x + (w-tw)//2
        ly = y - 26
        rounded_rect(draw, lx-8, ly-4, tw+16, 22, 6, color)
        draw.text((lx, ly), label, font=f, fill=WHITE)

# ── Scene 1: Title card ────────────────────────────────────────────────────────

def make_title_frames():
    frames = []
    dur = int(4 * FPS)
    for fi in range(dur):
        t = fi / dur
        img, draw = new_frame()

        # Radial glow
        for r in range(200, 0, -20):
            alpha = int(30 * (1 - r/200))
            draw.ellipse(
                [W//2-r, H//2-r-60, W//2+r, H//2+r-60],
                outline=(*ACCENT, alpha)
            )

        # Logo circle
        logo_cx, logo_cy = W//2, 240
        logo_r = 70
        draw.ellipse(
            [logo_cx-logo_r, logo_cy-logo_r, logo_cx+logo_r, logo_cy+logo_r],
            outline=ACCENT, width=2
        )
        draw.ellipse(
            [logo_cx-52, logo_cy-52, logo_cx+52, logo_cy+52],
            outline=(*ACCENT, 100), width=1
        )
        f_logo = font(36)
        draw.text((logo_cx, logo_cy), "AI", font=f_logo, fill=ACCENT, anchor="mm")

        # Title fade-in
        alpha_t = ease(t * 2)
        title_col = tuple(int(c * alpha_t) for c in TXT1)
        sub_col   = tuple(int(c * alpha_t) for c in TXT2)

        f_title = font(38)
        title = "Οδηγός Χρήσης Εφαρμογής"
        bb = draw.textbbox((0,0), title, font=f_title)
        draw.text(((W-(bb[2]-bb[0]))//2, 340), title, font=f_title, fill=title_col)

        f_sub = font(20)
        sub = "DDART AI – Πλατφόρμα Οφθαλμολογικού Ελέγχου"
        bb = draw.textbbox((0,0), sub, font=f_sub)
        draw.text(((W-(bb[2]-bb[0]))//2, 400), sub, font=f_sub, fill=sub_col)

        # Bottom line
        if t > 0.5:
            draw.line([(W//2-180, 460), (W//2+180, 460)], fill=(*BORDER, 120), width=1)
            f_sm = font(13)
            draw.text((W//2, 470), "Democritus University of Thrace – DDARTECH",
                      font=f_sm, fill=TXT2, anchor="mt")

        frames.append(np.array(img))
    return frames

# ── Scene 2: Login page overview ──────────────────────────────────────────────

def draw_login(draw, active_tab=0, email_val="", pass_val="",
               email_focus=False, pass_focus=False,
               show_register=False, reg_name="", reg_email="",
               reg_pass="", reg_confirm=""):
    header_bar(draw, "DDART AI – Σύνδεση",
               "Democritus University of Thrace")

    card_x, card_y = W//2-220, 90
    card_w, card_h = 440, 500
    rounded_rect(draw, card_x, card_y, card_w, card_h, 16, CARD, outline=BORDER, lw=1)

    if show_register:
        tabs = ["Κέντρο Υγείας", "Εγγραφή | Σύνδεση"]
    else:
        tabs = ["Κέντρο Υγείας", "Ερευνητής"]
    tab_bar(draw, card_x+16, card_y+16, card_w-32, tabs, active_tab)

    if not show_register:
        if active_tab == 0:
            f_h = font(18)
            draw.text((card_x+20, card_y+74), "Κέντρο Υγείας", font=f_h, fill=TXT1)
            f_s = font(13)
            draw.text((card_x+20, card_y+100), "Συνδεθείτε με τα στοιχεία του κέντρου σας",
                      font=f_s, fill=TXT2)
            input_field(draw, card_x+20, card_y+136, card_w-40,
                        "Όνομα χρήστη", email_val, email_focus)
            input_field(draw, card_x+20, card_y+206, card_w-40,
                        "Κωδικός πρόσβασης",
                        "•"*len(pass_val) if pass_val else "", pass_focus)
            button(draw, card_x+20, card_y+278, card_w-40, "Σύνδεση →")
        else:
            f_h = font(18)
            draw.text((card_x+20, card_y+74), "Ερευνητής", font=f_h, fill=TXT1)
            input_field(draw, card_x+20, card_y+110, card_w-40, "Email", email_val, email_focus)
            input_field(draw, card_x+20, card_y+180, card_w-40,
                        "Κωδικός", "•"*len(pass_val) if pass_val else "", pass_focus)
            button(draw, card_x+20, card_y+252, card_w-40, "Σύνδεση →")
            f_or = font(13)
            draw.text((card_x+card_w//2, card_y+314), "— ή —",
                      font=f_or, fill=TXT2, anchor="mt")
            button(draw, card_x+20, card_y+336, card_w-40, "Εγγραφή νέου ερευνητή",
                   color=CARD2, txt_color=ACCENT, outline=ACCENT)
    else:
        f_h = font(16)
        draw.text((card_x+20, card_y+74), "Εγγραφή Ερευνητή", font=f_h, fill=TXT1)
        input_field(draw, card_x+20, card_y+106, card_w-40, "Ονοματεπώνυμο", reg_name)
        input_field(draw, card_x+20, card_y+166, card_w-40, "Email", reg_email)
        input_field(draw, card_x+20, card_y+226, card_w-40, "Κωδικός",
                    "•"*len(reg_pass) if reg_pass else "")
        input_field(draw, card_x+20, card_y+286, card_w-40, "Επιβεβαίωση Κωδικού",
                    "•"*len(reg_confirm) if reg_confirm else "")
        button(draw, card_x+20, card_y+352, card_w-40,
               "Υποβολή αίτησης εγγραφής")
        f_note = font(11)
        draw.text((card_x+20, card_y+410),
                  "Η εγγραφή απαιτεί έγκριση διαχειριστή.",
                  font=f_note, fill=TXT2)

def make_login_overview_frames():
    frames = []
    dur = int(3 * FPS)
    for fi in range(dur):
        img, draw = new_frame()
        draw_login(draw, active_tab=0)
        annotation_box(draw, "Η σελίδα σύνδεσης – δύο τύποι χρηστών: Κέντρο Υγείας & Ερευνητής", H-52)
        step_indicator(draw, 0, 7)
        frames.append(np.array(img))
    return frames

# ── Scene 3: Health Center sign-in ─────────────────────────────────────────────

def make_hc_signin_frames():
    frames = []

    phases = [
        # (duration_s, description)
        (1.5, "show_page"),
        (1.5, "focus_user"),
        (2.0, "type_user"),
        (1.0, "focus_pass"),
        (2.0, "type_pass"),
        (1.5, "click_btn"),
    ]

    card_x, card_y = W//2-220, 90
    card_w = 440
    btn_x = card_x+20
    btn_y = card_y+278
    btn_w = card_w-40

    userfield_x = card_x+20+6
    userfield_y = card_y+136+22
    passfield_x = card_x+20+6
    passfield_y = card_y+206+22
    btn_cx = card_x+20+btn_w//2
    btn_cy = card_y+278+23

    cursor_pos = [(W//2, H//2),
                  (userfield_x, userfield_y),
                  (userfield_x, userfield_y),
                  (passfield_x, passfield_y),
                  (passfield_x, passfield_y),
                  (btn_cx, btn_cy)]

    username = "91127"
    password = "andreas"

    phase_frames = [int(d * FPS) for d, _ in phases]
    total_frames = sum(phase_frames)
    abs_starts = [sum(phase_frames[:i]) for i in range(len(phases))]

    for fi in range(total_frames):
        phase = 0
        for i, start in enumerate(abs_starts):
            if fi >= start:
                phase = i
        local = fi - abs_starts[phase]
        local_t = local / max(1, phase_frames[phase] - 1)
        next_phase = min(phase + 1, len(phases) - 1)

        cx, cy = lerp_pt(cursor_pos[phase], cursor_pos[next_phase], local_t)

        # Compute typed text
        if phase <= 1:
            uval, pval = "", ""
        elif phase == 2:
            chars = max(0, int(local_t * len(username)))
            uval, pval = username[:chars], ""
        elif phase == 3:
            uval, pval = username, ""
        elif phase == 4:
            chars = max(0, int(local_t * len(password)))
            uval, pval = username, password[:chars]
        else:
            uval, pval = username, password

        img, draw = new_frame()
        draw_login(draw,
                   active_tab=0,
                   email_val=uval,
                   pass_val=pval,
                   email_focus=(phase == 1 or phase == 2),
                   pass_focus=(phase == 3 or phase == 4))

        if phase == 5:
            # Button glow effect
            highlight_box(draw, btn_x, btn_y, btn_w, 46, "", GREEN)

        cursor(draw, int(cx), int(cy), clicking=(phase == 5 and local_t > 0.4))

        ann = {
            0: "Επιλέξτε καρτέλα «Κέντρο Υγείας»",
            1: "Κλικ στο πεδίο «Όνομα χρήστη»",
            2: "Πληκτρολογήστε το αναγνωριστικό κέντρου",
            3: "Κλικ στο πεδίο «Κωδικός»",
            4: "Εισάγετε τον κωδικό πρόσβασης",
            5: "Πατήστε «Σύνδεση» για πρόσβαση στην πύλη",
        }
        annotation_box(draw, ann[phase], H-52)
        step_indicator(draw, 1, 7)
        frames.append(np.array(img))
    return frames

# ── Scene 4: Health Center Dashboard ──────────────────────────────────────────

def draw_hc_dashboard(draw, amka="", img_loaded=False, show_result=False, result_type="glaucoma"):
    header_bar(draw, "Κέντρο Υγείας – Πύλη",
               "Democritus University of Thrace | DDART AI 1.0")

    # Left panel – instructions
    px, py = 40, 80
    pw = 360
    rounded_rect(draw, px, py, pw, 580, 14, CARD, outline=BORDER, lw=1)

    f_h = font(18)
    draw.text((px+20, py+20), "Πύλη Κέντρου Υγείας", font=f_h, fill=TXT1)

    f_sm = font(13)
    draw.text((px+20, py+50),
              "Ανεβάστε εικόνα βυθού για ανάλυση ΤΝ",
              font=f_sm, fill=TXT2)

    steps = [
        ("1", "Εξασφαλίστε φόρμα συναίνεσης"),
        ("2", "Εισάγετε ΑΜΚΑ ασθενή"),
        ("3", "Επιλέξτε εικόνα αμφιβληστροειδή"),
        ("4", "Υποβάλετε για ανάλυση ΤΝ"),
    ]
    for i, (num, txt) in enumerate(steps):
        sy = py + 90 + i * 56
        draw.ellipse([px+20, sy, px+42, sy+22], fill=ACCENT)
        f_n = font(13)
        draw.text((px+31, sy+11), num, font=f_n, fill=WHITE, anchor="mm")
        f_s = font(14)
        draw.text((px+52, sy+4), txt, font=f_s, fill=TXT1)

    # Badge
    badge(draw, px+20, py+330, "Γλαύκωμα", ACCENT)

    # Right panel – upload area
    ux, uy = 430, 80
    uw = W - ux - 40
    uh = 580

    rounded_rect(draw, ux, uy, uw, uh, 14, CARD, outline=BORDER, lw=1)

    # AMKA input
    input_field(draw, ux+20, uy+30, uw-40, "ΑΜΚΑ Ασθενή", amka, bool(amka) and not img_loaded)

    # Drop zone
    dz_y = uy + 110
    dz_h = 200
    dz_color = CARD2 if not img_loaded else (30, 60, 45)
    dz_border = ACCENT if not img_loaded else GREEN
    rounded_rect(draw, ux+20, dz_y, uw-40, dz_h, 12, dz_color,
                 outline=dz_border, lw=2)

    if not img_loaded:
        f_icon = font(36)
        draw.text((ux+uw//2, dz_y+60), "⬆", font=f_icon, fill=(*ACCENT, 180), anchor="mt")
        f_dz = font(15)
        draw.text((ux+uw//2, dz_y+110), "Σύρετε εικόνα εδώ",
                  font=f_dz, fill=TXT2, anchor="mt")
        f_dz2 = font(12)
        draw.text((ux+uw//2, dz_y+136), "ή κλικ για επιλογή αρχείου",
                  font=f_dz2, fill=TXT2, anchor="mt")
    else:
        # Simulated retinal image (dark circle)
        img_cx = ux + uw//2
        img_cy = dz_y + dz_h//2
        draw.ellipse(
            [img_cx-70, img_cy-65, img_cx+70, img_cy+65],
            fill=(15, 8, 5), outline=(80, 50, 30), width=2
        )
        # Retinal vessels (simple lines)
        import random; random.seed(42)
        for _ in range(12):
            x1 = img_cx + random.randint(-50, 50)
            y1 = img_cy + random.randint(-50, 50)
            x2 = x1 + random.randint(-30, 30)
            y2 = y1 + random.randint(-30, 30)
            draw.line([(x1, y1), (x2, y2)], fill=(160, 90, 60), width=1)
        draw.ellipse([img_cx+15, img_cy-20, img_cx+45, img_cy+10],
                     fill=(220, 180, 140), outline=(240, 200, 160), width=1)
        f_ok = font(12)
        draw.text((ux+uw//2, dz_y+dz_h-18), "✓  retinal_image.jpg",
                  font=f_ok, fill=GREEN, anchor="mt")

    # Submit button
    sub_y = dz_y + dz_h + 20
    active = bool(amka) and img_loaded
    btn_col = ACCENT if active else BORDER
    button(draw, ux+20, sub_y, uw-40, "Υποβολή για Ανάλυση ΤΝ →",
           color=btn_col, txt_color=WHITE if active else TXT2)

    # Result overlay
    if show_result:
        rounded_rect(draw, ux+20, sub_y+64, uw-40, 120, 12, (20, 45, 30),
                     outline=GREEN, lw=2)
        f_r = font(16)
        draw.text((ux+40, sub_y+80), "✓  Ανάλυση ολοκληρώθηκε", font=f_r, fill=GREEN)
        f_r2 = font(14)
        draw.text((ux+40, sub_y+108),
                  "Παραπομπή για Γλαύκωμα  –  94% εμπιστοσύνη",
                  font=f_r2, fill=TXT1)
        draw.text((ux+40, sub_y+134),
                  "Η ερευνητική ομάδα θα αξιολογήσει τα αποτελέσματα.",
                  font=font(12), fill=TXT2)

def make_hc_dashboard_frames():
    """HC dashboard overview then upload flow"""
    frames = []

    phases = [
        (2.0, "overview"),
        (2.0, "enter_amka"),
        (2.0, "type_amka"),
        (2.0, "drop_image"),
        (2.0, "click_submit"),
        (3.0, "show_result"),
    ]

    ux, uy = 430, 80
    uw = W - ux - 40
    amka_field_x = ux+26
    amka_field_y = uy+52
    dz_cx = ux+uw//2
    dz_cy = uy+210
    sub_btn_cx = ux+uw//2
    sub_btn_cy = uy+334

    cursor_positions = [
        (W//2, H//2),
        (amka_field_x, amka_field_y),
        (amka_field_x + 40, amka_field_y),
        (dz_cx, dz_cy),
        (sub_btn_cx, sub_btn_cy),
        (sub_btn_cx, sub_btn_cy),
    ]

    amka_full = "123456789"
    phase_frames = [int(d * FPS) for d, _ in phases]
    abs_starts = [sum(phase_frames[:i]) for i in range(len(phases))]
    total = sum(phase_frames)

    for fi in range(total):
        phase = 0
        for i, s in enumerate(abs_starts):
            if fi >= s: phase = i
        local = fi - abs_starts[phase]
        local_t = local / max(1, phase_frames[phase] - 1)
        next_phase = min(phase + 1, len(phases) - 1)

        cx, cy = lerp_pt(cursor_positions[phase], cursor_positions[next_phase], local_t)

        amka = ""
        img_loaded = False
        show_result = False

        if phase == 2:
            amka = amka_full[:max(0, int(local_t * len(amka_full)))]
        elif phase >= 3:
            amka = amka_full
        if phase >= 3:
            img_loaded = True
        if phase == 5:
            show_result = True

        img, draw = new_frame()
        draw_hc_dashboard(draw, amka=amka, img_loaded=img_loaded, show_result=show_result)

        # Highlights
        if phase == 1:
            highlight_box(draw, ux+20, uy+16, uw-40, 60,
                         "Πεδίο ΑΜΚΑ", ACCENT)
        elif phase == 3:
            highlight_box(draw, ux+20, uy+110, uw-40, 200,
                         "Ζώνη μεταφόρτωσης", ACCENT)
        elif phase == 4:
            highlight_box(draw, ux+20, uy+330, uw-40, 46,
                         "Υποβολή", GREEN)

        cursor(draw, int(cx), int(cy),
               clicking=(phase in (1, 3, 4) and local_t > 0.6))

        ann = {
            0: "Πύλη Κέντρου Υγείας – εδώ γίνεται η μεταφόρτωση εικόνων",
            1: "Κλικ στο πεδίο ΑΜΚΑ και εισάγετε τον αριθμό ασθενή",
            2: "Πληκτρολογήστε τον αριθμό ΑΜΚΑ",
            3: "Σύρετε ή επιλέξτε εικόνα βυθού αμφιβληστροειδούς",
            4: "Πατήστε «Υποβολή» – η ΤΝ αναλύει την εικόνα αυτόματα",
            5: "Αποτέλεσμα ΤΝ: Παραπομπή με 94% εμπιστοσύνη. Ολοκληρώθηκε!",
        }
        annotation_box(draw, ann[phase], H-52)
        step_indicator(draw, 2, 7)
        frames.append(np.array(img))
    return frames

# ── Scene 5: Researcher sign-up ───────────────────────────────────────────────

def make_researcher_signup_frames():
    frames = []
    card_x, card_y = W//2-220, 90
    card_w = 440

    phases = [
        (1.5, "show_tab"),
        (1.0, "click_register"),
        (2.0, "fill_name"),
        (2.0, "fill_email"),
        (2.0, "fill_pass"),
        (1.5, "submit"),
        (2.0, "pending"),
    ]
    phase_frames = [int(d * FPS) for d, _ in phases]
    abs_starts = [sum(phase_frames[:i]) for i in range(len(phases))]
    total = sum(phase_frames)

    reg_btn_x = card_x+20
    reg_btn_y = card_y+336
    reg_btn_w = card_w-40
    sub_btn_y = card_y+352

    full_name    = "Δρ. Μαρία Παπαδοπούλου"
    full_email   = "mpapadopoulou@med.duth.gr"
    full_pass    = "securePass123"
    full_confirm = "securePass123"

    for fi in range(total):
        phase = 0
        for i, s in enumerate(abs_starts):
            if fi >= s: phase = i
        local = fi - abs_starts[phase]
        local_t = local / max(1, phase_frames[phase] - 1)

        name_val    = ""
        email_val   = ""
        pass_val    = ""
        confirm_val = ""
        show_register = False

        if phase == 0:
            # Show researcher tab
            img, draw = new_frame()
            draw_login(draw, active_tab=1)
            annotation_box(draw, "Ο ερευνητής επιλέγει την καρτέλα «Ερευνητής»", H-52)
            highlight_box(draw, card_x+16+card_w//2, card_y+16, card_w//2-18, 42, "Ερευνητής", ACCENT)

        elif phase == 1:
            img, draw = new_frame()
            draw_login(draw, active_tab=1)
            annotation_box(draw, "Κλικ στο «Εγγραφή νέου ερευνητή»", H-52)
            highlight_box(draw, reg_btn_x, reg_btn_y, reg_btn_w, 46, "Εγγραφή", ACCENT)
            cx = reg_btn_x + reg_btn_w//2
            cy = reg_btn_y + 23
            cursor(draw, cx, cy, clicking=(local_t > 0.5))

        else:
            show_register = True
            chars_n  = int(ease((phase-2)/4.0 + local_t/4.0) * len(full_name))    if phase >= 2 else 0
            chars_e  = int(ease((phase-3)/3.0 + local_t/3.0) * len(full_email))   if phase >= 3 else 0
            chars_p  = int(ease((phase-4)/2.0 + local_t/2.0) * len(full_pass))    if phase >= 4 else 0
            chars_c  = int(ease((phase-5)/1.5 + local_t/1.5) * len(full_confirm)) if phase >= 5 else 0
            name_val    = full_name[:max(0, min(chars_n, len(full_name)))]
            email_val   = full_email[:max(0, min(chars_e, len(full_email)))]
            pass_val    = full_pass[:max(0, min(chars_p, len(full_pass)))]
            confirm_val = full_confirm[:max(0, min(chars_c, len(full_confirm)))]

            img, draw = new_frame()
            draw_login(draw, active_tab=1, show_register=True,
                       reg_name=name_val, reg_email=email_val,
                       reg_pass=pass_val, reg_confirm=confirm_val)

            if phase == 6:
                # Pending approval message
                rounded_rect(draw, card_x+20, card_y+380, card_w-40, 80, 10,
                             (40, 40, 20), outline=ORANGE, lw=2)
                f_p = font(14)
                draw.text((card_x+40, card_y+396),
                          "⏳ Αίτηση υποβλήθηκε!", font=f_p, fill=ORANGE)
                f_p2 = font(12)
                draw.text((card_x+40, card_y+420),
                          "Αναμένεται έγκριση από διαχειριστή.",
                          font=f_p2, fill=TXT2)

            ann_map = {2:"Εισάγετε το ονοματεπώνυμό σας",
                       3:"Εισάγετε το email σας",
                       4:"Επιλέξτε κωδικό πρόσβασης",
                       5:"Επαναλάβετε τον κωδικό και πατήστε Υποβολή",
                       6:"Η αίτηση στάλθηκε – αναμένεται έγκριση διαχειριστή"}
            annotation_box(draw, ann_map.get(phase, ""), H-52)

        if phase not in (0, 1):
            step_indicator(draw, 3, 7)
            frames.append(np.array(img))
            continue

        step_indicator(draw, 3, 7)
        frames.append(np.array(img))

    return frames

# ── Scene 6: Researcher sign-in ───────────────────────────────────────────────

def make_researcher_signin_frames():
    frames = []
    card_x, card_y = W//2-220, 90
    card_w = 440

    phases = [
        (1.5, "show"),
        (2.0, "type_email"),
        (2.0, "type_pass"),
        (1.5, "click"),
    ]
    phase_frames = [int(d * FPS) for d, _ in phases]
    abs_starts = [sum(phase_frames[:i]) for i in range(len(phases))]
    total = sum(phase_frames)

    email_full = "mpapadopoulou@med.duth.gr"
    pass_full  = "securePass123"

    for fi in range(total):
        phase = 0
        for i, s in enumerate(abs_starts):
            if fi >= s: phase = i
        local = fi - abs_starts[phase]
        local_t = local / max(1, phase_frames[phase] - 1)

        chars_e = int(local_t * len(email_full)) if phase == 1 else (len(email_full) if phase >= 2 else 0)
        chars_p = int(local_t * len(pass_full))  if phase == 2 else (len(pass_full)  if phase >= 3 else 0)

        img, draw = new_frame()
        draw_login(draw, active_tab=1,
                   email_val=email_full[:chars_e],
                   pass_val=pass_full[:chars_p],
                   email_focus=(phase == 1),
                   pass_focus=(phase == 2))

        btn_x = card_x+20
        btn_y = card_y+252
        btn_w = card_w-40
        if phase == 3:
            highlight_box(draw, btn_x, btn_y, btn_w, 46, "Σύνδεση", GREEN)
            cursor(draw, btn_x+btn_w//2, btn_y+23, clicking=(local_t > 0.5))

        ann = {0: "Ο ερευνητής επιστρέφει στη σύνδεση αφού εγκριθεί",
               1: "Εισάγετε email",
               2: "Εισάγετε κωδικό",
               3: "Πατήστε «Σύνδεση» – είσοδος στο περιβάλλον ερευνητή"}
        annotation_box(draw, ann[phase], H-52)
        step_indicator(draw, 4, 7)
        frames.append(np.array(img))
    return frames

# ── Scene 7: Research view + mark & submit ─────────────────────────────────────

def draw_research_view(draw, tab=0, selected_row=None, grade=None, submitted=False):
    header_bar(draw, "🔬 Ερευνητής – Expert Mode",
               "Democritus University of Thrace | DDART AI")

    # Tabs
    tabs = ["Εκκρεμείς Εξετάσεις", "Ολοκληρωμένες"]
    tab_bar(draw, 20, 70, W-40, tabs, tab, tab_w=(W-40)//2)

    if tab == 0:
        # List of pending exams
        exams = [
            ("ΕΞ-0042", "01/06/2025", "Γλαύκωμα", "94%", True),
            ("ΕΞ-0041", "30/05/2025", "Γλαύκωμα", "71%", False),
            ("ΕΞ-0039", "29/05/2025", "Γλαύκωμα", "88%", True),
        ]

        for i, (eid, date, spec, conf, high) in enumerate(exams):
            ry = 130 + i * 80
            selected = (selected_row == i)
            bg = (40, 60, 90) if selected else CARD
            bdr = ACCENT if selected else BORDER
            rounded_rect(draw, 20, ry, W-40, 70, 10, bg, outline=bdr, lw=2 if selected else 1)

            f_id = font(16)
            draw.text((40, ry+10), eid, font=f_id, fill=TXT1)
            f_dt = font(12)
            draw.text((40, ry+34), date, font=f_dt, fill=TXT2)

            # Specialty badge
            badge(draw, 170, ry+12, spec, ACCENT)

            # AI confidence
            conf_col = GREEN if float(conf[:-1]) >= 85 else (ORANGE if float(conf[:-1]) >= 75 else RED)
            f_conf = font(14)
            draw.text((W-180, ry+18), f"ΤΝ: {conf}", font=f_conf, fill=conf_col)

            # Review button
            btn_lbl = "Αξιολόγηση →" if not selected else "Επιλεγμένο ✓"
            button(draw, W-170, ry+36, 148, btn_lbl,
                   h=26, color=ACCENT if not selected else GREEN,
                   txt_color=WHITE)

        # Grading panel (shown when a row is selected)
        if selected_row is not None:
            py = 380
            rounded_rect(draw, 20, py, W-40, 280, 12, CARD, outline=BORDER, lw=1)
            f_h = font(17)
            draw.text((40, py+16), "Αξιολόγηση Εικόνας – ΕΞ-0042", font=f_h, fill=TXT1)

            # Simulated retinal image thumbnail
            draw.ellipse([50, py+50, 50+140, py+50+140],
                         fill=(12, 6, 4), outline=(80, 50, 30), width=1)
            import random; random.seed(99)
            for _ in range(10):
                x1 = 120 + random.randint(-40, 40)
                y1 = py+120 + random.randint(-40, 40)
                draw.line([(x1, y1), (x1+random.randint(-25,25),
                            y1+random.randint(-25,25))],
                          fill=(150, 90, 60), width=1)

            # Grade options
            options = [
                ("Παραπομπή",      "Γλαύκωμα πιθανό", RED),
                ("Χωρίς Παραπομπή","Υγιής αμφιβληστροειδής", GREEN),
                ("Αναποφάσιστο",   "Χρειάζεται έλεγχο",  ORANGE),
            ]
            for j, (lbl, desc, col) in enumerate(options):
                ox = 220 + j * 190
                oy = py + 55
                selected_opt = (grade == lbl)
                bg_opt = (*col, 40) if selected_opt else CARD2
                bdr_opt = col if selected_opt else BORDER
                rounded_rect(draw, ox, oy, 170, 80, 8, CARD2, outline=bdr_opt,
                             lw=2 if selected_opt else 1)
                if selected_opt:
                    draw.ellipse([ox+10, oy+10, ox+26, oy+26], fill=col)
                    draw.text((ox+32, oy+8), "✓", font=font(14), fill=col)
                f_opt = font(13)
                draw.text((ox+15, oy+32), lbl, font=f_opt, fill=col)
                f_desc = font(11)
                draw.text((ox+15, oy+54), desc, font=f_desc, fill=TXT2)

            # Comment field
            input_field(draw, 220, py+156, W-260, "Σχόλια (προαιρετικό)", "")

            # Submit
            sub_col = ACCENT if grade else BORDER
            button(draw, 220, py+220, W-260, "Υποβολή Αξιολόγησης",
                   color=sub_col, txt_color=WHITE)

            if submitted:
                # Green success
                rounded_rect(draw, 220, py+220, W-260, 46, 10, GREEN,
                             outline=GREEN, lw=1)
                f_s = font(15)
                draw.text(((W+220)//2, py+220+23), "✓ Υποβλήθηκε επιτυχώς!",
                          font=f_s, fill=WHITE, anchor="mm")

def make_research_view_frames():
    frames = []

    phases = [
        (2.0, "list"),
        (1.5, "click_row"),
        (2.0, "grade_panel"),
        (2.0, "select_grade"),
        (2.0, "submit"),
        (2.5, "submitted"),
    ]
    phase_frames = [int(d * FPS) for d, _ in phases]
    abs_starts = [sum(phase_frames[:i]) for i in range(len(phases))]
    total = sum(phase_frames)

    # cursor target positions
    row_btn_x = W - 96
    row_btn_y = 130 + 52
    grade_opt_x = 220 + 95
    grade_opt_y = 380 + 55 + 40
    sub_btn_x = (W + 220)//2
    sub_btn_y = 380 + 220 + 23

    cur_positions = [
        (W//2, H//2),
        (row_btn_x, row_btn_y),
        (row_btn_x, row_btn_y),
        (grade_opt_x, grade_opt_y),
        (sub_btn_x, sub_btn_y),
        (sub_btn_x, sub_btn_y),
    ]

    for fi in range(total):
        phase = 0
        for i, s in enumerate(abs_starts):
            if fi >= s: phase = i
        local = fi - abs_starts[phase]
        local_t = local / max(1, phase_frames[phase] - 1)
        next_phase = min(phase+1, len(phases)-1)

        cx, cy = lerp_pt(cur_positions[phase], cur_positions[next_phase], local_t)

        selected_row = None if phase == 0 else 0
        grade        = "Παραπομπή" if phase >= 3 else None
        submitted    = (phase == 5)

        img, draw = new_frame()
        draw_research_view(draw, tab=0,
                           selected_row=selected_row,
                           grade=grade,
                           submitted=submitted)

        if phase == 0:
            highlight_box(draw, 20, 130, W-40, 70, "Εκκρεμής εξέταση", ACCENT)

        cursor(draw, int(cx), int(cy),
               clicking=(phase in (1, 3, 4) and local_t > 0.5))

        ann = {
            0: "Λίστα εκκρεμών εξετάσεων – κλικ σε μία για αξιολόγηση",
            1: "Επιλογή εξέτασης ΕΞ-0042 για αξιολόγηση",
            2: "Ο πίνακας αξιολόγησης εμφανίζεται με την εικόνα βυθού",
            3: "Ο ερευνητής επιλέγει: «Παραπομπή» – Γλαύκωμα πιθανό",
            4: "Πατήστε «Υποβολή Αξιολόγησης» για αποθήκευση",
            5: "Η αξιολόγηση υποβλήθηκε! Η εξέταση μεταφέρεται στις ολοκληρωμένες.",
        }
        annotation_box(draw, ann[phase], H-52)
        step_indicator(draw, 6, 7)
        frames.append(np.array(img))
    return frames

# ── Scene 8: End card ─────────────────────────────────────────────────────────

def make_end_frames():
    frames = []
    dur = int(4 * FPS)
    for fi in range(dur):
        t = fi / dur
        img, draw = new_frame()

        # Glow
        for r in range(160, 0, -20):
            draw.ellipse([W//2-r, H//2-r-20, W//2+r, H//2+r-20],
                         outline=(*GREEN, int(20 * (1-r/160))))

        draw.ellipse([W//2-60, H//2-80, W//2+60, H//2-80+120],
                     fill=(20, 55, 35), outline=GREEN, width=2)
        f_chk = font(52)
        draw.text((W//2, H//2-20), "✓", font=f_chk, fill=GREEN, anchor="mm")

        alpha = ease(t * 2)
        c = tuple(int(x * alpha) for x in TXT1)
        c2 = tuple(int(x * alpha) for x in TXT2)

        f_t = font(30)
        msg = "Ολοκλήρωση οδηγού χρήσης"
        bb = draw.textbbox((0,0), msg, font=f_t)
        draw.text(((W-(bb[2]-bb[0]))//2, H//2+70), msg, font=f_t, fill=c)

        f_s = font(16)
        sub_lines = [
            "DDART AI – Πλατφόρμα Οφθαλμολογικού Ελέγχου",
            "Democritus University of Thrace – DDARTECH spin-off",
        ]
        for i, line in enumerate(sub_lines):
            bb = draw.textbbox((0,0), line, font=f_s)
            draw.text(((W-(bb[2]-bb[0]))//2, H//2+112+i*26), line, font=f_s, fill=c2)

        frames.append(np.array(img))
    return frames

# ── Transition (fade to black) ────────────────────────────────────────────────

def fade(frames_a, frames_b, n=15):
    """Cross-fade n frames between two scene lists"""
    result = list(frames_a)
    end_a  = frames_a[-1].astype(float)
    start_b = frames_b[0].astype(float)
    for i in range(n):
        t = (i + 1) / (n + 1)
        blended = ((1 - t) * end_a + t * start_b).astype(np.uint8)
        result.append(blended)
    result.extend(frames_b)
    return result

# ── Main ──────────────────────────────────────────────────────────────────────

def main():
    print("Generating frames…")

    all_scenes = [
        make_title_frames(),
        make_login_overview_frames(),
        make_hc_signin_frames(),
        make_hc_dashboard_frames(),
        make_researcher_signup_frames(),
        make_researcher_signin_frames(),
        make_research_view_frames(),
        make_end_frames(),
    ]

    print("Stitching scenes…")
    combined = all_scenes[0]
    for scene in all_scenes[1:]:
        combined = fade(combined, scene, n=12)

    print(f"Total frames: {len(combined)} ({len(combined)/FPS:.1f}s)")
    print("Encoding video…")
    clip = ImageSequenceClip(combined, fps=FPS)
    clip.write_videofile(OUT, codec="libx264", fps=FPS,
                         audio=False, logger="bar",
                         ffmpeg_params=["-crf", "18", "-preset", "fast"])
    print(f"\nSaved → {OUT}")

if __name__ == "__main__":
    main()
