import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="Baseball 9 Pro", layout="centered")

game_code = """
<!DOCTYPE html>
<html>
<head>
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <style>
        /* Base Setup */
        body, html { margin: 0; padding: 0; width: 100%; height: 100%; background: #000; font-family: 'Arial Black', sans-serif; overflow: hidden; touch-action: none; user-select: none; -webkit-user-select: none; }
        
        /* The 3D Stadium */
        #game-screen { position: relative; width: 100%; max-width: 500px; height: 100vh; max-height: 800px; margin: 0 auto; background: linear-gradient(to bottom, #1e3c72, #2a5298); overflow: hidden; }
        
        /* The Field */
        #field-perspective { position: absolute; bottom: 0; width: 100%; height: 60%; perspective: 600px; }
        #grass { position: absolute; bottom: -20%; left: -50%; width: 200%; height: 150%; background: linear-gradient(to top, #137547, #0b4529); transform: rotateX(60deg); border-top: 5px solid #fff; }
        #dirt-mound { position: absolute; top: 10%; left: 50%; transform: translateX(-50%); width: 120px; height: 40px; background: #a67c52; border-radius: 50%; border: 2px solid #5c4033; }
        #home-plate { position: absolute; bottom: 15%; left: 50%; transform: translateX(-50%); width: 60px; height: 40px; background: #fff; clip-path: polygon(0 0, 100% 0, 100% 60%, 50% 100%, 0 60%); }

        /* Jumbotron Scoreboard */
        #scoreboard { position: absolute; top: 15px; left: 50%; transform: translateX(-50%); width: 90%; background: #111; border: 4px solid #444; border-radius: 10px; display: flex; justify-content: space-between; padding: 10px 20px; color: #fff; box-sizing: border-box; z-index: 100; box-shadow: 0 10px 20px rgba(0,0,0,0.5); }
        .sb-stat { text-align: center; }
        .sb-label { font-size: 10px; color: #888; display: block; }
        .sb-val { font-size: 22px; color: #f1c40f; }

        /* Players */
        #pitcher { position: absolute; top: 40%; left: 50%; transform: translateX(-50%); font-size: 40px; z-index: 10; transition: transform 0.2s; }
        #batter { position: absolute; bottom: 18%; left: 25%; font-size: 70px; z-index: 30; transform-origin: bottom center; transition: transform 0.15s ease-out; filter: drop-shadow(5px 5px 2px rgba(0,0,0,0.5)); }

        /* The Strike Zone & PCI */
        #strike-zone { position: absolute; bottom: 25%; left: 50%; transform: translateX(-50%); width: 120px; height: 160px; border: 3px solid rgba(255, 255, 255, 0.4); background: rgba(255, 255, 255, 0.05); z-index: 20; box-sizing: border-box; }
        #pci { position: absolute; width: 44px; height: 44px; background: rgba(241, 196, 15, 0.4); border: 3px solid #f1c40f; border-radius: 50%; transform: translate(-50%, -50%); z-index: 25; box-shadow: 0 0 10px #f1c40f; pointer-events: none; }
        #pci::after { content: ''; position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%); width: 6px; height: 6px; background: #fff; border-radius: 50%; }

        /* The Ball */
        #ball { position: absolute; width: 15px; height: 15px; background: radial-gradient(circle at 30% 30%, #fff, #ccc); border-radius: 50%; z-index: 22; display: none; transform: translate(-50%, -50%); box-shadow: -2px 5px 5px rgba(0,0,0,0.3); }

        /* Controls Area (Two-Thumb System) */
        #controls-layer { position: absolute; top: 0; left: 0; width: 100%; height: 100%; z-index: 50; display: flex; }
        #left-joystick { width: 50%; height: 100%; } /* Invisible hit area for dragging PCI */
        #right-buttons { width: 50%; height: 100%; position: relative; }
        
        #swing-btn { position: absolute; bottom: 10%; right: 10%; width: 100px; height: 100px; border-radius: 50%; background: linear-gradient(#e74c3c, #c0392b); border: 6px solid #fff; color: white; font-size: 22px; font-weight: bold; box-shadow: 0 8px 0 #922b21, 0 15px 20px rgba(0,0,0,0.5); }
        #swing-btn:active { transform: translateY(8px); box-shadow: 0 0 0 #922b21, 0 5px 10px rgba(0,0,0,0.5); }

        /* UI Overlays */
        #ready-btn { position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%); padding: 15px 40px; font-size: 24px; background: #f1c40f; color: #000; border: none; border-radius: 30px; font-weight: bold; box-shadow: 0 5px 15px rgba(0,0,0,0.5); z-index: 100; }
        #message { position: absolute; top: 30%; left: 0; width: 100%; text-align: center; font-size: 40px; color: #fff; font-style: italic; text-shadow: 3px 3px 0 #000; z-index: 60; opacity: 0; transition: opacity 0.2s; pointer-events: none; }
    </style>
</head>
<body>

<div id="game-screen">
    
    <div id="scoreboard">
        <div class="sb-stat"><span class="sb-label">AWAY</span><span class="sb-val" id="score">0</span></div>
        <div class="sb-stat"><span class="sb-label">OUTS</span><span class="sb-val" id="outs">0</span></div>
        <div class="sb-stat"><span class="sb-label">INNING</span><span class="sb-val" id="inning">1</span></div>
    </div>

    <div id="field-perspective">
        <div id="grass"></div>
        <div id="dirt-mound"></div>
        <div id="home-plate"></div>
    </div>

    <div id="pitcher">⚾🧢</div>
    
    <div id="strike-zone"></div>
    
    <div id="pci"></div>
    
    <div id="ball"></div>

    <div id="batter">🏏🪖</div>

    <button id="ready-btn" onclick="setupPitch()">READY</button>
    <div id="message">PERFECT!</div>

    <div id="controls-layer">
        <div id="left-joystick"></div>
        <div id="right-buttons">
            <button id="swing-btn" onclick="swing()">SWING</button>
        </div>
    </div>

</div>

<script>
    // Game State
    let state = { score: 0, outs: 0, inning: 1 };
    let engine = { mode: 'idle', pitchStartTime: 0, pitchDuration: 900, reqId: null };
    
    // Elements
    const ball = document.getElementById('ball');
    const pci = document.getElementById('pci');
    const msg = document.getElementById('message');
    const readyBtn = document.getElementById('ready-btn');
    const batter = document.getElementById('batter');
    const leftPad = document.getElementById('left-joystick');
    const szRect = document.getElementById('strike-zone').getBoundingClientRect();
    const gameRect = document.getElementById('game-screen').getBoundingClientRect();

    // Physics Coordinates
    let pciPos = { x: gameRect.width / 2, y: gameRect.height * 0.65 };
    let ballStart = { x: gameRect.width / 2, y: gameRect.height * 0.45 };
    let ballTarget = { x: 0, y: 0 };
    let currentBall = { x: 0, y: 0 };

    // Set initial PCI position
    updatePCI();

    // ==========================================
    // 1. LEFT THUMB: DRAG PCI LOGIC
    // ==========================================
    let touchStart = null;
    let pciStart = null;

    leftPad.addEventListener('touchstart', (e) => {
        e.preventDefault(); // Stop scrolling
        touchStart = { x: e.touches[0].clientX, y: e.touches[0].clientY };
        pciStart = { x: pciPos.x, y: pciPos.y };
    });

    leftPad.addEventListener('touchmove', (e) => {
        e.preventDefault();
        if(!touchStart) return;
        
        let dx = e.touches[0].clientX - touchStart.x;
        let dy = e.touches[0].clientY - touchStart.y;
        
        // Move PCI (multiplier for sensitivity)
        pciPos.x = pciStart.x + (dx * 1.5);
        pciPos.y = pciStart.y + (dy * 1.5);
        
        updatePCI();
    });

    function updatePCI() {
        pci.style.left = pciPos.x + 'px';
        pci.style.top = pciPos.y + 'px';
    }

    // ==========================================
    // 2. THE PITCH ENGINE (requestAnimationFrame)
    // ==========================================
    function setupPitch() {
        if(engine.mode !== 'idle') return;
        
        readyBtn.style.display = 'none';
        msg.style.opacity = '0';
        
        // Randomize target INSIDE the strike zone
        let zoneRect = document.getElementById('strike-zone').getBoundingClientRect();
        ballTarget.x = zoneRect.left + (Math.random() * zoneRect.width);
        ballTarget.y = zoneRect.top + (Math.random() * zoneRect.height);

        // Reset ball
        ball.style.display = 'block';
        
        // Pitcher animation
        document.getElementById('pitcher').style.transform = 'translateX(-50%) scale(1.2) rotate(15deg)';
        setTimeout(() => { document.getElementById('pitcher').style.transform = 'translateX(-50%) scale(1) rotate(0)'; }, 200);

        // Start engine
        engine.mode = 'pitching';
        engine.pitchStartTime = performance.now();
        engine.reqId = requestAnimationFrame(animatePitch);
    }

    function animatePitch(now) {
        if(engine.mode !== 'pitching') return;

        let elapsed = now - engine.pitchStartTime;
        let t = elapsed / engine.pitchDuration; // 0.0 to 1.0

        if (t > 1.2) { // Ball went past catcher
            endPlay("STRIKE!", false);
            return;
        }

        // Math for 3D trajectory (Cubic ease-in makes it look like it's accelerating towards you)
        let easeT = t * t * t; 
        
        currentBall.x = ballStart.x + ((ballTarget.x - ballStart.x) * t);
        currentBall.y = ballStart.y + ((ballTarget.y - ballStart.y) * easeT);
        let scale = 0.3 + (1.5 * easeT); // Ball gets bigger

        ball.style.left = currentBall.x + 'px';
        ball.style.top = currentBall.y + 'px';
        ball.style.transform = `translate(-50%, -50%) scale(${scale})`;

        engine.reqId = requestAnimationFrame(animatePitch);
    }

    // ==========================================
    // 3. RIGHT THUMB: SWING LOGIC
    // ==========================================
    function swing() {
        if(engine.mode !== 'pitching') return;

        // Batter Swing Animation
        batter.style.transform = 'rotate(-45deg) scale(1.2) translateX(-20px)';
        setTimeout(() => { batter.style.transform = 'rotate(0) scale(1) translateX(0)'; }, 250);

        // Calculate Timing (t)
        let elapsed = performance.now() - engine.pitchStartTime;
        let t = elapsed / engine.pitchDuration;

        // Calculate Aim (Distance between PCI and Ball Target)
        let dist = Math.sqrt(Math.pow(pciPos.x - currentBall.x, 2) + Math.pow(pciPos.y - currentBall.y, 2));

        // Logic check!
        if (t > 0.80 && t < 1.1) { // Good Timing Window
            if (dist < 30) {
                endPlay("🔥 PERFECT! HR!", true);
                ball.style.display = 'none'; // Ball disappears off bat
            } else if (dist < 65) {
                endPlay("⚾ BASE HIT", true);
                ball.style.display = 'none';
            } else {
                endPlay("POP OUT!", false);
            }
        } else {
            endPlay("WHIFF!", false); // Swung too early or late
        }
    }

    function endPlay(message, isHit) {
        engine.mode = 'idle';
        cancelAnimationFrame(engine.reqId);
        
        msg.innerText = message;
        msg.style.opacity = '1';
        if(isHit) msg.style.color = '#2ecc71';
        else msg.style.color = '#e74c3c';

        if(isHit) state.score++;
        else state.outs++;

        if(state.outs >= 3) {
            state.outs = 0;
            state.inning++;
            setTimeout(() => alert("Inning Over!"), 100);
        }

        document.getElementById('score').innerText = state.score;
        document.getElementById('outs').innerText = state.outs;
        document.getElementById('inning').innerText = state.inning;

        setTimeout(() => {
            ball.style.display = 'none';
            readyBtn.style.display = 'block';
        }, 1500);
    }
</script>
</body>
</html>
"""

components.html(game_code, height=750)
