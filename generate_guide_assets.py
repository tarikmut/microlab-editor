# -*- coding: utf-8 -*-
"""
Generates crisp, high-definition visual infographic assets for MICROLab Editor Help Guide.
"""
import os
from PIL import Image, ImageDraw, ImageFont

ASSETS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets")
os.makedirs(ASSETS_DIR, exist_ok=True)

def get_font(size, bold=False):
    font_names = [
        "C:\\Windows\\Fonts\\segoeuib.ttf" if bold else "C:\\Windows\\Fonts\\segoeui.ttf",
        "C:\\Windows\\Fonts\\arialbd.ttf" if bold else "C:\\Windows\\Fonts\\arial.ttf",
        "C:\\Windows\\Fonts\\calibrib.ttf" if bold else "C:\\Windows\\Fonts\\calibri.ttf"
    ]
    for fn in font_names:
        if os.path.exists(fn):
            try:
                return ImageFont.truetype(fn, size)
            except Exception:
                pass
    return ImageFont.load_default()

def draw_rounded_rect(draw, bbox, radius, fill, outline=None, width=1):
    x0, y0, x1, y1 = bbox
    draw.rounded_rectangle([x0, y0, x1, y1], radius=radius, fill=fill, outline=outline, width=width)

def draw_arrow(draw, start_x, y, length=24, color=(148, 163, 184, 255)):
    # Draw horizontal line and triangle head
    draw.line([(start_x, y), (start_x + length, y)], fill=color, width=2)
    head_x = start_x + length
    draw.polygon([(head_x, y - 5), (head_x + 6, y), (head_x, y + 5)], fill=color)

def generate_workflow_image():
    W, H = 860, 220
    im = Image.new("RGBA", (W, H), (248, 250, 252, 255))
    draw = ImageDraw.Draw(im)

    # Outer border
    draw_rounded_rect(draw, (4, 4, W-5, H-5), 12, fill=(255, 255, 255, 255), outline=(226, 232, 240, 255), width=2)

    # Top title bar
    draw_rounded_rect(draw, (4, 4, W-5, 42), 12, fill=(15, 23, 42, 255))
    draw.rectangle([4, 24, W-5, 42], fill=(15, 23, 42, 255))
    
    font_h = get_font(13, bold=True)
    font_t = get_font(12, bold=True)
    font_d = get_font(10, bold=False)
    font_badge = get_font(10, bold=True)

    draw.text((20, 12), "MICROLab Standalone Calisma & Uretim Akisi", font=font_h, fill=(255, 255, 255, 255))

    steps = [
        ("1. Formu Doldur", "Baslik, ozet ve zengin\nbloklari sirayla ekleyin.", (37, 99, 235), "ADIM 1"),
        ("2. Canli Onizle", "Hot-Reload ile tarayicida\nanlik sonucu izleyin.", (16, 185, 129), "ADIM 2"),
        ("3. Hedef Sec & Kaydet", "Hedef klasore tek tikla\nHTML ve medya aktarimi.", (245, 158, 11), "ADIM 3"),
        ("4. Sitede Yayinda!", "Otomatik dinamik tarama,\nsitede aninda gorunur.", (139, 92, 246), "ADIM 4")
    ]

    card_w = 175
    card_h = 135
    start_x = 22
    spacing = 40
    y_pos = 58

    for i, (title, desc, color, badge_text) in enumerate(steps):
        cx = start_x + i * (card_w + spacing)
        
        # Shadow effect
        draw_rounded_rect(draw, (cx+2, y_pos+2, cx+card_w+2, y_pos+card_h+2), 8, fill=(241, 245, 249, 255))
        draw_rounded_rect(draw, (cx, y_pos, cx+card_w, y_pos+card_h), 8, fill=(255, 255, 255, 255), outline=(226, 232, 240, 255), width=1)
        
        # Color bar top
        draw_rounded_rect(draw, (cx, y_pos, cx+card_w, y_pos+28), 8, fill=color)
        draw.rectangle([cx, y_pos+16, cx+card_w, y_pos+28], fill=color)
        
        # Badge circle with number
        draw.ellipse([cx + 10, y_pos + 6, cx + 24, y_pos + 20], fill=(255, 255, 255, 255))
        draw.text((cx + 14, y_pos + 6), str(i+1), font=get_font(9, bold=True), fill=color)
        draw.text((cx + 32, y_pos + 7), badge_text, font=font_badge, fill=(255, 255, 255, 255))

        draw.text((cx + 10, y_pos + 38), title, font=font_t, fill=(15, 23, 42, 255))
        draw.text((cx + 10, y_pos + 62), desc, font=font_d, fill=(100, 116, 139, 255))

        if i < 3:
            arrow_x = cx + card_w + 6
            draw_arrow(draw, arrow_x, y_pos + 60, length=24)

    out_path = os.path.join(ASSETS_DIR, "guide_workflow.png")
    im.save(out_path, "PNG")
    print("Saved:", out_path)

