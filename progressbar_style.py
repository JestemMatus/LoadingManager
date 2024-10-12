html_content = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Loading...</title>
    <style>
        body {
            font-family: 'Arial', sans-serif;
            background-color: transparent;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
            margin: 0;
        }

        .progress-main-container {
            padding: 50px 30px;
            background: rgba(0, 0, 0, 0.8);
            backdrop-filter: blur(15px);
            border-radius: 16px;
            box-shadow: 0 10px 20px rgba(0, 0, 0, 0.2);
            display: flex;
            justify-content: center;
            align-items: center;
            max-width: 650px;
            width: 80%;
            border: 1px solid rgba(0, 0, 0, 0.2);
            opacity: 0;
            transform: translateY(-20px);
            animation: fadeIn 0.5s forwards ease-in-out;
        }

        .progress-container {
            width: 100%;
            max-width: 750px;
            background-color: #0d0d0d;
            border-radius: 16px;
            overflow: hidden;
            box-shadow: 0 6px 12px rgba(0, 0, 0, 0.2);
            position: relative;
            height: 50px;
        }

        .progress-bar {
            height: 100%;
            width: 33%;
            background: linear-gradient(90deg, #007bff, #003b75);
            animation: infiniteProgress 2s linear infinite;
            position: absolute;
            top: 0;
            left: 0;
            border-radius: 16px;
            z-index: 1;
        }

        .progress-bar-text {
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 24px;
            font-weight: bold;
            color: #ffffff;
            text-align: center;
            z-index: 2;
            text-shadow: 2px 2px 5px rgba(0, 0, 0, 0.8);
        }

        .progress-bar::after {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            height: 100%;
            width: 100%;
            background: linear-gradient(45deg,
                    rgba(255, 255, 255, 0.1) 25%,
                    transparent 25%,
                    transparent 50%,
                    rgba(255, 255, 255, 0.1) 50%,
                    rgba(255, 255, 255, 0.1) 75%,
                    transparent 75%,
                    transparent);
            background-size: 40px 40px;
            animation: move 1.5s linear infinite;
            border-radius: 16px;
            z-index: 0;
        }

        @keyframes infiniteProgress {
            0% { left: -25%; }
            100% { left: 100%; }
        }

        @keyframes move {
            0% { background-position: 0 0; }
            100% { background-position: 40px 40px; }
        }

        @keyframes fadeIn {
            0% {
                opacity: 0;
                transform: translateY(-20px);
            }
            100% {
                opacity: 1;
                transform: translateY(0);
            }
        }
    </style>
</head>
<body>
    <div class="progress-main-container">
        <div class="progress-container">
            <div class="progress-bar"></div>
            <span class="progress-bar-text">Loading...</span>
        </div>
    </div>
</body>
</html>
"""
