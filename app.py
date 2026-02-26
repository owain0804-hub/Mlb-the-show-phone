import streamlit as st
import streamlit.components.v1 as components

# Set up the mobile-friendly page layout
st.set_page_config(page_title="MLB Scout Pro", layout="centered")

# The HTML, CSS, and JavaScript for your game
game_html = """
<!DOCTYPE html>
<html>
<head>
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <style>
        :root { --bg: #0d1b2a; --field: #2d6a4f; --accent: #3498db; --ball-color: #ffffff; }
        body { font-family: 'Segoe UI', sans-serif; background: var(--bg); color: white; text-align: center; margin: 0; padding: 10px; overflow: hidden; }
        .stats-grid { display: grid; grid-template-columns: repeat(3, 1fr); background: rgba(0,0,0,0.3); padding: 10px; border-radius: 8px; margin-bottom: 10px; border: 1px solid #3e4c59; }
        .stat-val { font-size: 1.2rem; font-weight: bold; color: #f1c40f; }
        .stadium { background: var(--field); height: 220px; border-radius: 50% 50% 10px 10px; border: 3px solid #fff; position: relative; margin: 15px 0; box-shadow: inset 0 0 50px rgba(0,0,0,0.5); }
        .ball { width: 14px; height: 14px; background: var(--ball-color); border-radius: 50%; position: absolute; left: 50%; bottom: 40px; transform: translateX(-50%); display: none; box-shadow: 0 0 8px white; z-index: 10; }
        .controls { display: grid; grid-template-columns: 1fr 1fr; gap: 12px; }
        button { padding: 18px; font-size: 16px; border-radius: 12px; border: none; background: var(--accent); color: white; font-weight: bold; -webkit-tap-highlight-color: transparent; }
        #log { font-size: 0.9rem; height: 40px; margin: 10px 0; color: #bdc3c7; }
        .bases { position: absolute; bottom: 20px; width: 100%; display: flex; justify-content: center; gap: 40px; font-size: 20px; opacity: 0.5; }
    </style>
</head>
<body>
    <div class="stats-grid">
        <div>Score<br><span id="score" class="stat-val">0</span></div>
        <div>Inning<br><span id="inning" class="stat-val">1</span></div>
        <div>Outs<br><span id="outs" class="stat-val">0</span></div>
    </div>

    <div class="stadium">
        <div id="ball" class="ball"></div>
        <div class="bases"><span>⚾</span><span>🏠</span><span>⚾</span></div>
    </div>

    <div id="log">Welcome to the Big Leagues! Pitcher is ready...</div>

    <div class="controls">
        <button onclick="swing('Contact')">CONTACT</button>
        <button onclick="swing('Power')" style="background: #e67e22;">POWER</button>
    </div>

    <script>
        let state = { score: 0, outs: 0, inning: 1, runners: 0 };
        const ball = document.getElementById('ball');
        const log = document.getElementById('log');

        function swing(type) {
            // Disable buttons during animation
            const btns = document.querySelectorAll('button');
            btns.forEach(b => b.disabled = true);
            
            // Start Pitch
            ball.style.display = 'block';
            ball.style.transition = 'bottom 0.4s ease-in';
            ball.style.bottom = '180px'; 

            setTimeout(() => {
                const roll = Math.random();
                let result = "";
                let difficulty = type === 'Power' ? 0.75 : 0.45;

                if (roll > difficulty) {
                    // HIT LOGIC
                    if (type === 'Power' && Math.random() > 0.6) {
                        result = "⚾ CRUSHED! HOME RUN!";
                        state.score += (state.runners + 1);
                        state.runners = 0;
                        ball.style.transition = 'bottom 0.8s ease-out';
                        ball.style.bottom = '600px';
                    } else {
                        result = "Line Drive Single!";
                        state.runners++;
                        if (state.runners > 3) { state.score++; state.runners = 3; }
                        ball.style.bottom = '120px';
                        ball.style.left = Math.random() > 0.5 ? '20%' : '80%';
                    }
                } else {
                    // OUT LOGIC
                    state.outs++;
                    result = roll < 0.15 ? "Strikeout!" : "Fly out to center.";
                    ball.style.display = 'none';
                }

                update(result);
                btns.forEach(b => b.disabled = false);
            }, 400);
        }

        function update(msg) {
            log.innerText = msg;
            document.getElementById('score').innerText = state.score;
            document.getElementById('outs').innerText = state.outs;
            document.getElementById('inning').innerText = state.inning;

            if (state.outs >= 3) {
                alert("Three Outs! Inning Over.");
                state.outs = 0;
                state.inning++;
                state.runners = 0;
                update("New Inning!");
            }

            setTimeout(() => {
                ball.style.transition = 'none';
                ball.style.display = 'none';
                ball.style.bottom = '40px';
                ball.style.left = '50%';
            }, 800);
        }
    </script>
</body>
</html>
"""

# Render the game
components.html(game_html, height=550)

st.caption("Instructions: Use Contact for a higher hit chance, or Power for a chance at a Home Run!")