def generate_load_feature_image():
    W, H = 860, 220
    im = Image.new("RGBA", (W, H), (248, 250, 252, 255))
    draw = ImageDraw.Draw(im)

    draw_rounded_rect(draw, (4, 4, W-5, H-5), 12, fill=(255, 255, 255, 255), outline=(226, 232, 240, 255), width=2)

    # Top header bar
    draw_rounded_rect(draw, (4, 4, W-5, 42), 12, fill=(30, 41, 59, 255))
    draw.rectangle([4, 24, W-5, 42], fill=(30, 41, 59, 255))

    font_h = get_font(13, bold=True)
    font_t = get_font(12, bold=True)
    font_d = get_font(10, bold=False)
    font_badge = get_font(10, bold=True)

    draw.text((20, 12), "Akilli Proje Ice Aktarma & Yukleme Mekanizmasi (Project Loader)", font=font_h, fill=(255, 255, 255, 255))
    
    badge_bg = (245, 158, 11, 255)
    draw_rounded_rect(draw, (W-135, 10, W-18, 34), 6, fill=badge_bg)
    draw.text((W-125, 14), "YENI OZELLIK", font=font_badge, fill=(255, 255, 255, 255))

    steps = [
        ("Hedef Klasor Sec", "Hedef klasoru sectiginizde\nsistem klasoru aninda tarar.", (37, 99, 235), "ASAMA 1"),
        ("Kayitli Projeleri Bul", "projects/data altindaki tum\nprojeler otomatik listelenir.", (14, 165, 233), "ASAMA 2"),
        ("Tek Tikla Ice Aktar", "Baslik, uyeler, yayinlar ve\ntum bloklar forma yuklenir.", (16, 185, 129), "ASAMA 3"),
        ("Duzenle & Guncelle", "Degisiklik yapin, onizleyin\nve yeniden kaydedin.", (99, 102, 241), "ASAMA 4")
    ]

    card_w = 175
    card_h = 135
    start_x = 22
    spacing = 40
    y_pos = 58

    for i, (title, desc, color, badge_text) in enumerate(steps):
        cx = start_x + i * (card_w + spacing)
        
        draw_rounded_rect(draw, (cx+2, y_pos+2, cx+card_w+2, y_pos+card_h+2), 8, fill=(241, 245, 249, 255))
        draw_rounded_rect(draw, (cx, y_pos, cx+card_w, y_pos+card_h), 8, fill=(255, 255, 255, 255), outline=(226, 232, 240, 255), width=1)
        
        draw_rounded_rect(draw, (cx, y_pos, cx+card_w, y_pos+28), 8, fill=color)
        draw.rectangle([cx, y_pos+16, cx+card_w, y_pos+28], fill=color)
        
        draw.ellipse([cx + 10, y_pos + 6, cx + 24, y_pos + 20], fill=(255, 255, 255, 255))
        draw.text((cx + 14, y_pos + 6), str(i+1), font=get_font(9, bold=True), fill=color)
        draw.text((cx + 32, y_pos + 7), badge_text, font=font_badge, fill=(255, 255, 255, 255))

        draw.text((cx + 10, y_pos + 38), title, font=font_t, fill=(15, 23, 42, 255))
        draw.text((cx + 10, y_pos + 62), desc, font=font_d, fill=(100, 116, 139, 255))

        if i < 3:
            arrow_x = cx + card_w + 6
            draw_arrow(draw, arrow_x, y_pos + 60, length=24)

    out_path = os.path.join(ASSETS_DIR, "guide_load_feature.png")
    im.save(out_path, "PNG")
    print("Saved:", out_path)

