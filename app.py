import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="Pro Baseball Sim", layout="centered")

game_html = """
<!DOCTYPE html>
<html>
<head>
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <style>
        body { font-family: 'Arial', sans-serif; background: #121212; color: white; text-align: center; margin: 0; touch-action: manipulation; overflow: hidden; }
        #ui-layer { display: flex; justify-content: space-between; padding: 10px; background: #222; border-bottom: 2px solid #444; }
        .stat-box { font-size: 0.8rem; text-transform: uppercase; color: #aaa; }
        .stat-val { display: block; font-size: 1.2rem; color: #00ffcc; font-weight: bold; }
        
        #field { position: relative; width: 340px; height: 380px; background: #2d6a4f; margin: 20px auto; border: 4px solid #fff; border-radius: 10px; overflow: hidden; }
        #strike-zone { position: absolute; bottom: 40px; left: 50%; transform: translateX(-50%); width: 120px; height: 160px; border: 2px dashed rgba(255,255,255,0.5); }
        
        #ball { 
            position: absolute; width: 25px; height: 25px; background: radial-gradient(circle, #fff, #ccc); 
            border-radius: 50%; display: none; z-index: 100; transition: transform 0.1s linear;
        }
        
        .btn-container { display: flex; justify-content: center; gap: 10px; margin-top: 10px; }
        button { padding: 15px 30px; font-weight: bold; border-radius: 30px; border: none; background: #007bff; color: white; box-shadow: 0 4px #0056b3; }
        button:active { transform: translateY(2px); box-shadow: none; }
        #message { height: 30px; margin-top: 10px; font-weight: bold; color: #f1c40f; }
    </style>
</head>
<body>
    <div id="ui-layer">
        <div class="stat-box">Score<span id="score" class="stat-val">0</span></div>
        <div class="stat-box">Inning<span id="inning" class="stat-val">1</span></div>
        <div class="stat-box">Outs<span id="outs" class="stat-val">0</span></div>
    </div>

    <div id="field">
        <div id="strike-zone"></div>
        <div id="ball"></div>
    </div>

    <div id="message">Wait for the pitch...</div>

    <div class="btn-container">
        <button id="pitch-btn" onclick="startPitch()">READY PITCH</button>
    </div>

    <script>
        let gameState = { score: 0, outs: 0, inning: 1, runners: 0, pitcherSpeed: 800 };
        const ball = document.getElementById('ball');
        const msg = document.getElementById('message');
        const pitchBtn = document.getElementById('pitch-btn');
        let canHit = false;

        function startPitch() {
            pitchBtn.disabled = true;
            msg.innerText = "Here it comes!";
            
            // Random target in strike zone
            const targetX = 110 + Math.random() * 100; 
            const targetY = 200 + Math.random() * 100;
            
            ball.style.left = "50%";
            ball.style.top = "50px";
            ball.style.width = "10px";
            ball.style.height = "10px";
            ball.style.display = "block";

            // Animation: Pitcher to Catcher
            setTimeout(() => {
                ball.style.transition = `all ${gameState.pitcherSpeed}ms ease-in`;
                ball.style.left = targetX + "px";
                ball.style.top = targetY + "px";
                ball.style.width = "40px";
                ball.style.height = "40px";
                canHit = true;
            }, 100);

            // If user doesn't tap in time
            setTimeout(() => {
                if (canHit) {
                    strike();
                }
            }, gameState.pitcherSpeed + 150);
        }

        ball.addEventListener('touchstart', (e) => {
            if (canHit) {
                canHit = false;
                hitBall();
            }
        });

        // For desktop testing
        ball.addEventListener('mousedown', () => {
            if (canHit) {
                canHit = false;
                hitBall();
            }
        });

        function hitBall() {
            const power = Math.random();
            if (power > 0.8) {
                msg.innerText = "⚾ HOME RUN!";
                gameState.score += (gameState.runners + 1);
                gameState.runners = 0;
            } else {
                msg.innerText = "Single!";
                gameState.runners++;
                if (gameState.runners > 3) { gameState.score++; gameState.runners = 3; }
            }
            resetPlay();
        }

        function strike() {
            canHit = false;
            msg.innerText = "STRIKE!";
            gameState.outs++;
            if (gameState.outs >= 3) {
                gameState.inning++;
                gameState.outs = 0;
                gameState.runners = 0;
                gameState.pitcherSpeed -= 50; // Pitcher gets faster!
                alert("Inning Over!");
            }
            resetPlay();
        }

        function resetPlay() {
            ball.style.display = "none";
            ball.style.transition = "none";
            document.getElementById('score').innerText = gameState.score;
            document.getElementById('outs').innerText = gameState.outs;
            document.getElementById('inning').innerText = gameState.inning;
            pitchBtn.disabled = false;
        }
    </script>
</body>
</html>
"""

components.html(game_html, height=600)
