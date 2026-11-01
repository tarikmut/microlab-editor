# -*- coding: utf-8 -*-
"""
MICROLab Editor v1.0 (100% Independent)
=======================================
Tamamen Bağımsız (Standalone) Web Sitesi İçerik Yönetim ve Üretim Editörü.
- Canlı önizleme %100 dahili CSS ve JS içerir (Dış dosya yolu gerektirmez).
- Başka bir bilgisayara sadece bu klasör kopyalanıp gönderildiğinde sorunsuz çalışır.
- İçerik kaydederken "Nereye kaydedileceğini" kullanıcıya sorar.
- Görüntü seçilmeyen bloklarda şık canlı SVG görsel yer tutucuları gösterir.
- GitHub üzerinden sunucusuz, ücretsiz otomatik güncelleme altyapısı içerir.
- Tab 0: 🚀 Proje Editörü
- Tab 1: 👤 Ekip Üyesi Editörü
- Tab 2: 📰 Haber Editörü
- Tab 3: 📚 Yayın Editörü
"""

import os
import sys
import re
import json
import shutil
import tempfile
import webbrowser
import datetime
import subprocess
import threading
import hashlib
import ssl
import urllib.request
import urllib.error
from urllib.parse import urlparse
import tkinter as tk
from tkinter import ttk, filedialog, messagebox, simpledialog

# APP VERSION & REPO CONFIG
APP_VERSION = "1.0.0"
DEFAULT_GITHUB_REPO = "tarikmut/microlab-editor"

try:
    from PIL import Image, ImageTk
    PIL_AVAILABLE = True
except ImportError:
    PIL_AVAILABLE = False

# YOUTUBE ID EXTRACTOR
def extract_youtube_id(url):
    if not url: return ""
    patterns = [
        r'(?:v=|\/embed\/|\/v\/|youtu\.be\/|\/shorts\/)([0-9A-Za-z_-]{11})',
        r'^([0-9A-Za-z_-]{11})$'
    ]
    for pattern in patterns:
        match = re.search(pattern, url)
        if match:
            return match.group(1)
    return ""

# ACADEMIC & SOCIAL MEDIA PLATFORMS (WITH OFFICIAL SVG LOGOS)
ACADEMIC_SOCIAL_PLATFORMS = {
    "scholar": {
        "label": "Google Scholar",
        "short": "Scholar",
        "class": "scholar",
        "svg": """<svg viewBox="0 0 24 24" width="16" height="16" fill="currentColor" aria-hidden="true"><path d="M5.242 13.769L0 9.5 12 0l12 9.5-5.242 4.269C17.548 11.249 14.978 9.5 12 9.5c-2.977 0-5.548 1.748-6.758 4.269zM12 10a7 7 0 1 0 0 14 7 7 0 0 0 0-14z"/></svg>""",
        "prefix": "https://scholar.google.com/citations?user="
    },
    "orcid": {
        "label": "ORCID",
        "short": "ORCID",
        "class": "orcid",
        "svg": """<svg viewBox="0 0 24 24" width="16" height="16" fill="currentColor" aria-hidden="true"><path d="M12 0C5.372 0 0 5.372 0 12s5.372 12 12 12 12-5.372 12-12S18.628 0 12 0zM7.369 4.378c.525 0 .947.431.947.947s-.422.947-.947.947a.95.95 0 0 1-.947-.947c0-.525.422-.947.947-.947zm-.722 3.038h1.444v10.041H6.647V7.416zm3.562 0h3.9c3.712 0 5.344 2.653 5.344 5.025 0 2.578-2.016 5.025-5.325 5.025h-3.919V7.416zm1.444 1.306v7.444h2.297c3.272 0 4.022-2.484 4.022-3.722 0-2.016-1.284-3.722-4.097-3.722h-2.222z"/></svg>""",
        "prefix": "https://orcid.org/"
    },
    "researchgate": {
        "label": "ResearchGate",
        "short": "RG",
        "class": "researchgate",
        "svg": """<svg viewBox="0 0 24 24" width="16" height="16" fill="currentColor" aria-hidden="true"><path d="M19.586 0c-.818 0-1.508.19-2.072.565-.563.377-.97.936-1.213 1.68a3.193 3.193 0 0 0-1.128-.854 3.41 3.41 0 0 0-1.505-.333c-.768 0-1.46.182-2.072.547a4.417 4.417 0 0 0-1.536 1.517 4.154 4.154 0 0 0-.583 2.193c0 .823.195 1.554.583 2.193.389.64.901 1.145 1.536 1.517.612.365 1.304.547 2.072.547.568 0 1.07-.11 1.505-.333.436-.222.812-.507 1.128-.854v4.324c0 .878-.204 1.572-.613 2.083-.409.51-1.01.766-1.802.766-.563 0-1.045-.14-1.446-.42a2.38 2.38 0 0 1-.84-1.157l-1.92.8c.373.96 1.002 1.706 1.888 2.24.886.533 1.956.8 3.208.8 1.488 0 2.65-.453 3.486-1.36.836-.906 1.254-2.186 1.254-3.84V6.786h1.76V5.07h-1.76V2.366c.213-.19.497-.285.852-.285.355 0 .684.07.986.213l.747-1.573a4.28 4.28 0 0 0-1.827-.721zM14.73 3.22c.48 0 .89.124 1.228.373.338.249.59.596.757 1.04.167.445.25.96.25 1.547 0 .587-.083 1.102-.25 1.547a2.124 2.124 0 0 1-.757 1.04 2.215 2.215 0 0 1-1.228.373c-.48 0-.89-.124-1.228-.373a2.124 2.124 0 0 1-.757-1.04c-.167-.445-.25-.96-.25-1.547 0-.587.083-1.102.25-1.547.167-.444.42-.791.757-1.04.338-.25.748-.373 1.228-.373z"/></svg>""",
        "prefix": "https://www.researchgate.net/profile/"
    },
    "github": {
        "label": "GitHub",
        "short": "GitHub",
        "class": "github",
        "svg": """<svg viewBox="0 0 24 24" width="16" height="16" fill="currentColor" aria-hidden="true"><path fill-rule="evenodd" clip-rule="evenodd" d="M12 2C6.477 2 2 6.484 2 12.017c0 4.425 2.865 8.18 6.839 9.504.5.092.682-.217.682-.483 0-.237-.008-.868-.013-1.703-2.782.605-3.369-1.343-3.369-1.343-.454-1.158-1.11-1.466-1.11-1.466-.908-.62.069-.608.069-.608 1.003.07 1.53 1.032 1.53 1.032.892 1.53 2.341 1.088 2.91.832.092-.647.35-1.088.636-1.338-2.22-.253-4.555-1.113-4.555-4.951 0-1.093.39-1.988 1.029-2.688-.103-.253-.446-1.272.098-2.65 0 0 .84-.27 2.75 1.026A9.564 9.564 0 0112 6.844c.85.004 1.705.115 2.504.337 1.909-1.296 2.747-1.027 2.747-1.027.546 1.379.202 2.398.1 2.651.64.7 1.028 1.595 1.028 2.688 0 3.848-2.339 4.695-4.566 4.943.359.309.678.92.678 1.855 0 1.338-.012 2.419-.012 2.747 0 .268.18.58.688.482A10.019 10.019 0 0022 12.017C22 6.484 17.522 2 12 2z"/></svg>""",
        "prefix": "https://github.com/"
    },
    "linkedin": {
        "label": "LinkedIn",
        "short": "LinkedIn",
        "class": "linkedin",
        "svg": """<svg viewBox="0 0 24 24" width="16" height="16" fill="currentColor" aria-hidden="true"><path d="M19 3a2 2 0 0 1 2 2v14a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h14m-.5 15.5v-5.3a3.26 3.26 0 0 0-3.26-3.26c-.85 0-1.84.52-2.28 1.3v-1.11h-2.79v8.37h2.79v-4.93c0-.77.62-1.4 1.39-1.4a1.4 1.4 0 0 1 1.4 1.4v4.93h2.75M6.88 8.56a1.68 1.68 0 0 0 1.68-1.68c0-.93-.75-1.69-1.68-1.69a1.69 1.69 0 0 0-1.69 1.69c0 .93.76 1.68 1.69 1.68m1.39 9.94v-8.37H5.5v8.37h2.77z"/></svg>""",
        "prefix": "https://linkedin.com/in/"
    },
    "website": {
        "label": "Website",
        "short": "Web",
        "class": "website",
        "svg": """<svg viewBox="0 0 24 24" width="16" height="16" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><circle cx="12" cy="12" r="10"/><line x1="2" y1="12" x2="22" y2="12"/><path d="M12 2a15.3 15.3 0 0 1 4 10 15.3 15.3 0 0 1-4 10 15.3 15.3 0 0 1-4-10 15.3 15.3 0 0 1 4-10z"/></svg>""",
        "prefix": "https://"
    },
    "email": {
        "label": "Email",
        "short": "Email",
        "class": "email",
        "svg": """<svg viewBox="0 0 24 24" width="16" height="16" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><rect x="2" y="4" width="20" height="16" rx="2"/><path d="m22 7-8.97 5.7a1.94 1.94 0 0 1-2.06 0L2 7"/></svg>""",
        "prefix": "mailto:"
    }
}

def generate_person_social_links_html(meta, compact=False):
    """Generates HTML string with branded SVG icons for all present academic and social links."""
    keys = ["scholar", "orcid", "researchgate", "github", "linkedin", "website", "email"]
    html_parts = []
    for k in keys:
        raw_val = meta.get(k)
        if not raw_val and k == "scholar":
            raw_val = meta.get("google_scholar")
        if not raw_val and k == "orcid":
            raw_val = meta.get("orcid_id")
        if not raw_val and k == "researchgate":
            raw_val = meta.get("rg")

        if raw_val and str(raw_val).strip():
            val = str(raw_val).strip()
            item = ACADEMIC_SOCIAL_PLATFORMS[k]
            prefix = item.get("prefix", "")
            if k == "email":
                clean_email = val.replace("mailto:", "").strip()
                href = f"mailto:{clean_email}"
                target = ""
            elif k == "website":
                href = val if (val.startswith("http://") or val.startswith("https://")) else f"https://{val}"
                target = ' target="_blank" rel="noopener noreferrer"'
            elif val.startswith("http://") or val.startswith("https://"):
                href = val
                target = ' target="_blank" rel="noopener noreferrer"'
            else:
                if k == "github":
                    val = val.lstrip("@")
                href = f"{prefix}{val}"
                target = ' target="_blank" rel="noopener noreferrer"'

            label = item["short"] if compact else item["label"]
            btn_html = (
                f'<a href="{href}"{target} class="social-link-btn {item["class"]}" title="{item["label"]}">'
                f'{item["svg"]}<span>{label}</span></a>'
            )
            html_parts.append(btn_html)
    return " ".join(html_parts)

# EMBEDDED STANDALONE STYLES (main.css) - Included directly in live preview & output files
EMBEDDED_CSS_CONTENT = """/* MICROLab Core Standalone CSS */
:root {
    --bg-main: #f8fafc;
    --bg-card: #ffffff;
    --bg-header: rgba(255, 255, 255, 0.92);
    --bg-alt: #f1f5f9;
    --text-heading: #0f172a;
    --text-body: #334155;
    --text-muted: #64748b;
    --border-subtle: #e2e8f0;
    --primary: #2563eb;
    --primary-hover: #1d4ed8;
    --shadow-sm: 0 4px 15px -3px rgba(15, 23, 42, 0.04);
}

[data-theme="dark"] {
    --bg-main: #0b0f19;
    --bg-card: #151c2c;
    --bg-header: rgba(15, 23, 42, 0.92);
    --bg-alt: #1e293b;
    --text-heading: #f8fafc;
    --text-body: #cbd5e1;
    --text-muted: #94a3b8;
    --border-subtle: #1e293b;
    --primary: #3b82f6;
    --primary-hover: #60a5fa;
}

* { margin: 0; padding: 0; box-sizing: border-box; font-family: 'Inter', -apple-system, sans-serif; }
body { background-color: var(--bg-main); color: var(--text-body); line-height: 1.6; }
a { text-decoration: none; color: inherit; }

header { background-color: var(--bg-header); padding: 18px 50px; display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid var(--border-subtle); position: sticky; top: 0; z-index: 1000; }
.logo { font-size: 1.5rem; font-weight: 800; color: var(--primary); }
nav ul { list-style: none; display: flex; gap: 28px; }
nav ul li a { font-weight: 600; color: var(--text-muted); }

.container { max-width: 1000px; margin: 0 auto; padding: 30px 20px; }
.page-header { background: #0f172a; color: white; padding: 50px 20px; text-align: center; }
.page-header h1 { font-size: 2.2rem; font-weight: 800; }

.blog-content { background: var(--bg-card); padding: 35px; border-radius: 12px; border: 1px solid var(--border-subtle); margin-top: 25px; }
.blog-content h2 { color: var(--text-heading); margin: 25px 0 12px 0; font-size: 1.5rem; }
.blog-content h3 { color: var(--text-heading); margin: 20px 0 10px 0; font-size: 1.25rem; }
.blog-content p { color: var(--text-body); margin-bottom: 16px; font-size: 1.05rem; }

.media-grid { display: grid; gap: 20px; margin: 30px 0; align-items: start; }
@media (max-width: 768px) { .media-grid { grid-template-columns: 1fr !important; } }

.video-embed { position: relative; width: 100%; padding-bottom: 56.25%; height: 0; margin: 0 auto; border-radius: 12px; overflow: hidden; box-shadow: 0 10px 30px rgba(0,0,0,0.15); }
.video-embed iframe { position: absolute; top: 0; left: 0; width: 100%; height: 100%; border: none; }

.callout { display: flex; align-items: flex-start; gap: 14px; background: var(--bg-alt); border-left: 5px solid #f59e0b; border-radius: 8px; padding: 18px 22px; margin: 25px 0; }

/* Profile Card and Academic/Social Badges */
.profile-card { background: var(--bg-card); border-radius: 16px; box-shadow: var(--shadow-sm); border: 1px solid var(--border-subtle); padding: 40px; display: flex; gap: 36px; align-items: center; margin-bottom: 35px; }
.profile-photo { width: 200px; height: 200px; border-radius: 50%; border: 4px solid var(--bg-card); box-shadow: var(--shadow-sm); outline: 2px solid var(--border-subtle); overflow: hidden; flex-shrink: 0; background-color: var(--bg-alt); display: flex; align-items: center; justify-content: center; }
.profile-info { flex: 1; }
.profile-info h1 { font-size: 2.2rem; color: var(--text-heading); margin-bottom: 6px; font-weight: 800; }
.profile-info .role { font-size: 1.1rem; color: var(--primary); font-weight: 600; margin-bottom: 4px; }
.profile-info .department { font-size: 0.98rem; color: var(--text-muted); margin-bottom: 18px; }

.social-links { display: flex; flex-wrap: wrap; gap: 10px; align-items: center; margin-top: 14px; }
.social-link-btn { display: inline-flex; align-items: center; gap: 8px; padding: 7px 15px; border-radius: 8px; font-size: 0.86rem; font-weight: 600; text-decoration: none; color: var(--text-body); background: var(--bg-alt); border: 1px solid var(--border-subtle); box-shadow: 0 1px 3px rgba(15,23,42,0.04); transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1); }
.social-link-btn svg { display: inline-block; width: 16px; height: 16px; flex-shrink: 0; transition: transform 0.2s ease; }
.social-link-btn:hover { transform: translateY(-2px); box-shadow: 0 6px 16px rgba(15,23,42,0.08); }
.social-link-btn:hover svg { transform: scale(1.12); }

.social-link-btn.scholar:hover { background: #4285f4; color: #fff; border-color: #4285f4; }
.social-link-btn.scholar svg { color: #4285f4; }
.social-link-btn.scholar:hover svg { color: #ffffff; }
.social-link-btn.orcid:hover { background: #a6ce39; color: #fff; border-color: #a6ce39; }
.social-link-btn.orcid svg { color: #a6ce39; }
.social-link-btn.orcid:hover svg { color: #ffffff; }
.social-link-btn.researchgate:hover { background: #00ccbb; color: #fff; border-color: #00ccbb; }
.social-link-btn.researchgate svg { color: #00ccbb; }
.social-link-btn.researchgate:hover svg { color: #ffffff; }
.social-link-btn.github:hover { background: #24292e; color: #fff; border-color: #24292e; }
.social-link-btn.github svg { color: #24292e; }
[data-theme="dark"] .social-link-btn.github svg { color: #e2e8f0; }
.social-link-btn.github:hover svg { color: #ffffff; }
[data-theme="dark"] .social-link-btn.github:hover { background: #374151; border-color: #4b5563; }
.social-link-btn.linkedin:hover { background: #0077b5; color: #fff; border-color: #0077b5; }
.social-link-btn.linkedin svg { color: #0077b5; }
.social-link-btn.linkedin:hover svg { color: #ffffff; }
.social-link-btn.website:hover { background: #2563eb; color: #fff; border-color: #2563eb; }
.social-link-btn.website svg { color: #2563eb; }
.social-link-btn.website:hover svg { color: #ffffff; }
.social-link-btn.email:hover { background: #ea4335; color: #fff; border-color: #ea4335; }
.social-link-btn.email svg { color: #ea4335; }
.social-link-btn.email:hover svg { color: #ffffff; }
.social-link-btn.twitter:hover { background: #0f1419; color: #fff; border-color: #0f1419; }
.social-link-btn.twitter svg { color: #0f1419; }
[data-theme="dark"] .social-link-btn.twitter svg { color: #e2e8f0; }
.social-link-btn.twitter:hover svg { color: #ffffff; }

.about-section { background: var(--bg-card); border-radius: 16px; box-shadow: var(--shadow-sm); border: 1px solid var(--border-subtle); padding: 35px; }
.former-members-list { list-style: none; display: grid; grid-template-columns: repeat(auto-fill, minmax(280px, 1fr)); gap: 16px; margin-top: 15px; }
.former-member-item { background: var(--bg-card); padding: 18px 20px; border-radius: 10px; box-shadow: var(--shadow-sm); border: 1px solid var(--border-subtle); border-left: 4px solid var(--primary); }
.former-member-item h4 { color: var(--text-heading); font-size: 1.05rem; font-weight: 700; margin-bottom: 4px; }
.former-member-item p { font-size: 0.88rem; color: var(--text-muted); }

figure img, .blog-content img, .media-grid img { cursor: zoom-in; transition: transform 0.25s ease; }
.back-link { display: inline-block; margin-top: 30px; font-weight: 600; color: var(--primary); }
footer { background-color: #0b0f19; color: #94a3b8; text-align: center; padding: 30px 20px; margin-top: 60px; font-size: 0.9rem; }
"""

