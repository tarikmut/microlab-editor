# -*- coding: utf-8 -*-
"""
MICROLab Media Portability & Security Helper Module
===================================================
Provides cross-platform media handling, URI generation, collision-free copying,
path rehydration for imported projects, and security validation.
Compatible with macOS, Linux, and Windows.
"""

import os
import sys
import re
import html
import shutil
import hashlib
from pathlib import Path
from urllib.parse import urlparse

# CROSS-PLATFORM IMAGE FILETYPES FOR TKINTER FILE DIALOGS
# Tk expects a tuple of patterns for multi-extension filters on macOS / Linux.
# Semicolon-separated strings like "*.png;*.jpg" fail on Unix/macOS Finder globbing.
IMAGE_FILETYPES = [
    (
        "Görseller / Images",
        (
            "*.png", "*.PNG",
            "*.jpg", "*.JPG",
            "*.jpeg", "*.JPEG",
            "*.webp", "*.WEBP",
            "*.svg", "*.SVG",
            "*.gif", "*.GIF",
            "*.bmp", "*.BMP",
            "*.tiff", "*.TIFF",
            "*.tif", "*.TIF",
            "*.heic", "*.HEIC",
            "*.heif", "*.HEIF"
        )
    ),
    ("Tüm Dosyalar / All Files", "*")
]

HTML_FILETYPES = [
    ("MICROLab HTML Dosyaları", ("*.html", "*.HTML", "*.htm", "*.HTM")),
    ("Tüm Dosyalar / All Files", "*")
]


def path_to_file_uri(path_str):
    """
    Converts a file system path to a valid, portable file:// URI.
    Fixes the 4-slash bug on POSIX (file:////Users/...) and properly
    percent-encodes spaces, #, %, and Unicode characters.
    """
    if not path_str:
        return ""
    if path_str.startswith(('http://', 'https://', 'data:image/')):
        return path_str
    try:
        return Path(path_str).resolve().as_uri()
    except Exception:
        # Robust fallback
        resolved = os.path.abspath(path_str).replace('\\', '/')
        if not resolved.startswith('/'):
            resolved = '/' + resolved
        # URL-encode special characters
        from urllib.parse import quote
        parts = resolved.split('/')
        quoted_parts = [quote(p, safe='') for p in parts]
        return "file://" + '/'.join(quoted_parts)


def calculate_file_hash(file_path):
    """Calculates SHA-256 hash of a file."""
    h = hashlib.sha256()
    with open(file_path, 'rb') as f:
        while chunk := f.read(65536):
            h.update(chunk)
    return h.hexdigest()


def safe_copy_media_file(src_path, images_dir):
    """
    Safely copies an image to images_dir:
    1. Prevents shutil.SameFileError if source and target are the same file.
    2. If a file with the same name already exists in images_dir:
       - If SHA-256 matches: reuses the existing file (no redundant copy).
       - If SHA-256 differs: creates a collision-free filename '<stem>_<hash8><suffix>'.
    3. If src_path is not found on disk, checks if images_dir / basename(src_path)
       already exists (reusing previously bundled asset).
    Returns: The final filename (basename) stored in images_dir, or None if source cannot be found.
    """
    if not src_path:
        return None

    images_dir_path = Path(images_dir).resolve()
    images_dir_path.mkdir(parents=True, exist_ok=True)

    src_p = Path(src_path)

    # If src_path does not exist as given, check if it's already inside images_dir
    if not src_p.exists():
        candidate_in_images = images_dir_path / src_p.name
        if candidate_in_images.exists():
            return candidate_in_images.name
        # Cannot locate source file
        return None

    src_p = src_p.resolve()
    target_name = src_p.name
    dest_p = (images_dir_path / target_name).resolve()

    # Case 1: Same file check (SameFileError prevention)
    if src_p == dest_p:
        return target_name
    try:
        if dest_p.exists() and src_p.samefile(dest_p):
            return target_name
    except (OSError, ValueError):
        pass

    # Case 2: Target file already exists with this name
    if dest_p.exists():
        try:
            h_src = calculate_file_hash(src_p)
            h_dest = calculate_file_hash(dest_p)
            if h_src == h_dest:
                # Identical content: reuse existing without overwriting
                return target_name
            else:
                # Content collision: generate safe name with short hash
                target_name = f"{src_p.stem}_{h_src[:8]}{src_p.suffix}"
                dest_p = images_dir_path / target_name
                if dest_p.exists() and calculate_file_hash(dest_p) == h_src:
                    return target_name
        except Exception:
            pass

    # Case 3: Perform copy
    shutil.copy2(str(src_p), str(dest_p))
    return target_name