def generate_blocks_catalog_image():
    W, H = 860, 260
    im = Image.new("RGBA", (W, H), (248, 250, 252, 255))
    draw = ImageDraw.Draw(im)

    draw_rounded_rect(draw, (4, 4, W-5, H-5), 12, fill=(255, 255, 255, 255), outline=(226, 232, 240, 255), width=2)

    # Top header bar
    draw_rounded_rect(draw, (4, 4, W-5, 42), 12, fill=(15, 23, 42, 255))
    draw.rectangle([4, 24, W-5, 42], fill=(15, 23, 42, 255))

    font_h = get_font(13, bold=True)
    font_t = get_font(11, bold=True)
    font_d = get_font(9, bold=False)
    font_badge = get_font(8, bold=True)

    draw.text((20, 12), "Zengin Icerik Bloklari Katalogu (Modular Page Builder)", font=font_h, fill=(255, 255, 255, 255))

    blocks = [
        ("Baslik Bloklari (H2 / H3)", "Bolumleri ana ve alt basliklara ayirarak\nhiyerarsik duzen kurar.", (37, 99, 235), "H2/H3"),
        ("Paragraf Blogu", "Uzun makale ve aciklama metinleri icin.\nCok satirli ve otomatik formatlidir.", (14, 165, 233), "TEXT"),
        ("Tek Gorsel & Slider", "%10 - %100 genislik surgusu, sol/orta/sag\nhizalama ve maksimum yukseklik kontrolu.", (16, 185, 129), "IMG"),
        ("YouTube Video Embed", "Baglanti veya video ID ile responsive\nYouTube video oynatici yerlestirir.", (239, 68, 68), "YOUTUBE"),
        ("Medya Grid Galeri", "2, 3 veya 4 kolonlu yan yana fotograf ve\nvideo galerisi olusturur.", (168, 85, 247), "GRID"),
        ("Vurgu Kutusu (Callout)", "6 farkli ikonla renkli kutu icinde kritik\nduyuru, not veya uyarilari gosterir.", (245, 158, 11), "CALLOUT")
    ]

    card_w = 260
    card_h = 88
    
    for i, (title, desc, color, tag) in enumerate(blocks):
        row = i // 3
        col = i % 3
        cx = 20 + col * (card_w + 16)
        cy = 54 + row * (card_h + 12)

        draw_rounded_rect(draw, (cx+1, cy+1, cx+card_w+1, cy+card_h+1), 8, fill=(241, 245, 249, 255))
        draw_rounded_rect(draw, (cx, cy, cx+card_w, cy+card_h), 8, fill=(255, 255, 255, 255), outline=(226, 232, 240, 255), width=1)
        
        # Left colored accent line
        draw_rounded_rect(draw, (cx, cy, cx+5, cy+card_h), 8, fill=color)
        draw.rectangle([cx+3, cy, cx+5, cy+card_h], fill=color)

        # Small tag pill
        tag_w = 46 if len(tag) > 4 else 34
        draw_rounded_rect(draw, (cx+card_w-tag_w-8, cy+8, cx+card_w-8, cy+22), 4, fill=color)
        draw.text((cx+card_w-tag_w-4, cy+10), tag, font=font_badge, fill=(255, 255, 255, 255))

        draw.text((cx + 12, cy + 10), title, font=font_t, fill=(15, 23, 42, 255))
        draw.text((cx + 12, cy + 32), desc, font=font_d, fill=(100, 116, 139, 255))

    out_path = os.path.join(ASSETS_DIR, "guide_blocks.png")
    im.save(out_path, "PNG")
    print("Saved:", out_path)

