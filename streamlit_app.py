import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="Webページが表示されるまで｜通信の仕組みシミュレータ",
    page_icon="🌐",
    layout="wide",
)

# Streamlit 標準UIの余白を切り詰め、下の1画面シミュレータを主役にする
st.markdown(
    """
    <style>
        .block-container {padding-top: 1.2rem; padding-bottom: 0.5rem; max-width: 1500px;}
        header[data-testid="stHeader"] {background: transparent;}
        #MainMenu, footer {visibility: hidden;}
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    "### 🌐 Webページが表示されるまで — 通信の仕組みシミュレータ\n"
    "URLを入力して「アクセス」を押すと、DNS問い合わせ・HTTPリクエスト・パケットの流れ・"
    "ブラウザでの表示までを観察できます。（情報Ⅰ「情報通信ネットワーク」）"
)

SIM_HTML = r"""
<!DOCTYPE html>
<html lang="ja">
<head>
<meta charset="UTF-8">
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@500;600;700&family=Inter:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500;600&display=swap');

:root{
  --bg: #0a0f1c;
  --panel: #111a2b;
  --panel-2: #16223a;
  --panel-3: #1c2b47;
  --border: #263453;
  --text: #e7edf7;
  --muted: #8ba0c4;
  --muted-2: #5f7495;
  --dns: #b98ce8;
  --http: #45d9ce;
  --ok: #4ade80;
  --warn: #f5a623;
  --danger: #f2716d;
  --html-c: #6fb7ff;
  --css-c: #45d9ce;
  --img-c: #f5a623;
}
*{box-sizing:border-box;}
html,body{margin:0;padding:0;background:var(--bg);color:var(--text);
  font-family:'Inter','Hiragino Sans','Hiragino Kaku Gothic ProN',sans-serif;}
.wrap{padding:14px 16px 20px;}
h1,h2,h3,.disp{font-family:'Space Grotesk','Inter',sans-serif;}
.mono{font-family:'JetBrains Mono',monospace;}

/* ---------- layout ---------- */
.mode-switch{
  display:flex;
  gap:8px;
  align-items:center;
  margin-bottom:12px;
  flex-wrap:wrap;
}
.mode-tab{
  border:1px solid var(--border);
  background:var(--panel-2);
  color:var(--muted);
  border-radius:8px;
  padding:8px 12px;
  font-size:13px;
  font-weight:700;
  cursor:pointer;
}
.mode-tab.active{
  background:linear-gradient(135deg,#45d9ce,#6fb7ff);
  color:#04121a;
  border-color:transparent;
}
.mode-hint{font-size:11px;color:var(--muted-2);}
.hidden{display:none !important;}
.stage{
  display:grid;
  grid-template-columns: 300px 1fr 250px;
  grid-template-rows: auto auto;
  gap:12px;
  margin-bottom:12px;
}
.panel{
  background:linear-gradient(180deg, var(--panel-2), var(--panel));
  border:1px solid var(--border);
  border-radius:14px;
  padding:14px;
  position:relative;
}
.panel-title{
  font-family:'Space Grotesk',sans-serif;
  font-size:13px;
  font-weight:700;
  letter-spacing:.04em;
  color:var(--muted);
  text-transform:uppercase;
  display:flex;
  align-items:center;
  gap:6px;
  margin-bottom:10px;
}
.dot{width:8px;height:8px;border-radius:50%;display:inline-block;}
.dot-browser{background:#6fb7ff;}
.dot-dns{background:var(--dns);}
.dot-web{background:var(--warn);}
.dot-net{background:var(--http);}

/* browser panel */
.browser{grid-row: 1 / 3; display:flex; flex-direction:column;}
.addr-row{display:flex; gap:6px; margin-bottom:8px;}
.addr-row input{
  flex:1; min-width:0; background:#0c1424; border:1px solid var(--border);
  color:var(--text); border-radius:8px; padding:9px 10px; font-size:13px;
  font-family:'JetBrains Mono',monospace;
}
.addr-row input:focus{outline:2px solid var(--http);}
.btn{
  border:none; border-radius:8px; padding:9px 14px; font-size:13px; font-weight:600;
  cursor:pointer; font-family:'Inter',sans-serif; transition:filter .15s, transform .05s;
  white-space:nowrap;
}
.btn:active{transform:scale(.97);}
.btn-go{background:linear-gradient(135deg,#45d9ce,#3a9fe0); color:#04121a;}
.btn-reset{background:var(--panel-3); color:var(--text); border:1px solid var(--border);}
.btn-ghost{background:transparent; color:var(--muted); border:1px solid var(--border); font-size:12px; padding:6px 9px;}
.btn:hover{filter:brightness(1.12);}
.hint-text{font-size:10.5px; color:var(--muted-2); margin:-2px 0 10px;}
.controls-row{display:flex; gap:8px; align-items:center; margin-bottom:10px; flex-wrap:wrap;}
.controls-row select{
  background:#0c1424; color:var(--text); border:1px solid var(--border);
  border-radius:7px; padding:6px 8px; font-size:12px; font-family:'Inter',sans-serif;
}
.resolved-ip{
  font-family:'JetBrains Mono',monospace; font-size:11px; color:var(--muted);
  background:#0c1424; border:1px solid var(--border); border-radius:7px;
  padding:6px 8px; margin-bottom:10px; min-height:14px;
}
.resolved-ip b{color:var(--http);}

.browser-window{
  flex:1; background:#fff; color:#1a1a1a; border-radius:10px; overflow:hidden;
  display:flex; flex-direction:column; min-height:230px; border:3px solid #0c1424;
}
.browser-chrome{
  background:#e7ebf2; padding:6px 8px; display:flex; align-items:center; gap:5px;
}
.browser-chrome .dotc{width:9px;height:9px;border-radius:50%;}
.bc1{background:#f2716d;} .bc2{background:#f5a623;} .bc3{background:#4ade80;}
.browser-body{padding:14px; flex:1; overflow:auto; font-family:Georgia,'Hiragino Mincho ProN',serif;}
.browser-body.styled{
  font-family:'Space Grotesk','Hiragino Sans',sans-serif; background:linear-gradient(180deg,#eaf6ff,#ffffff);
  padding:0;
}
.browser-body .empty-msg{color:#999; font-size:12px; text-align:center; margin-top:60px; font-family:'Inter',sans-serif;}
.page-h1{font-size:20px; margin:0 0 8px;}
.browser-body.styled .page-h1{
  background:linear-gradient(135deg,#1c3d6b,#3a9fe0); color:#fff; margin:0; padding:16px 18px;
  font-size:19px; font-weight:700;
}
.page-p{font-size:13px; line-height:1.7; color:#333; margin:0 0 10px;}
.browser-body.styled .page-p{padding:0 18px; color:#334;}
.page-list{margin:0 0 8px; padding-left:18px; font-size:12px;}
.browser-body.styled .page-list{
  display:flex; gap:14px; list-style:none; padding:10px 18px; margin:0;
  background:#f2f7ff; border-bottom:1px solid #dce8f7;
}
.browser-body.styled .page-list li{color:#1c3d6b; font-size:12px; font-weight:600;}
.hero-img{
  margin:12px 18px; height:90px; border-radius:8px;
  background:linear-gradient(135deg,#ffd28a,#ff9d6c 55%,#7ec8ff);
  display:flex; align-items:center; justify-content:center; font-size:26px;
  animation:fadeIn .5s ease;
}
.img-caption{padding:0 18px 14px; font-size:11px; color:#88a; font-family:'Inter',sans-serif;}
@keyframes fadeIn{from{opacity:0; transform:translateY(6px);} to{opacity:1; transform:none;}}

.progress-group{display:flex; flex-direction:column; gap:7px; margin-top:10px;}
.prow{display:flex; align-items:center; gap:8px; font-size:11px;}
.prow .plabel{width:38px; font-family:'JetBrains Mono',monospace; color:var(--muted); flex-shrink:0;}
.pbar{flex:1; height:8px; background:#0c1424; border-radius:5px; overflow:hidden; border:1px solid var(--border);}
.pfill{height:100%; width:0%; border-radius:5px; transition:width .25s ease;}
.pfill.html{background:var(--html-c);} .pfill.css{background:var(--css-c);} .pfill.img{background:var(--img-c);}
.ppct{width:34px; text-align:right; font-family:'JetBrains Mono',monospace; color:var(--muted); flex-shrink:0;}

/* network panel */
.network{grid-row:1/3; padding:8px 6px 6px; overflow:hidden;}
.network svg{width:100%; height:100%; display:block; min-height:330px;}
.node-box rect{fill:var(--panel-3); stroke:var(--border); stroke-width:1.5;}
.node-label{fill:var(--muted); font-size:11px; font-family:'JetBrains Mono',monospace; text-anchor:middle;}
.cloud-label{fill:var(--muted-2); font-size:12px; font-family:'Space Grotesk',sans-serif; letter-spacing:.08em;}
.route-line{fill:none; stroke:#2b3c60; stroke-width:2; stroke-dasharray:5 6;}
.route-line.on{stroke:var(--http); stroke-dasharray:none; opacity:.9;}

.packet rect{stroke-width:1; rx:6;}
.packet text{font-family:'JetBrains Mono',monospace; font-size:9.5px; fill:#04121a; text-anchor:middle; pointer-events:none; font-weight:600;}
.packet{cursor:pointer;}
.packet.arrived{opacity:0; transition:opacity .35s ease;}
.pkt-dns rect{fill:var(--dns);}
.pkt-http rect{fill:var(--http);}
.pkt-html rect{fill:var(--html-c);}
.pkt-css rect{fill:var(--css-c);}
.pkt-img rect{fill:var(--img-c);}
.node-pulse{opacity:0;}
.node-pulse.on{animation:pulse 1s ease-in-out infinite;}
@keyframes pulse{0%{opacity:.65;} 50%{opacity:.15;} 100%{opacity:.65;}}

.detail-box{
  position:absolute; left:10px; bottom:10px; right:10px;
  background:#0c1424; border:1px solid var(--border); border-radius:10px;
  padding:9px 10px; font-size:11px; display:none; z-index:5;
}
.detail-box.show{display:block;}
.detail-box .dclose{float:right; cursor:pointer; color:var(--muted); font-size:13px;}
.detail-box .drow{margin:2px 0; font-family:'JetBrains Mono',monospace; color:var(--muted);}
.detail-box .drow b{color:var(--text);}

.tcp-note{
  position:absolute; top:10px; right:12px; font-size:10px; color:var(--muted-2);
  cursor:default; z-index:4;
}
.tcp-note details summary{list-style:none; cursor:pointer; font-size:15px;}
.tcp-note details summary::-webkit-details-marker{display:none;}
.tcp-note details[open] summary{color:var(--http);}
.tcp-note .note-body{
  margin-top:6px; width:210px; background:#0c1424; border:1px solid var(--border);
  border-radius:8px; padding:8px 9px; font-size:10.5px; color:var(--muted); line-height:1.6;
}

/* dns / web server side panels */
.side{display:flex; flex-direction:column; gap:6px;}
.side .status-line{font-size:11px; color:var(--muted); font-family:'JetBrains Mono',monospace; min-height:15px;}

/* server rack hardware illustration */
.server-box{
  position:relative;
  background:linear-gradient(180deg,#323f5c,#1a2338 85%);
  border:1px solid #3a4a6e;
  border-radius:7px;
  padding:8px 9px 9px;
  box-shadow: inset 0 1px 0 rgba(255,255,255,.06), inset 0 -6px 10px rgba(0,0,0,.35), 0 3px 8px rgba(0,0,0,.35);
  transition: box-shadow .25s ease, border-color .25s ease;
}
.server-box.busy{
  border-color: var(--http);
  box-shadow: inset 0 1px 0 rgba(255,255,255,.06), 0 0 0 2px rgba(69,217,206,.25), 0 0 14px rgba(69,217,206,.35);
}
.server-box .screw{
  position:absolute; width:4px; height:4px; border-radius:50%;
  background:radial-gradient(circle at 35% 35%, #dbe2ee, #7c8aa3 55%, #333f5c 100%);
}
.server-box .screw.tl{top:4px;left:4px;} .server-box .screw.tr{top:4px;right:4px;}
.server-box .screw.bl{bottom:4px;left:4px;} .server-box .screw.br{bottom:4px;right:4px;}
.server-rack{display:flex; flex-direction:column; gap:4px; margin:1px 9px;}
.server-unit{
  height:15px; background:#0b1220; border:1px solid #263453; border-radius:3px;
  display:flex; align-items:center; padding:0 6px; gap:5px;
}
.server-unit .vents{
  flex:1; height:6px; border-radius:2px;
  background-image:repeating-linear-gradient(90deg, #24314f 0 3px, transparent 3px 6px);
}
.server-unit .tag{font-family:'JetBrains Mono',monospace; font-size:7.5px; color:#4a5a80; flex-shrink:0; letter-spacing:.03em;}
.led{width:6px; height:6px; border-radius:50%; flex-shrink:0; background:#334; box-shadow:none;}
.led-green{background:#4ade80; box-shadow:0 0 4px #4ade80;}
.led-amber{background:#f5a623; box-shadow:0 0 4px #f5a623;}
.led.blink{animation:ledBlink 1.4s ease-in-out infinite;}
@keyframes ledBlink{0%,100%{opacity:1;} 50%{opacity:.25;}}
.server-label{
  display:flex; align-items:center; gap:6px; margin-top:8px; font-size:11px; color:var(--muted);
}
.server-label .ip{font-family:'JetBrains Mono',monospace; color:var(--text); font-size:10.5px;}
.server-label .rack-icon{font-size:14px;}
.file-list{list-style:none; margin:6px 0 0; padding:0; font-size:11px;}
.file-list li{
  display:flex; align-items:center; gap:6px; padding:5px 7px; margin-bottom:5px;
  background:#0c1424; border:1px solid var(--border); border-radius:6px; color:var(--muted);
  font-family:'JetBrains Mono',monospace; transition:all .2s;
}
.file-list li.active{border-color:var(--http); color:var(--text); box-shadow:0 0 0 1px var(--http) inset;}
.table-row{display:flex; justify-content:space-between; font-size:10.5px; color:var(--muted); font-family:'JetBrains Mono',monospace; padding:2px 0;}
.table-row b{color:var(--text); font-weight:500;}

/* bottom: stepper + log */
.bottom{display:grid; grid-template-columns: 1.15fr 1fr; gap:12px;}
.stepper{list-style:none; display:flex; margin:4px 0 0; padding:0; position:relative;}
.stepper li{
  flex:1; text-align:center; font-size:10.5px; color:var(--muted-2); position:relative; padding-top:26px;
}
.stepper li::before{
  content:''; position:absolute; top:6px; left:0; right:0; height:2px; background:var(--border); z-index:0;
}
.stepper li:first-child::before{left:50%;}
.stepper li:last-child::before{right:50%;}
.stepper li .num{
  position:absolute; top:0; left:50%; transform:translateX(-50%);
  width:14px; height:14px; border-radius:50%; background:var(--panel-3); border:2px solid var(--border);
  font-size:9px; line-height:10px; display:flex; align-items:center; justify-content:center; z-index:1; color:var(--muted-2);
}
.stepper li.done .num{background:var(--ok); border-color:var(--ok); color:#04210f;}
.stepper li.done::before{background:var(--ok);}
.stepper li.active .num{background:var(--http); border-color:var(--http); color:#04121a; box-shadow:0 0 0 4px rgba(69,217,206,.18);}
.stepper li.active{color:var(--text); font-weight:600;}
.stepper li.done{color:var(--muted);}

.log-box{
  height:150px; overflow-y:auto; background:#0c1424; border:1px solid var(--border);
  border-radius:8px; padding:8px 10px; margin-top:8px; font-family:'JetBrains Mono',monospace; font-size:11px;
}
.log-entry{color:var(--muted); margin-bottom:5px; display:flex; gap:8px;}
.log-entry .t{color:var(--muted-2); flex-shrink:0;}
.log-entry.hl{color:var(--text);}
.log-empty{color:var(--muted-2); font-style:italic;}

/* TCP/IP detail mode */
.tcp-mode{
  display:grid;
  grid-template-columns:minmax(0, 1fr) 310px;
  gap:12px;
  margin-bottom:12px;
}
.tcp-actions{
  display:flex;
  gap:8px;
  flex-wrap:wrap;
  margin-bottom:12px;
}
.tcp-actions .btn{padding:8px 10px;}
.tcp-actions .btn:disabled{
  opacity:.45;
  cursor:not-allowed;
  filter:none;
}
.tcp-map{
  position:relative;
  min-height:540px;
  background:linear-gradient(180deg,#081121,#0a1325);
  border:1px solid var(--border);
  border-radius:12px;
  padding:12px;
  overflow:hidden;
}
.tcp-map-grid{
  display:grid;
  grid-template-columns: 1fr 1.2fr 1fr;
  grid-template-rows: 42px repeat(4, 105px);
  gap:8px;
  height:100%;
}
.tcp-head{
  display:flex;
  flex-direction:column;
  justify-content:center;
  align-items:center;
  gap:2px;
  background:#0c1424;
  border:1px solid var(--border);
  border-radius:8px;
  font-size:12px;
  color:var(--muted);
}
.tcp-head b{color:var(--text);font-size:13px;}
.tcp-layer{
  border:1px solid var(--border);
  background:#101a2d;
  border-radius:8px;
  padding:9px 10px;
  display:flex;
  flex-direction:column;
  align-items:center;
  justify-content:center;
  position:relative;
  transition:border-color .18s, box-shadow .18s, background .18s;
}
.tcp-layer.active{
  border-color:var(--http);
  box-shadow:0 0 0 2px rgba(69,217,206,.20) inset, 0 0 14px rgba(69,217,206,.16);
  background:#13243b;
}
.tcp-layer .lname{
  font-family:'Space Grotesk',sans-serif;
  font-size:13px;
  font-weight:700;
  color:var(--text);
  margin-bottom:4px;
}
.tcp-layer .ldata{
  font-family:'JetBrains Mono',monospace;
  font-size:11px;
  color:var(--muted);
  line-height:1.45;
}
.layer-snapshot{
  position:absolute;
  top:50%;
  transform:translateY(-50%);
  width:92px;
  min-height:30px;
  margin:0;
  display:flex;
  gap:4px;
  align-items:flex-end;
  flex-wrap:wrap;
  z-index:2;
  pointer-events:none;
}
[id^="snap-c"]{
  left:10px;
  justify-content:flex-start;
}
[id^="snap-s"]{
  right:10px;
  justify-content:flex-end;
}
.layer-snapshot.return-snapshot{
  opacity:.72;
}
[id^="snapret-c"]{
  left:auto;
  right:10px;
  justify-content:flex-end;
}
[id^="snapret-s"]{
  left:10px;
  right:auto;
  justify-content:flex-start;
}
.snapshot-pkt{
  position:relative;
  min-width:22px;
  min-height:26px;
  border-radius:4px;
  border:1px solid rgba(255,255,255,.25);
  background:
    linear-gradient(90deg, #f58be9 0 5px, transparent 5px),
    repeating-conic-gradient(rgba(255,255,255,.70) 0 25%, rgba(10,15,28,.18) 0 50%) 0 0/8px 8px,
    rgba(255,255,255,.18);
  color:transparent;
  font-family:'JetBrains Mono',monospace;
  font-size:0;
  line-height:0;
  padding:0;
  opacity:.64;
  overflow:hidden;
}
.snapshot-pkt.single{
  min-width:58px;
}
.snapshot-pkt.response{
  background:
    linear-gradient(90deg, #f58be9 0 5px, transparent 5px),
    repeating-conic-gradient(rgba(255,255,255,.70) 0 25%, rgba(10,15,28,.18) 0 50%) 0 0/8px 8px,
    rgba(245,166,35,.20);
}
.snapshot-pkt.tcp{
  background:
    linear-gradient(90deg, #ffd7a3 0 5px, #f58be9 5px 10px, transparent 10px),
    repeating-conic-gradient(rgba(255,255,255,.70) 0 25%, rgba(10,15,28,.18) 0 50%) 0 0/8px 8px,
    rgba(255,255,255,.18);
}
.snapshot-pkt.ip{
  background:
    linear-gradient(90deg, #9ed8ff 0 5px, #ffd7a3 5px 10px, #f58be9 10px 15px, transparent 15px),
    repeating-conic-gradient(rgba(255,255,255,.70) 0 25%, rgba(10,15,28,.18) 0 50%) 0 0/8px 8px,
    rgba(255,255,255,.18);
}
.snapshot-pkt.signal{
  min-width:62px;
  background:
    linear-gradient(90deg, #7f1d1d 0 14%, #17217d 14% 38%, #7f1d1d 38% 52%, #17217d 52% 76%, #7f1d1d 76% 100%);
  border-color:rgba(255,255,255,.20);
}
.snapshot-pkt.signal::after{
  content:'10110010';
  position:absolute;
  inset:0;
  color:rgba(255,255,255,.78);
  font-size:8px;
  line-height:26px;
  letter-spacing:2px;
  text-align:center;
}
.snapshot-pkt.removed{
  background:rgba(139,160,196,.20);
  border-style:dashed;
}
.snapshot-label{
  display:none;
}
.tcp-wire{
  grid-row:2/6;
  grid-column:2;
  border:1px solid var(--border);
  background:rgba(12,20,36,.58);
  border-radius:8px;
  position:relative;
  display:flex;
  align-items:center;
  justify-content:center;
  color:var(--muted);
}
.tcp-wire::before,
.tcp-wire::after{
  content:'';
  position:absolute;
  left:8%;
  right:8%;
  height:2px;
  border-radius:2px;
  opacity:.55;
}
.tcp-wire::before{
  top:38%;
  background:linear-gradient(270deg,#f5a623,#6fb7ff);
}
.tcp-wire::after{
  top:62%;
  background:linear-gradient(90deg,#45d9ce,#6fb7ff);
}
.router-chain{
  display:flex;
  align-items:center;
  gap:12px;
  width:88%;
}
.router{
  flex:0 0 86px;
  background:#111a2b;
  border:1px solid var(--border);
  border-radius:9px;
  padding:10px 8px;
  font-size:12px;
  text-align:center;
}
.router-line{
  flex:1;
  height:2px;
  background:#304365;
  position:relative;
}
.router-line::after{
  content:'';
  position:absolute;
  right:0;
  top:-4px;
  border-left:8px solid #304365;
  border-top:5px solid transparent;
  border-bottom:5px solid transparent;
}
.tcp-packets-layer{
  position:absolute;
  inset:0;
  z-index:5;
  pointer-events:none;
}
.tcp-mini-packet{
  position:absolute;
  left:16%;
  top:18%;
  transform:translate(-50%,-50%);
  width:104px;
  min-height:48px;
  border-radius:9px;
  border:2px solid var(--http);
  background:#45d9ce;
  color:#04121a;
  text-align:center;
  font-family:'JetBrains Mono',monospace;
  font-size:10px;
  font-weight:700;
  padding:4px;
  box-shadow:0 6px 16px rgba(0,0,0,.26);
  opacity:.82;
  transition:width .2s ease, min-height .2s ease, opacity .2s ease;
}
.tcp-mini-packet.single{
  width:128px;
  min-height:44px;
}
.tcp-mini-packet.response{
  background:#f5a623;
  border-color:#f5a623;
}
.tcp-mini-packet.signal{
  width:92px;
  min-height:34px;
  background:#020617;
  border-color:#1f2937;
  color:#e5e7eb;
  padding:3px;
}
.tcp-mini-packet.signal .pkt-ip,
.tcp-mini-packet.signal .pkt-tcp{
  display:none !important;
}
.tcp-mini-packet.signal .pkt-body{
  background:#020617;
  border:0;
  color:rgba(255,255,255,.86);
  font-size:9px;
  letter-spacing:0;
  line-height:1;
  min-height:26px;
  height:100%;
  padding:0;
  overflow:hidden;
  position:relative;
}
.mini-signal-bits{
  display:grid;
  grid-template-columns:repeat(8, 1fr);
  min-height:100%;
}
.mini-signal-bit{
  display:flex;
  align-items:flex-end;
  justify-content:center;
  padding-bottom:2px;
  color:rgba(255,255,255,.86);
}
.mini-signal-bit.one{background:#7f1d1d;}
.mini-signal-bit.zero{background:#17217d;}
.mini-signal-wave{
  position:absolute;
  left:0;
  right:0;
  top:1px;
  width:100%;
  height:15px;
}
.mini-signal-wave path{
  fill:none;
  stroke:#fff;
  stroke-width:2;
  opacity:.92;
}
.pkt-ip,.pkt-tcp,.pkt-body{
  border-radius:5px;
  padding:2px 4px;
  line-height:1.25;
}
.pkt-ip{
  display:none;
  background:#d7ecff;
  border:1px solid rgba(4,18,26,.35);
  margin-bottom:2px;
}
.pkt-tcp{
  display:none;
  background:#dff8e7;
  border:1px solid rgba(4,18,26,.28);
  margin-bottom:2px;
}
.pkt-body{
  background:rgba(255,255,255,.38);
  border:1px solid rgba(4,18,26,.16);
}
.tcp-mini-packet.has-tcp .pkt-tcp,
.tcp-mini-packet.has-ip .pkt-ip{
  display:block;
}
.tcp-mini-packet.ghost{
  opacity:0;
}
.tcp-trail{
  position:absolute;
  border-radius:50%;
  width:8px;
  height:8px;
  background:rgba(69,217,206,.45);
  transform:translate(-50%,-50%);
  z-index:4;
}
.tcp-legend{
  display:grid;
  grid-template-columns: repeat(4, 1fr);
  gap:8px;
  margin-top:10px;
}
.legend-card{
  background:#0c1424;
  border:1px solid var(--border);
  border-radius:8px;
  padding:8px;
  min-height:64px;
}
.legend-card b{
  color:var(--text);
  font-size:12px;
}
.legend-card span{
  display:block;
  color:var(--muted);
  font-size:11px;
  line-height:1.45;
  margin-top:4px;
}
.tcp-summary{
  margin-top:12px;
  background:#0c1424;
  border:1px solid var(--border);
  border-radius:10px;
  padding:10px;
  color:var(--muted);
  font-size:12px;
  line-height:1.7;
}
.tcp-summary b{color:var(--text);}
.data-detail-panel{
  min-height:540px;
  display:flex;
  flex-direction:column;
  gap:10px;
}
.detail-status{
  background:#0c1424;
  border:1px solid var(--border);
  border-radius:8px;
  padding:9px 10px;
  font-size:12px;
  color:var(--muted);
  line-height:1.55;
}
.detail-status b{color:var(--text);}
.data-box-stage{
  flex:1;
  background:linear-gradient(180deg,#9c6a36,#70451f);
  border:1px solid #bd8b4f;
  border-radius:10px;
  padding:14px 12px;
  box-shadow:inset -12px -12px 0 rgba(0,0,0,.18), inset 0 1px 0 rgba(255,255,255,.24);
}
.data-box-title{
  font-family:'Space Grotesk',sans-serif;
  font-weight:700;
  font-size:14px;
  color:#fff5df;
  margin-bottom:10px;
  text-align:center;
}
.proto-box{
  border:2px solid rgba(4,18,26,.32);
  border-radius:6px;
  background:rgba(255,255,255,.88);
  color:#152033;
  padding:9px;
  margin-bottom:9px;
  box-shadow:6px 6px 0 rgba(0,0,0,.16);
}
.proto-box.ip-box{background:#dcefff;}
.proto-box.tcp-box{background:#e7f8ed;}
.proto-box.http-box{background:#fff;}
.proto-head{
  display:flex;
  justify-content:space-between;
  align-items:center;
  gap:8px;
  font-family:'JetBrains Mono',monospace;
  font-size:12px;
  font-weight:700;
  margin-bottom:7px;
}
.proto-row{
  display:flex;
  justify-content:space-between;
  gap:8px;
  border-top:1px solid rgba(4,18,26,.14);
  padding-top:5px;
  margin-top:5px;
  font-family:'JetBrains Mono',monospace;
  font-size:11px;
}
.proto-row span:first-child{color:#526078;}
.proto-row b{color:#111827;}
.payload-lines{
  font-family:'JetBrains Mono',monospace;
  font-size:11px;
  line-height:1.55;
  background:#f4f6f8;
  border:1px solid #d7dde7;
  border-radius:4px;
  padding:7px;
  color:#111827;
  white-space:normal;
}
.tcp-payload-grid{
  display:flex;
  flex-direction:column;
  gap:6px;
  margin-top:8px;
}
.tcp-piece{
  background:#f7fbf8;
  border:1px solid #b9dec3;
  border-left:5px solid #4ade80;
  border-radius:5px;
  padding:6px;
  min-height:48px;
  font-family:'JetBrains Mono',monospace;
  color:#152033;
}
.ip-packet-list{
  display:flex;
  flex-direction:column;
  gap:8px;
}
.ip-packet-item{
  background:#dcefff;
  border:2px solid rgba(4,18,26,.26);
  border-radius:6px;
  padding:7px;
  box-shadow:4px 4px 0 rgba(0,0,0,.12);
}
.ip-packet-item .proto-row{
  font-size:10px;
}
.tcp-piece-head{
  display:flex;
  justify-content:space-between;
  gap:6px;
  font-size:10px;
  font-weight:700;
  margin-bottom:5px;
}
.tcp-piece-body{
  background:#fff;
  border:1px solid #d7dde7;
  border-radius:4px;
  padding:4px;
  font-size:10px;
  line-height:1.35;
}
.signal-list{
  background:#020617;
  border:2px solid #111827;
  border-radius:6px;
  padding:10px;
  display:flex;
  flex-direction:column;
  gap:10px;
}
.signal-row{
  height:40px;
  border-radius:3px;
  overflow:hidden;
  background:#020617;
  color:rgba(255,255,255,.82);
  font-family:'JetBrains Mono',monospace;
  position:relative;
}
.signal-bits{
  position:absolute;
  inset:0;
  display:grid;
  grid-template-columns:repeat(8, 1fr);
}
.signal-bit{
  display:flex;
  align-items:flex-end;
  justify-content:center;
  padding-bottom:3px;
  font-size:15px;
  color:rgba(255,255,255,.82);
}
.signal-bit.one{background:#7f1d1d;}
.signal-bit.zero{background:#17217d;}
.signal-wave{
  position:relative;
  z-index:2;
  width:100%;
  height:20px;
  display:block;
  margin-top:2px;
}
.signal-wave path{
  fill:none;
  stroke:#fff;
  stroke-width:2;
  opacity:.92;
}
.detail-note{
  color:#dbe7ff;
  font-size:11px;
  line-height:1.55;
  margin-top:10px;
}

@media (max-width: 980px){
  .stage{grid-template-columns:1fr;}
  .tcp-mode{grid-template-columns:1fr;}
  .tcp-map{
    min-height:520px;
    overflow-x:auto;
    overflow-y:hidden;
    -webkit-overflow-scrolling:touch;
  }
  .tcp-map-grid{
    min-width:680px;
    grid-template-columns: 1fr 120px 1fr;
    grid-template-rows: 38px repeat(4, 92px);
    gap:6px;
    height:auto;
  }
  .tcp-head{font-size:10px;}
  .tcp-head b{font-size:12px;}
  .tcp-layer{padding:7px 8px;}
  .tcp-layer .lname{font-size:12px;}
  .tcp-layer .ldata{font-size:10px;}
  .tcp-wire{grid-row:2/6; grid-column:2; min-height:0;}
  .router-chain{flex-direction:column; width:auto; height:72%; gap:10px;}
  .router{
    flex:0 0 auto;
    width:82px;
    padding:8px 6px;
    font-size:11px;
  }
  .router-line{
    width:2px;
    height:44px;
    flex:0 0 44px;
  }
  .router-line::after{
    right:auto;
    left:-4px;
    top:auto;
    bottom:0;
    border-left:5px solid transparent;
    border-right:5px solid transparent;
    border-top:8px solid #304365;
    border-bottom:0;
  }
  .layer-snapshot{width:58px;}
  [id^="snap-c"]{left:6px;}
  [id^="snap-s"]{right:6px;}
  [id^="snapret-c"]{right:6px;}
  [id^="snapret-s"]{left:6px;}
  .snapshot-pkt{min-width:18px; min-height:22px;}
  .snapshot-pkt.single{min-width:42px;}
  .tcp-mini-packet{
    width:82px;
    min-height:42px;
    font-size:9px;
  }
  .tcp-mini-packet.single{
    width:98px;
    min-height:40px;
  }
  .tcp-legend{grid-template-columns:1fr 1fr;}
  .browser,.network,.side{grid-row:auto !important;}
  .bottom{grid-template-columns:1fr;}
}

@media (max-width: 560px){
  .wrap{padding:10px 8px 16px;}
  .panel{padding:10px; border-radius:10px;}
  .stage{gap:8px; margin-bottom:8px;}
  .mode-switch{gap:6px;}
  .mode-tab{font-size:12px; padding:8px 9px; flex:1 1 130px;}
  .mode-hint{width:100%; line-height:1.45;}
  .addr-row{flex-direction:column;}
  .addr-row input{font-size:12px;}
  .addr-row .btn{width:100%; min-height:40px;}
  .hint-text{font-size:10px; line-height:1.45;}
  .controls-row{
    display:grid;
    grid-template-columns:auto 1fr 1fr;
    gap:6px;
  }
  .controls-row select{min-width:0; width:100%; font-size:11px;}
  .controls-row .btn,
  .tcp-actions .btn{
    flex:1 1 120px;
    min-height:38px;
    margin-left:0 !important;
  }
  .resolved-ip{font-size:10px; overflow-wrap:anywhere;}
  .browser-window{min-height:220px;}
  .browser-body{padding:11px;}
  .browser-body .empty-msg{margin-top:42px; font-size:11px; line-height:1.6;}
  .page-h1{font-size:18px;}
  .browser-body.styled .page-h1{font-size:17px; padding:13px 14px;}
  .page-p{font-size:12px;}
  .browser-body.styled .page-p{padding:0 14px;}
  .browser-body.styled .page-list{
    flex-wrap:wrap;
    gap:8px;
    padding:9px 14px;
  }
  .hero-img{height:72px; margin:10px 14px;}
  .img-caption{padding:0 14px 12px;}
  .progress-group{gap:6px;}
  .prow{gap:6px;}
  .prow .plabel{width:34px; font-size:10px;}
  .ppct{width:30px; font-size:10px;}
  .network{
    min-height:300px;
    padding:8px 4px 4px;
  }
  .network svg{min-height:280px;}
  .tcp-note{top:8px; right:8px;}
  .tcp-note .note-body{
    width:min(230px, calc(100vw - 54px));
    font-size:10px;
  }
  .detail-box{
    left:8px;
    right:8px;
    bottom:8px;
    font-size:10px;
  }
  .side{
    min-height:0;
  }
  .server-box{padding:7px 8px;}
  .server-label{
    flex-wrap:wrap;
    line-height:1.35;
  }
  .table-row{
    gap:8px;
    overflow-wrap:anywhere;
  }
  .file-list li{font-size:10px;}
  .stepper{flex-wrap:wrap; row-gap:8px;}
  .stepper li{flex:1 1 33%; font-size:9.5px;}
  .stepper li::before{display:none;}
  .log-box{height:120px;}
  .tcp-map{
    min-height:500px;
    padding:8px;
  }
  .tcp-map-grid{
    min-width:620px;
    grid-template-columns: 1fr 104px 1fr;
    grid-template-rows: 34px repeat(4, 88px);
  }
  .tcp-actions{gap:6px;}
  .tcp-legend{grid-template-columns:1fr;}
  .data-detail-panel{min-height:auto;}
  .data-box-stage{max-height:420px; overflow:auto;}
  .proto-head{font-size:11px;}
  .proto-row{font-size:10px;}
}
</style>
</head>
<body>
<div class="wrap">
  <div class="mode-switch">
    <button class="mode-tab active" id="webModeBtn">Web表示モード</button>
    <button class="mode-tab" id="tcpModeBtn">TCP/IP詳細モード</button>
    <span class="mode-hint" id="modeHint">まずはURL入力からWebページ表示までの流れを見ます。</span>
  </div>

  <div id="webMode">
  <div class="stage">
    <!-- BROWSER -->
    <div class="panel browser">
      <div class="panel-title"><span class="dot dot-browser"></span>ブラウザ（クライアント）192.168.1.10</div>
      <div class="addr-row">
        <input id="urlInput" type="text" value="https://www.school.jp" class="mono" />
        <button class="btn btn-go" id="goBtn">アクセス</button>
      </div>
      <div class="hint-text">本校のWebサイト www.school.jp へのアクセスをシミュレートします</div>
      <div class="controls-row">
        <span style="font-size:11px;color:var(--muted);">速度</span>
        <select id="speedSel">
          <option value="0.5">低速 (0.5x)</option>
          <option value="1" selected>標準 (1x)</option>
          <option value="2">高速 (2x)</option>
          <option value="4">最高速 (4x)</option>
        </select>
        <button class="btn btn-ghost" id="pauseBtn">⏸ 一時停止</button>
        <button class="btn btn-reset" id="resetBtn" style="margin-left:auto;">リセット</button>
      </div>
      <div class="resolved-ip" id="resolvedIp">名前解決: <span class="mono">まだ通信していません</span></div>
      <div class="browser-window">
        <div class="browser-chrome">
          <span class="dotc bc1"></span><span class="dotc bc2"></span><span class="dotc bc3"></span>
        </div>
        <div class="browser-body" id="pageBody">
          <div class="empty-msg">「アクセス」を押すと、ここにWebページが少しずつ表示されます</div>
        </div>
      </div>
      <div class="progress-group">
        <div class="prow"><span class="plabel">HTML</span><div class="pbar"><div class="pfill html" id="pf-html"></div></div><span class="ppct" id="pp-html">0%</span></div>
        <div class="prow"><span class="plabel">CSS</span><div class="pbar"><div class="pfill css" id="pf-css"></div></div><span class="ppct" id="pp-css">0%</span></div>
        <div class="prow"><span class="plabel">IMG</span><div class="pbar"><div class="pfill img" id="pf-img"></div></div><span class="ppct" id="pp-img">0%</span></div>
      </div>
    </div>

    <!-- NETWORK -->
    <div class="panel network">
      <div class="panel-title"><span class="dot dot-net"></span>インターネット（ルータ経由）</div>
      <div class="tcp-note">
        <details>
          <summary>ℹ️</summary>
          <div class="note-body">
            実際の通信では <b style="color:#e7edf7">TCP</b> によってデータが分割・確認されながら確実に届けられています。<br><br>
            <b style="color:#e7edf7">HTTPS</b> では <b style="color:#e7edf7">TLS</b> により通信内容が暗号化され、盗聴や改ざんから守られています。
          </div>
        </details>
      </div>
      <svg id="netSvg" viewBox="0 0 640 500" preserveAspectRatio="xMidYMid meet">
        <ellipse cx="270" cy="250" rx="230" ry="150" fill="#16223a" opacity="0.35"></ellipse>
        <text x="270" y="90" class="cloud-label" text-anchor="middle">I N T E R N E T</text>

        <path id="pathDns" class="route-line" d="M10,250 L150,250 L400,250 L620,80"></path>
        <path id="pathWeb" class="route-line" d="M10,250 L150,250 L400,250 L620,420"></path>

        <g class="node-box">
          <rect x="120" y="228" width="60" height="44" rx="8"></rect>
          <text x="150" y="253" class="node-label">🔀</text>
          <text x="150" y="288" class="node-label">ルータ1</text>
        </g>
        <g class="node-box">
          <rect x="370" y="228" width="60" height="44" rx="8"></rect>
          <text x="400" y="253" class="node-label">🔀</text>
          <text x="400" y="288" class="node-label">ルータ2</text>
        </g>

        <circle id="pulseDns" class="node-pulse" cx="620" cy="80" r="26" fill="var(--dns)"></circle>
        <circle id="pulseWeb" class="node-pulse" cx="620" cy="420" r="26" fill="var(--warn)"></circle>

        <g id="packets-layer"></g>
      </svg>
      <div class="detail-box" id="detailBox">
        <span class="dclose" id="detailClose">✕</span>
        <div class="drow">種別: <b id="dType">-</b></div>
        <div class="drow">送信元IP: <b id="dSrc">-</b></div>
        <div class="drow">送信先IP: <b id="dDst">-</b></div>
      </div>
    </div>

    <!-- DNS + WEB stacked -->
    <div class="panel side" style="grid-row:1;">
      <div class="panel-title"><span class="dot dot-dns"></span>DNSサーバ</div>
      <div class="server-box" id="dnsServerBox">
        <span class="screw tl"></span><span class="screw tr"></span><span class="screw bl"></span><span class="screw br"></span>
        <div class="server-rack">
          <div class="server-unit"><span class="led led-green blink"></span><span class="vents"></span><span class="tag">PWR</span></div>
          <div class="server-unit"><span class="led led-amber" id="dnsLed"></span><span class="vents"></span><span class="tag">QUERY</span></div>
          <div class="server-unit"><span class="led led-green blink"></span><span class="vents"></span><span class="tag">ZONE</span></div>
        </div>
      </div>
      <div class="server-label"><span class="rack-icon">🗄️</span>dns.school.jp <span class="ip">203.0.113.53</span></div>
      <div class="status-line" id="dnsStatus">待機中...</div>
      <div class="table-row"><span>ドメイン</span><b>IPアドレス</b></div>
      <div class="table-row"><span>www.school.jp</span><b>192.0.2.10</b></div>
    </div>
    <div class="panel side" style="grid-row:2;">
      <div class="panel-title"><span class="dot dot-web">&nbsp;</span>Webサーバ</div>
      <div class="server-box" id="webServerBox">
        <span class="screw tl"></span><span class="screw tr"></span><span class="screw bl"></span><span class="screw br"></span>
        <div class="server-rack">
          <div class="server-unit"><span class="led led-green blink"></span><span class="vents"></span><span class="tag">PWR</span></div>
          <div class="server-unit"><span class="led led-amber" id="webLed"></span><span class="vents"></span><span class="tag">HTTP</span></div>
          <div class="server-unit"><span class="led led-green blink"></span><span class="vents"></span><span class="tag">DISK</span></div>
        </div>
      </div>
      <div class="server-label"><span class="rack-icon">🖥️</span>www.school.jp <span class="ip" id="webIpLabel">192.0.2.10</span></div>
      <div class="status-line" id="webStatus">待機中...</div>
      <ul class="file-list" id="fileList">
        <li id="file-html">📄 index.html</li>
        <li id="file-css">🎨 style.css</li>
        <li id="file-img">🖼 photo.jpg</li>
      </ul>
    </div>
  </div>

  <!-- BOTTOM: stepper + log -->
  <div class="bottom">
    <div class="panel">
      <div class="panel-title">処理の流れ</div>
      <ul class="stepper" id="stepper">
        <li class="pending" data-i="1"><span class="num">1</span>URL入力</li>
        <li class="pending" data-i="2"><span class="num">2</span>DNS問い合わせ</li>
        <li class="pending" data-i="3"><span class="num">3</span>HTTPリクエスト</li>
        <li class="pending" data-i="4"><span class="num">4</span>データ受信</li>
        <li class="pending" data-i="5"><span class="num">5</span>Webページ表示</li>
      </ul>
    </div>
    <div class="panel">
      <div class="panel-title">通信ログ</div>
      <div class="log-box" id="logBox"><div class="log-empty">まだ通信は行われていません。</div></div>
    </div>
  </div>
  </div>

  <div id="tcpMode" class="tcp-mode hidden">
    <div class="panel">
      <div class="panel-title"><span class="dot dot-net"></span>通信の中身</div>
      <div class="tcp-actions">
        <button class="btn btn-go" id="tcpPlayBtn">4層の流れを見る</button>
        <button class="btn btn-ghost" id="tcpPauseBtn">⏸ 一時停止</button>
        <button class="btn btn-reset" id="tcpResetBtn">最初から見る</button>
        <button class="btn btn-ghost" id="backToWebBtn">Web表示に戻る</button>
      </div>
      <div class="tcp-map" id="tcpMap">
        <div class="tcp-map-grid">
          <div class="tcp-head"><b>送信側PC</b><span class="mono">192.168.1.10</span></div>
          <div class="tcp-head"><b>ネットワーク</b><span>ルータを通って移動</span></div>
          <div class="tcp-head"><b id="tcpServerName">www.school.jp</b><span class="mono" id="tcpServerIp">192.0.2.10</span></div>

          <div class="tcp-layer" id="cApp"><div class="lname">アプリケーション層</div><div class="ldata">HTTP: <span id="tcpReqLabel">GET /index.html</span></div><div class="layer-snapshot" id="snap-cApp"></div></div>
          <div class="tcp-wire" id="tcpWire" rowspan="4">
            <div class="router-chain">
              <div class="router">ルータ1<br><span class="mono">中継</span></div>
              <div class="router-line"></div>
              <div class="router">ルータ2<br><span class="mono">中継</span></div>
            </div>
          </div>
          <div class="tcp-layer" id="sApp"><div class="lname">アプリケーション層</div><div class="ldata">HTTPデータを読み取る</div><div class="layer-snapshot" id="snap-sApp"></div></div>

          <div class="tcp-layer" id="cTrans"><div class="lname">トランスポート層</div><div class="ldata">TCP: 1/4, 2/4, 3/4, 4/4</div><div class="layer-snapshot" id="snap-cTrans"></div></div>
          <div class="tcp-layer" id="sTrans"><div class="lname">トランスポート層</div><div class="ldata">TCP番号で順番を確認</div><div class="layer-snapshot" id="snap-sTrans"></div></div>

          <div class="tcp-layer" id="cInet"><div class="lname">インターネット層</div><div class="ldata">IP: 192.168.1.10 → <span id="tcpDstInline">192.0.2.10</span></div><div class="layer-snapshot" id="snap-cInet"></div></div>
          <div class="tcp-layer" id="sInet"><div class="lname">インターネット層</div><div class="ldata">宛先IPが自分か確認</div><div class="layer-snapshot" id="snap-sInet"></div></div>

          <div class="tcp-layer" id="cNet"><div class="lname">ネットワーク<br>インタフェース層</div><div class="ldata">0と1の信号として送り出す</div><div class="layer-snapshot" id="snap-cNet"></div></div>
          <div class="tcp-layer" id="sNet"><div class="lname">ネットワーク<br>インタフェース層</div><div class="ldata">届いた信号を受け取る</div><div class="layer-snapshot" id="snap-sNet"></div></div>
        </div>
        <div class="tcp-packets-layer hidden" id="tcpPacketsLayer">
          <div class="tcp-mini-packet" id="tcpPkt1"><div class="pkt-ip"></div><div class="pkt-tcp"></div><div class="pkt-body"></div></div>
          <div class="tcp-mini-packet" id="tcpPkt2"><div class="pkt-ip"></div><div class="pkt-tcp"></div><div class="pkt-body"></div></div>
          <div class="tcp-mini-packet" id="tcpPkt3"><div class="pkt-ip"></div><div class="pkt-tcp"></div><div class="pkt-body"></div></div>
          <div class="tcp-mini-packet" id="tcpPkt4"><div class="pkt-ip"></div><div class="pkt-tcp"></div><div class="pkt-body"></div></div>
        </div>
      </div>
      <div class="tcp-legend">
        <div class="legend-card"><b>HTTP</b><span>Webページの要求や応答の中身を決める。</span></div>
        <div class="legend-card"><b>TCP</b><span>データを分け、番号で順番を管理する。</span></div>
        <div class="legend-card"><b>IP</b><span>DNSで分かったIPアドレスを使って届ける。</span></div>
        <div class="legend-card"><b>ネットワークI/F</b><span>実際の回線へ流せる信号にする。</span></div>
      </div>
      <div class="tcp-summary" id="tcpExplanation"></div>
    </div>
    <div class="panel data-detail-panel">
      <div class="panel-title"><span class="dot dot-web"></span>流れたデータ</div>
      <div class="detail-status" id="dataDetailStatus">
        <b>待機中</b><br>
        「4層の流れを見る」を押すと、現在流れているデータの中身がここに表示されます。
      </div>
      <div class="data-box-stage">
        <div class="data-box-title">データの中身</div>
        <div id="dataDetailBox">
          <div class="proto-box http-box">
            <div class="proto-head"><span>HTTP</span><span>待機中</span></div>
            <div class="payload-lines">GET /index.html</div>
          </div>
        </div>
        <div class="detail-note" id="dataDetailNote">
          層を通るたびに、外側へTCPやIPの情報が追加されます。受信側では外側から順に確認して取り外します。
        </div>
      </div>
    </div>
  </div>

</div>

<script>
(function(){
  var SPEED = 1;
  var PAUSED = false;
  var runId = 0;

  var LEFT = {x:10,y:250}, R1 = {x:150,y:250}, R2 = {x:400,y:250};
  var DNS_ENTRY = {x:620,y:80}, WEB_ENTRY = {x:620,y:420};
  var PATH_TO_DNS = [LEFT,R1,R2,DNS_ENTRY];
  var PATH_FROM_DNS = [DNS_ENTRY,R2,R1,LEFT];
  var PATH_TO_WEB = [LEFT,R1,R2,WEB_ENTRY];
  var PATH_FROM_WEB = [WEB_ENTRY,R2,R1,LEFT];

  var BROWSER_IP = "192.168.1.10";
  var DNS_IP = "203.0.113.53";
  var LAST_INFO = {domain:"www.school.jp", path:"/index.html", protocol:"https"};
  var LAST_IP = "192.0.2.10";
  var tcpAnimRun = 0;
  var tcpRunning = false;
  var DNS_TABLE = {
    "www.school.jp": "192.0.2.10"
  };

  function $(id){ return document.getElementById(id); }

  function wait(ms){
    return new Promise(function(resolve){
      var remaining = ms;
      var iv = setInterval(function(){
        if(!PAUSED){
          remaining -= 40*SPEED;
          if(remaining<=0){ clearInterval(iv); resolve(); }
        }
      },40);
    });
  }

  function pointAtProgress(wps, t){
    if(t<=0) return {x:wps[0].x,y:wps[0].y};
    if(t>=1) return {x:wps[wps.length-1].x,y:wps[wps.length-1].y};
    var segLens=[], total=0, i;
    for(i=0;i<wps.length-1;i++){
      var dx=wps[i+1].x-wps[i].x, dy=wps[i+1].y-wps[i].y;
      var len=Math.sqrt(dx*dx+dy*dy);
      segLens.push(len); total+=len;
    }
    var target = t*total;
    for(i=0;i<segLens.length;i++){
      if(target<=segLens[i] || i===segLens.length-1){
        var ratio = segLens[i]===0?0:Math.min(target/segLens[i],1);
        return {
          x: wps[i].x + (wps[i+1].x-wps[i].x)*ratio,
          y: wps[i].y + (wps[i+1].y-wps[i].y)*ratio
        };
      }
      target -= segLens[i];
    }
    return {x:wps[wps.length-1].x,y:wps[wps.length-1].y};
  }

  function animatePacket(el, waypoints, duration){
    return new Promise(function(resolve){
      var elapsed = 0, last = null;
      function frame(ts){
        if(last===null) last = ts;
        var dt = ts-last; last = ts;
        if(!PAUSED){ elapsed += dt*SPEED; }
        var t = Math.min(elapsed/duration, 1);
        var pt = pointAtProgress(waypoints, t);
        if(el.isConnected){ el.setAttribute('transform','translate('+pt.x+','+pt.y+')'); }
        if(t<1 && el.isConnected){
          requestAnimationFrame(frame);
        } else {
          resolve();
        }
      }
      requestAnimationFrame(frame);
    });
  }

  function spawnPacket(opts){
    var svgNS = 'http://www.w3.org/2000/svg';
    var g = document.createElementNS(svgNS,'g');
    g.setAttribute('class','packet '+opts.className);
    g.setAttribute('transform','translate('+opts.path[0].x+','+opts.path[0].y+')');
    var rect = document.createElementNS(svgNS,'rect');
    rect.setAttribute('x','-25'); rect.setAttribute('y','-11');
    rect.setAttribute('width','50'); rect.setAttribute('height','22'); rect.setAttribute('rx','6');
    var text = document.createElementNS(svgNS,'text');
    text.setAttribute('x','0'); text.setAttribute('y','4');
    text.textContent = opts.label;
    var hit = document.createElementNS(svgNS,'circle');
    hit.setAttribute('cx','0'); hit.setAttribute('cy','0'); hit.setAttribute('r','22'); hit.setAttribute('fill','transparent');
    g.appendChild(rect); g.appendChild(text); g.appendChild(hit);
    g.addEventListener('click', function(e){
      e.stopPropagation();
      showPacketDetail(opts.meta);
    });
    $('packets-layer').appendChild(g);
    return animatePacket(g, opts.path, opts.duration).then(function(){
      g.classList.add('arrived');
      setTimeout(function(){ if(g.isConnected){ g.remove(); } }, 400);
    });
  }

  function showPacketDetail(meta){
    $('dType').textContent = meta.type;
    $('dSrc').textContent = meta.src;
    $('dDst').textContent = meta.dst;
    $('detailBox').classList.add('show');
  }
  $('detailClose').addEventListener('click', function(){ $('detailBox').classList.remove('show'); });

  function nowStr(){
    var d = new Date();
    function p(n){ return (n<10?'0':'')+n; }
    return p(d.getHours())+':'+p(d.getMinutes())+':'+p(d.getSeconds());
  }

  function addLog(msg, hl){
    var box = $('logBox');
    if(box.querySelector('.log-empty')){ box.innerHTML=''; }
    var row = document.createElement('div');
    row.className = 'log-entry' + (hl ? ' hl' : '');
    row.innerHTML = '<span class="t">'+nowStr()+'</span><span>'+msg+'</span>';
    box.appendChild(row);
    box.scrollTop = box.scrollHeight;
  }

  function setStage(n){
    var items = document.querySelectorAll('#stepper li');
    items.forEach(function(li){
      var i = parseInt(li.getAttribute('data-i'),10);
      li.classList.remove('done','active','pending');
      if(i<n) li.classList.add('done');
      else if(i===n) li.classList.add('active');
      else li.classList.add('pending');
    });
  }

  function updateProgress(type, pct){
    $('pf-'+type).style.width = pct+'%';
    $('pp-'+type).textContent = pct+'%';
  }

  function updatePauseButtons(){
    $('pauseBtn').textContent = PAUSED ? '▶ 再開' : '⏸ 一時停止';
    $('tcpPauseBtn').textContent = PAUSED ? '▶ 再開' : '⏸ 一時停止';
  }

  function togglePause(){
    PAUSED = !PAUSED;
    updatePauseButtons();
  }

  function setMode(mode){
    var web = mode === 'web';
    $('webMode').classList.toggle('hidden', !web);
    $('tcpMode').classList.toggle('hidden', web);
    $('webModeBtn').classList.toggle('active', web);
    $('tcpModeBtn').classList.toggle('active', !web);
    $('modeHint').textContent = web
      ? 'まずはURL入力からWebページ表示までの流れを見ます。'
      : 'データが4層を下がって送られ、相手側で4層を上がって取り出される流れを見ます。';
    if(!web){ resetTcpFlow(); }
  }

  function updateTcpLabels(){
    $('tcpServerName').textContent = LAST_INFO.domain;
    $('tcpServerIp').textContent = LAST_IP;
    $('tcpDstInline').textContent = LAST_IP;
    $('tcpReqLabel').textContent = 'GET ' + LAST_INFO.path;
  }

  function clearTcpLayerHighlights(){
    document.querySelectorAll('.tcp-layer').forEach(function(el){
      el.classList.remove('active');
    });
  }

  function centerInMap(el){
    var mapRect = $('tcpMap').getBoundingClientRect();
    var r = el.getBoundingClientRect();
    return {
      x: r.left - mapRect.left + r.width/2,
      y: r.top - mapRect.top + r.height/2
    };
  }

  function pointBetween(a, b, ratio){
    return {x: a.x + (b.x-a.x)*ratio, y: a.y + (b.y-a.y)*ratio};
  }

  function tcpPoints(){
    var cNet = centerInMap($('cNet'));
    var sNet = centerInMap($('sNet'));
    var cInet = centerInMap($('cInet'));
    var sInet = centerInMap($('sInet'));
    var forwardY = cNet.y - 26;
    var backY = cInet.y + 26;
    var leftEdge = {x: pointBetween(cNet, sNet, .33).x, y: cNet.y};
    var rightEdge = {x: pointBetween(cNet, sNet, .67).x, y: sNet.y};
    return {
      cApp: centerInMap($('cApp')),
      cTrans: centerInMap($('cTrans')),
      cInet: cInet,
      cNet: cNet,
      r1: {x:leftEdge.x, y:forwardY},
      r2: {x:rightEdge.x, y:forwardY},
      rb1: {x:leftEdge.x, y:backY},
      rb2: {x:rightEdge.x, y:backY},
      sNet: sNet,
      sInet: sInet,
      sTrans: centerInMap($('sTrans')),
      sApp: centerInMap($('sApp'))
    };
  }

  function tcpPacketEls(){
    return [1,2,3,4].map(function(n){ return $('tcpPkt'+n); });
  }

  function tcpPacketOffset(i, clustered){
    if(clustered){ return {x:(i-1.5)*4, y:(i-1.5)*3}; }
    return {x:0, y:(i-1.5)*34};
  }

  function placeTcpPackets(pt, clustered){
    tcpPacketEls().forEach(function(el, i){
      var off = tcpPacketOffset(i, clustered);
      el.style.left = (pt.x + off.x) + 'px';
      el.style.top = (pt.y + off.y) + 'px';
    });
  }

  function configureTcpPackets(step){
    var pieces = ['GET', '/index', '.html', '完了'];
    var signalPieces = ['11100011','10000011','10010111','10101101'];
    var single = step.form === 'single';
    tcpPacketEls().forEach(function(el, i){
      el.classList.toggle('single', single);
      el.classList.toggle('ghost', single && i > 0);
      el.classList.toggle('has-tcp', !!step.tcp);
      el.classList.toggle('has-ip', !!step.ip);
      el.classList.toggle('response', !!step.response);
      el.classList.toggle('signal', !!step.signal);
      el.querySelector('.pkt-ip').textContent = step.response ? 'IP → '+BROWSER_IP : 'IP → '+LAST_IP;
      el.querySelector('.pkt-tcp').textContent = 'TCP '+(i+1)+'/4';
      el.querySelector('.pkt-body').innerHTML = single && i === 0
        ? step.label
        : (step.signal ? miniSignalHtml(signalPieces[i]) : (step.response ? 'HTML '+(i+1)+'/4' : pieces[i]+' '+(i+1)+'/4'));
    });
  }

  function clearSnapshots(){
    document.querySelectorAll('.layer-snapshot').forEach(function(el){
      el.innerHTML = '';
    });
  }

  function ensureReturnSnapshot(layerId){
    var id = 'snapret-' + layerId;
    var el = $(id);
    if(el) return el;
    var layer = $(layerId);
    if(!layer) return null;
    el = document.createElement('div');
    el.id = id;
    el.className = 'layer-snapshot return-snapshot';
    layer.appendChild(el);
    return el;
  }

  function snapshotPieces(kind, response){
    var prefix = response ? 'HTML' : 'HTTP';
    if(kind === 'single'){
      return '<div class="snapshot-pkt single '+(response?'response':'')+'">'+prefix+'データ</div>';
    }
    var cls = 'snapshot-pkt ' + kind + (response ? ' response' : '');
    return '<div class="'+cls+'"></div>';
  }

  function writeSnapshot(layerId, title, kind, response){
    if(!layerId) return;
    var el = response ? ensureReturnSnapshot(layerId) : $('snap-'+layerId);
    if(!el) return;
    el.innerHTML = '<div class="snapshot-label">'+title+'</div>' + snapshotPieces(kind, response);
  }

  function escapeHtml(s){
    return String(s).replace(/[&<>"']/g, function(c){
      return {'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c];
    });
  }

  function miniSignalHtml(bits){
    var html = '<div class="mini-signal-bits">';
    for(var i=0; i<bits.length; i++){
      var bit = bits.charAt(i);
      html += '<div class="mini-signal-bit '+(bit === '1' ? 'one' : 'zero')+'">'+bit+'</div>';
    }
    html += '</div>' +
      '<svg class="mini-signal-wave" viewBox="0 0 160 20" preserveAspectRatio="none" aria-hidden="true">' +
        '<path d="M0 10 C4 2 8 2 12 10 S20 18 24 10 S32 2 36 10 S44 18 48 10 S56 2 60 10 S68 18 72 10 S80 2 84 10 S92 18 96 10 S104 2 108 10 S116 18 120 10 S128 2 132 10 S140 18 144 10 S156 18 160 10" />' +
      '</svg>';
    return html;
  }

  function signalRowHtml(bits){
    var html = '<div class="signal-row">' +
      '<div class="signal-bits">';
    for(var i=0; i<bits.length; i++){
      var bit = bits.charAt(i);
      html += '<div class="signal-bit '+(bit === '1' ? 'one' : 'zero')+'">'+bit+'</div>';
    }
    html += '</div>' +
      '<svg class="signal-wave" viewBox="0 0 240 24" preserveAspectRatio="none" aria-hidden="true">' +
        '<path d="M0 12 C5 2 10 2 15 12 S25 22 30 12 S40 2 45 12 S55 22 60 12 S70 2 75 12 S85 22 90 12 S100 2 105 12 S115 22 120 12 S130 2 135 12 S145 22 150 12 S160 2 165 12 S175 22 180 12 S190 2 195 12 S205 22 210 12 S220 2 225 12 S235 22 240 12" />' +
      '</svg>' +
    '</div>';
    return html;
  }

  function currentDataKind(step){
    if(step.detailKind) return step.detailKind;
    if(step.snapKind) return step.snapKind;
    if(step.ip) return 'ip';
    if(step.tcp) return 'tcp';
    return 'single';
  }

  function detailDirection(step){
    return step.response
      ? {src: LAST_IP, dst: BROWSER_IP, body:'HTML応答', app:'HTTP/1.1 200 OK'}
      : {src: BROWSER_IP, dst: LAST_IP, body:'GET '+LAST_INFO.path, app:'GET '+LAST_INFO.path};
  }

  function updateDataDetail(step){
    var kind = currentDataKind(step);
    var dir = detailDirection(step);
    var phase = step.detailTitle || step.snapshot || '通信中';
    var body = escapeHtml(dir.body);
    var app = escapeHtml(dir.app);
    var directionLabel = step.response ? 'Webサーバ → ブラウザ' : 'ブラウザ → Webサーバ';
    $('dataDetailStatus').innerHTML =
      '<b>'+escapeHtml(phase)+'</b><br>' +
      escapeHtml(directionLabel) + '<br>' +
      '<span class="mono">'+escapeHtml(dir.src)+' → '+escapeHtml(dir.dst)+'</span>';

    var httpBox =
      '<div class="proto-box http-box">' +
        '<div class="proto-head"><span>HTTP</span><span>中身</span></div>' +
        '<div class="payload-lines">'+app+'<br>'+body+'</div>' +
      '</div>';
    var parts = step.response
      ? ['HTML 1', 'HTML 2', 'HTML 3', 'HTML 4']
      : ['GET', '/index', '.html', '完了'];
    var tcpPieces = '<div class="tcp-payload-grid">';
    for(var pi=0; pi<4; pi++){
      tcpPieces +=
        '<div class="tcp-piece">' +
          '<div class="tcp-piece-head"><span>TCP</span><span>'+(pi+1)+'/4</span></div>' +
          '<div class="tcp-piece-body">'+escapeHtml(parts[pi])+'</div>' +
        '</div>';
    }
    tcpPieces += '</div>';
    var ipPackets = '<div class="ip-packet-list">';
    for(var ii=0; ii<4; ii++){
      ipPackets +=
        '<div class="ip-packet-item">' +
          '<div class="proto-head"><span>IPv4</span><span>パケット '+(ii+1)+'/4</span></div>' +
          '<div class="proto-row"><span>送信元IP</span><b>'+escapeHtml(dir.src)+'</b></div>' +
          '<div class="proto-row"><span>宛先IP</span><b>'+escapeHtml(dir.dst)+'</b></div>' +
          '<div class="tcp-piece">' +
            '<div class="tcp-piece-head"><span>TCP</span><span>'+(ii+1)+'/4</span></div>' +
            '<div class="tcp-piece-body">'+escapeHtml(parts[ii])+'</div>' +
          '</div>' +
        '</div>';
    }
    ipPackets += '</div>';
    var tcpBox =
      '<div class="proto-box tcp-box">' +
        '<div class="proto-head"><span>TCP</span><span>4分割</span></div>' +
        '<div class="proto-row"><span>パケット番号</span><b>1/4〜4/4</b></div>' +
        '<div class="proto-row"><span>役割</span><b>順番を管理</b></div>' +
        tcpPieces +
      '</div>';
    var ipBox =
      '<div class="proto-box ip-box">' +
        '<div class="proto-head"><span>IPv4</span><span>それぞれに宛先つき</span></div>' +
        ipPackets +
      '</div>';
    var signalRows = ['11100011', '10000011', '10010111', '11100011', '10000011', '10101101', '11100011', '10010000'];
    var signalBox = '<div class="signal-list">';
    for(var si=0; si<signalRows.length; si++){
      signalBox += signalRowHtml(signalRows[si]);
    }
    signalBox += '</div>';

    if(kind === 'signal'){
      $('dataDetailBox').innerHTML = signalBox;
      $('dataDetailNote').textContent = 'ネットワークインタフェース層では、データを実際に流せる0と1の信号として扱います。';
    } else if(kind === 'ip'){
      $('dataDetailBox').innerHTML = ipBox;
      $('dataDetailNote').textContent = '外側のIP箱に宛先IPアドレスが入っています。ルータは主にこの宛先IPを見て中継します。';
    } else if(kind === 'tcp'){
      $('dataDetailBox').innerHTML = tcpBox;
      $('dataDetailNote').textContent = 'IPの情報は確認済みです。TCPの番号を使って、分かれたデータを正しい順番に扱います。';
    } else {
      $('dataDetailBox').innerHTML = httpBox;
      $('dataDetailNote').textContent = 'まだTCPやIPの外側の箱はありません。Web通信の中身であるHTTPデータだけが見えています。';
    }
  }

  function animateTcpPackets(from, to, duration, myRun, clustered){
    return new Promise(function(resolve){
      var finished = 0;
      tcpPacketEls().forEach(function(el, idx){
        var elapsed = 0, last = null;
        var delay = clustered ? 0 : idx * 150;
        function frame(ts){
          if(myRun !== tcpAnimRun){ resolve(); return; }
          if(last===null) last = ts;
          var dt = ts-last; last = ts;
          if(!PAUSED){ elapsed += dt*SPEED; }
          var t = Math.max(0, Math.min((elapsed-delay)/duration, 1));
          var ease = t < .5 ? 2*t*t : -1 + (4 - 2*t)*t;
          var base = pointBetween(from, to, ease);
          var off = tcpPacketOffset(idx, clustered);
          el.style.left = (base.x + off.x) + 'px';
          el.style.top = (base.y + off.y) + 'px';
          if(t<1){ requestAnimationFrame(frame); }
          else {
            finished++;
            if(finished === 4){ resolve(); }
          }
        }
        requestAnimationFrame(frame);
      });
    });
  }

  async function visitTcpPoint(step, myRun){
    if(myRun !== tcpAnimRun) return false;
    clearTcpLayerHighlights();
    if(step.layer){ $(step.layer).classList.add('active'); }
    configureTcpPackets(step);
    if(step.snapshot){ writeSnapshot(step.layer, step.snapshot, step.snapKind || 'single', !!step.response); }
    updateDataDetail(step);
    $('tcpExplanation').innerHTML = step.explain;
    await wait(step.pause || 360);
    return myRun === tcpAnimRun;
  }

  async function runTcpFlow(){
    if(tcpRunning) return;
    tcpRunning = true;
    var myRun = ++tcpAnimRun;
    updateTcpLabels();
    clearTcpLayerHighlights();
    $('tcpPlayBtn').disabled = true;
    $('tcpPlayBtn').textContent = '流れを表示中...';
    $('tcpPacketsLayer').classList.remove('hidden');
    var p = tcpPoints();
    var requestPath = [
      {key:'cApp', layer:'cApp', form:'single', label:'HTTP<br>GET '+LAST_INFO.path, snapshot:'HTTPデータを作成', snapKind:'single', explain:'<b>アプリケーション層</b>で、HTTPの「'+LAST_INFO.path+' がほしい」という1つのデータを作ります。'},
      {key:'cTrans', layer:'cTrans', tcp:true, label:'TCP', snapshot:'TCPを追加・4分割', snapKind:'tcp', explain:'<b>トランスポート層</b>で、1つのデータを4つに分け、TCP 1/4〜4/4の番号を付けます。'},
      {key:'cInet', layer:'cInet', tcp:true, ip:true, label:'IP', snapshot:'IPを外側に追加', snapKind:'ip', explain:'<b>インターネット層</b>で、それぞれの外側に宛先IPアドレスを付けます。'},
      {key:'cNet', layer:'cNet', tcp:true, ip:true, signal:true, label:'0/1', snapshot:'回線へ送信', snapKind:'signal', detailKind:'signal', explain:'<b>ネットワークインタフェース層</b>で、4つのパケットを0と1の信号として実際の回線へ送り出します。'},
      {key:'r1', tcp:true, ip:true, signal:true, detailKind:'signal', label:'0/1', explain:'ネットワークを通っている間も、データは0と1の信号として流れます。'},
      {key:'r2', tcp:true, ip:true, signal:true, detailKind:'signal', label:'0/1', explain:'ルータ間でも、実際に流れているものは0と1の信号です。'},
      {key:'sNet', layer:'sNet', tcp:true, ip:true, signal:true, label:'受信', snapshot:'回線から受信', snapKind:'signal', detailKind:'signal', explain:'Webサーバ側のネットワークインタフェース層が0と1の信号を受け取ります。'},
      {key:'sInet', layer:'sInet', tcp:true, ip:true, label:'IP確認', snapshot:'IPを確認して外す', snapKind:'tcp', explain:'IPの外側の情報を確認し、自分宛てのパケットだと判断します。ここでIPの情報は役目を終えます。'},
      {key:'sTrans', layer:'sTrans', tcp:true, label:'TCP確認', snapshot:'TCP番号で復元', snapKind:'single', explain:'TCPの番号を使って、分かれていたデータを正しい順番に整えます。ここでTCPの情報は役目を終えます。'},
      {key:'sApp', layer:'sApp', form:'single', label:'HTTP<br>GET '+LAST_INFO.path, snapshot:'HTTPデータを取得', snapKind:'single', explain:'最後にHTTPデータが取り出され、Webサーバが要求内容を読み取ります。'}
    ];
    var responsePath = [
      {key:'sApp', layer:'sApp', form:'single', label:'HTTP<br>HTML応答', response:true, snapshot:'HTTP応答を作成', snapKind:'single', explain:'Webサーバは、要求されたindex.htmlをHTTPの応答として用意します。'},
      {key:'sTrans', layer:'sTrans', tcp:true, response:true, label:'TCP', snapshot:'TCPを追加・4分割', snapKind:'tcp', explain:'応答データもTCPで4つに分けられ、順番の番号が付きます。'},
      {key:'sInet', layer:'sInet', tcp:true, ip:true, response:true, label:'IP', snapshot:'IPを外側に追加', snapKind:'ip', explain:'今度は送信側PCのIPアドレスを宛先として、IPの情報を外側に付けます。'},
      {key:'sNet', layer:'sNet', tcp:true, ip:true, signal:true, response:true, label:'0/1', snapshot:'回線へ送信', snapKind:'signal', detailKind:'signal', explain:'Webサーバ側から、応答データを0と1の信号としてネットワークへ送り出します。'},
      {key:'rb2', tcp:true, ip:true, signal:true, response:true, detailKind:'signal', label:'0/1', explain:'応答データも、ネットワークを通っている間は0と1の信号として流れます。'},
      {key:'rb1', tcp:true, ip:true, signal:true, response:true, detailKind:'signal', label:'0/1', explain:'帰り道でも、ルータ間を流れるものは0と1の信号です。'},
      {key:'cNet', layer:'cNet', tcp:true, ip:true, signal:true, response:true, label:'受信', snapshot:'回線から受信', snapKind:'signal', detailKind:'signal', explain:'送信側PCのネットワークインタフェース層が、戻ってきた0と1の信号を受け取ります。'},
      {key:'cInet', layer:'cInet', tcp:true, ip:true, response:true, label:'IP確認', snapshot:'IPを確認して外す', snapKind:'tcp', explain:'IPの情報を確認し、自分宛てのパケットだと分かります。ここでIPの情報は取り外されます。'},
      {key:'cTrans', layer:'cTrans', tcp:true, response:true, label:'TCP復元', snapshot:'TCP番号で復元', snapKind:'single', explain:'TCPが1/4〜4/4の番号を使ってHTMLデータを正しい順番に戻します。'},
      {key:'cApp', layer:'cApp', form:'single', label:'HTTP<br>HTML応答', response:true, snapshot:'ブラウザへ渡す', snapKind:'single', explain:'HTTPの応答がブラウザへ渡り、Webページ表示につながります。'}
    ];
    var steps = requestPath.concat(responsePath);
    configureTcpPackets(steps[0]);
    placeTcpPackets(p[steps[0].key], true);
    for(var i=0;i<steps.length;i++){
      if(!(await visitTcpPoint(steps[i], myRun))) return;
      if(i < steps.length-1){
        await animateTcpPackets(p[steps[i].key], p[steps[i+1].key], 620, myRun, steps[i].form === 'single' && steps[i+1].form === 'single');
      }
    }
    clearTcpLayerHighlights();
    $('tcpExplanation').innerHTML = '<b>まとめ：</b>送信側では上の層から下の層へ進みながら情報を付け加え、ネットワークを通って、受信側では下の層から上の層へ進みながら元のデータを取り出します。';
    $('tcpPlayBtn').disabled = false;
    $('tcpPlayBtn').textContent = 'もう一度流す';
    tcpRunning = false;
  }

  function resetTcpFlow(){
    tcpAnimRun++;
    tcpRunning = false;
    PAUSED = false;
    updatePauseButtons();
    updateTcpLabels();
    clearTcpLayerHighlights();
    clearSnapshots();
    $('tcpPacketsLayer').classList.add('hidden');
    tcpPacketEls().forEach(function(el){
      el.className = 'tcp-mini-packet';
    });
    $('tcpPlayBtn').disabled = false;
    $('tcpPlayBtn').textContent = '4層の流れを見る';
    $('dataDetailStatus').innerHTML = '<b>待機中</b><br>「4層の流れを見る」を押すと、現在流れているデータの中身がここに表示されます。';
    $('dataDetailBox').innerHTML =
      '<div class="proto-box http-box">' +
        '<div class="proto-head"><span>HTTP</span><span>待機中</span></div>' +
        '<div class="payload-lines">GET /index.html</div>' +
      '</div>';
    $('dataDetailNote').textContent = '層を通るたびに、外側へTCPやIPの情報が追加されます。受信側では外側から順に確認して取り外します。';
    $('tcpExplanation').innerHTML = '<b>流れの見方：</b>動くパケットは控えめに流れます。各層に残る小さな履歴を見ると、TCPやIPの情報がどこで追加され、どこで取り外されたか確認できます。';
  }

  function setFileActive(type, on){
    var el = $('file-'+type);
    if(el){ el.classList.toggle('active', !!on); }
  }

  function hashIp(domain){
    var h = 0;
    for(var i=0;i<domain.length;i++){ h = (h*31 + domain.charCodeAt(i)) >>> 0; }
    return '192.0.2.'+(50 + (h % 150));
  }

  function resetAll(){
    runId++;
    $('packets-layer').innerHTML = '';
    $('logBox').innerHTML = '<div class="log-empty">まだ通信は行われていません。</div>';
    ['html','css','img'].forEach(function(t){ updateProgress(t,0); setFileActive(t,false); });
    $('resolvedIp').innerHTML = '名前解決: <span class="mono">まだ通信していません</span>';
    $('dnsStatus').textContent = '待機中...';
    $('webStatus').textContent = '待機中...';
    $('pulseDns').classList.remove('on');
    $('pulseWeb').classList.remove('on');
    $('dnsServerBox').classList.remove('busy');
    $('webServerBox').classList.remove('busy');
    $('dnsLed').classList.remove('blink');
    $('webLed').classList.remove('blink');
    $('pathDns').classList.remove('on');
    $('pathWeb').classList.remove('on');
    $('detailBox').classList.remove('show');
    var body = $('pageBody');
    body.className = 'browser-body';
    body.innerHTML = '<div class="empty-msg">「アクセス」を押すと、ここにWebページが少しずつ表示されます</div>';
    setStage(0);
    $('goBtn').disabled = false;
    $('goBtn').textContent = 'アクセス';
    LAST_INFO = {domain:"www.school.jp", path:"/index.html", protocol:"https"};
    LAST_IP = "192.0.2.10";
    resetTcpFlow();
  }

  function onResourceComplete(type){
    var body = $('pageBody');
    if(type==='html'){
      body.innerHTML =
        '<h1 class="page-h1">ようこそ 情報高校 ホームページへ</h1>' +
        '<p class="page-p">本校は情報教育に力を入れています。今日も一日がんばりましょう。</p>' +
        '<ul class="page-list"><li>お知らせ</li><li>学校行事</li><li>部活動</li></ul>';
    } else if(type==='css'){
      body.classList.add('styled');
    } else if(type==='img'){
      var img = document.createElement('div');
      img.className = 'hero-img';
      img.textContent = '🖼️';
      body.appendChild(img);
      var cap = document.createElement('div');
      cap.className = 'img-caption';
      cap.textContent = 'photo.jpg（学校の写真）';
      body.appendChild(cap);
    }
  }

  function extractInfo(raw){
    var s = raw.trim();
    if(!/^https?:\/\//i.test(s)){ s = 'https://' + s; }
    var u;
    try{ u = new URL(s); } catch(e){ return null; }
    var path = u.pathname;
    if(!path || path === '/'){ path = '/index.html'; }
    return { domain: u.hostname, path: path, protocol: u.protocol.replace(':','') };
  }

  async function sendResource(name, type, total, webIp){
    addLog(webIp + ' が ' + name + ' を準備しています...');
    $('webStatus').textContent = name + ' を送信中...';
    setFileActive(type, true);
    var arrived = 0;
    var proms = [];
    var myRun = runId;
    for(var i=1;i<=total;i++){
      await wait(170);
      if(myRun !== runId) return;
      (function(idx){
        var p = spawnPacket({
          label: type.toUpperCase()+' '+idx+'/'+total,
          className: 'pkt-'+type,
          path: PATH_FROM_WEB,
          duration: 950,
          meta: { type: name+' パケット '+idx+'/'+total, src: webIp, dst: BROWSER_IP }
        }).then(function(){
          if(myRun !== runId) return;
          arrived++;
          var pct = Math.round(arrived/total*100);
          updateProgress(type, pct);
          if(arrived===total){
            addLog(name + ' を受信しました（'+type.toUpperCase()+' 100%）', true);
            setFileActive(type, false);
            onResourceComplete(type);
          }
        });
        proms.push(p);
      })(i);
    }
    await Promise.all(proms);
  }

  async function runSimulation(){
    var myRun = ++runId;
    $('packets-layer').innerHTML = '';
    $('detailBox').classList.remove('show');
    $('goBtn').disabled = true;
    $('goBtn').textContent = '通信中...';
    var body = $('pageBody');
    body.className = 'browser-body';
    body.innerHTML = '';
    ['html','css','img'].forEach(function(t){ updateProgress(t,0); });
    $('logBox').innerHTML = '';

    var raw = $('urlInput').value;
    var info = extractInfo(raw);
    if(!info){
      addLog('⚠ URLの形式が正しくありません。例: https://www.school.jp', true);
      $('goBtn').disabled = false;
      $('goBtn').textContent = 'アクセス';
      return;
    }

    setStage(1);
    addLog('入力されたURL: ' + raw);
    LAST_INFO = info;
    await wait(300);
    if(myRun!==runId) return;
    addLog('URLからドメイン名を抽出しました: <b class="mono">' + info.domain + '</b>');
    await wait(400);
    if(myRun!==runId) return;

    // --- DNS 問い合わせ ---
    setStage(2);
    $('pathDns').classList.add('on');
    $('dnsStatus').textContent = '問い合わせ受信中...';
    addLog('DNSサーバ ('+DNS_IP+') へ問い合わせを送信します');
    await spawnPacket({
      label: 'DNS?', className:'pkt-dns', path: PATH_TO_DNS, duration: 1100,
      meta: { type:'DNSクエリ ('+info.domain+')', src: BROWSER_IP, dst: DNS_IP }
    });
    if(myRun!==runId) return;
    $('pulseDns').classList.add('on');
    $('dnsServerBox').classList.add('busy');
    $('dnsLed').classList.add('blink');
    addLog('DNSサーバが ' + info.domain + ' を検索しています...');
    await wait(500);
    if(myRun!==runId) return;
    var ip = DNS_TABLE[info.domain] || hashIp(info.domain);
    LAST_IP = ip;
    $('pulseDns').classList.remove('on');
    $('dnsServerBox').classList.remove('busy');
    $('dnsLed').classList.remove('blink');
    $('dnsStatus').textContent = info.domain + ' → ' + ip;
    addLog('DNSサーバが変換結果を返送します: <b class="mono">'+info.domain+' → '+ip+'</b>');
    await spawnPacket({
      label:'IP応答', className:'pkt-dns', path: PATH_FROM_DNS, duration: 1100,
      meta: { type:'DNS応答 (IPアドレス)', src: DNS_IP, dst: BROWSER_IP }
    });
    if(myRun!==runId) return;
    $('pathDns').classList.remove('on');
    $('resolvedIp').innerHTML = '名前解決: <span class="mono">'+info.domain+' → <b>'+ip+'</b></span>';
    addLog('ブラウザがIPアドレスを取得しました: <b class="mono">'+ip+'</b>', true);
    await wait(400);
    if(myRun!==runId) return;

    // --- HTTPリクエスト ---
    setStage(3);
    $('pathWeb').classList.add('on');
    addLog('取得したIPアドレス宛にHTTP接続を開始します（'+ip+'）');
    await wait(200);
    if(myRun!==runId) return;
    $('webStatus').textContent = 'リクエスト受信中...';
    await spawnPacket({
      label:'GET '+info.path, className:'pkt-http', path: PATH_TO_WEB, duration: 1100,
      meta: { type:'HTTPリクエスト (GET '+info.path+')', src: BROWSER_IP, dst: ip }
    });
    if(myRun!==runId) return;
    $('pulseWeb').classList.add('on');
    $('webServerBox').classList.add('busy');
    $('webLed').classList.add('blink');
    addLog('Webサーバ ('+ip+') へHTTPリクエストが到着しました: GET '+info.path, true);
    await wait(500);
    if(myRun!==runId) return;
    $('pulseWeb').classList.remove('on');

    // --- データ受信 ---
    setStage(4);
    addLog('Webサーバがデータをパケットに分割して送信します');
    await sendResource('index.html', 'html', 5, ip);
    if(myRun!==runId) return;
    await sendResource('style.css', 'css', 4, ip);
    if(myRun!==runId) return;
    await sendResource('photo.jpg', 'img', 6, ip);
    if(myRun!==runId) return;
    $('pathWeb').classList.remove('on');
    $('webServerBox').classList.remove('busy');
    $('webLed').classList.remove('blink');
    $('webStatus').textContent = '送信完了';

    // --- 表示完了 ---
    setStage(5);
    await wait(300);
    if(myRun!==runId) return;
    addLog('すべてのデータを組み合わせてWebページの表示が完了しました 🎉', true);
    $('goBtn').disabled = false;
    $('goBtn').textContent = 'アクセス';
  }

  $('goBtn').addEventListener('click', function(){ runSimulation(); });
  $('resetBtn').addEventListener('click', resetAll);
  $('webModeBtn').addEventListener('click', function(){ setMode('web'); });
  $('tcpModeBtn').addEventListener('click', function(){ setMode('tcp'); });
  $('backToWebBtn').addEventListener('click', function(){ setMode('web'); });
  $('tcpResetBtn').addEventListener('click', resetTcpFlow);
  $('tcpPlayBtn').addEventListener('click', runTcpFlow);
  $('tcpPauseBtn').addEventListener('click', togglePause);
  $('urlInput').addEventListener('keydown', function(e){
    if(e.key === 'Enter'){ runSimulation(); }
  });
  $('speedSel').addEventListener('change', function(e){ SPEED = parseFloat(e.target.value); });
  $('pauseBtn').addEventListener('click', togglePause);
  document.getElementById('netSvg').addEventListener('click', function(){
    $('detailBox').classList.remove('show');
  });

  resetAll();
  resetTcpFlow();
})();
</script>
</body>
</html>
"""

components.html(SIM_HTML, height=1180, scrolling=True)

with st.expander("🧑‍🏫 この教材の使い方（教員・生徒向け）"):
    st.markdown(
        """
- アドレス欄にURL（例: `https://www.school.jp`）を入力し、**「アクセス」**を押すと通信が始まります。
- **DNS問い合わせ → IPアドレス取得 → HTTPリクエスト → データ受信 → 表示完了** の順に、パケットが
  ブラウザ・ルータ・DNSサーバ・Webサーバの間を移動する様子をアニメーションで確認できます。
- 右上の**速度**セレクタでゆっくり観察したり、**⏸ 一時停止**でアニメーションを止めて確認したりできます。
- 移動中のパケット（色のついた四角形）を**クリック**すると、送信元IP・送信先IP・データの種類が表示されます。
- HTML・CSS・画像はそれぞれ複数のパケットに分かれて届きます。ブラウザ画面ではHTMLが届くと文字だけの
  ページが、CSSが届くと色やレイアウトが、画像が届くと写真が段階的に追加される様子を観察してください。
- **TCP/IP詳細モード**では、同じ通信を4層モデルで表示します。送信側で上から下へ、ネットワークを通って、
  受信側で下から上へ進むアニメーションから、カプセル化と復元の流れを確認できます。
- 画面右上の「ℹ️」から、TCPやTLS（HTTPS）についての補足説明を確認できます。
        """
    )