# EMBEDDED STANDALONE SCRIPTS (main.js)
EMBEDDED_JS_CONTENT = """/* MICROLab Standalone Main JS */
document.addEventListener("DOMContentLoaded", () => {
    // Lightbox modal initializer
    if (!document.getElementById('lightboxModal')) {
        const lightbox = document.createElement('div');
        lightbox.id = 'lightboxModal';
        lightbox.style.cssText = 'position:fixed;top:0;left:0;width:100vw;height:100vh;background:rgba(11,15,25,0.92);backdrop-filter:blur(10px);z-index:999999;display:flex;flex-direction:column;align-items:center;justify-content:center;opacity:0;visibility:hidden;transition:opacity 0.3s;padding:20px;box-sizing:border-box;';
        lightbox.innerHTML = `
            <div id="lightboxClose" style="position:absolute;top:20px;right:25px;color:#fff;font-size:30px;cursor:pointer;background:rgba(255,255,255,0.2);width:40px;height:40px;border-radius:50%;display:flex;align-items:center;justify-content:center;">&times;</div>
            <img id="lightboxImg" style="max-width:90vw;max-height:82vh;object-fit:contain;border-radius:12px;box-shadow:0 20px 40px rgba(0,0,0,0.6);" alt="Enlarged view">
            <div id="lightboxCaption" style="color:#fff;margin-top:15px;font-size:1rem;text-align:center;"></div>
        `;
        document.body.appendChild(lightbox);

        const closeBtn = document.getElementById('lightboxClose');
        const imgEl = document.getElementById('lightboxImg');
        const capEl = document.getElementById('lightboxCaption');

        function closeLb() { lightbox.style.opacity = '0'; lightbox.style.visibility = 'hidden'; }
        closeBtn.addEventListener('click', closeLb);
        lightbox.addEventListener('click', (e) => { if(e.target === lightbox || e.target === imgEl) closeLb(); });
        document.addEventListener('keydown', (e) => { if(e.key === 'Escape') closeLb(); });

        document.addEventListener('click', (e) => {
            const img = e.target.closest('figure img, .blog-content img, .media-grid img');
            if (img) {
                imgEl.src = img.src;
                const figcap = img.closest('figure') ? img.closest('figure').querySelector('figcaption') : null;
                capEl.textContent = figcap ? figcap.textContent : (img.alt || '');
                lightbox.style.visibility = 'visible';
                lightbox.style.opacity = '1';
            }
        });
    }
});

function getInitialsAvatarSvg(name, size = 180) {
    if (!name || typeof name !== 'string') name = 'RL';
    const nameParts = name.trim().split(/\\s+/);
    let initials = "";
    if (nameParts.length >= 2) {
        initials = (nameParts[0][0] + nameParts[nameParts.length - 1][0]).toUpperCase();
    } else if (nameParts.length === 1 && nameParts[0].length > 0) {
        initials = nameParts[0].substring(0, 2).toUpperCase();
    } else {
        initials = "RL";
    }

    const gradients = [
        ['#2563eb', '#1d4ed8'],
        ['#0891b2', '#0e7490'],
        ['#7c3aed', '#6d28d9'],
        ['#059669', '#047857'],
        ['#d97706', '#b45309'],
        ['#db2777', '#be185d'],
    ];

    let hash = 0;
    for (let i = 0; i < name.length; i++) { hash += name.charCodeAt(i); }
    const pair = gradients[Math.abs(hash) % gradients.length];
    const fontSize = Math.round(size * 0.38);

    return `<svg width="${size}" height="${size}" viewBox="0 0 ${size} ${size}" xmlns="http://www.w3.org/2000/svg" style="width: 100%; height: 100%; display: block; border-radius: inherit;">
        <defs>
            <linearGradient id="avatarGrad-${Math.abs(hash)}" x1="0%" y1="0%" x2="100%" y2="100%">
                <stop offset="0%" stop-color="${pair[0]}" />
                <stop offset="100%" stop-color="${pair[1]}" />
            </linearGradient>
        </defs>
        <rect width="100%" height="100%" fill="url(#avatarGrad-${Math.abs(hash)})" />
        <text x="50%" y="54%" font-family="Inter, -apple-system, sans-serif" font-weight="700" font-size="${fontSize}px" fill="#ffffff" text-anchor="middle" dominant-baseline="middle">${initials}</text>
    </svg>`;
}

function renderMemberPhoto(photoUrl, name, size = 180) {
    if (photoUrl && photoUrl.trim() !== '') {
        return `<img src="${photoUrl}" alt="${name}" class="member-photo-img" style="width: 100%; height: 100%; object-fit: cover;" onerror="this.outerHTML=getInitialsAvatarSvg('${name.replace(/'/g, "\\\\'")}', ${size})">`;
    }
    return getInitialsAvatarSvg(name, size);
}

const SOCIAL_PLATFORMS = {
    scholar: {
        name: "Google Scholar",
        shortName: "Scholar",
        className: "scholar",
        svg: `<svg viewBox="0 0 24 24" width="16" height="16" fill="currentColor" aria-hidden="true"><path d="M5.242 13.769L0 9.5 12 0l12 9.5-5.242 4.269C17.548 11.249 14.978 9.5 12 9.5c-2.977 0-5.548 1.748-6.758 4.269zM12 10a7 7 0 1 0 0 14 7 7 0 0 0 0-14z"/></svg>`,
        normalize: (val) => (val.startsWith("http://") || val.startsWith("https://")) ? val : `https://scholar.google.com/citations?user=${encodeURIComponent(val)}`
    },
    orcid: {
        name: "ORCID",
        shortName: "ORCID",
        className: "orcid",
        svg: `<svg viewBox="0 0 24 24" width="16" height="16" fill="currentColor" aria-hidden="true"><path d="M12 0C5.372 0 0 5.372 0 12s5.372 12 12 12 12-5.372 12-12S18.628 0 12 0zM7.369 4.378c.525 0 .947.431.947.947s-.422.947-.947.947a.95.95 0 0 1-.947-.947c0-.525.422-.947.947-.947zm-.722 3.038h1.444v10.041H6.647V7.416zm3.562 0h3.9c3.712 0 5.344 2.653 5.344 5.025 0 2.578-2.016 5.025-5.325 5.025h-3.919V7.416zm1.444 1.306v7.444h2.297c3.272 0 4.022-2.484 4.022-3.722 0-2.016-1.284-3.722-4.097-3.722h-2.222z"/></svg>`,
        normalize: (val) => (val.startsWith("http://") || val.startsWith("https://")) ? val : `https://orcid.org/${val}`
    },
    researchgate: {
        name: "ResearchGate",
        shortName: "RG",
        className: "researchgate",
        svg: `<svg viewBox="0 0 24 24" width="16" height="16" fill="currentColor" aria-hidden="true"><path d="M19.586 0c-.818 0-1.508.19-2.072.565-.563.377-.97.936-1.213 1.68a3.193 3.193 0 0 0-1.128-.854 3.41 3.41 0 0 0-1.505-.333c-.768 0-1.46.182-2.072.547a4.417 4.417 0 0 0-1.536 1.517 4.154 4.154 0 0 0-.583 2.193c0 .823.195 1.554.583 2.193.389.64.901 1.145 1.536 1.517.612.365 1.304.547 2.072.547.568 0 1.07-.11 1.505-.333.436-.222.812-.507 1.128-.854v4.324c0 .878-.204 1.572-.613 2.083-.409.51-1.01.766-1.802.766-.563 0-1.045-.14-1.446-.42a2.38 2.38 0 0 1-.84-1.157l-1.92.8c.373.96 1.002 1.706 1.888 2.24.886.533 1.956.8 3.208.8 1.488 0 2.65-.453 3.486-1.36.836-.906 1.254-2.186 1.254-3.84V6.786h1.76V5.07h-1.76V2.366c.213-.19.497-.285.852-.285.355 0 .684.07.986.213l.747-1.573a4.28 4.28 0 0 0-1.827-.721zM14.73 3.22c.48 0 .89.124 1.228.373.338.249.59.596.757 1.04.167.445.25.96.25 1.547 0 .587-.083 1.102-.25 1.547a2.124 2.124 0 0 1-.757 1.04 2.215 2.215 0 0 1-1.228.373c-.48 0-.89-.124-1.228-.373a2.124 2.124 0 0 1-.757-1.04c-.167-.445-.25-.96-.25-1.547 0-.587.083-1.102.25-1.547.167-.444.42-.791.757-1.04.338-.25.748-.373 1.228-.373z"/></svg>`,
        normalize: (val) => (val.startsWith("http://") || val.startsWith("https://")) ? val : `https://www.researchgate.net/profile/${val}`
    },
    github: {
        name: "GitHub",
        shortName: "GitHub",
        className: "github",
        svg: `<svg viewBox="0 0 24 24" width="16" height="16" fill="currentColor" aria-hidden="true"><path fill-rule="evenodd" clip-rule="evenodd" d="M12 2C6.477 2 2 6.484 2 12.017c0 4.425 2.865 8.18 6.839 9.504.5.092.682-.217.682-.483 0-.237-.008-.868-.013-1.703-2.782.605-3.369-1.343-3.369-1.343-.454-1.158-1.11-1.466-1.11-1.466-.908-.62.069-.608.069-.608 1.003.07 1.53 1.032 1.53 1.032.892 1.53 2.341 1.088 2.91.832.092-.647.35-1.088.636-1.338-2.22-.253-4.555-1.113-4.555-4.951 0-1.093.39-1.988 1.029-2.688-.103-.253-.446-1.272.098-2.65 0 0 .84-.27 2.75 1.026A9.564 9.564 0 0112 6.844c.85.004 1.705.115 2.504.337 1.909-1.296 2.747-1.027 2.747-1.027.546 1.379.202 2.398.1 2.651.64.7 1.028 1.595 1.028 2.688 0 3.848-2.339 4.695-4.566 4.943.359.309.678.92.678 1.855 0 1.338-.012 2.419-.012 2.747 0 .268.18.58.688.482A10.019 10.019 0 0022 12.017C22 6.484 17.522 2 12 2z"/></svg>`,
        normalize: (val) => (val.startsWith("http://") || val.startsWith("https://")) ? val : `https://github.com/${val.replace(/^@/, '')}`
    },
    linkedin: {
        name: "LinkedIn",
        shortName: "LinkedIn",
        className: "linkedin",
        svg: `<svg viewBox="0 0 24 24" width="16" height="16" fill="currentColor" aria-hidden="true"><path d="M19 3a2 2 0 0 1 2 2v14a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h14m-.5 15.5v-5.3a3.26 3.26 0 0 0-3.26-3.26c-.85 0-1.84.52-2.28 1.3v-1.11h-2.79v8.37h2.79v-4.93c0-.77.62-1.4 1.39-1.4a1.4 1.4 0 0 1 1.4 1.4v4.93h2.75M6.88 8.56a1.68 1.68 0 0 0 1.68-1.68c0-.93-.75-1.69-1.68-1.69a1.69 1.69 0 0 0-1.69 1.69c0 .93.76 1.68 1.69 1.68m1.39 9.94v-8.37H5.5v8.37h2.77z"/></svg>`,
        normalize: (val) => (val.startsWith("http://") || val.startsWith("https://")) ? val : `https://linkedin.com/in/${val}`
    },
    website: {
        name: "Website",
        shortName: "Web",
        className: "website",
        svg: `<svg viewBox="0 0 24 24" width="16" height="16" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><circle cx="12" cy="12" r="10"/><line x1="2" y1="12" x2="22" y2="12"/><path d="M12 2a15.3 15.3 0 0 1 4 10 15.3 15.3 0 0 1-4 10 15.3 15.3 0 0 1-4-10 15.3 15.3 0 0 1 4-10z"/></svg>`,
        normalize: (val) => (val.startsWith("http://") || val.startsWith("https://")) ? val : `https://${val}`
    },
    email: {
        name: "Email",
        shortName: "Email",
        className: "email",
        svg: `<svg viewBox="0 0 24 24" width="16" height="16" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><rect x="2" y="4" width="20" height="16" rx="2"/><path d="m22 7-8.97 5.7a1.94 1.94 0 0 1-2.06 0L2 7"/></svg>`,
        normalize: (val) => val.startsWith("mailto:") ? val : `mailto:${val}`
    }
};

function renderSocialLinks(personData, compact = false) {
    if (!personData || typeof personData !== 'object') return '';
    const linkMap = {
        scholar: personData.scholar || personData.google_scholar,
        orcid: personData.orcid || personData.orcid_id,
        researchgate: personData.researchgate || personData.rg,
        github: personData.github,
        linkedin: personData.linkedin,
        website: personData.website,
        email: personData.email
    };
    const keys = ['scholar', 'orcid', 'researchgate', 'github', 'linkedin', 'website', 'email'];
    let html = '';
    for (const key of keys) {
        const rawVal = linkMap[key];
        if (rawVal && typeof rawVal === 'string' && rawVal.trim() !== '') {
            const platform = SOCIAL_PLATFORMS[key];
            if (!platform) continue;
            const url = platform.normalize(rawVal.trim());
            const isEmail = key === 'email';
            const targetAttr = isEmail ? '' : 'target="_blank" rel="noopener noreferrer"';
            const label = compact ? platform.shortName : platform.name;
            html += `<a href="${url}" ${targetAttr} class="social-link-btn ${platform.className}" title="${platform.name}">${platform.svg}<span>${label}</span></a>`;
        }
    }
    return html;
}
"""

# HTML TEMPLATES WITH INLINE & FALLBACK STYLES
PROJECT_HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{TITLE}} | MICROLab</title>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="../../css/main.css">
    <link rel="stylesheet" href="../css/main.css">
    <link rel="stylesheet" href="css/main.css">
    <style>{{EMBEDDED_CSS}}</style>
</head>
<body>
    <header>
        <div class="logo">MICROLab</div>
        <nav>
            <ul>
                <li><a href="../../index.html">Home</a></li>
                <li><a href="../../people/index.html">People</a></li>
                <li><a href="../../projects/index.html" style="color: #2563eb;">Projects</a></li>
                <li><a href="../../publications.html">Publications</a></li>
                <li><a href="../../news/index.html">News</a></li>
            </ul>
        </nav>
    </header>

    <div class="page-header" style="{{HEADER_STYLE}}">
        <h1>{{TITLE}}</h1>
    </div>

    <div class="container">
        <div class="blog-content">
            {{PROJECT_META_HTML}}

            {{CONTENT_BODY_HTML}}

            <h2>Team Members</h2>
            <div class="members-grid" id="projectMembersGrid" style="display:flex; flex-wrap:wrap; gap:15px; margin-bottom: 30px;">
                {{TEAM_MEMBERS_HTML}}
            </div>

            {{PUBLICATIONS_SECTION_HTML}}
            
            <a href="../index.html" class="back-link">&larr; Back to Projects Hub</a>
        </div>
    </div>

    <footer>
        <p>&copy; 2026 Yildiz Technical University - MICROLab. All rights reserved.</p>
    </footer>
    {{LIVE_RELOAD_SCRIPT}}
    <script src="../../js/main.js"></script>
    <script src="../js/main.js"></script>
    <script src="js/main.js"></script>
    <script>{{EMBEDDED_JS}}</script>
</body>
</html>

<!--
PROJECT_METADATA:
{{METADATA_JSON}}
-->
"""

PERSON_HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{NAME}} | MICROLab</title>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="../../css/main.css">
    <link rel="stylesheet" href="../css/main.css">
    <link rel="stylesheet" href="css/main.css">
    <style>{{EMBEDDED_CSS}}</style>
</head>
<body>
    <header>
        <div class="logo">MICROLab</div>
        <nav>
            <ul>
                <li><a href="../../index.html">Home</a></li>
                <li><a href="../index.html" style="color: #2563eb;">People</a></li>
                <li><a href="../../projects/index.html">Projects</a></li>
                <li><a href="../../publications.html">Publications</a></li>
                <li><a href="../../news/index.html">News</a></li>
            </ul>
        </nav>
    </header>

    <div class="page-header">
        <h1>Team Member Profile</h1>
    </div>

    <div class="container">
        <div class="profile-card">
            <div class="profile-photo" id="personProfilePhoto">
                {{PHOTO_HTML}}
            </div>
            <div class="profile-info">
                <h1>{{NAME}}</h1>
                <p class="role">{{ROLE}}</p>
                <p class="department">{{DEPARTMENT}}</p>
                <div class="social-links">
                    {{SOCIAL_LINKS_HTML}}
                </div>
            </div>
        </div>

        <div class="about-section">
            <h2>About Me</h2>
            {{ABOUT_HTML}}
        </div>

        <div class="about-section" style="margin-top: 40px;">
            <h2>Projects</h2>
            <ul class="former-members-list" id="personProjectsList" style="grid-template-columns: 1fr;">
                <!-- Dinamik Projeler Buraya Gelecek -->
            </ul>
        </div>
    </div>

    <footer>
        <p>&copy; 2026 Yildiz Technical University - MICROLab. All rights reserved.</p>
        <p>Contact: info@microlab.edu.tr</p>
    </footer>
    {{LIVE_RELOAD_SCRIPT}}
    <script src="../../js/main.js"></script>
    <script src="../js/main.js"></script>
    <script src="js/main.js"></script>
    <script>{{EMBEDDED_JS}}</script>
    <script>
        document.addEventListener('DOMContentLoaded', () => {
            const projectsList = document.getElementById('personProjectsList');
            if (!projectsList) return;
            
            const commentNode = Array.from(document.childNodes).find(
                node => node.nodeType === Node.COMMENT_NODE && node.nodeValue.includes('PERSON_METADATA')
            );
            if (!commentNode) return;
            
            const match = commentNode.nodeValue.match(/PERSON_METADATA:\s*([\s\S]*)/);
            if (!match) return;
            
            let personData;
            try {
                personData = JSON.parse(match[1]);
                const photoEl = document.getElementById('personProfilePhoto');
                if (photoEl && typeof renderMemberPhoto === 'function') {
                    photoEl.innerHTML = renderMemberPhoto(personData.photo, personData.name, 220);
                }
                const socialEl = document.querySelector('.profile-info .social-links');
                if (socialEl && typeof renderSocialLinks === 'function') {
                    const linksHtml = renderSocialLinks(personData);
                    if (linksHtml) socialEl.innerHTML = linksHtml;
                }
            } catch (e) {
                console.error("Failed to parse person metadata:", e);
                return;
            }
            
            fetch('../../projects/data/')
                .then(res => res.text())
                .then(html => {
                    const parser = new DOMParser();
                    const doc = parser.parseFromString(html, 'text/html');
                    const links = Array.from(doc.querySelectorAll('a'))
                        .map(a => a.getAttribute('href'))
                        .filter(href => href && href.endsWith('.html') && href !== 'index.html' && href !== 'template.html');

                    return Promise.all(links.map(link => 
                        fetch('../../projects/data/' + link)
                            .then(r => r.text())
                            .then(content => {
                                const m = content.match(/<!--\s*PROJECT_METADATA:\s*([\s\S]*?)\s*-->/);
                                if (m) {
                                    const projData = JSON.parse(m[1]);
                                    projData.url = '../../projects/data/' + link;
                                    return projData;
                                }
                                return null;
                            }).catch(() => null)
                    ));
                })
                .then(projects => {
                    const matchedProjects = projects.filter(p => p !== null && p.team && p.team.some(member => {
                        const name = typeof member === 'string' ? member : member.name;
                        return name && name.toLowerCase().trim() === personData.name.toLowerCase().trim();
                    }));
                    
                    projectsList.innerHTML = '';
                    if (matchedProjects.length === 0) {
                        projectsList.innerHTML = '<li class="former-member-item"><p style="margin-bottom: 0; color: #a0aec0;">No active projects listed.</p></li>';
                        return;
                    }
                    
                    matchedProjects.forEach(proj => {
                        const item = document.createElement('li');
                        item.className = 'former-member-item';
                        item.style.borderLeftColor = '#2563eb';
                        item.innerHTML = `
                            <h4><a href="${proj.url}" style="color: inherit; font-weight: 600;">${proj.title}</a></h4>
                            <p style="margin-bottom: 0;">${proj.short_description || ''}</p>
                        `;
                        projectsList.appendChild(item);
                    });
                })
                .catch(() => {});
        });
    </script>
</body>
</html>

<!--
PERSON_METADATA:
{{METADATA_JSON}}
-->
"""

NEWS_HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{TITLE}} | MICROLab News</title>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="../../css/main.css">
    <link rel="stylesheet" href="../css/main.css">
    <link rel="stylesheet" href="css/main.css">
    <style>{{EMBEDDED_CSS}}</style>
</head>
<body>
    <header>
        <div class="logo">MICROLab</div>
        <nav>
            <ul>
                <li><a href="../../index.html">Home</a></li>
                <li><a href="../../people/index.html">People</a></li>
                <li><a href="../../projects/index.html">Projects</a></li>
                <li><a href="../../publications.html">Publications</a></li>
                <li><a href="../index.html" style="color: #2563eb;">News</a></li>
            </ul>
        </nav>
    </header>

    <div class="page-header">
        <h1>{{TITLE}}</h1>
        <div style="margin-top: 10px; color: #94a3b8; font-weight: 600;">{{DATE}} &bull; {{CATEGORY}}</div>
    </div>

    <div class="container">
        <div class="blog-content">
            {{CONTENT_BODY_HTML}}
            <a href="../index.html" class="back-link">&larr; Back to News Articles</a>
        </div>
    </div>

    <footer>
        <p>&copy; 2026 Yildiz Technical University - MICROLab. All rights reserved.</p>
    </footer>
    {{LIVE_RELOAD_SCRIPT}}
    <script src="../../js/main.js"></script>
    <script src="../js/main.js"></script>
    <script src="js/main.js"></script>
    <script>{{EMBEDDED_JS}}</script>
</body>
</html>

<!--
NEWS_METADATA:
{{METADATA_JSON}}
-->
"""

PUBLICATION_HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{TITLE}} | Publication</title>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="../../css/main.css">
    <link rel="stylesheet" href="../css/main.css">
    <link rel="stylesheet" href="css/main.css">
    <style>{{EMBEDDED_CSS}}</style>
</head>
<body>
    <header>
        <div class="logo">MICROLab</div>
        <nav>
            <ul>
                <li><a href="../../index.html">Home</a></li>
                <li><a href="../../publications.html" style="color: #2563eb;">Publications</a></li>
            </ul>
        </nav>
    </header>

    <div class="page-header">
        <h1>Research Publication</h1>
    </div>

    <div class="container">
        <div class="blog-content">
            <h1 style="font-size: 1.5rem; margin-bottom: 12px;">{{TITLE}}</h1>
            <p style="font-size: 1.1rem; margin-bottom: 10px;">{{AUTHORS}}</p>
            <p style="font-size: 1rem; color: #64748b; margin-bottom: 20px;">{{VENUE}} ({{YEAR}})</p>
            {{LINKS_HTML}}
            <a href="../../publications.html" class="back-link">&larr; Back to Publications</a>
        </div>
    </div>

    <footer>
        <p>&copy; 2026 Yildiz Technical University - MICROLab. All rights reserved.</p>
    </footer>
    {{LIVE_RELOAD_SCRIPT}}
    <script src="../../js/main.js"></script>
    <script src="../js/main.js"></script>
    <script src="js/main.js"></script>
    <script>{{EMBEDDED_JS}}</script>
</body>
</html>

<!--
PUBLICATION_METADATA:
{{METADATA_JSON}}
-->
"""

def slugify(text):
    text = text.lower().strip()
    text = text.replace('ı', 'i').replace('ğ', 'g').replace('ü', 'u').replace('ş', 's').replace('ö', 'o').replace('ç', 'c')
    text = re.sub(r'[^a-z0-9]+', '_', text)
    cleaned = text.strip('_')
    return cleaned if cleaned else "untitled"

# SVG PLACEHOLDER FOR PREVIEW
def get_svg_placeholder(label="Görsel Seçi̇lmedi̇"):
    return f"data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' width='800' height='400' viewBox='0 0 800 400'><rect width='100%' height='100%' fill='%231e293b'/><text x='50%' y='50%' fill='%2394a3b8' font-family='sans-serif' font-size='24' font-weight='bold' text-anchor='middle' dominant-baseline='middle'>📷 {label}</text></svg>"

# MOUSEWHEEL HELPER
def bind_mouse_wheel(widget, canvas):
    def _on_mousewheel(event):
        if sys.platform == "darwin":
            canvas.yview_scroll(int(-1 * event.delta), "units")
        else:
            canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

    widget.bind("<MouseWheel>", _on_mousewheel)
    widget.bind("<Button-4>", lambda e: canvas.yview_scroll(-1, "units"))
    widget.bind("<Button-5>", lambda e: canvas.yview_scroll(1, "units"))

    for child in widget.winfo_children():
        bind_mouse_wheel(child, canvas)

