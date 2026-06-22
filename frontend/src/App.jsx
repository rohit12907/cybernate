import { useEffect } from "react";

import markup from "./cybermate-markup.html?raw";
import engineScript from "./cybermate-engine.js?raw";
import {
  getHealth,
  getThreats,
  ingestLog,
  sendAlert,
  reset
} from "./api/client";
/**
 * App
 * ----------------------------------------------------------------------
 * This renders the exact CyberMate experience from the reference
 * cybermate.html file: theme switcher -> animated intro -> operation
 * menu -> normal log scan / brute-force pipeline simulation -> success
 * screen. The markup and the vanilla-JS "engine" that drives it are kept
 * verbatim (as separate .html/.js source files, imported as raw text via
 * Vite's `?raw` loader) so behaviour and visuals match the original 1:1.
 *
 * The engine script is injected as a real <script> tag (rather than via
 * dangerouslySetInnerHTML, which never executes <script> contents) so that
 * its top-level `function` declarations attach to `window`, exactly as
 * they did in the original static HTML file. That's required because the
 * markup's inline `onclick="goMenu()"` style handlers resolve through the
 * global scope.
 */
function App() {
  useEffect(() => {
window.CyberMateAPI = {
  getHealth,
  getThreats,
  ingestLog,
  sendAlert,
  reset
};

    // Guard against double-injection (React StrictMode re-invokes effects
    // once in dev, and Vite HMR can re-run this module) — CyberMate's
    // engine starts animation loops / intervals that must only run once.
    if (window.__cybermateBooted) return;
    window.__cybermateBooted = true;

    const script = document.createElement("script");
    script.id = "cybermate-engine";
    script.text = engineScript;
    document.body.appendChild(script);

  }, []);

  return (
    <div id="cybermate-root" dangerouslySetInnerHTML={{ __html: markup }} />
  );
}

export default App;
