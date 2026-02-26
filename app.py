import streamlit as st
import streamlit.components.v1 as components

# Set up the Streamlit page
st.set_page_config(page_title="Diamond Pro 26", layout="centered")

# This is where your actual game code lives
game_code = """
<!DOCTYPE html>
<html>
<head>
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <style>
        body { font-family: 'Arial Black', sans-serif; background: #121212; color: white; text-align: center; margin: 0; overflow: hidden; touch-action: none; }
        #stadium { position: relative; width: 100%; height: 500px; background: linear-gradient(#1a2a6c, #b21f1f, #fdbb2d); overflow: hidden; }
        #field { position: absolute; bottom: 0; width: 200%; left: -50%; height: 350px; background: radial-gradient(circle at 50% 100%, #137547 0%, #054a29 100%); transform: rotateX(65deg); transform-origin: bottom; border-top: 4px solid #fff; }
        #zone-container { position: absolute; bottom: 50px; left: 50%; transform: translateX(-50%); width: 140px; height: 180px; z-index: 20; }
        #strike-zone { width: 100%; height: 100%; border: 2px solid rgba(255,255,255,0.2); position: absolute; }
        #pci { width: 40px; height: 40px; border: 2px solid #f1c40f; border-radius: 50%; position: absolute; left: 50px; top: 70px; background: rgba(241, 196, 15, 0.2); pointer-events: auto; box-shadow: 0 0 10px #f1c40f; }
        .player { position: absolute; font-size: 50px; z-index: 10; pointer-events: none; }
        #pitcher { bottom: 220px; left: 50%; transform: translateX(-50%) scale(0.6); }
        #batter { bottom: 10px; left: 15%; transform: scale(1.3); }
        #ball { position: absolute; width: 8px; height: 8px; background: #fff; border-radius: 50%; display: none; z-index: 15; box-shadow: 0 0 10px #fff; }
        #swing-btn { position: absolute; bottom: 20px; right: 20px; width: 80px; height: 80px; border-radius: 50%; background: #e74c3c; color: white; border: 4px solid #fff; font-weight: bold; z-index: 30; }
        #hud { position: absolute; top: 0; width: 100%; display: flex; justify-content: space-around; background: rgba(0,0,0,0.7); padding: 10px 0; z-index: 40; }
        #msg { position: absolute; top: 80px; width: 100%; font-size: 20px; font-weight: bold; z-index: 40; text-shadow: 2px 2px #000; }
    </style>
</head>
<body>
    <div id="stadium">
        <div id="hud">
            <div>SCORE: <span id="score">0</span></div>
            <div>OUTS: <span id="outs">0</span></div>
            <div>INNING: <span id="inning">1</span></div>
        </div>
        <div id="msg">DRAG PCI • TAP PITCHER</div>
        <div id="field"></div>
        <div id="pitcher" onclick="startPitch()">⚾🏃</div>
        <div id="zone-container">
            <div id="strike-zone"></div>
            <div id="pci"></div>
        </div>
        <div id="ball"></div>
        <div id="batter">🏏🧔</div>
        <button id="swing-btn" onclick="swing()">SWING</button>
    </div>

    <script>
        let state = { score: 0, outs: 0, inning: 1, pitching: false, canHit: false, ballPos: {x:0, y:0} };
        const pci = document.getElementById('pci');
        const container = document.getElementById('zone-container');
        const ball = document.getElementById('ball');

        // PCI Drag Logic for Mobile
        container.addEventListener('touchstart', (e) => { e.preventDefault(); });
        container.addEventListener('touchmove', (e) => {
            let rect = container.getBoundingClientRect();
            let x = e.touches[0].clientX - rect.left - 20;
            let y = e.touches[0].clientY - rect.top - 20;
            x = Math.max(0, Math.min(x, 100));
            y = Math.max(0, Math.min(y, 140));
            pci.style.left = x + 'px';
            pci.style.top = y + 'px';
        });

        function startPitch() {
            if(state.pitching) return;
            state.pitching = true;
            document.getElementById('msg').innerText = "HERE IT COMES!";
            ball.style.display = "block";
            ball.style.bottom = "240px";
            ball.style.left = "50%";
            ball.style.width = "8px";
            ball.style.height = "8px";
            
            state.ballPos.x = Math.random() * 100;
            state.ballPos.y = 40 + Math.random() * 100;
            
            setTimeout(() => {
                ball.style.transition = "all 0.6s ease-in";
                ball.style.bottom = "80px";
                ball.style.left = `calc(50% - 70px + ${state.ballPos.x}px)`;
                ball.style.width = "35px";
                ball.style.height = "35px";
                setTimeout(() => { state.canHit = true; }, 400);
                setTimeout(() => { if(state.canHit) resolve("STRIKE!"); }, 750);
            }, 50);
        }

        function swing() {
            if(!state.pitching || !state.canHit) return;
            state.canHit = false;
            let pX = parseInt(pci.style.left);
            let pY = parseInt(pci.style.top);
            let dist = Math.sqrt(Math.pow(pX - state.ballPos.x, 2) + Math.pow(pY - (180 - state.ballPos.y), 2));
            
            if(dist < 30) resolve("🚀 HOME RUN!", true);
            else if (dist < 55) resolve("⚾ SINGLE!", true);
            else resolve("OUT!");
        }

        function resolve(m, hit) {
            state.canHit = false;
            document.getElementById('msg').innerText = m;
            if(hit) state.score++; else state.outs++;
            setTimeout(() => {
                state.pitching = false;
                ball.style.display = "none";
                if(state.outs >= 3) { state.outs = 0; state.inning++; alert("Inning Over!"); }
                document.getElementById('score').innerText = state.score;
                document.getElementById('outs').innerText = state.outs;
                document.getElementById('inning').innerText = state.inning;
            }, 1000);
        }
    </script>
</body>
</html>
"""

# Render the game at a good height for mobile
components.html(game_code, height=550)