def rehydrate_media_path(path_or_uri, html_file_path=None, website_root=None):
    """
    Rehydrates a media path from saved project/person/news metadata.
    If the metadata contains an old absolute path from another machine (e.g. C:\\Users\\...
    or /Users/olduser/...), or a relative path (../../images/foo.png), this function
    resolves it to the actual file on the local machine if it exists.

    Returns: Absolute local path string if found, else original path_or_uri.
    """
    if not path_or_uri or str(path_or_uri).startswith(('http://', 'https://', 'data:image/')):
        return path_or_uri

    raw_path = str(path_or_uri).strip()

    # 1. Check if the path exists directly on the current machine
    try:
        if os.path.exists(raw_path):
            return str(Path(raw_path).resolve())
    except Exception:
        pass

    basename = os.path.basename(raw_path.replace('\\', '/'))
    if not basename:
        return raw_path

    candidates = []

    # 2. Candidate paths relative to html_file_path (where the HTML is stored)
    if html_file_path:
        doc_dir = Path(html_file_path).resolve().parent
        # Clean relative path if it uses Unix or Windows slashes
        clean_rel = raw_path.replace('\\', '/')
        if clean_rel.startswith('../../') or clean_rel.startswith('../'):
            candidates.append(doc_dir / clean_rel)
        candidates.extend([
            doc_dir / ".." / ".." / "images" / basename,
            doc_dir / ".." / "images" / basename,
            doc_dir / "images" / basename,
            doc_dir / basename
        ])

    # 3. Candidate paths relative to website_root
    if website_root:
        w_root = Path(website_root).resolve()
        candidates.extend([
            w_root / "images" / basename,
            w_root / basename
        ])

    for cand in candidates:
        try:
            cand_resolved = cand.resolve()
            if cand_resolved.is_file():
                return str(cand_resolved)
        except Exception:
            continue

    return raw_path


def rehydrate_blocks_data(blocks_data, html_file_path=None, website_root=None):
    """
    Recursively rehydrates all image and gallery block paths in blocks_data.
    Returns a new list with rehydrated paths.
    """
    if not blocks_data or not isinstance(blocks_data, list):
        return []

    rehydrated = []
    for b in blocks_data:
        if not isinstance(b, dict):
            rehydrated.append(b)
            continue

        b_copy = dict(b)
        btype = b_copy.get('type')

        if btype == 'image' and 'path' in b_copy:
            b_copy['path'] = rehydrate_media_path(b_copy['path'], html_file_path, website_root)

        elif btype == 'gallery' and 'items' in b_copy and isinstance(b_copy['items'], list):
            new_items = []
            for item in b_copy['items']:
                if isinstance(item, dict) and item.get('type') == 'image' and 'path' in item:
                    item_copy = dict(item)
                    item_copy['path'] = rehydrate_media_path(item_copy['path'], html_file_path, website_root)
                    new_items.append(item_copy)
                else:
                    new_items.append(item)
            b_copy['items'] = new_items

        rehydrated.append(b_copy)

    return rehydrated


def make_portable_blocks_data(blocks_data, saved_images_map=None):
    """
    Transforms blocks_data so that image paths reference relative project paths
    like '../../images/<filename>' rather than host-specific absolute paths.
    saved_images_map: optional dict {original_path: saved_filename}
    """
    if not blocks_data or not isinstance(blocks_data, list):
        return []

    portable = []
    for b in blocks_data:
        if not isinstance(b, dict):
            portable.append(b)
            continue

        b_copy = dict(b)
        btype = b_copy.get('type')

        if btype == 'image' and 'path' in b_copy:
            p = b_copy['path']
            if saved_images_map and p in saved_images_map:
                b_copy['path'] = f"../../images/{saved_images_map[p]}"
            elif p and not p.startswith(('http://', 'https://', '../../images/')):
                b_copy['path'] = f"../../images/{os.path.basename(p.replace(chr(92), '/'))}"

        elif btype == 'gallery' and 'items' in b_copy and isinstance(b_copy['items'], list):
            new_items = []
            for item in b_copy['items']:
                if isinstance(item, dict) and item.get('type') == 'image' and 'path' in item:
                    item_copy = dict(item)
                    p = item_copy['path']
                    if saved_images_map and p in saved_images_map:
                        item_copy['path'] = f"../../images/{saved_images_map[p]}"
                    elif p and not p.startswith(('http://', 'https://', '../../images/')):
                        item_copy['path'] = f"../../images/{os.path.basename(p.replace(chr(92), '/'))}"
                    new_items.append(item_copy)
                else:
                    new_items.append(item)
            b_copy['items'] = new_items

        portable.append(b_copy)

    return portable


def escape_html_text(text):
    """Safely escapes text for inclusion in HTML body."""
    if text is None:
        return ""
    return html.escape(str(text))


def escape_html_attr(text):
    """Safely escapes text for inclusion in HTML attributes (quote=True)."""
    if text is None:
        return ""
    return html.escape(str(text), quote=True)


def is_safe_url(url):
    """
    Validates that a URL uses safe protocols (http, https, mailto)
    or is a safe internal relative path, blocking javascript: and dangerous schemes.
    """
    if not url:
        return True
    u = str(url).strip()
    if u.startswith(('#', '/', './', '../')):
        return True
    parsed = urlparse(u)
    return parsed.scheme.lower() in ('http', 'https', 'mailto')


def sanitize_url_for_href(url):
    """Returns safe URL for href attribute, or '#' if dangerous/invalid."""
    if not url:
        return "#"
    u = str(url).strip()
    if is_safe_url(u):
        return escape_html_attr(u)
    return "#"