# CONTENT BLOCK EDITOR
class ContentBlockEditor(ttk.LabelFrame):
    def __init__(self, parent, parent_canvas=None, title=" 📝 Sayfa İçerik Blokları Editörü "):
        super().__init__(parent, text=title)
        self.blocks = []
        self.parent_canvas = parent_canvas
        self.create_ui()

    def create_ui(self):
        btn_bar = ttk.Frame(self)
        btn_bar.pack(fill="x", padx=10, pady=8)

        ttk.Label(btn_bar, text="Yeni Blok Ekle:", font=('Inter', 9, 'bold')).pack(side="left", padx=(0, 8))
        
        ttk.Button(btn_bar, text="+ Başlık", command=lambda: self.add_block('heading')).pack(side="left", padx=3)
        ttk.Button(btn_bar, text="+ Paragraf", command=lambda: self.add_block('paragraph')).pack(side="left", padx=3)
        ttk.Button(btn_bar, text="+ Tek Görsel", command=lambda: self.add_block('image')).pack(side="left", padx=3)
        ttk.Button(btn_bar, text="+ Tek YouTube Video", command=lambda: self.add_block('youtube')).pack(side="left", padx=3)
        ttk.Button(btn_bar, text="+ 🖼️ Yan Yana Medya Galerisi (Grid)", command=lambda: self.add_block('gallery')).pack(side="left", padx=3)
        ttk.Button(btn_bar, text="+ Vurgu Kutusu", command=lambda: self.add_block('callout')).pack(side="left", padx=3)

        self.blocks_container = ttk.Frame(self)
        self.blocks_container.pack(fill="x", expand=True, padx=10, pady=5)

    def add_block(self, btype, data=None):
        block_frame = ttk.LabelFrame(self.blocks_container, text=f" Blok #{len(self.blocks)+1}: {btype.upper()} ")
        block_frame.pack(fill="x", expand=True, padx=2, pady=6)

        block_obj = {'type': btype, 'frame': block_frame, 'widgets': {}}

        ctrl_frame = ttk.Frame(block_frame)
        ctrl_frame.pack(fill="x", padx=5, pady=2)

        ttk.Button(ctrl_frame, text="▲ Yukarı", width=7, command=lambda: self.move_block(block_obj, -1)).pack(side="left", padx=2)
        ttk.Button(ctrl_frame, text="▼ Aşağı", width=7, command=lambda: self.move_block(block_obj, 1)).pack(side="left", padx=2)
        ttk.Button(ctrl_frame, text="✕ Sil", width=6, command=lambda: self.remove_block(block_obj)).pack(side="right", padx=2)

        help_desc_map = {
            'heading': "ℹ️ Açıklama: Sayfa içine alt başlık ekler. 'h2' Ana Bölüm Başlığı, 'h3' ise Alt Bölüm Başlığıdır.",
            'paragraph': "ℹ️ Açıklama: Ana metin içeriğinizi buraya yazın.",
            'image': "ℹ️ Açıklama: Fotoğraf ekler. Sürgüyü (Slider) çekerek genişliğini ve hizalamasını ayarlayabilirsiniz.",
            'youtube': "ℹ️ Açıklama: YouTube videosu ekler. Herhangi bir YouTube video bağlantısını yapıştırıp sürgü ile genişliğini ayarlayabilirsiniz.",
            'gallery': "ℹ️ Açıklama: 2, 3 veya 4 adet fotoğraf/videoyu yan yana sıralar.",
            'callout': "ℹ️ Açıklama: Önemli duyuruları dikkat çekici renkli bilgi kutusunda gösterir."
        }
        
        info_lbl = ttk.Label(block_frame, text=help_desc_map.get(btype, ""), font=('Inter', 8, 'italic'), foreground='#2563eb', wraplength=700)
        info_lbl.pack(anchor="w", padx=8, pady=(2, 6))

        if btype == 'heading':
            f = ttk.Frame(block_frame)
            f.pack(fill="x", padx=5, pady=4)
            ttk.Label(f, text="Seviye:").pack(side="left")
            lvl_combo = ttk.Combobox(f, values=['h2', 'h3'], width=5, state="readonly")
            lvl_combo.set(data.get('level', 'h3') if data else 'h3')
            lvl_combo.pack(side="left", padx=5)

            ttk.Label(f, text="Başlık Metni:").pack(side="left", padx=(10, 5))
            txt_entry = ttk.Entry(f)
            txt_entry.insert(0, data.get('text', '') if data else '')
            txt_entry.pack(side="left", fill="x", expand=True)
            block_obj['widgets'] = {'level': lvl_combo, 'text': txt_entry}

        elif btype == 'paragraph':
            txt = tk.Text(block_frame, height=5, font=('Inter', 9), wrap="word")
            txt.pack(fill="x", padx=5, pady=4)
            if data and 'text' in data:
                txt.insert("1.0", data['text'])
            block_obj['widgets'] = {'text': txt}

        elif btype == 'image':
            f = ttk.Frame(block_frame)
            f.pack(fill="x", padx=5, pady=4)
            
            ttk.Label(f, text="Görsel Dosyası:").grid(row=0, column=0, sticky="w")
            path_entry = ttk.Entry(f, width=45)
            path_entry.insert(0, data.get('path', '') if data else '')
            path_entry.grid(row=0, column=1, padx=5, sticky="ew")

            def browse_img():
                p = filedialog.askopenfilename(filetypes=[("Images", "*.png;*.jpg;*.jpeg;*.svg;*.webp")])
                if p:
                    path_entry.delete(0, tk.END)
                    path_entry.insert(0, p)

            ttk.Button(f, text="Görsel Seç...", command=browse_img).grid(row=0, column=2, padx=2)

            ttk.Label(f, text="Altyazı (Caption):").grid(row=1, column=0, sticky="w", pady=4)
            cap_entry = ttk.Entry(f)
            cap_entry.insert(0, data.get('caption', '') if data else '')
            cap_entry.grid(row=1, column=1, columnspan=2, padx=5, sticky="ew", pady=4)

            f_w = ttk.Frame(f)
            f_w.grid(row=2, column=0, columnspan=3, sticky="w", pady=4)

            ttk.Label(f_w, text="Genişlik (Width %):", font=('Inter', 9, 'bold')).pack(side="left")

            init_w = '100'
            if data and 'width' in data:
                m = re.search(r'\d+', data['width'])
                if m: init_w = m.group(0)

            val_lbl = ttk.Label(f_w, text=f"{init_w}%", width=5, font=('Inter', 9, 'bold'), foreground='#2563eb')

            def update_w_lbl(val):
                val_lbl.config(text=f"{int(float(val))}%")

            slider = ttk.Scale(f_w, from_=10, to=100, orient="horizontal", command=update_w_lbl, length=180)
            try: slider.set(float(init_w))
            except Exception: slider.set(100)
            slider.pack(side="left", padx=8)
            val_lbl.pack(side="left", padx=2)

            for pct in [100, 75, 50, 35]:
                def make_preset_cmd(p=pct, s=slider, l=val_lbl):
                    return lambda: (s.set(p), l.config(text=f"{p}%"))
                ttk.Button(f_w, text=f"{pct}%", width=5, command=make_preset_cmd(pct, slider, val_lbl)).pack(side="left", padx=2)

            f_h = ttk.Frame(f)
            f_h.grid(row=3, column=0, columnspan=3, sticky="w", pady=4)

            ttk.Label(f_h, text="Hizalama:").pack(side="left")
            align_combo = ttk.Combobox(f_h, values=['Center', 'Left', 'Right'], width=8, state="readonly")
            align_combo.set(data.get('align', 'Center') if data else 'Center')
            align_combo.pack(side="left", padx=5)

            ttk.Label(f_h, text="Maks Yükseklik:").pack(side="left", padx=(15, 5))
            maxh_combo = ttk.Combobox(f_h, values=['Auto (Sınırsız)', '500px', '400px', '300px', '200px'], width=14, state="readonly")
            maxh_combo.set(data.get('max_height', 'Auto (Sınırsız)') if data else 'Auto (Sınırsız)')
            maxh_combo.pack(side="left", padx=5)

            f.columnconfigure(1, weight=1)
            block_obj['widgets'] = {'path': path_entry, 'caption': cap_entry, 'slider': slider, 'align': align_combo, 'max_height': maxh_combo}

        elif btype == 'youtube':
            f = ttk.Frame(block_frame)
            f.pack(fill="x", padx=5, pady=4)

            ttk.Label(f, text="YouTube Linki veya Video ID:").grid(row=0, column=0, sticky="w")
            url_entry = ttk.Entry(f)
            url_entry.insert(0, data.get('url', '') if data else '')
            url_entry.grid(row=0, column=1, columnspan=2, padx=5, sticky="ew")

            f_w = ttk.Frame(f)
            f_w.grid(row=1, column=0, columnspan=3, sticky="w", pady=4)

            ttk.Label(f_w, text="Video Genişliği (Width %):", font=('Inter', 9, 'bold')).pack(side="left")

            init_w = '100'
            if data and 'width' in data:
                m = re.search(r'\d+', data['width'])
                if m: init_w = m.group(0)

            val_lbl = ttk.Label(f_w, text=f"{init_w}%", width=5, font=('Inter', 9, 'bold'), foreground='#2563eb')

            def update_w_lbl(val):
                val_lbl.config(text=f"{int(float(val))}%")

            slider = ttk.Scale(f_w, from_=20, to=100, orient="horizontal", command=update_w_lbl, length=180)
            try: slider.set(float(init_w))
            except Exception: slider.set(100)
            slider.pack(side="left", padx=8)
            val_lbl.pack(side="left", padx=2)

            for pct in [100, 80, 60, 50]:
                def make_yt_preset_cmd(p=pct, s=slider, l=val_lbl):
                    return lambda: (s.set(p), l.config(text=f"{p}%"))
                ttk.Button(f_w, text=f"{pct}%", width=5, command=make_yt_preset_cmd(pct, slider, val_lbl)).pack(side="left", padx=2)

            f.columnconfigure(1, weight=1)
            block_obj['widgets'] = {'url': url_entry, 'slider': slider}

        elif btype == 'gallery':
            f = ttk.Frame(block_frame)
            f.pack(fill="x", padx=5, pady=4)

            f_cols = ttk.Frame(f)
            f_cols.pack(fill="x", pady=2)
            ttk.Label(f_cols, text="Düzen (Yan yana kaç medya):", font=('Inter', 9, 'bold')).pack(side="left")
            cols_combo = ttk.Combobox(f_cols, values=['2 Kolon (Yan Yana 2)', '3 Kolon (Yan Yana 3)', '4 Kolon (Yan Yana 4)'], width=22, state="readonly")
            cols_combo.set(data.get('cols', '2 Kolon (Yan Yana 2)') if data else '2 Kolon (Yan Yana 2)')
            cols_combo.pack(side="left", padx=6)

            items_container = ttk.Frame(f)
            items_container.pack(fill="x", padx=2, pady=6)

            gallery_items = []

            def add_gallery_item(itype='image', item_data=None):
                item_frame = ttk.LabelFrame(items_container, text=f" Öğe ({itype.upper()}) ")
                item_frame.pack(fill="x", padx=2, pady=4)

                item_obj = {'type': itype, 'frame': item_frame}

                if itype == 'image':
                    f_row = ttk.Frame(item_frame)
                    f_row.pack(fill="x", padx=4, pady=2)
                    ttk.Label(f_row, text="Görsel:").pack(side="left")
                    p_entry = ttk.Entry(f_row, width=32)
                    p_entry.insert(0, item_data.get('path', '') if item_data else '')
                    p_entry.pack(side="left", padx=4)

                    def browse_gal_img(pe=p_entry):
                        p = filedialog.askopenfilename(filetypes=[("Images", "*.png;*.jpg;*.jpeg;*.svg;*.webp")])
                        if p:
                            pe.delete(0, tk.END)
                            pe.insert(0, p)

                    ttk.Button(f_row, text="Gözat...", command=browse_gal_img).pack(side="left", padx=2)

                    ttk.Label(f_row, text="Altyazı:").pack(side="left", padx=(8, 2))
                    c_entry = ttk.Entry(f_row, width=20)
                    c_entry.insert(0, item_data.get('caption', '') if item_data else '')
                    c_entry.pack(side="left", padx=2)

                    item_obj['path'] = p_entry
                    item_obj['caption'] = c_entry

                elif itype == 'youtube':
                    f_row = ttk.Frame(item_frame)
                    f_row.pack(fill="x", padx=4, pady=2)
                    ttk.Label(f_row, text="YouTube URL/ID:").pack(side="left")
                    u_entry = ttk.Entry(f_row, width=45)
                    u_entry.insert(0, item_data.get('url', '') if item_data else '')
                    u_entry.pack(side="left", padx=4)
                    item_obj['url'] = u_entry

                def remove_gal_item(io=item_obj):
                    io['frame'].destroy()
                    if io in gallery_items: gallery_items.remove(io)

                ttk.Button(f_row if itype=='image' or itype=='youtube' else item_frame, text="✕", width=3, command=remove_gal_item).pack(side="right", padx=2)
                gallery_items.append(item_obj)

            btn_bar_gal = ttk.Frame(f)
            btn_bar_gal.pack(fill="x", pady=4)
            ttk.Button(btn_bar_gal, text="+ Görsel Ögesi Ekle", command=lambda: add_gallery_item('image')).pack(side="left", padx=2)
            ttk.Button(btn_bar_gal, text="+ YouTube Video Ögesi Ekle", command=lambda: add_gallery_item('youtube')).pack(side="left", padx=2)

            if data and 'items' in data:
                for item in data['items']:
                    add_gallery_item(item.get('type', 'image'), item)
            else:
                add_gallery_item('image')
                add_gallery_item('image')

            block_obj['widgets'] = {'cols': cols_combo, 'items': gallery_items}

        elif btype == 'callout':
            f = ttk.Frame(block_frame)
            f.pack(fill="x", padx=5, pady=4)
            ttk.Label(f, text="İkon:").pack(side="left")
            icon_combo = ttk.Combobox(f, values=['ℹ️', '⚠️', '🚀', '💡', '🔬', '🔥'], width=5)
            icon_combo.set(data.get('icon', 'ℹ️') if data else 'ℹ️')
            icon_combo.pack(side="left", padx=5)

            ttk.Label(f, text="Vurgu Metni:").pack(side="left", padx=(10, 5))
            txt_entry = ttk.Entry(f)
            txt_entry.insert(0, data.get('text', '') if data else '')
            txt_entry.pack(side="left", fill="x", expand=True)
            block_obj['widgets'] = {'icon': icon_combo, 'text': txt_entry}

        self.blocks.append(block_obj)

        if self.parent_canvas:
            self.parent_canvas.update_idletasks()
            self.parent_canvas.configure(scrollregion=self.parent_canvas.bbox("all"))
            bind_mouse_wheel(block_frame, self.parent_canvas)
            if not data:
                self.parent_canvas.yview_moveto(1.0)

    def remove_block(self, block_obj):
        block_obj['frame'].destroy()
        self.blocks.remove(block_obj)
        self.renumber_blocks()
        if self.parent_canvas:
            self.parent_canvas.update_idletasks()
            self.parent_canvas.configure(scrollregion=self.parent_canvas.bbox("all"))

    def move_block(self, block_obj, direction):
        idx = self.blocks.index(block_obj)
        new_idx = idx + direction
        if 0 <= new_idx < len(self.blocks):
            self.blocks[idx], self.blocks[new_idx] = self.blocks[new_idx], self.blocks[idx]
            for b in self.blocks:
                b['frame'].pack_forget()
            for b in self.blocks:
                b['frame'].pack(fill="x", expand=True, padx=2, pady=6)
            self.renumber_blocks()
            if self.parent_canvas:
                self.parent_canvas.update_idletasks()
                self.parent_canvas.configure(scrollregion=self.parent_canvas.bbox("all"))

    def renumber_blocks(self):
        for i, b in enumerate(self.blocks):
            b['frame'].configure(text=f" Blok #{i+1}: {b['type'].upper()} ")

    def render_html(self, media_copy_callback=None):
        html_parts = []
        for b in self.blocks:
            btype = b['type']
            w = b['widgets']
            if btype == 'heading':
                lvl = w['level'].get()
                txt = w['text'].get().strip()
                if txt: html_parts.append(f"<{lvl}>{txt}</{lvl}>")
            elif btype == 'paragraph':
                txt = w['text'].get("1.0", tk.END).strip()
                if txt:
                    formatted_p = txt.replace('\n\n', '</p><p>').replace('\n', '<br>')
                    html_parts.append(f"<p>{formatted_p}</p>")
            elif btype == 'image':
                path = w['path'].get().strip()
                caption = w['caption'].get().strip()
                img_width = f"{int(w['slider'].get())}%"
                img_align = w['align'].get().strip() or 'Center'
                max_h_str = w['max_height'].get().strip()

                max_h_css = ""
                if max_h_str and 'Auto' not in max_h_str:
                    max_h_css = f"max-height: {max_h_str}; object-fit: contain;"

                margin_css = "margin: 25px auto;"
                if img_align == 'Left':
                    margin_css = "margin: 25px auto 25px 0;"
                elif img_align == 'Right':
                    margin_css = "margin: 25px 0 25px auto;"

                final_path = get_svg_placeholder("Görsel Seçilmedi")
                if path:
                    if media_copy_callback:
                        final_path = media_copy_callback(path)
                    elif not path.startswith(('http://', 'https://', 'file:///', '../../images/')):
                        final_path = f"../../images/{os.path.basename(path)}"
                    else:
                        final_path = path

                cap_html = f"<figcaption style=\"text-align: center; font-size: 0.9rem; color: #64748b; margin-top: 8px;\">{caption}</figcaption>" if caption else ""
                html_parts.append(f"<figure style=\"max-width: {img_width}; {margin_css}\"><img src=\"{final_path}\" alt=\"{caption}\" style=\"width:100%; {max_h_css} border-radius:12px; display:block;\">{cap_html}</figure>")

            elif btype == 'youtube':
                raw_url = w['url'].get().strip()
                yt_width = f"{int(w['slider'].get())}%"
                yt_id = extract_youtube_id(raw_url)

                if yt_id:
                    html_parts.append(f"""<div class="video-embed-container" style="max-width: {yt_width}; margin: 25px auto;">
    <div class="video-embed">
        <iframe src="https://www.youtube-nocookie.com/embed/{yt_id}?rel=0&enablejsapi=1" 
                title="YouTube video player" 
                allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" 
                referrerpolicy="no-referrer"
                allowfullscreen></iframe>
    </div>
</div>""")
                else:
                    html_parts.append(f"""<div class="video-embed-container" style="max-width: {yt_width}; margin: 25px auto; padding: 20px; background: #1e293b; color: #94a3b8; text-align: center; border-radius: 12px;">
    🎥 <em>YouTube Video Bağlantısı Girilmedi</em>
</div>""")

            elif btype == 'gallery':
                cols_str = w['cols'].get()
                m_cols = re.search(r'\d+', cols_str)
                cols_num = m_cols.group(0) if m_cols else '2'

                grid_items_html = []
                for item in w['items']:
                    itype = item['type']
                    if itype == 'image':
                        p = item['path'].get().strip()
                        c = item['caption'].get().strip()
                        final_p = get_svg_placeholder("Galeri Görseli")
                        if p:
                            if media_copy_callback:
                                final_p = media_copy_callback(p)
                            elif not p.startswith(('http://', 'https://', 'file:///', '../../images/')):
                                final_p = f"../../images/{os.path.basename(p)}"
                            else:
                                final_p = p
                        c_html = f"<figcaption style=\"font-size: 0.85rem; color: #64748b; margin-top: 6px; text-align: center;\">{c}</figcaption>" if c else ""
                        grid_items_html.append(f"""<figure style="margin:0; text-align:center;">
    <img src="{final_p}" alt="{c}" style="width:100%; aspect-ratio:16/9; object-fit:cover; border-radius:12px; display:block;">
    {c_html}
</figure>""")
                    elif itype == 'youtube':
                        raw_u = item['url'].get().strip()
                        yt_id = extract_youtube_id(raw_u)
                        if yt_id:
                            grid_items_html.append(f"""<div class="video-embed-container" style="width:100%; margin:0;">
    <div class="video-embed">
        <iframe src="https://www.youtube-nocookie.com/embed/{yt_id}?rel=0&enablejsapi=1" 
                title="YouTube video player" 
                allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" 
                referrerpolicy="no-referrer"
                allowfullscreen></iframe>
    </div>
</div>""")
                        else:
                            grid_items_html.append(f"""<div style="width:100%; padding: 20px; background: #1e293b; color: #94a3b8; text-align: center; border-radius: 12px;">🎥 <em>YouTube Link Yok</em></div>""")

                if grid_items_html:
                    items_str = "\n".join(grid_items_html)
                    html_parts.append(f"""<div class="media-grid" style="display: grid; grid-template-columns: repeat({cols_num}, 1fr); gap: 20px; margin: 30px 0; align-items: start;">
{items_str}
</div>""")

            elif btype == 'callout':
                icon = w['icon'].get().strip()
                txt = w['text'].get().strip()
                if txt:
                    html_parts.append(f"""<div class="callout"><span class="callout-icon">{icon}</span><div>{txt}</div></div>""")
        return "\n\n".join(html_parts)

    def clear_blocks(self):
        for b in list(self.blocks):
            try:
                b['frame'].destroy()
            except Exception:
                pass
        self.blocks.clear()
        if self.parent_canvas:
            self.parent_canvas.update_idletasks()
            self.parent_canvas.configure(scrollregion=self.parent_canvas.bbox("all"))

    def get_blocks_data(self):
        data_list = []
        for b in self.blocks:
            btype = b['type']
            w = b['widgets']
            if btype == 'heading':
                data_list.append({
                    'type': 'heading',
                    'level': w['level'].get(),
                    'text': w['text'].get()
                })
            elif btype == 'paragraph':
                data_list.append({
                    'type': 'paragraph',
                    'text': w['text'].get("1.0", tk.END).rstrip()
                })
            elif btype == 'image':
                data_list.append({
                    'type': 'image',
                    'path': w['path'].get(),
                    'caption': w['caption'].get(),
                    'width': f"{int(w['slider'].get())}%",
                    'align': w['align'].get(),
                    'max_height': w['max_height'].get()
                })
            elif btype == 'youtube':
                data_list.append({
                    'type': 'youtube',
                    'url': w['url'].get(),
                    'width': f"{int(w['slider'].get())}%"
                })
            elif btype == 'gallery':
                items = []
                for item in w['items']:
                    if item['type'] == 'image':
                        items.append({
                            'type': 'image',
                            'path': item['path'].get(),
                            'caption': item['caption'].get()
                        })
                    elif item['type'] == 'youtube':
                        items.append({
                            'type': 'youtube',
                            'url': item['url'].get()
                        })
                data_list.append({
                    'type': 'gallery',
                    'cols': w['cols'].get(),
                    'items': items
                })
            elif btype == 'callout':
                data_list.append({
                    'type': 'callout',
                    'icon': w['icon'].get(),
                    'text': w['text'].get()
                })
        return data_list

    def load_blocks_data(self, data_list):
        self.clear_blocks()
        if not data_list:
            return
        for item in data_list:
            if isinstance(item, dict) and 'type' in item:
                self.add_block(item['type'], item)

