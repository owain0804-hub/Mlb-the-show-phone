import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="Baseball 9 Web", layout="centered")

game_code = """
<!DOCTYPE html>
<html>
<head>
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <style>
        body, html { margin: 0; padding: 0; width: 100%; height: 100%; background: #111; font-family: 'Arial', sans-serif; overflow: hidden; touch-action: none; user-select: none; -webkit-user-select: none; }
        
        #game-screen { position: relative; width: 100%; max-width: 800px; height: 100vh; max-height: 450px; margin: 0 auto; background: url('https://upload.wikimedia.org/wikipedia/commons/thumb/c/c5/Target_Field_Minnesota_Twins.jpg/800px-Target_Field_Minnesota_Twins.jpg') no-repeat center center/cover; overflow: hidden; }
        
        /* Dark overlay to match the night game vibe */
        #game-screen::after { content: ''; position: absolute; top: 0; left: 0; width: 100%; height: 100%; background: rgba(0,0,0,0.4); z-index: 1; pointer-events: none; }

        /* --- BASEBALL 9 UI RECREATION --- */
        
        /* Top Left Scoreboard */
        #top-left-sb { position: absolute; top: 10px; left: 10px; background: rgba(0,0,0,0.7); border: 2px solid #555; border-radius: 5px; display: flex; z-index: 10; width: 160px; color: white; }
        .team-col { flex: 2; padding: 5px; font-size: 12px; font-weight: bold; border-right: 1px solid #444; }
        .team-row { display: flex; justify-content: space-between; margin-bottom: 2px; }
        .score-col { flex: 1; padding: 5px; display: flex; flex-direction: column; align-items: center; justify-content: center; background: #fff; color: black; font-weight: bold; font-size: 14px; }
        
        /* Top Right Player Card */
        #top-right-card { position: absolute; top: 10px; right: 10px; background: rgba(0,0,0,0.7); border: 2px solid #555; border-radius: 5px; padding: 5px 10px; z-index: 10; color: white; width: 140px; }
        .card-name { font-size: 12px; font-weight: bold; border-bottom: 1px solid #555; padding-bottom: 3px; margin-bottom: 3px; text-align: right; }
        .card-stats { display: flex; justify-content: space-between; font-size: 10px; color: #ccc; }

        /* Strike Zone (Like the screenshot) */
        #strike-zone { position: absolute; bottom: 20%; left: 50%; transform: translateX(-50%); width: 100px; height: 130px; border: 1px solid rgba(255, 255, 255, 0.2); z-index: 20; display: flex; align-items: center; justify-content: center; }
        /* The corner brackets */
        #strike-zone::before { content: ''; position: absolute; top: 0; left: 0; width: 100%; height: 100%; background: 
            linear-gradient(to right, #fff 2px, transparent 2px) 0 0, linear-gradient(to right, #fff 2px, transparent 2px) 0 100%, 
            linear-gradient(to left, #fff 2px, transparent 2px) 100% 0, linear-gradient(to left, #fff 2px, transparent 2px) 100% 100%, 
            linear-gradient(to bottom, #fff 2px, transparent 2px) 0 0, linear-gradient(to bottom, #fff 2px, transparent 2px) 100% 0, 
            linear-gradient(to top, #fff 2px, transparent 2px) 0 100%, linear-gradient(to top, #fff 2px, transparent 2px) 100% 100%; 
            background-repeat: no-repeat; background-size: 10px 10px; }
        /* Center reticle */
        #pci { position: absolute; width: 30px; height: 30px; border: 1px dashed rgba(255,255,255,0.7); z-index: 25; display: flex; align-items: center; justify-content: center; pointer-events: none; }
        #pci::after { content: ''; width: 4px; height: 4px; background: red; border-radius: 50%; }

        /* Bottom Center Toggles */
        #bottom-toggles { position: absolute; bottom: 10px; left: 50%; transform: translateX(-50%); display: flex; background: rgba(0,0,0,0.6); border: 1px solid #555; border-radius: 20px; overflow: hidden; z-index: 10; }
        .toggle-btn { padding: 5px 15px; font-size: 10px; color: #888; font-weight: bold; text-transform: uppercase; border-right: 1px solid #444; }
        .toggle-active { background: #3498db; color: white; }

        /* The Big "READY" Button */
        #ready-btn { position: absolute; bottom: 20px; right: 20px; width: 80px; height: 80px; border-radius: 50%; background: rgba(0,0,0,0.6); border: 2px solid rgba(255,255,255,0.3); color: white; font-size: 14px; font-weight: bold; z-index: 50; display: flex; align-items: center; justify-content: center; box-shadow: inset 0 0 10px rgba(0,0,0,0.8); }
        #ready-btn:active { background: rgba(255,255,255,0.2); }

        /* Field Elements */
        #pitcher { position: absolute; top: 45%; left: 50%; transform: translateX(-50%); font-size: 30px; z-index: 5; }
        #batter { position: absolute; bottom: 10%; left: 35%; font-size: 60px; z-index: 30; transform-origin: bottom center; }
        #ball { position: absolute; width: 10px; height: 10px; background: #fff; border-radius: 50%; z-index: 22; display: none; transform: translate(-50%, -50%); box-shadow: 0 0 5px #fff; }

        #controls-layer { position: absolute; top: 0; left: 0; width: 50%; height: 100%; z-index: 40; }
        #message { position: absolute; top: 30%; width: 100%; text-align: center; font-size: 30px; color: #fff; font-weight: bold; z-index: 60; opacity: 0; text-shadow: 2px 2px 4px #000; pointer-events: none; }
    </style>
</head>
<body>

<div id="game-screen">
    
    <div id="top-left-sb">
        <div class="team-col">
            <div class="team-row"><span style="color:#e74c3c;">RANGERS</span> <span>3</span></div>
            <div class="team-row"><span style="color:#3498db;">CHALLENGERS</span> <span>3</span></div>
        </div>
        <div class="score-col">
            <div>▲ 6</div>
            <div>0 - 0</div>
        </div>
    </div>

    <div id="top-right-card">
        <div class="card-name">SP T. Howell ⚾</div>
        <div class="card-stats"><span>ERA 4.16</span> <span>102 MPH</span></div>
    </div>

    <div id="pitcher">⚾</div>
    <div id="batter">🏏</div>

    <div id="strike-zone"></div>
    <div id="pci"></div>
    <div id="ball"></div>

    <div id="message">PERFECT!</div>

    <div id="bottom-toggles">
        <div class="toggle-btn">CONTACT</div>
        <div class="toggle-btn toggle-active">POWER</div>
        <div class="toggle-btn">BUNT</div>
    </div>

    <div id="controls-layer"></div>
    <div id="ready-btn" onclick="startPlay()">READY</div>

</div>

<script>
    let mode = 'idle';
    let pTime = 0;
    const pDur = 800;
    let reqId = null;
    
    const ball = document.getElementById('ball');
    const pci = document.getElementById('pci');
    const msg = document.getElementById('message');
    const readyBtn = document.getElementById('ready-btn');
    const leftPad = document.getElementById('controls-layer');
    const gameRect = document.getElementById('game-screen').getBoundingClientRect();

    let pciPos = { x: gameRect.width / 2, y: gameRect.height * 0.7 };
    let bStart = { x: gameRect.width / 2, y: gameRect.height * 0.5 };
    let bTarget = { x: 0, y: 0 };
    let cBall = { x: 0, y: 0 };

    pci.style.left = pciPos.x + 'px';
    pci.style.top = pciPos.y + 'px';

    // Drag PCI
    let tStart = null;
    let pStart = null;
    leftPad.addEventListener('touchstart', (e) => {
        e.preventDefault();
        tStart = { x: e.touches[0].clientX, y: e.touches[0].clientY };
        pStart = { x: pciPos.x, y: pciPos.y };
    });
    leftPad.addEventListener('touchmove', (e) => {
        e.preventDefault();
        if(!tStart) return;
        pciPos.x = pStart.x + ((e.touches[0].clientX - tStart.x) * 1.5);
        pciPos.y = pStart.y + ((e.touches[0].clientY - tStart.y) * 1.5);
        pci.style.left = pciPos.x + 'px';
        pci.style.top = pciPos.y + 'px';
    });

    function startPlay() {
        if(mode === 'pitching') {
            swing();
            return;
        }
        
        // Setup Pitch
        readyBtn.innerText = "SWING";
        readyBtn.style.background = "rgba(231, 76, 60, 0.6)"; // Turns red like a swing button
        msg.style.opacity = '0';
        
        let zRect = document.getElementById('strike-zone').getBoundingClientRect();
        let screenRect = document.getElementById('game-screen').getBoundingClientRect();
        
        bTarget.x = (zRect.left - screenRect.left) + (Math.random() * zRect.width);
        bTarget.y = (zRect.top - screenRect.top) + (Math.random() * zRect.height);

        ball.style.display = 'block';
        mode = 'pitching';
        pTime = performance.now();
        reqId = requestAnimationFrame(animate);
    }

    function animate(now) {
        if(mode !== 'pitching') return;
        let t = (now - pTime) / pDur;

        if (t > 1.2) { end("STRIKE!"); return; }

        let ease = t * t * t; 
        cBall.x = bStart.x + ((bTarget.x - bStart.x) * t);
        cBall.y = bStart.y + ((bTarget.y - bStart.y) * ease);
        
        ball.style.left = cBall.x + 'px';
        ball.style.top = cBall.y + 'px';
        ball.style.transform = `translate(-50%, -50%) scale(${0.5 + (2 * ease)})`;

        reqId = requestAnimationFrame(animate);
    }

    function swing() {
        document.getElementById('batter').style.transform = 'rotate(-30deg) scale(1.1)';
        setTimeout(() => { document.getElementById('batter').style.transform = 'rotate(0) scale(1)'; }, 200);

        let t = (performance.now() - pTime) / pDur;
        let dist = Math.sqrt(Math.pow(pciPos.x - cBall.x, 2) + Math.pow(pciPos.y - cBall.y, 2));

        if (t > 0.85 && t < 1.1) {
            if (dist < 25) end("PERFECT HIT!");
            else if (dist < 50) end("GOOD HIT");
            else end("FLY OUT");
        } else {
            end("SWING & MISS");
        }
    }

    function end(m) {
        mode = 'idle';
        cancelAnimationFrame(reqId);
        msg.innerText = m;
        msg.style.opacity = '1';
        readyBtn.innerText = "READY";
        readyBtn.style.background = "rgba(0,0,0,0.6)";
        setTimeout(() => { ball.style.display = 'none'; }, 1000);
    }
</script>
</body>
</html>
"""

# Adjust height to match a landscape mobile game perspective
components.html(game_code, height=450)