def generate_ui_screenshot():
    """Generates an aesthetic mockup of the application interface with the project loader in action."""
    W, H = 860, 420
    im = Image.new("RGBA", (W, H), (241, 245, 249, 255))
    draw = ImageDraw.Draw(im)

    # Window frame
    draw_rounded_rect(draw, (4, 4, W-5, H-5), 10, fill=(255, 255, 255, 255), outline=(203, 213, 225, 255), width=2)

    # Window titlebar (OS style)
    draw_rounded_rect(draw, (4, 4, W-5, 30), 10, fill=(15, 23, 42, 255))
    draw.rectangle([4, 18, W-5, 30], fill=(15, 23, 42, 255))
    
    # 3 dots
    draw.ellipse([14, 11, 22, 19], fill=(239, 68, 68, 255))
    draw.ellipse([28, 11, 36, 19], fill=(245, 158, 11, 255))
    draw.ellipse([42, 11, 50, 19], fill=(16, 185, 129, 255))
    
    font_sm = get_font(9, bold=False)
    font_b = get_font(10, bold=True)
    font_hb = get_font(12, bold=True)
    draw.text((60, 8), "MICROLab Editor v1.0", font=font_sm, fill=(203, 213, 225, 255))

    # App Banner
    draw.rectangle([4, 30, W-5, 68], fill=(30, 41, 59, 255))
    draw.text((20, 36), "MICROLab Editor", font=font_hb, fill=(255, 255, 255, 255))
    draw.text((20, 52), "Web Sitesi Icerik Yonetim Editoru (v1.0)", font=font_sm, fill=(148, 163, 184, 255))
    
    # Top guide button
    draw_rounded_rect(draw, (W-180, 36, W-20, 60), 4, fill=(37, 99, 235, 255))
    draw.text((W-172, 42), "? Kullanim Kilavuzu", font=font_b, fill=(255, 255, 255, 255))

    # Notebook Tabs
    tabs = [
        ("Proje Editoru", True),
        ("Ekip Uyesi", False),
        ("Haber Editoru", False),
        ("Yayin Editoru", False),
        ("Yardim & Rehber", False)
    ]
    tab_x = 20
    tab_y = 74
    for title, is_active in tabs:
        tw = len(title) * 7 + 24
        if is_active:
            draw_rounded_rect(draw, (tab_x, tab_y, tab_x + tw, tab_y + 24), 4, fill=(248, 250, 252, 255), outline=(203, 213, 225, 255), width=1)
            draw.rectangle([tab_x, tab_y + 18, tab_x + tw, tab_y + 25], fill=(248, 250, 252, 255))
            draw.text((tab_x + 12, tab_y + 6), title, font=font_b, fill=(37, 99, 235, 255))
        else:
            draw.text((tab_x + 12, tab_y + 6), title, font=font_sm, fill=(100, 116, 139, 255))
        tab_x += tw + 4

    # Main content split: Left (Form) & Right (Sidebar)
    left_w = 540
    draw_rounded_rect(draw, (16, tab_y + 25, 16 + left_w, H - 15), 6, fill=(248, 250, 252, 255), outline=(226, 232, 240, 255), width=1)
    
    # Inside Left: Section 1
    draw_rounded_rect(draw, (26, tab_y + 35, 16 + left_w - 10, tab_y + 155), 6, fill=(255, 255, 255, 255), outline=(226, 232, 240, 255), width=1)
    draw.text((36, tab_y + 40), "1. Proje Temel Bilgileri", font=font_b, fill=(15, 23, 42, 255))
    
    # Form elements mock
    labels = ["Proje Basligi:", "Etiketler (Tags):", "Durum (Status):"]
    for idx, lb in enumerate(labels):
        ly = tab_y + 65 + idx * 26
        draw.text((36, ly), lb, font=font_sm, fill=(71, 85, 105, 255))
        draw_rounded_rect(draw, (140, ly - 3, 16 + left_w - 20, ly + 18), 3, fill=(248, 250, 252, 255), outline=(203, 213, 225, 255))
    
    # Fill in sample title
    draw.text((146, tab_y + 65), "Autonomous Drone Path Planning", font=font_sm, fill=(15, 23, 42, 255))
    draw.text((146, tab_y + 91), "autonomy, perception, control", font=font_sm, fill=(15, 23, 42, 255))
    draw.text((146, tab_y + 117), "Active", font=font_sm, fill=(16, 185, 129, 255))

    # Section 2: Content blocks mock
    draw_rounded_rect(draw, (26, tab_y + 165, 16 + left_w - 10, H - 25), 6, fill=(255, 255, 255, 255), outline=(226, 232, 240, 255), width=1)
    draw.text((36, tab_y + 172), "3. Proje Sayfa Icerik Bloklari Editoru", font=font_b, fill=(15, 23, 42, 255))
    
    # Block buttons toolbar
    b_types = ["+ Baslik", "+ Paragraf", "+ Tek Gorsel", "+ YouTube", "+ Galeri", "+ Vurgu"]
    bx = 36
    for bt in b_types:
        bw = len(bt) * 6 + 12
        draw_rounded_rect(draw, (bx, tab_y + 195, bx + bw, tab_y + 215), 3, fill=(241, 245, 249, 255), outline=(203, 213, 225, 255))
        draw.text((bx + 6, tab_y + 200), bt, font=get_font(8, bold=True), fill=(37, 99, 235, 255))
        bx += bw + 5

    # Sample block preview
    draw_rounded_rect(draw, (36, tab_y + 225, 16 + left_w - 20, H - 35), 4, fill=(248, 250, 252, 255), outline=(226, 232, 240, 255))
    draw.text((46, tab_y + 232), "Blok #1: HEADING (h2) - Project Overview", font=font_b, fill=(30, 41, 59, 255))
    draw.text((46, tab_y + 252), "Blok #2: PARAGRAPH - This research project addresses autonomous navigation...", font=font_sm, fill=(100, 116, 139, 255))
    draw.text((46, tab_y + 272), "Blok #3: IMAGE - SLAM Terrain Mapping Live Feed (Gorsel: %100 genislik)", font=font_sm, fill=(16, 185, 129, 255))

    # Right side: Sidebar
    right_x = 16 + left_w + 14
    right_w = W - right_x - 20
    draw_rounded_rect(draw, (right_x, tab_y + 25, right_x + right_w, H - 15), 6, fill=(248, 250, 252, 255), outline=(226, 232, 240, 255), width=1)
    
    # Target folder card
    draw_rounded_rect(draw, (right_x + 10, tab_y + 35, right_x + right_w - 10, tab_y + 130), 6, fill=(255, 255, 255, 255), outline=(226, 232, 240, 255))
    draw.text((right_x + 18, tab_y + 42), "Hedef Klasor", font=font_b, fill=(15, 23, 42, 255))
    draw.text((right_x + 18, tab_y + 60), ".../KOM-LAB-WEBSITE-main", font=font_sm, fill=(100, 116, 139, 255))
    
    # Buttons
    draw_rounded_rect(draw, (right_x + 18, tab_y + 78, right_x + right_w - 18, tab_y + 98), 4, fill=(241, 245, 249, 255), outline=(203, 213, 225, 255))
    draw.text((right_x + 28, tab_y + 83), "Hedef Klasor Degistir...", font=font_sm, fill=(30, 41, 59, 255))

    # NEW FEATURE BUTTON IN SIDEBAR
    draw_rounded_rect(draw, (right_x + 18, tab_y + 104, right_x + right_w - 18, tab_y + 124), 4, fill=(37, 99, 235, 255))
    draw.text((right_x + 24, tab_y + 109), "Kayitli Proje Yukle / Ice Aktar", font=get_font(9, bold=True), fill=(255, 255, 255, 255))

    # Action buttons card
    draw_rounded_rect(draw, (right_x + 10, tab_y + 140, right_x + right_w - 10, H - 25), 6, fill=(255, 255, 255, 255), outline=(226, 232, 240, 255))
    draw.text((right_x + 18, tab_y + 148), "Sayfa Uretim & Canli Onizleme", font=font_b, fill=(15, 23, 42, 255))
    
    draw_rounded_rect(draw, (right_x + 18, tab_y + 172, right_x + right_w - 18, tab_y + 204), 4, fill=(16, 185, 129, 255))
    draw.text((right_x + 24, tab_y + 182), "Aktif Sekmedeki Icerigi Uret", font=font_b, fill=(255, 255, 255, 255))

    draw_rounded_rect(draw, (right_x + 18, tab_y + 212, right_x + right_w - 18, tab_y + 242), 4, fill=(241, 245, 249, 255), outline=(203, 213, 225, 255))
    draw.text((right_x + 28, tab_y + 222), "Tarayicida Canli Onizle", font=font_sm, fill=(15, 23, 42, 255))

    # Modal Dialog Overlay Mock (Illustrating the project loader in action!)
    modal_x = 180
    modal_y = 120
    modal_w = 480
    modal_h = 240
    
    # Shadow
    draw_rounded_rect(draw, (modal_x + 6, modal_y + 6, modal_x + modal_w + 6, modal_y + modal_h + 6), 10, fill=(0, 0, 0, 60))
    # Modal Window
    draw_rounded_rect(draw, (modal_x, modal_y, modal_x + modal_w, modal_y + modal_h), 8, fill=(255, 255, 255, 255), outline=(37, 99, 235, 255), width=2)
    
    # Modal Header
    draw_rounded_rect(draw, (modal_x, modal_y, modal_x + modal_w, modal_y + 36), 8, fill=(15, 23, 42, 255))
    draw.rectangle([modal_x, modal_y + 24, modal_x + modal_w, modal_y + 36], fill=(15, 23, 42, 255))
    draw.text((modal_x + 16, modal_y + 10), "Kayitli Projeler Tespit Edildi (Project Loader)", font=font_b, fill=(255, 255, 255, 255))

    draw.text((modal_x + 16, modal_y + 45), "Secilen hedef klasorde 4 kayitli proje bulundu. Duzenlemek icin secin:", font=font_sm, fill=(71, 85, 105, 255))

    # Table / Listbox
    table_y = modal_y + 68
    draw_rounded_rect(draw, (modal_x + 14, table_y, modal_x + modal_w - 14, table_y + 115), 4, fill=(248, 250, 252, 255), outline=(203, 213, 225, 255))
    
    # Row 1 (Selected)
    draw.rectangle([modal_x + 15, table_y + 1, modal_x + modal_w - 15, table_y + 26], fill=(219, 234, 254, 255))
    draw.text((modal_x + 22, table_y + 6), "> Autonomous Drone Path Planning", font=font_b, fill=(29, 78, 216, 255))
    draw.text((modal_x + 360, table_y + 6), "[Active]", font=font_sm, fill=(16, 185, 129, 255))

    # Row 2
    draw.text((modal_x + 22, table_y + 32), "  Planetary Rover Localization & Mapping", font=font_sm, fill=(30, 41, 59, 255))
    draw.text((modal_x + 360, table_y + 32), "[Active]", font=font_sm, fill=(16, 185, 129, 255))

    # Row 3
    draw.text((modal_x + 22, table_y + 58), "  Real-Time Multi-Sensor Object Detection", font=font_sm, fill=(30, 41, 59, 255))
    draw.text((modal_x + 360, table_y + 58), "[Active]", font=font_sm, fill=(16, 185, 129, 255))

    # Row 4
    draw.text((modal_x + 22, table_y + 84), "  Soft Robotics Control Policies", font=font_sm, fill=(30, 41, 59, 255))
    draw.text((modal_x + 360, table_y + 84), "[Completed]", font=font_sm, fill=(100, 116, 139, 255))

    # Modal Action Buttons
    btn_y = modal_y + 195
    draw_rounded_rect(draw, (modal_x + 14, btn_y, modal_x + 220, btn_y + 30), 4, fill=(37, 99, 235, 255))
    draw.text((modal_x + 24, btn_y + 8), "Secilen Projeyi Editore Yukle", font=font_b, fill=(255, 255, 255, 255))

    draw_rounded_rect(draw, (modal_x + 230, btn_y, modal_x + 350, btn_y + 30), 4, fill=(241, 245, 249, 255), outline=(203, 213, 225, 255))
    draw.text((modal_x + 242, btn_y + 8), "Baska Dosya Sec...", font=font_sm, fill=(15, 23, 42, 255))

    draw_rounded_rect(draw, (modal_x + 360, btn_y, modal_x + modal_w - 14, btn_y + 30), 4, fill=(241, 245, 249, 255), outline=(203, 213, 225, 255))
    draw.text((modal_x + 385, btn_y + 8), "Iptal", font=font_sm, fill=(100, 116, 139, 255))

    out_path = os.path.join(ASSETS_DIR, "guide_ui_screenshot.png")
    im.save(out_path, "PNG")
    print("Saved:", out_path)

if __name__ == "__main__":
    generate_workflow_image()
    generate_load_feature_image()
    generate_blocks_catalog_image()
    generate_ui_screenshot()
    print("All updated guide assets generated successfully.")
