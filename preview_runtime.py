# -*- coding: utf-8 -*-
"""
MICROLab Preview Runtime Manager
================================
Provides isolated, collision-free, revision-aware live HTML preview sessions.
Features:
- Unique per-instance preview directory (PREV-05)
- Atomic file operations (no partial reads, PREV-06)
- Content hash & revision tracking: reloads ONLY when content actually changes (PREV-01, PREV-03)
- Real-time sync status communication with browser via sibling state script (PREV-01, PREV-02)
- Clean session cleanup on exit
"""

import os
import sys
import time
import uuid
import json
import shutil
import hashlib
import tempfile
from pathlib import Path


class PreviewRuntimeSession:
    """
    Manages an active preview session for a MICROLab Editor instance.
    """
    def __init__(self, sync_enabled=True):
        self.sync_enabled = bool(sync_enabled)
        self.revision = 1
        self.last_content_hash = ""
        self.last_rendered_html = ""
        
        # Unique isolated session directory
        pid = os.getpid()
        unique_token = uuid.uuid4().hex[:8]
        self.session_dir = os.path.join(tempfile.gettempdir(), f"microlab_preview_{pid}_{unique_token}")
        os.makedirs(self.session_dir, exist_ok=True)
        
        self.html_path = os.path.join(self.session_dir, "preview.html")
        self.state_path = os.path.join(self.session_dir, "preview_state.js")
        
        # Initialize state file
        self.write_state_file()

    def write_state_file(self):
        """Atomically writes preview_state.js with current revision and enabled status."""
        state_data = {
            "enabled": self.sync_enabled,
            "revision": self.revision,
            "timestamp": time.time()
        }
        content = f"window.__MICROLAB_PREVIEW_STATE__ = {json.dumps(state_data, indent=2)};\n"
        tmp_path = self.state_path + ".tmp"
        try:
            with open(tmp_path, "w", encoding="utf-8") as f:
                f.write(content)
            os.replace(tmp_path, self.state_path)
        except Exception:
            try:
                with open(self.state_path, "w", encoding="utf-8") as f:
                    f.write(content)
            except Exception:
                pass

    def set_sync_enabled(self, enabled):
        """Updates the auto-sync state and notifies the browser via state file."""
        new_val = bool(enabled)
        if self.sync_enabled != new_val:
            self.sync_enabled = new_val
            self.write_state_file()

    def generate_live_reload_snippet(self, revision=None):
        """Generates client-side banner and polling JavaScript."""
        rev = self.revision if revision is None else revision
        initial_dot_color = "#22c55e" if self.sync_enabled else "#94a3b8"
        initial_text = "MICROLab Live Preview (Otomatik Yenileniyor)" if self.sync_enabled else "MICROLab Live Preview (Duraklatıldı)"

        return f"""
        <div id="livePreviewBanner" style="position: fixed; bottom: 15px; right: 15px; z-index: 99999; background: #0f172a; color: #38bdf8; font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif; font-size: 12px; font-weight: 600; padding: 10px 18px; border-radius: 30px; box-shadow: 0 4px 20px rgba(0,0,0,0.3); border: 1px solid #1e293b; display: flex; align-items: center; gap: 8px; pointer-events: none; user-select: none;">
            <span id="livePreviewDot" style="width: 8px; height: 8px; background: {initial_dot_color}; border-radius: 50%; display: inline-block; transition: background 0.3s;"></span>
            <span id="livePreviewText">{initial_text}</span>
        </div>
        <script>
        (function() {{
            var myRevision = {rev};
            var isPolling = false;
            function pollState() {{
                if (isPolling) return;
                isPolling = true;
                var s = document.createElement("script");
                s.src = "preview_state.js?t=" + Date.now();
                s.onload = function() {{
                    s.remove();
                    isPolling = false;
                    if (window.__MICROLAB_PREVIEW_STATE__) {{
                        var st = window.__MICROLAB_PREVIEW_STATE__;
                        var dot = document.getElementById("livePreviewDot");
                        var txt = document.getElementById("livePreviewText");
                        if (st.enabled) {{
                            if (dot) dot.style.background = "#22c55e";
                            if (txt) txt.textContent = "MICROLab Live Preview (Otomatik Yenileniyor)";
                            if (st.revision > myRevision) {{
                                window.location.reload();
                                return;
                            }}
                        }} else {{
                            if (dot) dot.style.background = "#94a3b8";
                            if (txt) txt.textContent = "MICROLab Live Preview (Duraklatıldı)";
                        }}
                    }}
                    setTimeout(pollState, 900);
                }};
                s.onerror = function() {{
                    s.remove();
                    isPolling = false;
                    setTimeout(pollState, 1500);
                }};
                document.head.appendChild(s);
            }}
            setTimeout(pollState, 900);
        }})();
        </script>
        """

    def write_html_atomic(self, html_content):
        """Atomically writes preview HTML to avoid partial reads."""
        tmp_path = self.html_path + ".tmp"
        try:
            with open(tmp_path, "w", encoding="utf-8") as f:
                f.write(html_content)
            os.replace(tmp_path, self.html_path)
        except Exception:
            with open(self.html_path, "w", encoding="utf-8") as f:
                f.write(html_content)

    def update_content_if_changed(self, raw_html_generator, force=False):
        """
        Executes raw_html_generator to produce HTML.
        Calculates content hash. If content changed or force=True:
        - Increments revision
        - Injects reload script with new revision
        - Atomically writes HTML and state
        Returns: (bool updated, str final_html)
        """
        raw_html = raw_html_generator()
        if not raw_html:
            return False, ""

        content_hash = hashlib.sha256(raw_html.encode("utf-8")).hexdigest()

        if not force and content_hash == self.last_content_hash:
            # No changes detected: skip writing to disk to prevent unnecessary reloads / I/O
            return False, self.last_rendered_html

        # Content changed
        if not force:
            self.revision += 1

        self.last_content_hash = content_hash
        snippet = self.generate_live_reload_snippet(self.revision)
        final_html = raw_html.replace("{{LIVE_RELOAD_SCRIPT}}", snippet)
        self.last_rendered_html = final_html

        self.write_html_atomic(final_html)
        self.write_state_file()

        return True, final_html

    def cleanup(self):
        """Cleans up the temporary session directory on application shutdown."""
        try:
            if os.path.exists(self.session_dir):
                shutil.rmtree(self.session_dir, ignore_errors=True)
        except Exception:
            pass
