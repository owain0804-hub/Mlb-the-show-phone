import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="Diamond Pro 26: Elite", layout="centered")

game_code = """
<!DOCTYPE html>
<html>
<head>
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <style>
        body { font-family: 'Arial Black', sans-serif; background: #000; color: white; text-align: center; margin: 0; overflow: hidden; touch-action: none; }
        
        /* Stadium & Environment */
        #stadium { position: relative; width: 100%; height: 550px; background: #87ceeb; overflow: hidden; }
        
        #sky { height: 40%; background: linear-gradient(#1a2a6c, #2a5298); position: relative; }
        #crowd { position: absolute; bottom: 0; width: 100%; height: 30px; background: repeating-linear-gradient(90deg, #555 0px, #333 10px, #444 20px); opacity: 0.8; }
        
        #field { 
            position: absolute; bottom: 0; width: 180%; left: -40%; height: 65%; 
            background: radial-gradient(circle at 50% 100%, #1d7a46 0%, #134e2c 100%); 
            transform: rotateX(65deg); transform-origin: bottom; border-top: 10px solid #2d6a4f;
        }

        /* Dirt Diamond */
        #diamond { 
            position: absolute; bottom: 0; left: 50%; transform: translateX(-50%); 
            width: 250px; height: 250px; background: #c28e46; clip-path: polygon(50% 0%, 100% 50%, 50% 100%, 0% 50%); opacity: 0.8;
        }

        /* HUD Styling like Baseball 9 */
        #hud { position: absolute; top: 0; width: 100%; display: grid; grid-template-columns: 1fr 1fr 1fr; background: rgba(0,0,0,0.8); padding: 10px 0; z-index: 50; border-bottom: 2px solid #f1c40f; }
        .stat-label { font-size: 10px; color: #aaa; }
        .stat-num { display: block; font-size: 18px; color: #fff; }

        /* Game Mechanics */
        #zone-container { position: absolute; bottom: 60px; left: 50%; transform: translateX(-50%); width: 130px; height: 170px; z-index: 30; }
        #strike-zone { width: 100%; height: 100%; border: 2px solid rgba(255,255,255,0.4); box-sizing: border-box; }
        #pci { width: 35px; height: 35px; border: 3px solid #f1c40f; border-radius: 50%; position: absolute; left: 45px; top: 65px; background: rgba(241, 196, 15, 0.3); box-shadow: 0 0 15px #f1c40f; z-index: 40; }

        .player { position: absolute; z-index: 25; pointer-events: none; text-shadow: 2px 2px 4px #000; }
        #pitcher { bottom: 250px; left: 50%; transform: translateX(-50%) scale(0.8); font-size: 40px; }
        #batter { bottom: 15px; left: 20%; transform: scale(1.5); font-size: 50px; transition: transform 0.2s; }
        
        #ball { position: absolute; width: 8px; height: 8px; background: #fff; border-radius: 50%; display: none; z-index: 35; box-shadow: 0 0 8px #fff; }

        /* Controls */
        #swing-btn { position: absolute; bottom: 30px; right: 20px; width: 90px; height: 90px; border-radius: 50%; background: radial-gradient(#ff4b2b, #ff416c); color: white; border: 5px solid #fff; font-size: 18px; font-weight: bold; z-index: 100; box-shadow: 0 5px 15px rgba(0,0,0,0.5); }
        #msg { position: absolute; top: 85px; width: 100%; font-size: 22px; font-weight: bold; color: #f1c40f; z-index: 60; text-shadow: 2px 2px #000; }
    </style>
</head>
<body>
    <div id="stadium">
        <div id="hud">
            <div><span class="stat-label">SCORE</span><span id="score" class="stat-num">0</span></div>
            <div><span class="stat-label">OUTS</span><span id="outs" class="stat-num">0</span></div>
            <div><span class="stat-label">INNING</span><span id="inning" class="stat-num">1</span></div>
        </div>

        <div id="sky"><div id="crowd"></div></div>
        <div id="msg">READY PLAYER ONE</div>
        <div id="field"><div id="diamond"></div></div>
        
        <div id="pitcher" onclick="startPitch()">⚾🧢</div>
        
        <div id="zone-container">
            <div id="strike-zone"></div>
            <div id="pci"></div>
        </div>

        <div id="ball"></div>
        <div id="batter">🏏👕</div>
        <button id="swing-btn" onclick="swing()">SWING</button>
    </div>

    <script>
        let state = { score: 0, outs: 0, inning: 1, pitching: false, canHit: false, ballPos: {x:0, y:0} };
        const pci = document.getElementById('pci');
        const container = document.getElementById('zone-container');
        const ball = document.getElementById('ball');

        container.addEventListener('touchstart', (e) => { e.preventDefault(); });
        container.addEventListener('touchmove', (e) => {
            let rect = container.getBoundingClientRect();
            let x = e.touches[0].clientX - rect.left - 17;
            let y = e.touches[0].clientY - rect.top - 17;
            x = Math.max(0, Math.min(x, 95));
            y = Math.max(0, Math.min(y, 135));
            pci.style.left = x + 'px';
            pci.style.top = y + 'px';
        });

        function startPitch() {
            if(state.pitching) return;
            state.pitching = true;
            document.getElementById('msg').innerText = "WATCH THE PITCH!";
            ball.style.display = "block";
            ball.style.bottom = "280px";
            ball.style.left = "50%";
            ball.style.width = "6px";
            ball.style.height = "6px";
            
            state.ballPos.x = Math.random() * 95;
            state.ballPos.y = 40 + Math.random() * 100;
            
            setTimeout(() => {
                ball.style.transition = "all 0.65s cubic-bezier(0.1, 0.5, 0.5, 1)";
                ball.style.bottom = "75px";
                ball.style.left = `calc(50% - 65px + ${state.ballPos.x}px)`;
                ball.style.width = "38px";
                ball.style.height = "38px";
                setTimeout(() => { state.canHit = true; }, 450);
                setTimeout(() => { if(state.canHit) resolve("STRIKE!", false); }, 800);
            }, 50);
        }

        function swing() {
            if(!state.pitching || !state.canHit) return;
            state.canHit = false;
            document.getElementById('batter').style.transform = "scale(1.5) rotate(-35deg) translateX(10px)";
            setTimeout(() => document.getElementById('batter').style.transform = "scale(1.5) rotate(0deg)", 200);

            let pX = parseInt(pci.style.left);
            let pY = parseInt(pci.style.top);
            let dist = Math.sqrt(Math.pow(pX - state.ballPos.x, 2) + Math.pow(pY - (170 - state.ballPos.y), 2));
            
            if(dist < 28) resolve("🚀 SMOKED IT!", true);
            else if (dist < 52) resolve("⚾ BASE HIT!", true);
            else resolve("OUT!");
        }

        function resolve(m, hit) {
            state.canHit = false;
            document.getElementById('msg').innerText = m;
            if(hit) state.score++; else state.outs++;
            setTimeout(() => {
                state.pitching = false;
                ball.style.display = "none";
                ball.style.transition = "none";
                if(state.outs >= 3) { state.outs = 0; state.inning++; alert("Change Sides!"); }
                document.getElementById('score').innerText = state.score;
                document.getElementById('outs').innerText = state.outs;
                document.getElementById('inning').innerText = state.inning;
            }, 1200);
        }
    </script>
</body>
</html>
"""

components.html(game_code, height=600)