# GITHUB AUTO UPDATER CLASS (SERVERLESS & CROSS-PLATFORM)
class GitHubAutoUpdater:
    """
    Sunucu gerektirmeyen, doğrudan GitHub Releases & Raw API kullanan
    çapraz platform (Windows & Linux) otomatik güncelleyici.
    """
    def __init__(self, app_instance, current_version=APP_VERSION):
        self.app = app_instance
        self.current_version = current_version
        self.script_path = os.path.abspath(__file__)
        self.config_path = os.path.join(os.path.dirname(self.script_path), "updater_config.json")
        self.repo = self._load_repo()

    def _load_repo(self):
        if os.path.exists(self.config_path):
            try:
                with open(self.config_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    return data.get("repo", DEFAULT_GITHUB_REPO)
            except Exception:
                pass
        return DEFAULT_GITHUB_REPO

    ALLOWED_UPDATE_DOMAINS = {
        "github.com",
        "raw.githubusercontent.com",
        "objects.githubusercontent.com",
        "github-releases.githubusercontent.com"
    }

    @staticmethod
    def _get_ssl_context():
        """Windows ve Linux sistemlerde SSL kök sertifikalarını güvenle yükler"""
        try:
            import certifi
            return ssl.create_default_context(cafile=certifi.where())
        except Exception:
            pass
        try:
            return ssl.create_default_context()
        except Exception:
            pass
        return ssl._create_unverified_context()

    def _is_safe_download_url(self, url):
        """İndirme adresinin sadece resmi GitHub HTTPS alan adlarına ait olduğunu doğrular"""
        try:
            parsed = urlparse(url)
            if parsed.scheme != "https":
                return False
            host = parsed.netloc.lower().split(':')[0]
            if host in self.ALLOWED_UPDATE_DOMAINS:
                return True
            if host.endswith(".github.com") or host.endswith(".githubusercontent.com") or host.endswith(".amazonaws.com"):
                return True
            return False
        except Exception:
            return False

    def _validate_repo_name(self, repo):
        """Depo adının geçerli ve zararsız 'sahip/repo' formatında olduğunu regex ile doğrular"""
        if not repo or not re.match(r'^[a-zA-Z0-9_\-\.]+/[a-zA-Z0-9_\-\.]+$', repo.strip()):
            return False
        return True

    def _load_repo(self):
        if os.path.exists(self.config_path):
            try:
                with open(self.config_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    val = data.get("repo", DEFAULT_GITHUB_REPO)
                    if self._validate_repo_name(val):
                        return val
            except Exception:
                pass
        return DEFAULT_GITHUB_REPO

    def save_repo(self, repo_str):
        clean_repo = repo_str.strip()
        if not self._validate_repo_name(clean_repo):
            raise ValueError("Geçersiz depo formatı! Örnek: 'kullanici_adi/repo_adi'")
        self.repo = clean_repo
        try:
            with open(self.config_path, "w", encoding="utf-8") as f:
                json.dump({"repo": self.repo}, f, indent=2)
        except Exception:
            pass

    @staticmethod
    def parse_version(ver_str):
        cleaned = str(ver_str).lower().lstrip('v').strip()
        parts = []
        for part in cleaned.split('.'):
            num = ''.join(filter(str.isdigit, part))
            parts.append(int(num) if num else 0)
        while len(parts) < 3:
            parts.append(0)
        return tuple(parts[:3])

    def check_for_updates_async(self, silent=True):
        threading.Thread(target=self._check_worker, args=(silent,), daemon=True).start()

    def _check_worker(self, silent):
        if not self._validate_repo_name(self.repo):
            if not silent:
                self.app.after(0, lambda: self._prompt_repo_config("Lütfen geçerli bir GitHub depo adresi girin (örn: kullanici_adi/repo_adi):"))
            return

        latest_tag = None
        release_body = ""
        download_url = None
        release_found = False

        # 1. Aşama: GitHub Releases API'yi kontrol et
        api_url = f"https://api.github.com/repos/{self.repo}/releases/latest"
        req = urllib.request.Request(
            api_url,
            headers={
                "User-Agent": "MICROLab-Editor-Updater",
                "Accept": "application/vnd.github.v3+json"
            }
        )
        try:
            with urllib.request.urlopen(req, context=self._get_ssl_context(), timeout=8) as response:
                if response.status == 200:
                    data = json.loads(response.read().decode('utf-8'))
                    latest_tag = data.get("tag_name", "v1.0.0")
                    release_body = data.get("body", "Herhangi bir sürüm notu girilmemiş.")
                    for asset in data.get("assets", []):
                        if asset.get("name") in ["app.py", "MICROLab_app.py"] or asset.get("name", "").endswith(".py"):
                            cand = asset.get("browser_download_url")
                            if cand and self._is_safe_download_url(cand):
                                download_url = cand
                                break
                    if not download_url:
                        download_url = f"https://raw.githubusercontent.com/{self.repo}/main/app.py"
                    release_found = True
        except urllib.error.HTTPError as he:
            if he.code == 404:
                # Henüz resmi bir GitHub Release oluşturulmamış - main dalını deneyeceğiz
                release_found = False
            elif he.code == 403:
                if not silent:
                    self.app.after(0, lambda: messagebox.showwarning("GitHub Limit", "GitHub API saatlik istek sınırına ulaşıldı. Lütfen daha sonra tekrar deneyin."))
                return
            else:
                if not silent:
                    self.app.after(0, lambda: messagebox.showwarning("Bağlantı Hatası", f"GitHub bağlantı hatası: HTTP {he.code}"))
                return
        except Exception as e:
            # SSL veya ağ hatası durumunda doğrudan 2. Aşamayı (raw main) dene
            release_found = False

        # 2. Aşama: Eğer resmi Release yoksa, doğrudan main dalındaki app.py dosyasını kontrol et
        if not release_found:
            raw_url = f"https://raw.githubusercontent.com/{self.repo}/main/app.py"
            try:
                raw_req = urllib.request.Request(raw_url, headers={"User-Agent": "MICROLab-Editor-Updater"})
                with urllib.request.urlopen(raw_req, context=self._get_ssl_context(), timeout=8) as raw_resp:
                    if raw_resp.status == 200:
                        raw_code = raw_resp.read().decode('utf-8')
                        m = re.search(r'APP_VERSION\s*=\s*[\"\']([^\"\']+)[\"\']', raw_code)
                        if m:
                            remote_ver_str = m.group(1)
                            latest_tag = f"v{remote_ver_str}"
                            release_body = f"GitHub deposundaki (main dalı) en güncel sürüm: {latest_tag}"
                            download_url = raw_url
                            release_found = True
            except urllib.error.HTTPError as he:
                if he.code == 404:
                    if not silent:
                        self.app.after(0, lambda: self._prompt_repo_config(
                            f"'{self.repo}' deposuna veya 'main/app.py' dosyasına erişilemedi.\n\n"
                            "Lütfen deponun public olduğundan ve dosyaların yüklendiğinden emin olun.\n"
                            "Depo adresinizi kontrol etmek ister misiniz?"
                        ))
                    return
            except Exception as e:
                if not silent:
                    self.app.after(0, lambda: messagebox.showwarning("Bağlantı Hatası", f"GitHub kontrolü yapılamadı:\n{e}"))
                return

        # 3. Aşama: Sürüm Karşılaştırması ve Kullanıcı Bildirimi
        cur_v = self.parse_version(self.current_version)
        if latest_tag:
            lat_v = self.parse_version(latest_tag)
            if lat_v > cur_v:
                # Yeni bir sürüm mevcut
                if download_url and self._is_safe_download_url(download_url):
                    self.app.after(0, lambda: self._show_update_modal(latest_tag, release_body, download_url))
                elif not silent:
                    self.app.after(0, lambda: messagebox.showerror("Güvenlik Uyarısı", "Güncelleme URL'i güvenli bir GitHub alan adına ait değil!"))
                return

        # Sürüm güncel veya eşit
        if not silent:
            self.app.after(0, lambda: messagebox.showinfo(
                "Uygulama Güncel",
                f"MICROLab Editor en son sürümde!\n\n"
                f"Mevcut Sürüm: v{self.current_version}\n"
                f"GitHub Deposu: {self.repo}\n\n"
                f"GitHub üzerinde daha yeni bir sürüm bulunmuyor, uygulamanız tamamen günceldir."
            ))

    def _prompt_repo_config(self, message):
        new_repo = simpledialog.askstring("GitHub Depo Ayarı", message, initialvalue=self.repo)
        if new_repo and new_repo.strip():
            try:
                self.save_repo(new_repo.strip())
                messagebox.showinfo("Kaydedildi", f"GitHub deposu '{self.repo}' olarak ayarlandı.\nŞimdi tekrar güncelleme kontrolü yapabilirsiniz.")
            except ValueError as ve:
                messagebox.showerror("Hata", str(ve))

    def _show_update_modal(self, new_tag, release_body, download_url):
        notes = release_body.strip()
        if len(notes) > 400:
            notes = notes[:400] + "..."
        msg = (
            f"🎉 Yeni bir sürüm mevcut: {new_tag}\n"
            f"(Şu anki sürümünüz: v{self.current_version})\n\n"
            f"--- Değişiklikler ---\n"
            f"{notes}\n\n"
            f"Uygulama otomatik güncellenip yeniden başlatılsın mı?"
        )
        if messagebox.askyesno("Yeni Güncelleme Bulundu!", msg):
            self.download_and_apply_update(download_url, new_tag)

    def _verify_code_integrity(self, code_bytes):
        """İndirilen kodun boyut, sözdizimi ve beklenen MICROLab Editor imzalarını doğrulayarak zararlı veya eksik kod enjeksiyonunu engeller"""
        if len(code_bytes) < 10000:
            raise ValueError("İndirilen dosya boyutu beklenenden çok küçük veya eksik!")
        
        code_str = code_bytes.decode('utf-8')
        
        required_markers = [
            "APP_VERSION",
            "GitHubAutoUpdater"
        ]
        for marker in required_markers:
            if marker not in code_str:
                raise ValueError(f"Güvenlik Doğrulama Hatası: İndirilen kod geçerli MICROLab Editor imzalarını içermiyor ('{marker}' eksik).")
        
        if "MicroLabEditorApp" not in code_str and "StandaloneProjectCreatorApp" not in code_str:
            raise ValueError("Güvenlik Doğrulama Hatası: İndirilen kod geçerli MICROLab Editor ana uygulama sınıfını içermiyor.")

        compile(code_str, '<update_code>', 'exec')
        return code_str

    def download_and_apply_update(self, download_url, new_tag):
        try:
            # 1. URL Güvenlik Doğrulaması
            if not self._is_safe_download_url(download_url):
                raise ValueError(f"Güvenlik Uyarısı: İndirme URL'i ({download_url}) onaylı GitHub alan adlarına ait değil!")

            req = urllib.request.Request(download_url, headers={"User-Agent": "MICROLab-Editor-Updater"})
            with urllib.request.urlopen(req, context=self._get_ssl_context(), timeout=30) as resp:
                code_bytes = resp.read()

            # 2. Bütünlük ve İmza Kontrolü
            self._verify_code_integrity(code_bytes)

            # 3. Güvenli Yedekleme
            backup_file = self.script_path + ".bak"
            if os.path.exists(backup_file):
                try: os.remove(backup_file)
                except Exception: pass
            shutil.copy2(self.script_path, backup_file)

            # 4. Geçici Dosya ve Atomik Değiştirme
            temp_file = self.script_path + ".tmp"
            with open(temp_file, "wb") as f:
                f.write(code_bytes)

            os.replace(temp_file, self.script_path)

            messagebox.showinfo(
                "Güncelleme Tamamlandı",
                f"MICROLab Editor başarıyla {new_tag} sürümüne güncellendi!\n\n"
                "Uygulama şimdi yeniden başlatılıyor..."
            )

            # 5. Güvenli Yeniden Başlatma
            subprocess.Popen([sys.executable, self.script_path] + sys.argv[1:])
            self.app.destroy()
            sys.exit(0)

        except Exception as e:
            messagebox.showerror("Güncelleme Hatası", f"Güncelleme uygulanamadı:\n{e}\n\nMevcut sürümünüz korunmuştur.")

# MAIN STANDALONE APP WITH ASK-ON-SAVE DIRECTORY PROMPT & 100% INLINE PREVIEW
# class StandaloneProjectCreatorApp (alias for backward compatibility)
class MicroLabEditorApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title(f"MICROLab Editor v{APP_VERSION}")
        self.geometry("1280x900")
        
        script_dir = os.path.dirname(os.path.abspath(__file__))
        candidates = [
            os.path.abspath(os.path.join(script_dir, "..", "website")),
            os.path.abspath(os.path.join(script_dir, "..")),
            os.path.abspath(os.path.join(script_dir, "..", ".."))
        ]
        found_export_dir = None
        for cand in candidates:
            if os.path.exists(os.path.join(cand, "index.html")):
                found_export_dir = cand
                break

        if found_export_dir:
            self.default_export_dir = found_export_dir
        else:
            self.default_export_dir = os.path.join(script_dir, "exports")
            os.makedirs(self.default_export_dir, exist_ok=True)
        
        self.output_dir_var = tk.StringVar(value=self.default_export_dir)
        self.auto_sync_var = tk.BooleanVar(value=True)
        self.live_preview_opened = False
        self.guide_images = []
        
        self.preview_temp_path = os.path.join(tempfile.gettempdir(), "microlab_live_preview.html")

        self.existing_people_names = [
            "Dr. Alex Mercer",
            "Gizem Asya Yılmaz",
            "David Chen",
            "Elena Rodriguez",
            "Sarah Jenkins",
            "Nurettin Tarık Mut"
        ]
        self.proj_cover_path = ""
        self.person_photo_path = ""

        self.loaded_file_paths = {0: "", 1: "", 2: "", 3: ""}
        self.loaded_slugs = {0: "", 1: "", 2: "", 3: ""}
        self.loaded_titles = {0: "", 1: "", 2: "", 3: ""}

        self.member_rows = []
        self.pub_rows = []

        self.setup_styles()
        
        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=3)
        self.grid_columnconfigure(1, weight=1, minsize=340)

        self.create_header_banner()
        self.create_tabbed_interface()
        self.create_right_panel()

        self.add_member_row()

        self.updater = GitHubAutoUpdater(self, current_version=APP_VERSION)
        self.after(2500, self.auto_update_preview_loop)
        self.after(3500, lambda: self.updater.check_for_updates_async(silent=True))

    def setup_styles(self):
        self.style = ttk.Style(self)
        self.style.theme_use('vista' if sys.platform == 'win32' else 'clam')
        self.bg_light = "#f8fafc"
        self.border_gray = "#cbd5e1"
        self.configure(background=self.bg_light)
        
        self.style.configure('TFrame', background=self.bg_light)
        self.style.configure('TLabelframe', background=self.bg_light, bordercolor=self.border_gray, borderwidth=1)
        self.style.configure('TLabelframe.Label', font=('Inter', 10, 'bold'), foreground='#0f172a', background=self.bg_light)
        self.style.configure('TLabel', background=self.bg_light, font=('Inter', 9), foreground='#334155')
        self.style.configure('Header.TLabel', font=('Inter', 15, 'bold'), foreground='#ffffff', background='#0f172a')
        self.style.configure('SubHeader.TLabel', font=('Inter', 9), foreground='#94a3b8', background='#0f172a')
        self.style.configure('Primary.TButton', font=('Inter', 11, 'bold'), padding=8)
        self.style.configure('Accent.TButton', font=('Inter', 9, 'bold'), foreground='#2563eb')

    def create_header_banner(self):
        header_frame = tk.Frame(self, bg='#0f172a', height=75)
        header_frame.grid(row=0, column=0, columnspan=2, sticky="ew")
        header_frame.grid_propagate(False)
        header_frame.rowconfigure(0, weight=1)
        
        inner_frame = tk.Frame(header_frame, bg='#0f172a')
        inner_frame.pack(side="left", padx=20, fill="y")
        
        title_lbl = ttk.Label(inner_frame, text="MICROLab Editor", style="Header.TLabel")
        title_lbl.pack(anchor="w", pady=(8, 0))
        subtitle_lbl = ttk.Label(inner_frame, text=f"Web Sitesi İçerik Yönetim Editörü (v{APP_VERSION})", style="SubHeader.TLabel")
        subtitle_lbl.pack(anchor="w", pady=(2, 0))

        guide_btn = tk.Button(header_frame, text="📖 Kılavuz & Nasıl Kullanılır", font=('Inter', 9, 'bold'), bg='#2563eb', fg='#ffffff', activebackground='#1d4ed8', activeforeground='#ffffff', relief="flat", padx=12, pady=6, cursor="hand2", command=self.switch_to_guide_tab)
        guide_btn.pack(side="right", padx=(10, 20), pady=18)

        update_btn = tk.Button(header_frame, text="🔄 Güncelleme Kontrolü", font=('Inter', 9), bg='#334155', fg='#ffffff', activebackground='#475569', activeforeground='#ffffff', relief="flat", padx=10, pady=6, cursor="hand2", command=lambda: self.updater.check_for_updates_async(silent=False))
        update_btn.pack(side="right", padx=(0, 5), pady=18)

    def switch_to_guide_tab(self):
        if hasattr(self, 'guide_tab'):
            self.notebook.select(self.guide_tab)
        else:
            self.show_user_guide()

    def show_user_guide(self):
        if hasattr(self, 'guide_tab'):
            self.notebook.select(self.guide_tab)
            return
        guide_win = tk.Toplevel(self)
        guide_win.title("❓ MICROLab Editor Kullanım Kılavuzu & Adım Adım Rehber")
        guide_win.geometry("800x700")
        guide_win.configure(bg="#f8fafc")
        txt = tk.Text(guide_win, font=('Inter', 10), wrap="word", padx=20, pady=20)
        txt.pack(fill="both", expand=True)
        txt.insert("1.0", "Detaylı rehber ve görseller için lütfen ana ekrandaki '📖 Yardım & Nasıl Kullanılır' sekmesine tıklayınız.")
        txt.configure(state="disabled")

    def build_guide_tab(self):
        canvas = tk.Canvas(self.guide_tab, bg=self.bg_light, highlightthickness=0)
        scrollbar = ttk.Scrollbar(self.guide_tab, orient="vertical", command=canvas.yview)
        scroll_frame = ttk.Frame(canvas)

        def _update_scroll_region(event=None):
            canvas.update_idletasks()
            canvas.configure(scrollregion=canvas.bbox("all"))

        scroll_frame.bind("<Configure>", _update_scroll_region)
        canvas.create_window((0, 0), window=scroll_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        bind_mouse_wheel(scroll_frame, canvas)

        script_dir = os.path.dirname(os.path.abspath(__file__))
        assets_dir = os.path.join(script_dir, "assets")

        def add_guide_image(parent_frame, fname, caption=""):
            p = os.path.join(assets_dir, fname)
            if PIL_AVAILABLE and os.path.exists(p):
                try:
                    pil_img = Image.open(p)
                    tk_img = ImageTk.PhotoImage(pil_img)
                    self.guide_images.append(tk_img)
                    img_f = ttk.Frame(parent_frame)
                    img_f.pack(fill="x", padx=10, pady=8)
                    lbl = ttk.Label(img_f, image=tk_img)
                    lbl.pack(anchor="center")
                    if caption:
                        ttk.Label(img_f, text=caption, font=('Inter', 8, 'italic'), foreground='#64748b').pack(anchor="center", pady=(4, 0))
                    return True
                except Exception:
                    pass
            return False

        # --- HERO BANNER ---
        hero_frame = tk.Frame(scroll_frame, bg="#0f172a", padx=20, pady=16)
        hero_frame.pack(fill="x", padx=10, pady=(10, 8))

        ttk.Label(hero_frame, text="📘 MICROLab Editor Kapsamlı İçerik Yönetimi & Kullanım Kılavuzu", font=('Inter', 13, 'bold'), foreground="#ffffff", background="#0f172a").pack(anchor="w")
        ttk.Label(hero_frame, text="Web sitesine yeni proje, araştırmacı, haber ve yayın ekleme; kayıtlı projeleri içe aktarma ve modüler sayfa üretimi rehberi.", font=('Inter', 9), foreground="#94a3b8", background="#0f172a").pack(anchor="w", pady=(3, 10))

        quick_bar = tk.Frame(hero_frame, bg="#0f172a")
        quick_bar.pack(anchor="w")
        tk.Button(quick_bar, text="🚀 Proje Editörüne Git", font=('Inter', 8, 'bold'), bg="#2563eb", fg="#ffffff", activebackground="#1d4ed8", relief="flat", padx=10, pady=4, command=lambda: self.notebook.select(self.project_tab)).pack(side="left", padx=(0, 6))
        tk.Button(quick_bar, text="📂 Kayıtlı Proje Aç / Yükle", font=('Inter', 8, 'bold'), bg="#10b981", fg="#ffffff", activebackground="#059669", relief="flat", padx=10, pady=4, command=self.open_project_prompt).pack(side="left", padx=6)
        tk.Button(quick_bar, text="🌐 Canlı Siteyi Aç (localhost:8000)", font=('Inter', 8, 'bold'), bg="#475569", fg="#ffffff", activebackground="#334155", relief="flat", padx=10, pady=4, command=lambda: webbrowser.open("http://localhost:8000")).pack(side="left", padx=6)

        # --- SECTION 1: NEW FEATURE - UNIVERSAL CONTENT LOADER ---
        lf_load = ttk.LabelFrame(scroll_frame, text=" ✨ YENİ ÖZELLİK: Akıllı İçerik Yükleme & Düzenleme (Universal Content Loader) ")
        lf_load.pack(fill="x", padx=10, pady=8)

        add_guide_image(lf_load, "guide_ui_screenshot.png", "Ekran Görüntüsü: Hedef klasör seçildiğinde tespit edilen içerikler listelenir ve tek tıkla düzenleyiciye aktarılır.")
        add_guide_image(lf_load, "guide_load_feature.png", "İçerik Yükleme Süreci: Hedef Klasör -> Otomatik Tarama -> Tek Tıkla Yükleme -> Kaldığın Yerden Düzenleme")

        load_desc = """Bu yeni evrensel özellik sayesinde artık TÜM sekmelerde (Projeler, Ekip Üyeleri, Haberler, Yayınlar) kayıtlı dosyalarınızı tek tıkla geri yükleyip düzenleyebilirsiniz:
• 📁 Otomatik Tarama & Kategori Filtreleme: Sağ panelden 'Hedef Klasör Değiştir' dediğinizde, sistem seçtiğiniz klasördeki tüm projeleri, ekip üyelerini, haberleri ve yayınları saniyeler içinde otomatik olarak tarar.
• 📋 Evrensel İçerik Seçim Penceresi: Açılan modal pencerede kategori sekmeleri [🌟 Tümü] [🚀 Projeler] [👤 Ekip Üyeleri] [📰 Haberler] [📚 Yayınlar] ve anlık arama çubuğu yer alır. Düzenlemek istediğiniz içeriği seçip '✅ Seçilen İçeriği Editöre Yükle' butonuna tıklamanız yeterlidir.
• 🔄 Doğru Sekmeye Otomatik Geçiş: Hangi içerik türünü seçtiyseniz (örneğin bir yayın veya ekip üyesi), sistem sizi otomatik olarak o sekmeye aktarır ve formu o dosyanın tüm verileriyle doldurur.
• ✏️ Canlı Düzenleme Rozeti (Badge): Editörün üst kısmında '✏️ Düzenleniyor: dosya_adi.html' rozeti belirir. Değişikliklerinizi yapıp '💾 Aktif Sekmedeki İçeriği Üret' dediğinizde aynı dosya güncellenir ve '✓ Kaydedildi' bildirimi alırsınız.
• 🧩 İçerik Blokları ve Bağlantılar Eksiksiz Yüklenir: Proje ve haberlerin gövde blokları (Başlıklar, Paragraflar, Görseller, Videolar), kişilerin rolleri ve yayınların DOI, PDF, Code, Video gibi tüm kaynak linkleri eksiksiz biçimde editöre yüklenir.
• ⚡ Her Sekmede Bağımsız Araç Çubuğu: Her sekmenin üstünde yer alan '📂 Kayıtlı İçerik Yükle / Düzenle' ve '🔄 Formu Temizle / Yeni...' butonlarıyla dilediğiniz an eski kayıtları açabilir veya sıfırdan yeni kayıt oluşturabilirsiniz."""
        ttk.Label(lf_load, text=load_desc, font=('Inter', 9), wraplength=880, justify="left").pack(anchor="w", padx=12, pady=6)

        # --- SECTION 2: 4-STEP WORKFLOW ---
        lf_flow = ttk.LabelFrame(scroll_frame, text=" 🚀 4 Adımda Genel Çalışma ve Üretim Akışı ")
        lf_flow.pack(fill="x", padx=10, pady=8)

        add_guide_image(lf_flow, "guide_workflow.png", "Çalışma Akışı: Formu Doldur -> Canlı Önizle -> Hedef Seç & Kaydet -> Sitede Yayında!")

        flow_desc = """MICROLab Editor, harici bağımlılık veya karmaşık web sunucusu kurulumu gerektirmeden bağımsız çalışan bir içerik yönetim ve sayfa üretim aracıdır:
1. İlgili Sekmeyi Seçin: Proje, Ekip Üyesi, Haber veya Yayın sekmelerinden eklemek istediğiniz içerik türünü seçin ve formu doldurun.
2. Canlı Önizleyin (Hot-Reload): '👁️ Tarayıcıda Canlı Önizle' butonuna basarak tasarımınızı tarayıcıda görün. '⚡ Otomatik Önizleme Yenile' seçeneği aktifken, formda yaptığınız her değişiklik 2.5 saniye içinde tarayıcıda anında güncellenir.
3. Hedef Klasöre Kaydedin: '💾 Aktif Sekmedeki İçeriği Üret' butonuna basın. Sayfa ve görsellerin nereye kaydedileceğini soran pencerede web sitenizin kök dizinini seçin. Sistem gerekli HTML, CSS, JS ve görsel dosyalarını otomatik olarak doğru alt klasörlere kopyalar.
4. Web Sitesinde Görün: Web sitesi açıkken sayfayı yenilemeniz (F5 veya Ctrl+F5) yeterlidir. Dinamik tarama motoru yeni eklenen içeriği otomatik olarak algılar ve hub sayfasında listeler."""
        ttk.Label(lf_flow, text=flow_desc, font=('Inter', 9), wraplength=880, justify="left").pack(anchor="w", padx=12, pady=6)

        # --- SECTION 3: CONTENT BLOCKS CATALOG ---
        lf_blocks = ttk.LabelFrame(scroll_frame, text=" 🧩 Modüler Sayfa İçerik Blokları Kataloğu ")
        lf_blocks.pack(fill="x", padx=10, pady=8)

        add_guide_image(lf_blocks, "guide_blocks.png", "Modüler Bloklar: Başlık, Paragraf, Tek Görsel & Slider, YouTube Video, Medya Grid Galeri, Vurgu Kutusu")

        blocks_desc = """Proje ve Haber sayfalarınızın gövdesini modüler bloklar kullanarak dilediğiniz gibi tasarlayabilirsiniz:
• 📌 Başlık Blokları (H2 / H3): Sayfanızı ana başlıklara (H2) ve alt başlıklara (H3) ayırarak akademik ve kurumsal bir hiyerarşi sağlar.
• 📄 Paragraf Bloğu: Uzun araştırma metinleri, yöntem açıklamaları ve sonuçlar için kullanılır. Çok satırlı metinleri paragraflara (<p>) ve satır sonlarına (<br>) otomatik dönüştürür.
• 🖼️ Tek Görsel & Slider: Bilgisayarınızdan fotoğraf seçebilirsiniz. Genişlik sürgüsü (%10 - %100) ve buton presetleri (%100, %75, %50, %35) ile görsel boyutunu belirleyin. Hizalama (Sol, Orta, Sağ) ve Maksimum Yükseklik (Auto, 500px, 400px, 300px, 200px) ayarları sunar. Tıklandığında tam ekran Lightbox açılır!
• 🎥 YouTube Video: YouTube video linkini veya 11 haneli video ID'sini yapıştırın. Genişlik sürgüsüyle (%20 - %100) boyutlandırın. Çerezsiz ve güvenli (youtube-nocookie) duyarlı oynatıcı ekler.
• 🔲 Medya Grid Galerisi: 2, 3 veya 4 kolonlu yan yana fotoğraf ve YouTube videosu düzeni kurar. Aynı galeride hem resimleri hem de videoları yan yana sergileyebilirsiniz.
• 💡 Vurgu Kutusu (Callout): 6 farklı ikon (ℹ️ Bilgi, ⚠️ Uyarı, 🚀 Öne Çıkan, 💡 Fikir, 🔬 Deney, 🔥 Duyuru) ile renkli, dikkat çekici duyuru kutuları oluşturur."""
        ttk.Label(lf_blocks, text=blocks_desc, font=('Inter', 9), wraplength=880, justify="left").pack(anchor="w", padx=12, pady=6)

        # --- SECTION 4: PEOPLE MANAGEMENT ---
        lf_people = ttk.LabelFrame(scroll_frame, text=" 👤 Ekip Üyeleri (People) ve Dinamik Eşleşme ")
        lf_people.pack(fill="x", padx=10, pady=8)

        people_desc = """Ekip üyeleri yönetimi ve projelerle otomatik bağlantı:
• Kategori Seçimi: Doktora Sonrası Araştırmacı (Postdoc), Doktora Öğrencisi (PhD), Yüksek Lisans (Masters) veya Lisans (Undergraduate) kategorisini seçin.
• Akademik & Sosyal Profiller: Google Scholar, ORCID iD, ResearchGate, GitHub, LinkedIn, Web Sitesi ve E-posta bağlantılarını ekleyin; profil kartında ve ekip sayfasında resmi SVG logolu şık butonlar olarak otomatik görüntülenir.
• Projelerle Dinamik Eşleşme: Bir proje sayfası oluştururken 'Projedeki Üyeler' kısmına eklediğiniz isimler, web sitesinde 'people/data/' altındaki araştırmacı sayfalarıyla ad-soyad üzerinden dinamik eşleşir. Kişinin fotoğrafı ve profil sayfası linki proje kartına otomatik olarak entegre edilir."""
        ttk.Label(lf_people, text=people_desc, font=('Inter', 9), wraplength=880, justify="left").pack(anchor="w", padx=12, pady=6)

        # --- SECTION 5: NEWS & PUBLICATIONS ---
        lf_news = ttk.LabelFrame(scroll_frame, text=" 📰 Haberler ve 📚 Araştırma Yayınları ")
        lf_news.pack(fill="x", padx=10, pady=8)

        news_desc = """Laboratuvar duyuruları ve bilimsel yayınların yönetimi:
• Haberler: Başlık, yayın tarihi, kategori (Announcements, Grants, Awards, Research, Events) ve zengin içerik blokları ekleyerek laboratuvar haberleri yayınlayabilirsiniz.
• Yayınlar: Makale başlığı, yazar listesi, sunulduğu konferans veya dergi (Venue), yayın yılı, DOI bağlantısı ve tam metin PDF linki tanımlayabilirsiniz."""
        ttk.Label(lf_news, text=news_desc, font=('Inter', 9), wraplength=880, justify="left").pack(anchor="w", padx=12, pady=6)

        # --- SECTION 6: FILE STRUCTURE ---
        lf_struct = ttk.LabelFrame(scroll_frame, text=" 📁 Web Sitesi Klasör Mimarisi & Standalone Güvencesi ")
        lf_struct.pack(fill="x", padx=10, pady=8)

        struct_desc = """Kök klasör yapısı ve üretilen dosyaların konumları:
MICROLab-WEBSITE/
├── index.html              ← Ana vitrin sayfası
├── publications.html       ← Tüm yayınların listelendiği sayfa
├── projects/
│   ├── index.html          ← Projeler Hub (data/ altını otomatik tarar)
│   └── data/*.html         ← Proje detay sayfaları (gömülü PROJECT_METADATA içerir)
├── people/
│   ├── index.html          ← Ekip Hub (data/ altını otomatik tarar)
│   └── data/*.html         ← Araştırmacı profil sayfaları
├── news/
│   ├── index.html          ← Haberler Hub (data/ altını otomatik tarar)
│   └── data/*.html         ← Haber yazıları
├── images/                 ← Proje kapakları, üye fotoğrafları ve galeri resimleri
├── css/ & js/              ← Tema ve dinamik tarama betikleri
└── microlab-editor/        ← Bu bağımsız masaüstü yazılımı ve varlıkları

💡 Standalone Güvencesi: Üretilen her HTML sayfasının içine tüm CSS stilleri ve JS scriptleri inline olarak da gömülür. Dosyaları başka bir bilgisayara tek başına gönderseniz dahi kusursuz olarak görüntülenir."""
        ttk.Label(lf_struct, text=struct_desc, font=('Consolas', 8), wraplength=880, justify="left").pack(anchor="w", padx=12, pady=6)

        # --- SECTION 7: FAQ & TIPS ---
        lf_faq = ttk.LabelFrame(scroll_frame, text=" 💡 Sıkça Sorulan Sorular (SSS) & Pratik İpuçları ")
        lf_faq.pack(fill="x", padx=10, pady=(8, 20))

        faq_desc = """S: Kaydettiğim proje web sitesinde görünmüyor, ne yapmalıyım?
C: Web sitesi yerel HTTP sunucusu üzerinden çalışmalıdır ('python -m http.server 8000'). Tarayıcınızda Ctrl+F5 yaparak önbelleği temizleyin.

S: Daha önce oluşturduğum bir projeyi nasıl düzenlerim?
C: 'Hedef Klasör Değiştir' butonuna basıp web sitesi klasörünüzü seçin; açılan listeden projenizi seçip 'Editöre Yükle'ye tıklayın. Değişiklikleri yaptıktan sonra 'Aktif Sekmedeki İçeriği Üret'e basarak aynı isimle üzerine kaydedebilirsiniz.

S: Canlı önizleme için internet bağlantısı gerekir mi?
C: Hayır! Uygulama %100 yerel CSS ve dahili SVG yer tutucular içerir. Çevrimdışı ortamda da sorunsuz çalışır.

S: Seçtiğim fotoğraflar web sitesinde nereye kopyalanır?
C: Uygulama seçtiğiniz tüm görselleri hedef klasörün 'images/' dizinine otomatik olarak kopyalar ve HTML sayfasına bağlar."""
        ttk.Label(lf_faq, text=faq_desc, font=('Inter', 9), wraplength=880, justify="left").pack(anchor="w", padx=12, pady=6)

    def create_tabbed_interface(self):
        self.notebook = ttk.Notebook(self)
        self.notebook.grid(row=1, column=0, sticky="nsew", padx=15, pady=15)
        
        self.project_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.project_tab, text=" 🚀 Proje Editörü ")
        self.build_project_tab()

        self.person_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.person_tab, text=" 👤 Ekip Üyesi Editörü ")
        self.build_person_tab()

        self.news_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.news_tab, text=" 📰 Haber Editörü ")
        self.build_news_tab()

        self.pub_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.pub_tab, text=" 📚 Yayın Editörü ")
        self.build_pub_tab()

        self.guide_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.guide_tab, text=" 📖 Yardım & Nasıl Kullanılır ")
        self.build_guide_tab()

    def build_project_tab(self):
        canvas = tk.Canvas(self.project_tab, bg=self.bg_light, highlightthickness=0)
        scrollbar = ttk.Scrollbar(self.project_tab, orient="vertical", command=canvas.yview)
        scroll_frame = ttk.Frame(canvas)

        def _update_scroll_region(event=None):
            canvas.update_idletasks()
            canvas.configure(scrollregion=canvas.bbox("all"))

        scroll_frame.bind("<Configure>", _update_scroll_region)
        canvas.create_window((0, 0), window=scroll_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        bind_mouse_wheel(scroll_frame, canvas)

        # Quick project load & action toolbar
        proj_actions_bar = ttk.Frame(scroll_frame)
        proj_actions_bar.pack(fill="x", padx=10, pady=(8, 4))
        
        ttk.Button(proj_actions_bar, text="📂 Kayıtlı Proje Yükle / Düzenle", style="Accent.TButton", command=self.open_project_prompt).pack(side="left", padx=(0, 6))
        ttk.Button(proj_actions_bar, text="🔄 Formu Temizle / Yeni Proje", command=self.reset_project_form).pack(side="left", padx=2)
        self.proj_loaded_badge = ttk.Label(proj_actions_bar, text="", font=('Inter', 8, 'bold'), foreground='#2563eb')
        self.proj_loaded_badge.pack(side="left", padx=10)
        ttk.Label(proj_actions_bar, text="💡 Hedef klasördeki kayıtlı projeleri yükleyip düzenleyebilirsiniz.", font=('Inter', 8, 'italic'), foreground='#64748b').pack(side="left", padx=4)

        lf_basic = ttk.LabelFrame(scroll_frame, text=" 1. Proje Temel Bilgileri ")
        lf_basic.pack(fill="x", padx=10, pady=8)

        ttk.Label(lf_basic, text="Proje Başlığı:").grid(row=0, column=0, sticky="w", padx=10, pady=2)
        self.proj_title_entry = ttk.Entry(lf_basic, width=50)
        self.proj_title_entry.grid(row=0, column=1, sticky="ew", padx=10, pady=2)
        ttk.Label(lf_basic, text="💡 Projenizin sitede görünecek tam adıdır (örn: Autonomous Drone Path Planning).", font=('Inter', 8, 'italic'), foreground='#64748b').grid(row=1, column=1, sticky="w", padx=10, pady=(0, 6))

        ttk.Label(lf_basic, text="Etiketler (Tags):").grid(row=2, column=0, sticky="w", padx=10, pady=2)
        self.proj_tags_entry = ttk.Entry(lf_basic)
        self.proj_tags_entry.insert(0, "vision, autonomy, control")
        self.proj_tags_entry.grid(row=2, column=1, sticky="ew", padx=10, pady=2)
        ttk.Label(lf_basic, text="💡 Virgülle ayırarak yazın (örn: vision, autonomy, control).", font=('Inter', 8, 'italic'), foreground='#64748b').grid(row=3, column=1, sticky="w", padx=10, pady=(0, 6))

        ttk.Label(lf_basic, text="Durum (Status):").grid(row=4, column=0, sticky="w", padx=10, pady=2)
        self.proj_status_combo = ttk.Combobox(lf_basic, values=["Active", "Completed"], state="readonly", width=15)
        self.proj_status_combo.set("Active")
        self.proj_status_combo.grid(row=4, column=1, sticky="w", padx=10, pady=2)
        ttk.Label(lf_basic, text="💡 Active: Devam eden araştırma | Completed: Tamamlanmış proje.", font=('Inter', 8, 'italic'), foreground='#64748b').grid(row=5, column=1, sticky="w", padx=10, pady=(0, 6))

        ttk.Label(lf_basic, text="Başlangıç Tarihi:").grid(row=6, column=0, sticky="w", padx=10, pady=2)
        self.proj_start_entry = ttk.Entry(lf_basic, width=20)
        self.proj_start_entry.insert(0, "June 2026")
        self.proj_start_entry.grid(row=6, column=1, sticky="w", padx=10, pady=2)

        ttk.Label(lf_basic, text="Bitiş Tarihi (Completed ise):").grid(row=7, column=0, sticky="w", padx=10, pady=2)
        self.proj_end_entry = ttk.Entry(lf_basic, width=20)
        self.proj_end_entry.grid(row=7, column=1, sticky="w", padx=10, pady=2)

        ttk.Label(lf_basic, text="Kısa Özet:").grid(row=8, column=0, sticky="nw", padx=10, pady=2)
        self.proj_short_desc_text = tk.Text(lf_basic, height=3, font=('Inter', 9))
        self.proj_short_desc_text.grid(row=8, column=1, sticky="ew", padx=10, pady=2)
        ttk.Label(lf_basic, text="💡 Projeler listesinde kartın üzerinde görünecek 1-2 cümlelik tanıtım özeti.", font=('Inter', 8, 'italic'), foreground='#64748b').grid(row=9, column=1, sticky="w", padx=10, pady=(0, 6))
        
        lf_basic.columnconfigure(1, weight=1)

        lf_cover = ttk.LabelFrame(scroll_frame, text=" 2. Proje Kapak Görseli (Cover Image) ")
        lf_cover.pack(fill="x", padx=10, pady=8)

        ttk.Button(lf_cover, text="Görsel Seç...", command=self.select_proj_cover).pack(side="left", padx=10, pady=10)
        self.proj_cover_label = ttk.Label(lf_cover, text="Henüz görsel seçilmedi")
        self.proj_cover_label.pack(side="left", padx=10)

        self.content_editor = ContentBlockEditor(scroll_frame, parent_canvas=canvas, title=" 3. Proje Sayfa İçerik Blokları Editörü ")
        self.content_editor.pack(fill="x", padx=10, pady=8)

        self.content_editor.add_block('heading', {'level': 'h2', 'text': 'Project Overview'})
        self.content_editor.add_block('paragraph', {'text': 'This research project addresses autonomous navigation and adaptive decision making...'})

        lf_team = ttk.LabelFrame(scroll_frame, text=" 4. Projedeki Üyeler ")
        lf_team.pack(fill="x", padx=10, pady=8)

        self.team_container = ttk.Frame(lf_team)
        self.team_container.pack(fill="x", padx=5, pady=5)

        ttk.Button(lf_team, text="+ Üye Ekle", command=self.add_member_row).pack(anchor="w", padx=10, pady=5)

        lf_pubs = ttk.LabelFrame(scroll_frame, text=" 5. İlgili Yayınlar (Publications) ")
        lf_pubs.pack(fill="x", padx=10, pady=8)

        self.pub_container = ttk.Frame(lf_pubs)
        self.pub_container.pack(fill="x", padx=5, pady=5)

        ttk.Button(lf_pubs, text="+ Yayın Ekle", command=self.add_pub_row).pack(anchor="w", padx=10, pady=5)

        bind_mouse_wheel(scroll_frame, canvas)

    def build_person_tab(self):
        canvas = tk.Canvas(self.person_tab, bg=self.bg_light, highlightthickness=0)
        scrollbar = ttk.Scrollbar(self.person_tab, orient="vertical", command=canvas.yview)
        scroll_frame = ttk.Frame(canvas)

        def _update_scroll_region(event=None):
            canvas.update_idletasks()
            canvas.configure(scrollregion=canvas.bbox("all"))

        scroll_frame.bind("<Configure>", _update_scroll_region)
        canvas.create_window((0, 0), window=scroll_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        bind_mouse_wheel(scroll_frame, canvas)

        # Quick person load & action toolbar
        person_actions_bar = ttk.Frame(scroll_frame)
        person_actions_bar.pack(fill="x", padx=10, pady=(8, 4))

        ttk.Button(person_actions_bar, text="📂 Kayıtlı Kişi Yükle / Düzenle", style="Accent.TButton", command=self.open_person_prompt).pack(side="left", padx=(0, 6))
        ttk.Button(person_actions_bar, text="🔄 Formu Temizle / Yeni Kişi", command=self.reset_person_form).pack(side="left", padx=2)
        self.person_loaded_badge = ttk.Label(person_actions_bar, text="", font=('Inter', 8, 'bold'), foreground='#2563eb')
        self.person_loaded_badge.pack(side="left", padx=10)
        ttk.Label(person_actions_bar, text="💡 Hedef klasördeki kayıtlı ekip üyelerini yükleyip düzenleyebilirsiniz.", font=('Inter', 8, 'italic'), foreground='#64748b').pack(side="left", padx=4)

        lf = ttk.LabelFrame(scroll_frame, text=" Kişi Profil Bilgileri (Person Metadata) ")
        lf.pack(fill="x", padx=10, pady=10)

        ttk.Label(lf, text="Ad Soyad (Tam İsim):").grid(row=0, column=0, sticky="w", padx=10, pady=2)
        self.person_name_entry = ttk.Entry(lf, width=40)
        self.person_name_entry.grid(row=0, column=1, sticky="ew", padx=10, pady=2)

        ttk.Label(lf, text="Kategori:").grid(row=1, column=0, sticky="w", padx=10, pady=2)
        self.person_cat_combo = ttk.Combobox(lf, values=[
            'Postdoctoral Researchers',
            'PhD Graduate Students',
            'Masters Graduate Students',
            'Undergraduate Students'
        ], state="readonly")
        self.person_cat_combo.set('PhD Graduate Students')
        self.person_cat_combo.grid(row=1, column=1, sticky="ew", padx=10, pady=2)

        ttk.Label(lf, text="Unvan/Rol (Role):").grid(row=2, column=0, sticky="w", padx=10, pady=2)
        self.person_role_entry = ttk.Entry(lf)
        self.person_role_entry.insert(0, "PhD Researcher")
        self.person_role_entry.grid(row=2, column=1, sticky="ew", padx=10, pady=2)

        ttk.Label(lf, text="Departman/Bölüm:").grid(row=3, column=0, sticky="w", padx=10, pady=2)
        self.person_dept_entry = ttk.Entry(lf)
        self.person_dept_entry.insert(0, "Control and Automation Engineering")
        self.person_dept_entry.grid(row=3, column=1, sticky="ew", padx=10, pady=2)

        ttk.Label(lf, text="Profil Fotoğrafı:").grid(row=4, column=0, sticky="w", padx=10, pady=2)
        f_photo = ttk.Frame(lf)
        f_photo.grid(row=4, column=1, sticky="w", padx=10, pady=2)
        ttk.Button(f_photo, text="Fotoğraf Seç...", command=self.select_person_photo).pack(side="left")
        self.person_photo_label = ttk.Label(f_photo, text="İsteğe bağlı")
        self.person_photo_label.pack(side="left", padx=10)

        ttk.Label(lf, text="Hakkında (About Me):").grid(row=5, column=0, sticky="nw", padx=10, pady=2)
        self.person_about_text = tk.Text(lf, height=4, font=('Inter', 9))
        self.person_about_text.grid(row=5, column=1, sticky="ew", padx=10, pady=2)

        lf.columnconfigure(1, weight=1)

        # 🎓 Akademik Profiller & Sosyal Ağlar (Logolu)
        lf_social = ttk.LabelFrame(scroll_frame, text=" 🎓 Akademik & Sosyal Ağ Bağlantıları (Logolu) ")
        lf_social.pack(fill="x", padx=10, pady=(0, 10))

        ttk.Label(lf_social, text="Google Scholar:").grid(row=0, column=0, sticky="w", padx=10, pady=3)
        self.person_scholar_entry = ttk.Entry(lf_social)
        self.person_scholar_entry.grid(row=0, column=1, sticky="ew", padx=10, pady=3)
        ttk.Label(lf_social, text="💡 URL veya kullanıcı ID (örn: https://scholar.google.com/citations?user=...)", font=('Inter', 8, 'italic'), foreground='#64748b').grid(row=1, column=1, sticky="w", padx=10, pady=(0, 4))

        ttk.Label(lf_social, text="ORCID iD / URL:").grid(row=2, column=0, sticky="w", padx=10, pady=3)
        self.person_orcid_entry = ttk.Entry(lf_social)
        self.person_orcid_entry.grid(row=2, column=1, sticky="ew", padx=10, pady=3)
        ttk.Label(lf_social, text="💡 16 haneli ORCID iD veya URL (örn: 0000-0002-1825-0097 veya https://orcid.org/...)", font=('Inter', 8, 'italic'), foreground='#64748b').grid(row=3, column=1, sticky="w", padx=10, pady=(0, 4))

        ttk.Label(lf_social, text="ResearchGate:").grid(row=4, column=0, sticky="w", padx=10, pady=3)
        self.person_rg_entry = ttk.Entry(lf_social)
        self.person_rg_entry.grid(row=4, column=1, sticky="ew", padx=10, pady=3)
        ttk.Label(lf_social, text="💡 Profil URL veya kullanıcı adı (örn: https://www.researchgate.net/profile/...)", font=('Inter', 8, 'italic'), foreground='#64748b').grid(row=5, column=1, sticky="w", padx=10, pady=(0, 4))

        ttk.Label(lf_social, text="GitHub:").grid(row=6, column=0, sticky="w", padx=10, pady=3)
        self.person_github_entry = ttk.Entry(lf_social)
        self.person_github_entry.grid(row=6, column=1, sticky="ew", padx=10, pady=3)
        ttk.Label(lf_social, text="💡 GitHub profil URL veya kullanıcı adı (örn: https://github.com/kullanici)", font=('Inter', 8, 'italic'), foreground='#64748b').grid(row=7, column=1, sticky="w", padx=10, pady=(0, 4))

        ttk.Label(lf_social, text="LinkedIn:").grid(row=8, column=0, sticky="w", padx=10, pady=3)
        self.person_linkedin_entry = ttk.Entry(lf_social)
        self.person_linkedin_entry.grid(row=8, column=1, sticky="ew", padx=10, pady=3)
        ttk.Label(lf_social, text="💡 LinkedIn profil URL (örn: https://linkedin.com/in/...)", font=('Inter', 8, 'italic'), foreground='#64748b').grid(row=9, column=1, sticky="w", padx=10, pady=(0, 4))

        ttk.Label(lf_social, text="Kişisel Web Sitesi:").grid(row=10, column=0, sticky="w", padx=10, pady=3)
        self.person_website_entry = ttk.Entry(lf_social)
        self.person_website_entry.grid(row=10, column=1, sticky="ew", padx=10, pady=3)
        ttk.Label(lf_social, text="💡 Kişisel web sitesi, portfolyo veya blog adresi", font=('Inter', 8, 'italic'), foreground='#64748b').grid(row=11, column=1, sticky="w", padx=10, pady=(0, 4))

        ttk.Label(lf_social, text="E-Posta (Email):").grid(row=12, column=0, sticky="w", padx=10, pady=3)
        self.person_email_entry = ttk.Entry(lf_social)
        self.person_email_entry.grid(row=12, column=1, sticky="ew", padx=10, pady=3)
        ttk.Label(lf_social, text="💡 Kurumsal veya kişisel iletişim e-posta adresi", font=('Inter', 8, 'italic'), foreground='#64748b').grid(row=13, column=1, sticky="w", padx=10, pady=(0, 4))

        lf_social.columnconfigure(1, weight=1)

    def build_news_tab(self):
        canvas = tk.Canvas(self.news_tab, bg=self.bg_light, highlightthickness=0)
        scrollbar = ttk.Scrollbar(self.news_tab, orient="vertical", command=canvas.yview)
        scroll_frame = ttk.Frame(canvas)

        def _update_scroll_region(event=None):
            canvas.update_idletasks()
            canvas.configure(scrollregion=canvas.bbox("all"))

        scroll_frame.bind("<Configure>", _update_scroll_region)
        canvas.create_window((0, 0), window=scroll_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        bind_mouse_wheel(scroll_frame, canvas)

        # Quick news load & action toolbar
        news_actions_bar = ttk.Frame(scroll_frame)
        news_actions_bar.pack(fill="x", padx=10, pady=(8, 4))

        ttk.Button(news_actions_bar, text="📂 Kayıtlı Haber Yükle / Düzenle", style="Accent.TButton", command=self.open_news_prompt).pack(side="left", padx=(0, 6))
        ttk.Button(news_actions_bar, text="🔄 Formu Temizle / Yeni Haber", command=self.reset_news_form).pack(side="left", padx=2)
        self.news_loaded_badge = ttk.Label(news_actions_bar, text="", font=('Inter', 8, 'bold'), foreground='#2563eb')
        self.news_loaded_badge.pack(side="left", padx=10)
        ttk.Label(news_actions_bar, text="💡 Hedef klasördeki kayıtlı haberleri yükleyip düzenleyebilirsiniz.", font=('Inter', 8, 'italic'), foreground='#64748b').pack(side="left", padx=4)

        lf_basic = ttk.LabelFrame(scroll_frame, text=" 1. Haber Temel Bilgileri ")
        lf_basic.pack(fill="x", padx=10, pady=8)

        ttk.Label(lf_basic, text="Haber Başlığı:").grid(row=0, column=0, sticky="w", padx=10, pady=2)
        self.news_title_entry = ttk.Entry(lf_basic, width=50)
        self.news_title_entry.grid(row=0, column=1, sticky="ew", padx=10, pady=2)

        ttk.Label(lf_basic, text="Tarih:").grid(row=1, column=0, sticky="w", padx=10, pady=2)
        today_str = datetime.date.today().strftime("%B %d, %Y")
        self.news_date_entry = ttk.Entry(lf_basic, width=25)
        self.news_date_entry.insert(0, today_str)
        self.news_date_entry.grid(row=1, column=1, sticky="w", padx=10, pady=2)

        ttk.Label(lf_basic, text="Kategori / Etiket:").grid(row=2, column=0, sticky="w", padx=10, pady=2)
        self.news_cat_combo = ttk.Combobox(lf_basic, values=['Announcements', 'Awards', 'Grants', 'Conference', 'Research Breakthrough'], width=25)
        self.news_cat_combo.set('Announcements')
        self.news_cat_combo.grid(row=2, column=1, sticky="w", padx=10, pady=2)

        ttk.Label(lf_basic, text="Kısa Özet (Excerpt):").grid(row=3, column=0, sticky="nw", padx=10, pady=2)
        self.news_summary_text = tk.Text(lf_basic, height=3, font=('Inter', 9))
        self.news_summary_text.grid(row=3, column=1, sticky="ew", padx=10, pady=2)

        lf_basic.columnconfigure(1, weight=1)

        self.news_content_editor = ContentBlockEditor(scroll_frame, parent_canvas=canvas, title=" 2. Haber Detay İçerik Blokları Editörü ")
        self.news_content_editor.pack(fill="x", padx=10, pady=8)

        self.news_content_editor.add_block('paragraph', {'text': 'We are excited to announce our latest milestone...'})

    def build_pub_tab(self):
        canvas = tk.Canvas(self.pub_tab, bg=self.bg_light, highlightthickness=0)
        scrollbar = ttk.Scrollbar(self.pub_tab, orient="vertical", command=canvas.yview)
        scroll_frame = ttk.Frame(canvas)

        def _update_scroll_region(event=None):
            canvas.update_idletasks()
            canvas.configure(scrollregion=canvas.bbox("all"))

        scroll_frame.bind("<Configure>", _update_scroll_region)
        canvas.create_window((0, 0), window=scroll_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        bind_mouse_wheel(scroll_frame, canvas)

        # Quick publication load & action toolbar
        pub_actions_bar = ttk.Frame(scroll_frame)
        pub_actions_bar.pack(fill="x", padx=10, pady=(8, 4))

        ttk.Button(pub_actions_bar, text="📂 Kayıtlı Yayın Yükle / Düzenle", style="Accent.TButton", command=self.open_publication_prompt).pack(side="left", padx=(0, 6))
        ttk.Button(pub_actions_bar, text="🔄 Formu Temizle / Yeni Yayın", command=self.reset_pub_form).pack(side="left", padx=2)
        self.pub_loaded_badge = ttk.Label(pub_actions_bar, text="", font=('Inter', 8, 'bold'), foreground='#2563eb')
        self.pub_loaded_badge.pack(side="left", padx=10)
        ttk.Label(pub_actions_bar, text="💡 Hedef klasördeki kayıtlı yayınları yükleyip düzenleyebilirsiniz.", font=('Inter', 8, 'italic'), foreground='#64748b').pack(side="left", padx=4)

        lf = ttk.LabelFrame(scroll_frame, text=" Yayın Detayları (Publication Metadata) ")
        lf.pack(fill="x", padx=10, pady=10)

        ttk.Label(lf, text="Yayın Başlığı (Title):").grid(row=0, column=0, sticky="w", padx=10, pady=2)
        self.pub_item_title_entry = ttk.Entry(lf, width=50)
        self.pub_item_title_entry.grid(row=0, column=1, sticky="ew", padx=10, pady=2)

        ttk.Label(lf, text="Yazarlar (Authors):").grid(row=1, column=0, sticky="w", padx=10, pady=2)
        self.pub_item_authors_entry = ttk.Entry(lf, width=50)
        self.pub_item_authors_entry.insert(0, "Gizem Asya Yılmaz, Nurettin Tarık Mut")
        self.pub_item_authors_entry.grid(row=1, column=1, sticky="ew", padx=10, pady=2)

        ttk.Label(lf, text="Konferans / Dergi (Venue):").grid(row=2, column=0, sticky="w", padx=10, pady=2)
        self.pub_item_venue_entry = ttk.Entry(lf, width=50)
        self.pub_item_venue_entry.insert(0, "IEEE Transactions on Robotics (T-RO)")
        self.pub_item_venue_entry.grid(row=2, column=1, sticky="ew", padx=10, pady=2)

        ttk.Label(lf, text="Yıl (Year):").grid(row=3, column=0, sticky="w", padx=10, pady=2)
        self.pub_item_year_entry = ttk.Entry(lf, width=15)
        self.pub_item_year_entry.insert(0, "2026")
        self.pub_item_year_entry.grid(row=3, column=1, sticky="w", padx=10, pady=2)

        ttk.Label(lf, text="Tarih (YYYY-MM-DD):").grid(row=4, column=0, sticky="w", padx=10, pady=2)
        self.pub_item_date_entry = ttk.Entry(lf, width=20)
        self.pub_item_date_entry.insert(0, datetime.date.today().strftime("%Y-%m-%d"))
        self.pub_item_date_entry.grid(row=4, column=1, sticky="w", padx=10, pady=2)

        lf_links = ttk.LabelFrame(scroll_frame, text=" Yayın Bağlantıları (Links & Resources) ")
        lf_links.pack(fill="x", padx=10, pady=10)

        ttk.Label(lf_links, text="Paper PDF Link:").grid(row=0, column=0, sticky="w", padx=10, pady=4)
        self.pub_link_pdf_entry = ttk.Entry(lf_links)
        self.pub_link_pdf_entry.insert(0, "#")
        self.pub_link_pdf_entry.grid(row=0, column=1, sticky="ew", padx=10, pady=4)

        ttk.Label(lf_links, text="DOI Link:").grid(row=1, column=0, sticky="w", padx=10, pady=4)
        self.pub_link_doi_entry = ttk.Entry(lf_links)
        self.pub_link_doi_entry.grid(row=1, column=1, sticky="ew", padx=10, pady=4)

        ttk.Label(lf_links, text="Kod Deposu (Code):").grid(row=2, column=0, sticky="w", padx=10, pady=4)
        self.pub_link_code_entry = ttk.Entry(lf_links)
        self.pub_link_code_entry.insert(0, "#")
        self.pub_link_code_entry.grid(row=2, column=1, sticky="ew", padx=10, pady=4)

        ttk.Label(lf_links, text="Proje Sayfası (Project):").grid(row=3, column=0, sticky="w", padx=10, pady=4)
        self.pub_link_proj_entry = ttk.Entry(lf_links)
        self.pub_link_proj_entry.grid(row=3, column=1, sticky="ew", padx=10, pady=4)

        ttk.Label(lf_links, text="Video Link:").grid(row=4, column=0, sticky="w", padx=10, pady=4)
        self.pub_link_video_entry = ttk.Entry(lf_links)
        self.pub_link_video_entry.grid(row=4, column=1, sticky="ew", padx=10, pady=4)

        ttk.Label(lf_links, text="Veri Seti (Dataset):").grid(row=5, column=0, sticky="w", padx=10, pady=4)
        self.pub_link_data_entry = ttk.Entry(lf_links)
        self.pub_link_data_entry.grid(row=5, column=1, sticky="ew", padx=10, pady=4)

        lf.columnconfigure(1, weight=1)
        lf_links.columnconfigure(1, weight=1)

    def create_right_panel(self):
        right_frame = ttk.Frame(self)
        right_frame.grid(row=1, column=1, sticky="nsew", padx=(0, 15), pady=15)

        lf_dest = ttk.LabelFrame(right_frame, text=" ⚙️ Kayıt Hedef Klasörü ")
        lf_dest.pack(fill="x", pady=(0, 10))

        ttk.Label(lf_dest, text="Seçilen Hedef Dizin:").pack(anchor="w", padx=8, pady=(6, 2))
        dest_entry = ttk.Entry(lf_dest, textvariable=self.output_dir_var)
        dest_entry.pack(fill="x", padx=8, pady=2)

        dest_btn_box = ttk.Frame(lf_dest)
        dest_btn_box.pack(fill="x", padx=8, pady=6)
        ttk.Button(dest_btn_box, text="Hedef Klasör Değiştir...", command=self.browse_output_dir).pack(side="left", fill="x", expand=True, padx=(0, 4))
        ttk.Button(dest_btn_box, text="📂 İçerik İçe Aktar / Düzenle", style="Accent.TButton", command=self.open_universal_content_prompt).pack(side="left", fill="x", expand=True)

        lf_actions = ttk.LabelFrame(right_frame, text=" 📦 Sayfa Üretim & Canlı Önizleme ")
        lf_actions.pack(fill="x", pady=10)

        ttk.Button(lf_actions, text="💾 Aktif Sekmedeki İçeriği Üret", style="Primary.TButton", command=self.generate_files_prompt).pack(fill="x", padx=10, pady=8)
        ttk.Button(lf_actions, text="👁️ Tarayıcıda Canlı Önizle", command=self.open_live_preview).pack(fill="x", padx=10, pady=5)

        ttk.Checkbutton(lf_actions, text="⚡ Otomatik Önizleme Yenile (Hot-Reload)", variable=self.auto_sync_var).pack(anchor="w", padx=12, pady=6)

        lf_info = ttk.LabelFrame(right_frame, text=" 💡 Standalone Garanti ")
        lf_info.pack(fill="x", pady=10)

        ttk.Label(lf_info, text="• Canlı önizleme %100 dahili CSS/JS içerir ve herhangi bir bilgisayarda dış dosya olmadan kusursuz çalışır.\n• Üretim esnasında kaydedilecek hedef klasör sorulur.", font=('Inter', 8), wraplength=280).pack(anchor="w", padx=10, pady=5)

    def select_proj_cover(self):
        p = filedialog.askopenfilename(filetypes=[("Images", "*.png;*.jpg;*.jpeg;*.webp;*.svg")])
        if p:
            self.proj_cover_path = p
            self.proj_cover_label.configure(text=os.path.basename(p))

    def select_person_photo(self):
        p = filedialog.askopenfilename(filetypes=[("Images", "*.png;*.jpg;*.jpeg;*.webp;*.svg")])
        if p:
            self.person_photo_path = p
            self.person_photo_label.configure(text=os.path.basename(p))

    def add_member_row(self):
        f = ttk.Frame(self.team_container)
        f.pack(fill="x", pady=2)
        
        combo = ttk.Combobox(f, values=self.existing_people_names, width=32)
        if self.existing_people_names:
            combo.set(self.existing_people_names[len(self.member_rows) % len(self.existing_people_names)])
        combo.pack(side="left", padx=2)
        
        btn_del = ttk.Button(f, text="✕", width=3, command=lambda: self.remove_member_row(f, combo))
        btn_del.pack(side="left", padx=2)
        self.member_rows.append(combo)

    def remove_member_row(self, frame, combo):
        frame.destroy()
        if combo in self.member_rows:
            self.member_rows.remove(combo)

    def add_pub_row(self):
        f = ttk.Frame(self.pub_container)
        f.pack(fill="x", pady=2)
        e_title = ttk.Entry(f, width=35)
        e_title.insert(0, "Yayın Başlığı")
        e_title.pack(side="left", padx=2)

        e_link = ttk.Entry(f, width=25)
        e_link.insert(0, "")
        e_link.pack(side="left", padx=2)

        btn_del = ttk.Button(f, text="✕", width=3, command=lambda: self.remove_pub_row(f, (e_title, e_link)))
        btn_del.pack(side="left", padx=2)
        self.pub_rows.append((e_title, e_link))

    def remove_pub_row(self, frame, pub_tuple):
        frame.destroy()
        if pub_tuple in self.pub_rows:
            self.pub_rows.remove(pub_tuple)

    def browse_output_dir(self):
        d = filedialog.askdirectory(title="Varsayılan Hedef Klasörü Seçin", initialdir=self.output_dir_var.get())
        if d:
            self.output_dir_var.set(d)
            self.check_and_prompt_saved_content(d, silent_if_empty=False)

    def scan_all_saved_content(self, base_dir):
        """
        Scans base_dir and all standard website subdirectories for saved HTML content across:
        - Projects (projects/data/)
        - People / Team Members (people/data/)
        - News (news/data/)
        - Publications (publications/data/)
        - Base directory root or general data folders
        Returns a unified list of scanned items with metadata.
        """
        items = []
        if not base_dir or not os.path.isdir(base_dir):
            return items

        search_dirs = [
            ("project", os.path.join(base_dir, "projects", "data")),
            ("person", os.path.join(base_dir, "people", "data")),
            ("news", os.path.join(base_dir, "news", "data")),
            ("publication", os.path.join(base_dir, "publications", "data")),
            ("auto", os.path.join(base_dir, "data")),
            ("auto", base_dir)
        ]

        visited_paths = set()
        for default_type, sdir in search_dirs:
            if not os.path.isdir(sdir):
                continue
            try:
                for fname in sorted(os.listdir(sdir)):
                    if fname.lower().endswith(".html") and not fname.startswith(".") and not fname.startswith("index"):
                        fpath = os.path.join(sdir, fname)
                        norm_p = os.path.normpath(fpath)
                        if norm_p in visited_paths:
                            continue
                        visited_paths.add(norm_p)

                        try:
                            with open(fpath, "r", encoding="utf-8", errors="ignore") as f:
                                content = f.read()

                            m_proj = re.search(r'<!--\s*PROJECT_METADATA:\s*(\{[\s\S]*?\})\s*-->', content)
                            m_pers = re.search(r'<!--\s*PERSON_METADATA:\s*(\{[\s\S]*?\})\s*-->', content)
                            m_news = re.search(r'<!--\s*NEWS_METADATA:\s*(\{[\s\S]*?\})\s*-->', content)
                            m_pub = re.search(r'<!--\s*PUBLICATION_METADATA:\s*(\{[\s\S]*?\})\s*-->', content)

                            mtime = os.path.getmtime(fpath)
                            mtime_str = datetime.datetime.fromtimestamp(mtime).strftime("%Y-%m-%d %H:%M")

                            if m_proj:
                                meta = json.loads(m_proj.group(1))
                                tags_val = meta.get('tags', [])
                                tag_str = ', '.join(tags_val[:2]) if isinstance(tags_val, list) else str(tags_val)
                                items.append({
                                    "type": "project",
                                    "type_label": "🚀 Proje",
                                    "title": meta.get("title", fname.replace(".html", "").replace("_", " ").title()),
                                    "detail": f"{meta.get('status', 'Active')} • {tag_str}",
                                    "date": meta.get("date", mtime_str),
                                    "mtime": mtime_str,
                                    "filename": fname,
                                    "file_path": fpath,
                                    "meta": meta,
                                    "content": content
                                })
                            elif m_pers:
                                meta = json.loads(m_pers.group(1))
                                items.append({
                                    "type": "person",
                                    "type_label": "👤 Ekip Üyesi",
                                    "title": meta.get("name", fname.replace(".html", "").replace("_", " ").title()),
                                    "detail": f"{meta.get('role', '')} ({meta.get('category', '')})",
                                    "date": mtime_str,
                                    "mtime": mtime_str,
                                    "filename": fname,
                                    "file_path": fpath,
                                    "meta": meta,
                                    "content": content
                                })
                            elif m_news:
                                meta = json.loads(m_news.group(1))
                                items.append({
                                    "type": "news",
                                    "type_label": "📰 Haber",
                                    "title": meta.get("title", fname.replace(".html", "").replace("_", " ").title()),
                                    "detail": meta.get("category", "Announcements"),
                                    "date": meta.get("date", mtime_str),
                                    "mtime": mtime_str,
                                    "filename": fname,
                                    "file_path": fpath,
                                    "meta": meta,
                                    "content": content
                                })
                            elif m_pub:
                                meta = json.loads(m_pub.group(1))
                                items.append({
                                    "type": "publication",
                                    "type_label": "📚 Yayın",
                                    "title": meta.get("title", fname.replace(".html", "").replace("_", " ").title()),
                                    "detail": f"{meta.get('venue', '')[:45]} ({meta.get('year', '')})",
                                    "date": str(meta.get("year", meta.get("date", mtime_str))),
                                    "mtime": mtime_str,
                                    "filename": fname,
                                    "file_path": fpath,
                                    "meta": meta,
                                    "content": content
                                })
                            elif "profile-card" in content or "personProfilePhoto" in content:
                                # Legacy Person fallback
                                m_name = re.search(r'<h2>(.*?)</h2>', content)
                                name_val = m_name.group(1).strip() if m_name else fname.replace(".html", "").title()
                                items.append({
                                    "type": "person",
                                    "type_label": "👤 Ekip Üyesi",
                                    "title": name_val,
                                    "detail": "Kişi Profili (HTML)",
                                    "date": mtime_str,
                                    "mtime": mtime_str,
                                    "filename": fname,
                                    "file_path": fpath,
                                    "meta": {"name": name_val},
                                    "content": content
                                })
                        except Exception:
                            pass
            except Exception:
                pass

        return items

    def scan_saved_projects(self, base_dir):
        """Backward-compatible helper returning only project items."""
        return [it for it in self.scan_all_saved_content(base_dir) if it.get("type") == "project"]

    def show_content_picker_dialog(self, items, base_dir, initial_filter=None):
        """Displays an interactive modal dialog listing discovered saved content across all categories for loading."""
        if not items:
            return

        dlg = tk.Toplevel(self)
        dlg.title("📂 Kayıtlı İçerikler (İçe Aktar & Düzenle)")
        dlg.geometry("860x540")
        dlg.configure(bg="#f8fafc")
        dlg.transient(self)
        dlg.grab_set()

        try:
            dlg.update_idletasks()
            x = self.winfo_x() + (self.winfo_width() - 860) // 2
            y = self.winfo_y() + (self.winfo_height() - 540) // 2
            dlg.geometry(f"+{max(0, x)}+{max(0, y)}")
        except Exception:
            pass

        hdr = tk.Frame(dlg, bg="#0f172a", padx=18, pady=14)
        hdr.pack(fill="x")

        ttk.Label(hdr, text="📂 Kayıtlı İçerikler Tespit Edildi (Content Loader & Editor)", font=('Inter', 12, 'bold'), foreground="#ffffff", background="#0f172a").pack(anchor="w")
        folder_display = os.path.basename(base_dir) or base_dir
        ttk.Label(hdr, text=f"'{folder_display}' hedef klasöründe toplam {len(items)} kayıtlı içerik bulundu. Düzenlemek istediğiniz içeriği seçip ilgili sekmeye aktarabilirsiniz:", font=('Inter', 9), foreground="#94a3b8", background="#0f172a").pack(anchor="w", pady=(2, 0))

        counts = {
            "all": len(items),
            "project": sum(1 for it in items if it.get("type") == "project"),
            "person": sum(1 for it in items if it.get("type") == "person"),
            "news": sum(1 for it in items if it.get("type") == "news"),
            "publication": sum(1 for it in items if it.get("type") == "publication")
        }

        # Filter bar
        filter_bar = ttk.Frame(dlg, padding=(12, 8))
        filter_bar.pack(fill="x")

        start_filter = initial_filter if (initial_filter in counts and counts[initial_filter] > 0) else "all"
        current_type_filter = tk.StringVar(value=start_filter)

        pills_f = ttk.Frame(filter_bar)
        pills_f.pack(side="left", fill="x", expand=True)

        search_f = ttk.Frame(filter_bar)
        search_f.pack(side="right")
        ttk.Label(search_f, text="🔍 Ara:", font=('Inter', 9)).pack(side="left", padx=(0, 4))
        search_entry = ttk.Entry(search_f, width=18)
        search_entry.pack(side="left")

        content_f = ttk.Frame(dlg, padding=(12, 0, 12, 8))
        content_f.pack(fill="both", expand=True)

        cols = ("type", "title", "detail", "date", "filename")
        tree = ttk.Treeview(content_f, columns=cols, show="headings", selectmode="browse")
        tree.heading("type", text="Tür")
        tree.heading("title", text="Başlık / İsim")
        tree.heading("detail", text="Detay / Kategori / Rol")
        tree.heading("date", text="Tarih")
        tree.heading("filename", text="Dosya Adı")

        tree.column("type", width=110, anchor="center")
        tree.column("title", width=260, anchor="w")
        tree.column("detail", width=220, anchor="w")
        tree.column("date", width=90, anchor="center")
        tree.column("filename", width=140, anchor="w")

        tree_scroll = ttk.Scrollbar(content_f, orient="vertical", command=tree.yview)
        tree.configure(yscrollcommand=tree_scroll.set)

        tree.pack(side="left", fill="both", expand=True)
        tree_scroll.pack(side="right", fill="y")

        item_map = {}

        def refresh_tree(*args):
            tree.delete(*tree.get_children())
            item_map.clear()

            ftype = current_type_filter.get()
            q = search_entry.get().strip().lower()

            filtered = []
            for it in items:
                if ftype != "all" and it.get("type") != ftype:
                    continue
                if q:
                    searchable = f"{it.get('title', '')} {it.get('detail', '')} {it.get('filename', '')}".lower()
                    if q not in searchable:
                        continue
                filtered.append(it)

            for idx, it in enumerate(filtered):
                iid = f"item_{idx}"
                tree.insert("", "end", iid=iid, values=(
                    it.get("type_label", it.get("type")),
                    it.get("title", ""),
                    it.get("detail", ""),
                    it.get("date", ""),
                    it.get("filename", "")
                ))
                item_map[iid] = it

            if filtered:
                first_id = "item_0"
                if tree.exists(first_id):
                    tree.selection_set(first_id)
                    tree.focus(first_id)

        pill_defs = [
            ("all", f"🌟 Tümü ({counts['all']})"),
            ("project", f"🚀 Projeler ({counts['project']})"),
            ("person", f"👤 Ekip Üyeleri ({counts['person']})"),
            ("news", f"📰 Haberler ({counts['news']})"),
            ("publication", f"📚 Yayınlar ({counts['publication']})")
        ]

        for pkey, plabel in pill_defs:
            btn = ttk.Radiobutton(
                pills_f,
                text=plabel,
                value=pkey,
                variable=current_type_filter,
                command=refresh_tree
            )
            btn.pack(side="left", padx=2)

        search_entry.bind("<KeyRelease>", refresh_tree)
        refresh_tree()

        def on_select_and_load(event=None):
            sel = tree.selection()
            if not sel:
                messagebox.showwarning("Uyarı", "Lütfen listeden bir içerik seçin.", parent=dlg)
                return
            selected_data = item_map[sel[0]]
            dlg.destroy()
            self.load_scanned_item(selected_data)

        tree.bind("<Double-1>", on_select_and_load)
        tree.bind("<Return>", on_select_and_load)

        btn_bar = ttk.Frame(dlg, padding=(12, 10))
        btn_bar.pack(fill="x")

        ttk.Button(btn_bar, text="✅ Seçilen İçeriği Editöre Yükle", style="Primary.TButton", command=on_select_and_load).pack(side="left", padx=(0, 8))
        ttk.Button(btn_bar, text="🔍 Başka HTML Dosyası Seç...", command=lambda: (dlg.destroy(), self.browse_and_load_any_file())).pack(side="left", padx=4)
        ttk.Button(btn_bar, text="➕ Yeni İçerik Olarak Devam Et (Kapat)", command=dlg.destroy).pack(side="right", padx=4)

    def show_project_picker_dialog(self, projects, base_dir):
        """Backward-compatible helper redirecting to show_content_picker_dialog."""
        self.show_content_picker_dialog(projects, base_dir, initial_filter="project")

    def check_and_prompt_saved_content(self, directory, silent_if_empty=True, initial_filter=None):
        items = self.scan_all_saved_content(directory)
        if items:
            self.show_content_picker_dialog(items, directory, initial_filter=initial_filter)
        elif not silent_if_empty:
            ans = messagebox.askyesno(
                "İçerik Bulunamadı",
                f"'{os.path.basename(directory)}' klasöründe kayıtlı içerik bulunamadı.\n\nBaşka bir konumdan HTML dosyası seçmek ister misiniz?"
            )
            if ans:
                self.browse_and_load_any_file()

    def check_and_prompt_saved_projects(self, directory, silent_if_empty=True):
        self.check_and_prompt_saved_content(directory, silent_if_empty=silent_if_empty, initial_filter="project")

    def prompt_for_category(self, cat_filter=None):
        """Unified prompt triggered by tab toolbar or right panel button."""
        current_dir = self.output_dir_var.get()
        items = self.scan_all_saved_content(current_dir) if current_dir else []
        matching = [it for it in items if it.get("type") == cat_filter] if cat_filter else items

        if matching:
            self.show_content_picker_dialog(items, current_dir, initial_filter=cat_filter)
        else:
            cat_name = {
                "project": "proje",
                "person": "ekip üyesi",
                "news": "haber",
                "publication": "yayın"
            }.get(cat_filter, "içerik")
            ans = messagebox.askyesno(
                f"Kayıtlı {cat_name.title()} Bulunamadı",
                f"'{os.path.basename(current_dir)}' klasöründe kayıtlı {cat_name} bulunamadı.\n\nBaşka bir konumdan HTML dosyası (.html) seçmek ister misiniz?"
            )
            if ans:
                self.browse_and_load_any_file()

    def open_project_prompt(self):
        self.prompt_for_category("project")

    def open_person_prompt(self):
        self.prompt_for_category("person")

    def open_news_prompt(self):
        self.prompt_for_category("news")

    def open_publication_prompt(self):
        self.prompt_for_category("publication")

    def open_universal_content_prompt(self):
        curr_tab = self.notebook.index(self.notebook.select())
        cat_map = {0: "project", 1: "person", 2: "news", 3: "publication"}
        default_filter = cat_map.get(curr_tab, None)
        self.prompt_for_category(default_filter)

    def browse_and_load_any_file(self):
        """Allows selecting any HTML file directly from file dialog."""
        initial_dir = self.output_dir_var.get()
        file_p = filedialog.askopenfilename(
            title="Açılacak MICROLab HTML Dosyasını Seçin",
            initialdir=initial_dir,
            filetypes=[("MICROLab HTML Dosyaları", "*.html"), ("Tüm Dosyalar", "*.*")]
        )
        if file_p:
            self.load_any_html_file(file_p)

    def browse_and_load_project_file(self):
        self.browse_and_load_any_file()

    def load_project_file(self, file_path):
        self.load_any_html_file(file_path)

    def load_any_html_file(self, file_path):
        """Inspects and loads any HTML file into its matching editor tab."""
        if not os.path.isfile(file_path):
            messagebox.showerror("Hata", f"Dosya bulunamadı: {file_path}")
            return
        try:
            with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                content = f.read()

            m_proj = re.search(r'<!--\s*PROJECT_METADATA:\s*(\{[\s\S]*?\})\s*-->', content)
            m_pers = re.search(r'<!--\s*PERSON_METADATA:\s*(\{[\s\S]*?\})\s*-->', content)
            m_news = re.search(r'<!--\s*NEWS_METADATA:\s*(\{[\s\S]*?\})\s*-->', content)
            m_pub = re.search(r'<!--\s*PUBLICATION_METADATA:\s*(\{[\s\S]*?\})\s*-->', content)

            if m_proj:
                meta = json.loads(m_proj.group(1))
                self.load_project_from_data(meta, html_content=content, file_path=file_path)
            elif m_pers:
                meta = json.loads(m_pers.group(1))
                self.load_person_from_data(meta, html_content=content, file_path=file_path)
            elif m_news:
                meta = json.loads(m_news.group(1))
                self.load_news_from_data(meta, html_content=content, file_path=file_path)
            elif m_pub:
                meta = json.loads(m_pub.group(1))
                self.load_publication_from_data(meta, html_content=content, file_path=file_path)
            elif "profile-card" in content or "personProfilePhoto" in content:
                self.load_person_from_data({}, html_content=content, file_path=file_path)
            elif "blog-content" in content and "news" in file_path.lower():
                self.load_news_from_data({}, html_content=content, file_path=file_path)
            elif "blog-content" in content:
                self.load_project_from_data({}, html_content=content, file_path=file_path)
            elif "Venue:" in content or "Authors:" in content:
                self.load_publication_from_data({}, html_content=content, file_path=file_path)
            else:
                messagebox.showerror("Geçersiz Dosya", "Bu HTML dosyasında tanınabilir bir MICROLab içerik bloğu (Proje, Kişi, Haber veya Yayın) bulunamadı.")
        except Exception as e:
            messagebox.showerror("Hata", f"Dosya okunurken hata oluştu:\n{e}")

    def load_scanned_item(self, item):
        """Loads a structured item dictionary into its corresponding editor."""
        itype = item.get("type")
        meta = item.get("meta", {})
        content = item.get("content", "")
        fpath = item.get("file_path", "")

        if itype == "project":
            self.load_project_from_data(meta, html_content=content, file_path=fpath)
        elif itype == "person":
            self.load_person_from_data(meta, html_content=content, file_path=fpath)
        elif itype == "news":
            self.load_news_from_data(meta, html_content=content, file_path=fpath)
        elif itype == "publication":
            self.load_publication_from_data(meta, html_content=content, file_path=fpath)

    def load_project_from_data(self, meta, html_content="", file_path=""):
        try:
            title = meta.get("title", "")
            if not title and html_content:
                m_t = re.search(r'<title>(.*?) \| MICROLab</title>', html_content)
                title = m_t.group(1).strip() if m_t else ""

            self.proj_title_entry.delete(0, tk.END)
            self.proj_title_entry.insert(0, title)

            tags = meta.get("tags", [])
            if isinstance(tags, list):
                tags_str = ", ".join(str(t) for t in tags)
            else:
                tags_str = str(tags)
            self.proj_tags_entry.delete(0, tk.END)
            self.proj_tags_entry.insert(0, tags_str)

            status = meta.get("status", "Active")
            if status in ["Active", "Completed"]:
                self.proj_status_combo.set(status)
            else:
                self.proj_status_combo.set("Active")

            start_date = meta.get("start_date_text", "")
            if not start_date and meta.get("timeline"):
                start_date = meta.get("timeline").split("&mdash;")[0].strip()
            self.proj_start_entry.delete(0, tk.END)
            self.proj_start_entry.insert(0, start_date or "June 2026")

            end_date = meta.get("end_date_text", "")
            self.proj_end_entry.delete(0, tk.END)
            self.proj_end_entry.insert(0, end_date)

            short_desc = meta.get("short_description", "")
            self.proj_short_desc_text.delete("1.0", tk.END)
            self.proj_short_desc_text.insert("1.0", short_desc)

            img_uri = meta.get("image", "")
            self.proj_cover_path = ""
            if img_uri:
                target_dir = self.output_dir_var.get()
                resolved = None
                img_name = os.path.basename(img_uri)
                candidates = []
                if file_path:
                    file_dir = os.path.dirname(file_path)
                    candidates.extend([
                        os.path.normpath(os.path.join(file_dir, img_uri)),
                        os.path.normpath(os.path.join(file_dir, "..", "..", "images", img_name)),
                        os.path.normpath(os.path.join(file_dir, "..", "images", img_name)),
                    ])
                if target_dir:
                    candidates.extend([
                        os.path.normpath(os.path.join(target_dir, "images", img_name)),
                        os.path.normpath(os.path.join(target_dir, img_name))
                    ])
                for c in candidates:
                    if os.path.exists(c):
                        resolved = c
                        break
                if resolved:
                    self.proj_cover_path = resolved
                    self.proj_cover_label.configure(text=f"✓ {os.path.basename(resolved)}")
                else:
                    self.proj_cover_label.configure(text=f"Kayıtlı: {img_name}")
            else:
                self.proj_cover_label.configure(text="Henüz görsel seçilmedi")

            for combo in list(self.member_rows):
                try: combo.master.destroy()
                except Exception: pass
            self.member_rows.clear()

            team_items = meta.get("team", [])
            if team_items:
                for tm in team_items:
                    if isinstance(tm, dict):
                        m_name = tm.get("name", "").strip()
                    else:
                        m_name = str(tm).strip()
                    if m_name:
                        if m_name not in self.existing_people_names:
                            self.existing_people_names.append(m_name)
                        self.add_member_row()
                        if self.member_rows:
                            self.member_rows[-1].set(m_name)
            else:
                self.add_member_row()

            for row in list(self.pub_rows):
                try: row[0].master.destroy()
                except Exception: pass
            self.pub_rows.clear()

            pub_items = meta.get("publications", [])
            if pub_items:
                for pb in pub_items:
                    if isinstance(pb, dict):
                        p_title = pb.get("title", "")
                        p_link = pb.get("link", "")
                    else:
                        p_title = str(pb)
                        p_link = ""
                    self.add_pub_row()
                    if self.pub_rows:
                        self.pub_rows[-1][0].delete(0, tk.END)
                        self.pub_rows[-1][0].insert(0, p_title)
                        self.pub_rows[-1][1].delete(0, tk.END)
                        self.pub_rows[-1][1].insert(0, p_link)
            else:
                self.add_pub_row()

            blocks_data = meta.get("blocks")
            if blocks_data and isinstance(blocks_data, list) and len(blocks_data) > 0:
                self.content_editor.load_blocks_data(blocks_data)
            else:
                self.content_editor.clear_blocks()
                extracted = self.parse_html_body_to_blocks(html_content, file_path) if html_content else []
                if extracted:
                    self.content_editor.load_blocks_data(extracted)
                elif meta.get("about"):
                    self.content_editor.add_block('heading', {'level': 'h2', 'text': 'About the Project'})
                    self.content_editor.add_block('paragraph', {'text': meta.get('about')})
                else:
                    self.content_editor.add_block('heading', {'level': 'h2', 'text': 'Project Overview'})
                    self.content_editor.add_block('paragraph', {'text': short_desc or 'Bu araştırma projesi hakkında detaylar...'})

            self.loaded_file_paths[0] = file_path
            self.loaded_slugs[0] = meta.get("slug", slugify(title))
            self.loaded_titles[0] = title
            fname_display = os.path.basename(file_path) if file_path else f"{self.loaded_slugs[0]}.html"
            if hasattr(self, 'proj_loaded_badge'):
                self.proj_loaded_badge.configure(text=f"✏️ Düzenleniyor: {fname_display}")

            self.notebook.select(self.project_tab)

            messagebox.showinfo(
                "Proje Başarıyla Yüklendi",
                f"'{title or 'Proje'}' başarıyla editöre aktarıldı!\n\nTüm temel bilgiler, ekip üyeleri, yayınlar ve içerik blokları düzenleme için hazır."
            )
        except Exception as e:
            messagebox.showerror("Yükleme Hatası", f"Proje verileri yüklenirken bir hata oluştu:\n{e}")

    def load_person_from_data(self, meta, html_content="", file_path=""):
        try:
            name = meta.get("name", "")
            if not name and html_content:
                m_t = re.search(r'<title>(.*?) \| MICROLab</title>', html_content)
                name = m_t.group(1).strip() if m_t else ""

            self.person_name_entry.delete(0, tk.END)
            self.person_name_entry.insert(0, name)

            category = meta.get("category", "PhD Graduate Students")
            valid_cats = [
                'Postdoctoral Researchers',
                'PhD Graduate Students',
                'Masters Graduate Students',
                'Undergraduate Students'
            ]
            if category in valid_cats:
                self.person_cat_combo.set(category)
            else:
                self.person_cat_combo.set("PhD Graduate Students")

            role = meta.get("role", "")
            self.person_role_entry.delete(0, tk.END)
            self.person_role_entry.insert(0, role or "PhD Researcher")

            dept = meta.get("department", "")
            self.person_dept_entry.delete(0, tk.END)
            self.person_dept_entry.insert(0, dept or "Control and Automation Engineering")

            photo_uri = meta.get("photo", "")
            self.person_photo_path = ""
            if photo_uri:
                target_dir = self.output_dir_var.get()
                img_name = os.path.basename(photo_uri)
                resolved = None
                candidates = []
                if file_path:
                    file_dir = os.path.dirname(file_path)
                    candidates.extend([
                        os.path.normpath(os.path.join(file_dir, photo_uri)),
                        os.path.normpath(os.path.join(file_dir, "..", "..", "images", img_name)),
                        os.path.normpath(os.path.join(file_dir, "..", "images", img_name)),
                    ])
                if target_dir:
                    candidates.extend([
                        os.path.normpath(os.path.join(target_dir, "images", img_name)),
                        os.path.normpath(os.path.join(target_dir, img_name))
                    ])
                for c in candidates:
                    if os.path.exists(c):
                        resolved = c
                        break
                if resolved:
                    self.person_photo_path = resolved
                    self.person_photo_label.configure(text=f"✓ {os.path.basename(resolved)}")
                else:
                    self.person_photo_label.configure(text=f"Kayıtlı: {img_name}")
            else:
                self.person_photo_label.configure(text="İsteğe bağlı")

            scholar = meta.get("scholar", meta.get("google_scholar", ""))
            self.person_scholar_entry.delete(0, tk.END)
            self.person_scholar_entry.insert(0, scholar)

            orcid = meta.get("orcid", meta.get("orcid_id", ""))
            self.person_orcid_entry.delete(0, tk.END)
            self.person_orcid_entry.insert(0, orcid)

            rg = meta.get("researchgate", meta.get("rg", ""))
            self.person_rg_entry.delete(0, tk.END)
            self.person_rg_entry.insert(0, rg)

            github = meta.get("github", "")
            self.person_github_entry.delete(0, tk.END)
            self.person_github_entry.insert(0, github)

            linkedin = meta.get("linkedin", "")
            self.person_linkedin_entry.delete(0, tk.END)
            self.person_linkedin_entry.insert(0, linkedin)

            website = meta.get("website", meta.get("site", ""))
            self.person_website_entry.delete(0, tk.END)
            self.person_website_entry.insert(0, website)

            email = meta.get("email", meta.get("mail", ""))
            self.person_email_entry.delete(0, tk.END)
            self.person_email_entry.insert(0, email)

            about = meta.get("about", "")
            if not about and html_content:
                m_ab = re.search(r'<div class="profile-info">[\s\S]*?<p>(.*?)</p>', html_content)
                about = m_ab.group(1).strip() if m_ab else ""

            self.person_about_text.delete("1.0", tk.END)
            self.person_about_text.insert("1.0", about)

            self.loaded_file_paths[1] = file_path
            self.loaded_slugs[1] = meta.get("slug", slugify(name))
            self.loaded_titles[1] = name
            fname_display = os.path.basename(file_path) if file_path else f"{self.loaded_slugs[1]}.html"
            if hasattr(self, 'person_loaded_badge'):
                self.person_loaded_badge.configure(text=f"✏️ Düzenleniyor: {fname_display}")

            self.notebook.select(self.person_tab)

            messagebox.showinfo(
                "Kişi Başarıyla Yüklendi",
                f"'{name or 'Kişi'}' profil bilgileri başarıyla editöre aktarıldı!\n\nTüm alanlar düzenlenebilir durumdadır."
            )
        except Exception as e:
            messagebox.showerror("Yükleme Hatası", f"Kişi verileri yüklenirken bir hata oluştu:\n{e}")

    def load_news_from_data(self, meta, html_content="", file_path=""):
        try:
            title = meta.get("title", "")
            if not title and html_content:
                m_t = re.search(r'<title>(.*?) \| MICROLab</title>', html_content)
                title = m_t.group(1).strip() if m_t else ""

            self.news_title_entry.delete(0, tk.END)
            self.news_title_entry.insert(0, title)

            date_str = meta.get("date", "")
            self.news_date_entry.delete(0, tk.END)
            self.news_date_entry.insert(0, date_str or datetime.date.today().strftime("%B %d, %Y"))

            category = meta.get("category", "Announcements")
            self.news_cat_combo.set(category if category else "Announcements")

            summary = meta.get("short_description", "")
            self.news_summary_text.delete("1.0", tk.END)
            self.news_summary_text.insert("1.0", summary)

            blocks_data = meta.get("blocks") or meta.get("content_blocks")
            if blocks_data and isinstance(blocks_data, list) and len(blocks_data) > 0:
                self.news_content_editor.load_blocks_data(blocks_data)
            else:
                self.news_content_editor.clear_blocks()
                extracted = self.parse_html_body_to_blocks(html_content, file_path) if html_content else []
                if extracted:
                    self.news_content_editor.load_blocks_data(extracted)
                else:
                    self.news_content_editor.add_block('paragraph', {'text': summary or 'Haber detayları...'})

            self.loaded_file_paths[2] = file_path
            s = slugify(title)
            self.loaded_slugs[2] = meta.get("slug", s if s.startswith("news_") else f"news_{s}")
            self.loaded_titles[2] = title
            fname_display = os.path.basename(file_path) if file_path else f"{self.loaded_slugs[2]}.html"
            if hasattr(self, 'news_loaded_badge'):
                self.news_loaded_badge.configure(text=f"✏️ Düzenleniyor: {fname_display}")

            self.notebook.select(self.news_tab)

            messagebox.showinfo(
                "Haber Başarıyla Yüklendi",
                f"'{title or 'Haber'}' içeriği başarıyla editöre aktarıldı!\n\nBaşlık, özet ve içerik blokları düzenleme için hazır."
            )
        except Exception as e:
            messagebox.showerror("Yükleme Hatası", f"Haber verileri yüklenirken bir hata oluştu:\n{e}")

    def load_publication_from_data(self, meta, html_content="", file_path=""):
        try:
            title = meta.get("title", "")
            if not title and html_content:
                m_t = re.search(r'<title>(.*?)</title>', html_content)
                title = m_t.group(1).strip() if m_t else ""

            self.pub_item_title_entry.delete(0, tk.END)
            self.pub_item_title_entry.insert(0, title)

            authors = meta.get("authors", "")
            if not authors and html_content:
                m_a = re.search(r'<p>Authors:\s*(.*?)</p>', html_content)
                authors = m_a.group(1).strip() if m_a else ""
            self.pub_item_authors_entry.delete(0, tk.END)
            self.pub_item_authors_entry.insert(0, authors)

            venue = meta.get("venue", "")
            if not venue and html_content:
                m_v = re.search(r'<p>Venue:\s*(.*?)</p>', html_content)
                venue = m_v.group(1).strip() if m_v else ""
            self.pub_item_venue_entry.delete(0, tk.END)
            self.pub_item_venue_entry.insert(0, venue)

            year = meta.get("year", "2026")
            self.pub_item_year_entry.delete(0, tk.END)
            self.pub_item_year_entry.insert(0, str(year))

            date_str = meta.get("date", "")
            self.pub_item_date_entry.delete(0, tk.END)
            self.pub_item_date_entry.insert(0, date_str or datetime.date.today().strftime("%Y-%m-%d"))

            links = meta.get("links", {})
            if not isinstance(links, dict):
                links = {}

            self.pub_link_pdf_entry.delete(0, tk.END)
            self.pub_link_pdf_entry.insert(0, links.get("pdf", "#" if not links else ""))

            self.pub_link_doi_entry.delete(0, tk.END)
            self.pub_link_doi_entry.insert(0, links.get("doi", ""))

            self.pub_link_code_entry.delete(0, tk.END)
            self.pub_link_code_entry.insert(0, links.get("code", ""))

            self.pub_link_proj_entry.delete(0, tk.END)
            self.pub_link_proj_entry.insert(0, links.get("project", ""))

            self.pub_link_video_entry.delete(0, tk.END)
            self.pub_link_video_entry.insert(0, links.get("video", ""))

            self.pub_link_data_entry.delete(0, tk.END)
            self.pub_link_data_entry.insert(0, links.get("dataset", ""))

            self.loaded_file_paths[3] = file_path
            self.loaded_slugs[3] = meta.get("slug", slugify(title))
            self.loaded_titles[3] = title
            fname_display = os.path.basename(file_path) if file_path else f"{self.loaded_slugs[3]}.html"
            if hasattr(self, 'pub_loaded_badge'):
                self.pub_loaded_badge.configure(text=f"✏️ Düzenleniyor: {fname_display}")

            self.notebook.select(self.pub_tab)

            messagebox.showinfo(
                "Yayın Başarıyla Yüklendi",
                f"'{title or 'Yayın'}' kaydı başarıyla editöre aktarıldı!\n\nTüm alanlar ve bağlantı linkleri düzenlenebilir durumdadır."
            )
        except Exception as e:
            messagebox.showerror("Yükleme Hatası", f"Yayın verileri yüklenirken bir hata oluştu:\n{e}")

    def parse_html_body_to_blocks(self, html_content, file_path=""):
        """Extracts content blocks from HTML body for pages without 'blocks' metadata."""
        blocks = []
        if not html_content:
            return blocks

        m_blog = re.search(r'<div class="blog-content">([\s\S]*?)(?:<h2>Team Members</h2>|<a href="\.\./index\.html"|<footer>|$)', html_content)
        content_section = m_blog.group(1) if m_blog else html_content

        content_section = re.sub(r'<div class="project-meta"[\s\S]*?</div>', '', content_section)

        token_pattern = re.compile(
            r'(<h[23][^>]*>[\s\S]*?</h[23]>|<p[^>]*>[\s\S]*?</p>|<figure[^>]*>[\s\S]*?</figure>|<div class="media-grid"[\s\S]*?</div>|<div class="project-gallery"[\s\S]*?</div>|<iframe[^>]*>[\s\S]*?</iframe>|<div class="callout"[\s\S]*?</div>)',
            re.IGNORECASE
        )

        matches = token_pattern.findall(content_section)
        for token in matches:
            token = token.strip()
            if not token:
                continue

            m_h = re.match(r'<(h[23])[^>]*>(.*?)</\1>', token, re.DOTALL | re.IGNORECASE)
            if m_h:
                lvl = m_h.group(1).lower()
                clean_t = re.sub(r'<[^>]+>', '', m_h.group(2)).strip()
                if clean_t and clean_t.lower() not in ("team members", "related publications"):
                    blocks.append({'type': 'heading', 'level': lvl, 'text': clean_t})
                continue

            m_p = re.match(r'<p[^>]*>(.*?)</p>', token, re.DOTALL | re.IGNORECASE)
            if m_p:
                clean_p = m_p.group(1).replace('<br>', '\n').replace('<br/>', '\n')
                clean_p = re.sub(r'<[^>]+>', '', clean_p).strip()
                if clean_p and not clean_p.startswith("&copy;"):
                    blocks.append({'type': 'paragraph', 'text': clean_p})
                continue

            if 'class="callout"' in token:
                icon_m = re.search(r'<span class="callout-icon">(.*?)</span>', token)
                icon = icon_m.group(1).strip() if icon_m else "💡"
                body_t = re.sub(r'<span class="callout-icon">.*?</span>', '', token)
                body_t = re.sub(r'<[^>]+>', '', body_t).strip()
                blocks.append({'type': 'callout', 'icon': icon, 'text': body_t})
                continue

            m_img = re.search(r'<img[^>]+src=["\'](.*?)["\']', token, re.IGNORECASE)
            if m_img and 'media-grid' not in token and 'project-gallery' not in token:
                img_src = m_img.group(1)
                m_cap = re.search(r'<figcaption[^>]*>(.*?)</figcaption>', token, re.IGNORECASE)
                cap = re.sub(r'<[^>]+>', '', m_cap.group(1)).strip() if m_cap else ""
                blocks.append({
                    'type': 'image',
                    'path': img_src,
                    'caption': cap,
                    'width': '100%',
                    'align': 'Center',
                    'max_height': 'Auto (Sınırsız)'
                })
                continue

            if 'media-grid' in token or 'project-gallery' in token:
                gal_imgs = re.findall(r'<img[^>]+src=["\'](.*?)["\']', token, re.IGNORECASE)
                gal_caps = re.findall(r'<figcaption[^>]*>(.*?)</figcaption>', token, re.IGNORECASE)
                if gal_imgs:
                    items = []
                    for idx, gsrc in enumerate(gal_imgs):
                        gcap = re.sub(r'<[^>]+>', '', gal_caps[idx]).strip() if idx < len(gal_caps) else ""
                        items.append({'type': 'image', 'path': gsrc, 'caption': gcap})
                    blocks.append({'type': 'gallery', 'cols': '2 Kolon (Yan Yana 2)', 'items': items})
                continue

            m_yt = re.search(r'youtube(?:-nocookie)?\.com/embed/([a-zA-Z0-9_-]{11})', token)
            if m_yt:
                blocks.append({'type': 'youtube', 'url': f"https://www.youtube.com/watch?v={m_yt.group(1)}", 'width': '100%'})
                continue

        return blocks

    def reset_project_form(self):
        """Resets the project editor to a blank state for creating a new project."""
        ans = messagebox.askyesno("Formu Temizle", "Proje formundaki tüm alanlar temizlenecek ve yeni proje moduna geçilecek. Devam etmek istiyor musunuz?")
        if not ans:
            return
        self.proj_title_entry.delete(0, tk.END)
        self.proj_tags_entry.delete(0, tk.END)
        self.proj_tags_entry.insert(0, "vision, autonomy, control")
        self.proj_status_combo.set("Active")
        self.proj_start_entry.delete(0, tk.END)
        self.proj_start_entry.insert(0, "June 2026")
        self.proj_end_entry.delete(0, tk.END)
        self.proj_short_desc_text.delete("1.0", tk.END)
        self.proj_cover_path = ""
        self.proj_cover_label.configure(text="Henüz görsel seçilmedi")

        for combo in list(self.member_rows):
            try: combo.master.destroy()
            except Exception: pass
        self.member_rows.clear()
        self.add_member_row()

        for row in list(self.pub_rows):
            try: row[0].master.destroy()
            except Exception: pass
        self.pub_rows.clear()
        self.add_pub_row()

        self.content_editor.clear_blocks()
        self.content_editor.add_block('heading', {'level': 'h2', 'text': 'Project Overview'})
        self.content_editor.add_block('paragraph', {'text': 'This research project addresses autonomous navigation and adaptive decision making...'})

        self.loaded_file_paths[0] = ""
        self.loaded_slugs[0] = ""
        self.loaded_titles[0] = ""
        if hasattr(self, 'proj_loaded_badge'):
            self.proj_loaded_badge.configure(text="")

        messagebox.showinfo("Hazır", "Proje formu temizlendi, yeni proje oluşturmaya başlayabilirsiniz.")

    def reset_person_form(self):
        ans = messagebox.askyesno("Formu Temizle", "Kişi formundaki tüm alanlar temizlenecek ve yeni kişi moduna geçilecek. Devam etmek istiyor musunuz?")
        if not ans:
            return
        self.person_name_entry.delete(0, tk.END)
        self.person_cat_combo.set("PhD Graduate Students")
        self.person_role_entry.delete(0, tk.END)
        self.person_role_entry.insert(0, "PhD Researcher")
        self.person_dept_entry.delete(0, tk.END)
        self.person_dept_entry.insert(0, "Control and Automation Engineering")
        self.person_photo_path = ""
        self.person_photo_label.configure(text="İsteğe bağlı")
        self.person_scholar_entry.delete(0, tk.END)
        self.person_orcid_entry.delete(0, tk.END)
        self.person_rg_entry.delete(0, tk.END)
        self.person_github_entry.delete(0, tk.END)
        self.person_linkedin_entry.delete(0, tk.END)
        self.person_website_entry.delete(0, tk.END)
        self.person_email_entry.delete(0, tk.END)
        self.person_about_text.delete("1.0", tk.END)

        self.loaded_file_paths[1] = ""
        self.loaded_slugs[1] = ""
        self.loaded_titles[1] = ""
        if hasattr(self, 'person_loaded_badge'):
            self.person_loaded_badge.configure(text="")

        messagebox.showinfo("Hazır", "Kişi formu temizlendi, yeni profil oluşturabilirsiniz.")

    def reset_news_form(self):
        ans = messagebox.askyesno("Formu Temizle", "Haber formundaki tüm alanlar temizlenecek ve yeni haber moduna geçilecek. Devam etmek istiyor musunuz?")
        if not ans:
            return
        self.news_title_entry.delete(0, tk.END)
        self.news_date_entry.delete(0, tk.END)
        self.news_date_entry.insert(0, datetime.date.today().strftime("%B %d, %Y"))
        self.news_cat_combo.set("Announcements")
        self.news_summary_text.delete("1.0", tk.END)
        self.news_content_editor.clear_blocks()
        self.news_content_editor.add_block('paragraph', {'text': 'We are excited to announce our latest milestone...'})

        self.loaded_file_paths[2] = ""
        self.loaded_slugs[2] = ""
        self.loaded_titles[2] = ""
        if hasattr(self, 'news_loaded_badge'):
            self.news_loaded_badge.configure(text="")

        messagebox.showinfo("Hazır", "Haber formu temizlendi, yeni haber yazabilirsiniz.")

    def reset_pub_form(self):
        ans = messagebox.askyesno("Formu Temizle", "Yayın formundaki tüm alanlar temizlenecek ve yeni yayın moduna geçilecek. Devam etmek istiyor musunuz?")
        if not ans:
            return
        self.pub_item_title_entry.delete(0, tk.END)
        self.pub_item_authors_entry.delete(0, tk.END)
        self.pub_item_authors_entry.insert(0, "Gizem Asya Yılmaz, Nurettin Tarık Mut")
        self.pub_item_venue_entry.delete(0, tk.END)
        self.pub_item_venue_entry.insert(0, "IEEE Transactions on Robotics (T-RO)")
        self.pub_item_year_entry.delete(0, tk.END)
        self.pub_item_year_entry.insert(0, "2026")
        self.pub_item_date_entry.delete(0, tk.END)
        self.pub_item_date_entry.insert(0, datetime.date.today().strftime("%Y-%m-%d"))
        self.pub_link_pdf_entry.delete(0, tk.END)
        self.pub_link_pdf_entry.insert(0, "#")
        self.pub_link_doi_entry.delete(0, tk.END)
        self.pub_link_code_entry.delete(0, tk.END)
        self.pub_link_code_entry.insert(0, "#")
        self.pub_link_proj_entry.delete(0, tk.END)
        self.pub_link_video_entry.delete(0, tk.END)
        self.pub_link_data_entry.delete(0, tk.END)

        self.loaded_file_paths[3] = ""
        self.loaded_slugs[3] = ""
        self.loaded_titles[3] = ""
        if hasattr(self, 'pub_loaded_badge'):
            self.pub_loaded_badge.configure(text="")

        messagebox.showinfo("Hazır", "Yayın formu temizlendi, yeni yayın kaydı girebilirsiniz.")

    def generate_files_prompt(self):
        curr_tab = self.notebook.index(self.notebook.select())
        if curr_tab == 4:
            messagebox.showinfo("Bilgi", "Yardım sekmesindesiniz. Kayıt yapmak için lütfen Proje, Kişi, Haber veya Yayın sekmesine geçin.")
            return

        target_base_dir = self.output_dir_var.get().strip()
        if not target_base_dir or not os.path.isdir(target_base_dir):
            target_base_dir = filedialog.askdirectory(
                title="Lütfen Sayfa ve Görsellerin Kaydedileceği Hedef Klasörü Seçin",
                initialdir=self.output_dir_var.get()
            )
            if not target_base_dir:
                return
            self.output_dir_var.set(target_base_dir)

        self.ensure_standalone_assets(target_base_dir)

        if curr_tab == 0:
            self._save_project(target_base_dir)
        elif curr_tab == 1:
            self._save_person(target_base_dir)
        elif curr_tab == 2:
            self._save_news(target_base_dir)
        elif curr_tab == 3:
            self._save_publication(target_base_dir)

    def ensure_standalone_assets(self, target_base_dir):
        css_dir = os.path.join(target_base_dir, "css")
        js_dir = os.path.join(target_base_dir, "js")
        os.makedirs(css_dir, exist_ok=True)
        os.makedirs(js_dir, exist_ok=True)

        css_file = os.path.join(css_dir, "main.css")
        with open(css_file, "w", encoding="utf-8") as f:
            f.write(EMBEDDED_CSS_CONTENT)

        js_file = os.path.join(js_dir, "main.js")
        with open(js_file, "w", encoding="utf-8") as f:
            f.write(EMBEDDED_JS_CONTENT)

    def _save_project(self, target_base_dir):
        title = self.proj_title_entry.get().strip()
        if not title:
            messagebox.showerror("Hata", "Proje Başlığı zorunludur.")
            return

        if self.loaded_slugs.get(0) and self.loaded_titles.get(0) == title:
            slug = self.loaded_slugs[0]
        else:
            slug = slugify(title)

        tags_raw = [t.strip() for t in self.proj_tags_entry.get().split(',') if t.strip()]
        status = self.proj_status_combo.get()
        start_date = self.proj_start_entry.get().strip()
        end_date = self.proj_end_entry.get().strip() if status == "Completed" else ""
        short_desc = self.proj_short_desc_text.get("1.0", tk.END).strip()

        projects_data_dir = os.path.join(target_base_dir, "projects", "data")
        images_dir = os.path.join(target_base_dir, "images")

        os.makedirs(projects_data_dir, exist_ok=True)
        os.makedirs(images_dir, exist_ok=True)

        cover_uri = "../../images/project_drone.svg"
        if self.proj_cover_path and os.path.exists(self.proj_cover_path):
            filename = os.path.basename(self.proj_cover_path)
            shutil.copy2(self.proj_cover_path, os.path.join(images_dir, filename))
            cover_uri = f"../../images/{filename}"

        def copy_block_image(src_path):
            if not src_path or not os.path.exists(src_path):
                return src_path
            filename = os.path.basename(src_path)
            shutil.copy2(src_path, os.path.join(images_dir, filename))
            return f"../../images/{filename}"

        body_html = self.content_editor.render_html(media_copy_callback=copy_block_image)

        team_names = []
        team_members_html_parts = []
        for combo in self.member_rows:
            try:
                val = combo.get().strip()
                if val and val not in team_names:
                    team_names.append(val)
                    team_members_html_parts.append(f'<div class="member-card" style="padding:15px; background:var(--bg-alt); border-radius:8px;"><h3 style="font-size:1.1rem; color:#2563eb;">{val}</h3></div>')
            except Exception: pass

        team_html = "\n".join(team_members_html_parts) if team_members_html_parts else '<p style="color:#64748b;">No members listed.</p>'

        pub_list = []
        for t_e, l_e in self.pub_rows:
            try:
                t_val = t_e.get().strip()
                l_val = l_e.get().strip()
                if t_val:
                    pub_list.append({"title": t_val, "link": l_val})
            except Exception: pass

        pub_section_html = ""
        if pub_list:
            items_h = "\n".join([f"                    <li><a href='{p['link']}'>{p['title']}</a></li>" if p['link'] else f"                    <li>{p['title']}</li>" for p in pub_list])
            pub_section_html = f"<h2>Related Publications</h2>\n<div class='related-pubs-container' style='margin-top:0;'>\n<ul class='related-pubs-list'>\n{items_h}\n</ul>\n</div>"

        header_style = f"background-image: linear-gradient(135deg, rgba(15,23,42,0.9), rgba(30,41,59,0.85)), url('{cover_uri}');"
        timeline = f"{start_date} &mdash; <span style=\"color: #38a169;\">Active</span>" if status == "Active" else f"{start_date} &mdash; {end_date}"
        
        project_meta_html = f"""<div class="project-meta" style="margin-bottom: 25px; font-size: 0.95rem; color: #475569; background: var(--bg-alt); padding: 15px; border-left: 4px solid #2563eb; border-radius: 8px;">
            <strong>Timeline:</strong> {timeline} <span style="margin: 0 10px;">|</span> <strong>Status:</strong> {status}
        </div>"""

        metadata_dict = {
            "title": title,
            "slug": slug,
            "tags": tags_raw,
            "date": datetime.date.today().strftime("%Y-%m-%d"),
            "timeline": timeline,
            "status": status,
            "start_date_text": start_date,
            "end_date_text": end_date,
            "short_description": short_desc,
            "image": cover_uri,
            "team": team_names,
            "publications": pub_list,
            "blocks": self.content_editor.get_blocks_data()
        }

        html = PROJECT_HTML_TEMPLATE.replace("{{TITLE}}", title)
        html = html.replace("{{HEADER_STYLE}}", header_style)
        html = html.replace("{{PROJECT_META_HTML}}", project_meta_html)
        html = html.replace("{{CONTENT_BODY_HTML}}", body_html)
        html = html.replace("{{TEAM_MEMBERS_HTML}}", team_html)
        html = html.replace("{{PUBLICATIONS_SECTION_HTML}}", pub_section_html)
        html = html.replace("{{LIVE_RELOAD_SCRIPT}}", "")
        html = html.replace("{{EMBEDDED_CSS}}", EMBEDDED_CSS_CONTENT)
        html = html.replace("{{EMBEDDED_JS}}", EMBEDDED_JS_CONTENT)
        html = html.replace("{{METADATA_JSON}}", json.dumps(metadata_dict, ensure_ascii=False, indent=2))

        output_file_path = os.path.join(projects_data_dir, f"{slug}.html")
        with open(output_file_path, "w", encoding="utf-8") as f:
            f.write(html)

        self.loaded_file_paths[0] = output_file_path
        self.loaded_slugs[0] = slug
        self.loaded_titles[0] = title
        if hasattr(self, 'proj_loaded_badge'):
            self.proj_loaded_badge.configure(text=f"✓ Kaydedildi: {os.path.basename(output_file_path)}")

        messagebox.showinfo("Başarılı", f"Proje sayfası başarıyla kaydedildi!\n\nKaydedilen Konum:\n{output_file_path}")

    def _save_person(self, target_base_dir):
        name = self.person_name_entry.get().strip()
        if not name:
            messagebox.showerror("Hata", "Ad Soyad zorunludur.")
            return

        if self.loaded_slugs.get(1) and self.loaded_titles.get(1) == name:
            slug = self.loaded_slugs[1]
        else:
            slug = slugify(name)

        category = self.person_cat_combo.get()
        role = self.person_role_entry.get().strip()
        department = self.person_dept_entry.get().strip()
        scholar = self.person_scholar_entry.get().strip()
        orcid = self.person_orcid_entry.get().strip()
        rg = self.person_rg_entry.get().strip()
        github = self.person_github_entry.get().strip()
        linkedin = self.person_linkedin_entry.get().strip()
        website = self.person_website_entry.get().strip()
        email = self.person_email_entry.get().strip()
        about = self.person_about_text.get("1.0", tk.END).strip()

        people_data_dir = os.path.join(target_base_dir, "people", "data")
        images_dir = os.path.join(target_base_dir, "images")

        os.makedirs(people_data_dir, exist_ok=True)
        os.makedirs(images_dir, exist_ok=True)

        photo_uri = ""
        if self.person_photo_path and os.path.exists(self.person_photo_path):
            filename = os.path.basename(self.person_photo_path)
            shutil.copy2(self.person_photo_path, os.path.join(images_dir, filename))
            photo_uri = f"../../images/{filename}"

        metadata_dict = {
            "name": name,
            "slug": slug,
            "role": role,
            "department": department,
            "about": about,
            "photo": photo_uri,
            "scholar": scholar,
            "orcid": orcid,
            "researchgate": rg,
            "github": github,
            "linkedin": linkedin,
            "website": website,
            "email": email,
            "category": category
        }

        social_links_html = generate_person_social_links_html(metadata_dict)
        about_html = f"<p>{about}</p>" if about else "<p>MICROLab team researcher.</p>"
        photo_html = f'<img src="{photo_uri}" alt="{name}" style="width:100%;height:100%;object-fit:cover;">' if photo_uri else ""

        html = PERSON_HTML_TEMPLATE.replace("{{NAME}}", name)
        html = html.replace("{{ROLE}}", role)
        html = html.replace("{{DEPARTMENT}}", department)
        html = html.replace("{{PHOTO_HTML}}", photo_html)
        html = html.replace("{{SOCIAL_LINKS_HTML}}", social_links_html)
        github_html = f'<a href="{github}" target="_blank" class="social-link-btn github">GitHub</a>' if github else ""
        linkedin_html = f'<a href="{linkedin}" target="_blank" class="social-link-btn linkedin">LinkedIn</a>' if linkedin else ""
        html = html.replace("{{GITHUB_LINK_HTML}}", github_html)
        html = html.replace("{{LINKEDIN_LINK_HTML}}", linkedin_html)
        html = html.replace("{{ABOUT_HTML}}", about_html)
        html = html.replace("{{LIVE_RELOAD_SCRIPT}}", "")
        html = html.replace("{{EMBEDDED_CSS}}", EMBEDDED_CSS_CONTENT)
        html = html.replace("{{EMBEDDED_JS}}", EMBEDDED_JS_CONTENT)
        html = html.replace("{{METADATA_JSON}}", json.dumps(metadata_dict, ensure_ascii=False, indent=2))

        output_file_path = os.path.join(people_data_dir, f"{slug}.html")
        with open(output_file_path, "w", encoding="utf-8") as f:
            f.write(html)

        if name not in self.existing_people_names:
            self.existing_people_names.append(name)

        self.loaded_file_paths[1] = output_file_path
        self.loaded_slugs[1] = slug
        self.loaded_titles[1] = name
        if hasattr(self, 'person_loaded_badge'):
            self.person_loaded_badge.configure(text=f"✓ Kaydedildi: {os.path.basename(output_file_path)}")

        messagebox.showinfo("Başarılı", f"Kişi profil sayfası başarıyla kaydedildi!\n\nKaydedilen Konum:\n{output_file_path}")

    def _save_news(self, target_base_dir):
        title = self.news_title_entry.get().strip()
        if not title:
            messagebox.showerror("Hata", "Haber Başlığı zorunludur.")
            return

        if self.loaded_slugs.get(2) and self.loaded_titles.get(2) == title:
            slug = self.loaded_slugs[2]
        else:
            s = slugify(title)
            slug = s if s.startswith("news_") else f"news_{s}"

        date_str = self.news_date_entry.get().strip()
        category = self.news_cat_combo.get().strip()
        summary = self.news_summary_text.get("1.0", tk.END).strip()

        news_data_dir = os.path.join(target_base_dir, "news", "data")
        images_dir = os.path.join(target_base_dir, "images")

        os.makedirs(news_data_dir, exist_ok=True)
        os.makedirs(images_dir, exist_ok=True)

        def copy_block_image(src_path):
            if not src_path or not os.path.exists(src_path):
                return src_path
            filename = os.path.basename(src_path)
            shutil.copy2(src_path, os.path.join(images_dir, filename))
            return f"../../images/{filename}"

        body_html = self.news_content_editor.render_html(media_copy_callback=copy_block_image)

        metadata_dict = {
            "title": title,
            "slug": slug,
            "date": date_str,
            "category": category,
            "short_description": summary,
            "blocks": self.news_content_editor.get_blocks_data()
        }

        html = NEWS_HTML_TEMPLATE.replace("{{TITLE}}", title)
        html = html.replace("{{DATE}}", date_str)
        html = html.replace("{{CATEGORY}}", category)
        html = html.replace("{{CONTENT_BODY_HTML}}", body_html)
        html = html.replace("{{LIVE_RELOAD_SCRIPT}}", "")
        html = html.replace("{{EMBEDDED_CSS}}", EMBEDDED_CSS_CONTENT)
        html = html.replace("{{EMBEDDED_JS}}", EMBEDDED_JS_CONTENT)
        html = html.replace("{{METADATA_JSON}}", json.dumps(metadata_dict, ensure_ascii=False, indent=2))

        output_file_path = os.path.join(news_data_dir, f"{slug}.html")
        with open(output_file_path, "w", encoding="utf-8") as f:
            f.write(html)

        self.loaded_file_paths[2] = output_file_path
        self.loaded_slugs[2] = slug
        self.loaded_titles[2] = title
        if hasattr(self, 'news_loaded_badge'):
            self.news_loaded_badge.configure(text=f"✓ Kaydedildi: {os.path.basename(output_file_path)}")

        messagebox.showinfo("Başarılı", f"Haber yazısı başarıyla kaydedildi!\n\nKaydedilen Konum:\n{output_file_path}")

    def _save_publication(self, target_base_dir):
        title = self.pub_item_title_entry.get().strip()
        if not title:
            messagebox.showerror("Hata", "Yayın Başlığı zorunludur.")
            return

        if self.loaded_slugs.get(3) and self.loaded_titles.get(3) == title:
            slug = self.loaded_slugs[3]
        else:
            slug = slugify(title)

        authors = self.pub_item_authors_entry.get().strip()
        venue = self.pub_item_venue_entry.get().strip()
        year = self.pub_item_year_entry.get().strip() or "2026"
        date_str = self.pub_item_date_entry.get().strip()

        links_dict = {}
        links_html_parts = []

        link_specs = [
            ("pdf", self.pub_link_pdf_entry.get().strip(), "Paper (PDF)"),
            ("doi", self.pub_link_doi_entry.get().strip(), "DOI"),
            ("code", self.pub_link_code_entry.get().strip(), "Code"),
            ("project", self.pub_link_proj_entry.get().strip(), "Project"),
            ("video", self.pub_link_video_entry.get().strip(), "Video"),
            ("dataset", self.pub_link_data_entry.get().strip(), "Dataset")
        ]

        for key, val, label in link_specs:
            if val:
                links_dict[key] = val
                links_html_parts.append(f'<a href="{val}" class="pub-link-btn" target="_blank" style="color:#2563eb; font-weight:600; margin-right:10px;">{label}</a>')

        links_html = f'<div class="pub-links">{" ".join(links_html_parts)}</div>' if links_html_parts else ""

        pub_data_dir = os.path.join(target_base_dir, "publications", "data")
        os.makedirs(pub_data_dir, exist_ok=True)

        metadata_dict = {
            "title": title,
            "slug": slug,
            "authors": authors,
            "venue": venue,
            "year": year,
            "date": date_str,
            "links": links_dict
        }

        html = PUBLICATION_HTML_TEMPLATE.replace("{{TITLE}}", title)
        html = html.replace("{{AUTHORS}}", authors)
        html = html.replace("{{VENUE}}", venue)
        html = html.replace("{{YEAR}}", year)
        html = html.replace("{{LINKS_HTML}}", links_html)
        html = html.replace("{{LIVE_RELOAD_SCRIPT}}", "")
        html = html.replace("{{EMBEDDED_CSS}}", EMBEDDED_CSS_CONTENT)
        html = html.replace("{{EMBEDDED_JS}}", EMBEDDED_JS_CONTENT)
        html = html.replace("{{METADATA_JSON}}", json.dumps(metadata_dict, ensure_ascii=False, indent=2))

        output_file_path = os.path.join(pub_data_dir, f"{slug}.html")
        with open(output_file_path, "w", encoding="utf-8") as f:
            f.write(html)

        self.loaded_file_paths[3] = output_file_path
        self.loaded_slugs[3] = slug
        self.loaded_titles[3] = title
        if hasattr(self, 'pub_loaded_badge'):
            self.pub_loaded_badge.configure(text=f"✓ Kaydedildi: {os.path.basename(output_file_path)}")

        messagebox.showinfo("Başarılı", f"Yayın kaydı başarıyla kaydedildi!\n\nKaydedilen Konum:\n{output_file_path}")

    def render_live_html(self):
        curr_tab = self.notebook.index(self.notebook.select())

        def preview_media_url(p):
            if not p:
                return get_svg_placeholder("Görsel Seçilmedi")
            if p.startswith(('http://', 'https://', 'file:///', 'data:image/')):
                return p
            abs_p = os.path.abspath(p).replace('\\', '/')
            return f"file:///{abs_p}"

        live_reload_html = """
        <div id="livePreviewBanner" style="position: fixed; bottom: 15px; right: 15px; z-index: 99999; background: #0f172a; color: #38bdf8; font-family: 'Inter', sans-serif; font-size: 12px; font-weight: 600; padding: 10px 18px; border-radius: 30px; box-shadow: 0 4px 20px rgba(0,0,0,0.3); border: 1px solid #1e293b; display: flex; align-items: center; gap: 8px;">
            <span style="width: 8px; height: 8px; background: #22c55e; border-radius: 50%; display: inline-block;"></span>
            MICROLab Live Preview (Otomatik Yenileniyor)
        </div>
        <script>
            setTimeout(() => {
                window.location.reload();
            }, 3000);
        </script>
        """

        if curr_tab == 0: # Project
            title = self.proj_title_entry.get().strip() or "Untitled Project"
            body = self.content_editor.render_html(media_copy_callback=preview_media_url)
            cover_uri = preview_media_url(self.proj_cover_path)
            
            header_style = f"background-image: linear-gradient(135deg, rgba(15,23,42,0.9), rgba(30,41,59,0.85)), url('{cover_uri}');"
            
            tags_raw = [t.strip() for t in self.proj_tags_entry.get().split(',') if t.strip()]
            status = self.proj_status_combo.get()
            start_date = self.proj_start_entry.get().strip()
            end_date = self.proj_end_entry.get().strip() if status == "Completed" else ""
            short_desc = self.proj_short_desc_text.get("1.0", tk.END).strip()
            timeline = f"{start_date} &mdash; <span style=\"color: #38a169;\">Active</span>" if status == "Active" else f"{start_date} &mdash; {end_date}"

            project_meta_html = f"""<div class="project-meta" style="margin-bottom: 25px; font-size: 0.95rem; color: #475569; background: var(--bg-alt); padding: 15px; border-left: 4px solid #2563eb; border-radius: 8px;">
                <strong>Timeline:</strong> {timeline} <span style="margin: 0 10px;">|</span> <strong>Status:</strong> {status}
            </div>"""

            team_names = [combo.get().strip() for combo in self.member_rows if combo.get().strip()]
            team_members_html_parts = [f'<div class="member-card" style="padding:15px; background:var(--bg-alt); border-radius:8px;"><h3 style="font-size:1.1rem; color:#2563eb;">{val}</h3></div>' for val in team_names]
            team_html = "\n".join(team_members_html_parts) if team_members_html_parts else '<p style="color:#64748b;">No members listed.</p>'

            pub_list = [{"title": t.get().strip(), "link": l.get().strip()} for t, l in self.pub_rows if t.get().strip()]

            pub_section_html = ""
            if pub_list:
                items_h = "\n".join([f"<li><a href='{p['link']}'>{p['title']}</a></li>" if p['link'] else f"<li>{p['title']}</li>" for p in pub_list])
                pub_section_html = f"<h2>Related Publications</h2>\n<div class='related-pubs-container' style='margin-top:0;'>\n<ul class='related-pubs-list'>\n{items_h}\n</ul>\n</div>"

            metadata_dict = {
                "title": title,
                "slug": slugify(title),
                "tags": tags_raw,
                "date": "2026-08-22",
                "timeline": timeline,
                "status": status,
                "short_description": short_desc,
                "image": cover_uri,
                "team": team_names,
                "publications": pub_list,
                "blocks": self.content_editor.get_blocks_data()
            }

            html = PROJECT_HTML_TEMPLATE.replace("{{TITLE}}", title)
            html = html.replace("{{HEADER_STYLE}}", header_style)
            html = html.replace("{{PROJECT_META_HTML}}", project_meta_html)
            html = html.replace("{{CONTENT_BODY_HTML}}", body)
            html = html.replace("{{TEAM_MEMBERS_HTML}}", team_html)
            html = html.replace("{{PUBLICATIONS_SECTION_HTML}}", pub_section_html)
            html = html.replace("{{LIVE_RELOAD_SCRIPT}}", live_reload_html)
            html = html.replace("{{EMBEDDED_CSS}}", EMBEDDED_CSS_CONTENT)
            html = html.replace("{{EMBEDDED_JS}}", EMBEDDED_JS_CONTENT)
            html = html.replace("{{METADATA_JSON}}", json.dumps(metadata_dict, ensure_ascii=False, indent=2))

        elif curr_tab == 1: # Person
            name = self.person_name_entry.get().strip() or "Untitled Person"
            role = self.person_role_entry.get().strip()
            department = self.person_dept_entry.get().strip()
            scholar = self.person_scholar_entry.get().strip()
            orcid = self.person_orcid_entry.get().strip()
            rg = self.person_rg_entry.get().strip()
            github = self.person_github_entry.get().strip()
            linkedin = self.person_linkedin_entry.get().strip()
            website = self.person_website_entry.get().strip()
            email = self.person_email_entry.get().strip()
            about = self.person_about_text.get("1.0", tk.END).strip()

            preview_photo_uri = preview_media_url(self.person_photo_path) if self.person_photo_path else ""

            metadata_dict = {
                "name": name,
                "slug": slugify(name),
                "role": role,
                "department": department,
                "about": about,
                "photo": preview_photo_uri,
                "scholar": scholar,
                "orcid": orcid,
                "researchgate": rg,
                "github": github,
                "linkedin": linkedin,
                "website": website,
                "email": email,
                "category": self.person_cat_combo.get()
            }

            social_links_html = generate_person_social_links_html(metadata_dict)
            about_html = f"<p>{about}</p>" if about else "<p>MICROLab team researcher.</p>"
            photo_html = f'<img src="{preview_photo_uri}" alt="{name}" style="width:100%;height:100%;object-fit:cover;">' if preview_photo_uri else ""

            html = PERSON_HTML_TEMPLATE.replace("{{NAME}}", name)
            html = html.replace("{{ROLE}}", role)
            html = html.replace("{{DEPARTMENT}}", department)
            html = html.replace("{{PHOTO_HTML}}", photo_html)
            html = html.replace("{{SOCIAL_LINKS_HTML}}", social_links_html)
            github_html = f'<a href="{github}" target="_blank" class="social-link-btn github">GitHub</a>' if github else ""
            linkedin_html = f'<a href="{linkedin}" target="_blank" class="social-link-btn linkedin">LinkedIn</a>' if linkedin else ""
            html = html.replace("{{GITHUB_LINK_HTML}}", github_html)
            html = html.replace("{{LINKEDIN_LINK_HTML}}", linkedin_html)
            html = html.replace("{{ABOUT_HTML}}", about_html)
            html = html.replace("{{LIVE_RELOAD_SCRIPT}}", live_reload_html)
            html = html.replace("{{EMBEDDED_CSS}}", EMBEDDED_CSS_CONTENT)
            html = html.replace("{{EMBEDDED_JS}}", EMBEDDED_JS_CONTENT)
            html = html.replace("{{METADATA_JSON}}", json.dumps(metadata_dict, ensure_ascii=False, indent=2))

        elif curr_tab == 2: # News
            title = self.news_title_entry.get().strip() or "Untitled News"
            date_str = self.news_date_entry.get().strip() or "2026-08-22"
            category = self.news_cat_combo.get().strip() or "Announcements"
            summary = self.news_summary_text.get("1.0", tk.END).strip()
            body_html = self.news_content_editor.render_html(media_copy_callback=preview_media_url)

            metadata_dict = {
                "title": title,
                "slug": f"news_{slugify(title)}",
                "date": date_str,
                "category": category,
                "short_description": summary
            }

            html = NEWS_HTML_TEMPLATE.replace("{{TITLE}}", title)
            html = html.replace("{{DATE}}", date_str)
            html = html.replace("{{CATEGORY}}", category)
            html = html.replace("{{CONTENT_BODY_HTML}}", body_html)
            html = html.replace("{{LIVE_RELOAD_SCRIPT}}", live_reload_html)
            html = html.replace("{{EMBEDDED_CSS}}", EMBEDDED_CSS_CONTENT)
            html = html.replace("{{EMBEDDED_JS}}", EMBEDDED_JS_CONTENT)
            html = html.replace("{{METADATA_JSON}}", json.dumps(metadata_dict, ensure_ascii=False, indent=2))

        elif curr_tab == 3: # Publication
            title = self.pub_item_title_entry.get().strip() or "Untitled Publication"
            authors = self.pub_item_authors_entry.get().strip()
            venue = self.pub_item_venue_entry.get().strip()
            year = self.pub_item_year_entry.get().strip() or "2026"
            date_str = self.pub_item_date_entry.get().strip()

            links_dict = {}
            links_html_parts = []

            if self.pub_link_pdf_entry.get().strip():
                links_dict["pdf"] = self.pub_link_pdf_entry.get().strip()
                links_html_parts.append(f'<a href="{links_dict["pdf"]}" class="pub-link-btn" target="_blank">Paper (PDF)</a>')
            if self.pub_link_doi_entry.get().strip():
                links_dict["doi"] = self.pub_link_doi_entry.get().strip()
                links_html_parts.append(f'<a href="{links_dict["doi"]}" class="pub-link-btn" target="_blank">DOI</a>')

            links_html = f'<div class="pub-links">{" ".join(links_html_parts)}</div>' if links_html_parts else ""

            metadata_dict = {
                "title": title,
                "slug": slugify(title),
                "authors": authors,
                "venue": venue,
                "year": year,
                "date": date_str,
                "links": links_dict
            }

            html = PUBLICATION_HTML_TEMPLATE.replace("{{TITLE}}", title)
            html = html.replace("{{AUTHORS}}", authors)
            html = html.replace("{{VENUE}}", venue)
            html = html.replace("{{YEAR}}", year)
            html = html.replace("{{LINKS_HTML}}", links_html)
            html = html.replace("{{LIVE_RELOAD_SCRIPT}}", live_reload_html)
            html = html.replace("{{EMBEDDED_CSS}}", EMBEDDED_CSS_CONTENT)
            html = html.replace("{{EMBEDDED_JS}}", EMBEDDED_JS_CONTENT)
            html = html.replace("{{METADATA_JSON}}", json.dumps(metadata_dict, ensure_ascii=False, indent=2))

        return html

    def open_live_preview(self):
        html = self.render_live_html()
        try:
            with open(self.preview_temp_path, 'w', encoding='utf-8') as f:
                f.write(html)
            self.live_preview_opened = True
            webbrowser.open(f"file:///{self.preview_temp_path.replace(chr(92), '/')}")
        except Exception as e:
            messagebox.showerror("Hata", f"Canlı önizleme açılamadı: {e}")

    def auto_update_preview_loop(self):
        if self.live_preview_opened and self.auto_sync_var.get():
            try:
                html = self.render_live_html()
                with open(self.preview_temp_path, 'w', encoding='utf-8') as f:
                    f.write(html)
            except Exception: pass
        
        self.after(2500, self.auto_update_preview_loop)

# Geriye donuk uyumluluk takma adi (Backward compatibility alias)
StandaloneProjectCreatorApp = MicroLabEditorApp

if __name__ == "__main__":
    app = MicroLabEditorApp()
    app.mainloop()
