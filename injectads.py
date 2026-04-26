import os

# --- CONFIGURATION DES SCRIPTS ---
CLARITY_CODE = """<script type="text/javascript">
    (function(c,l,a,r,i,t,y){
        c[a]=c[a]||function(){(c[a].q=c[a].q||[]).push(arguments)};
        t=l.createElement(r);t.async=1;t.src="https://www.clarity.ms/tag/"+i;
        y=l.getElementsByTagName(r)[0];y.parentNode.insertBefore(t,y);
    })(window, document, "clarity", "script", "whddotnjjk");
</script>"""

ANALYTICS_CODE = """<script async src="https://www.googletagmanager.com/gtag/js?id=G-CGX0C765PG"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());
  gtag('config', 'G-CGX0C765PG');
</script>"""

# Configuration des bannières avec style pour les placer sur les côtés
BANNERS_CODE = """
<div style="position:fixed; left:0; top:50%; transform:translateY(-50%); z-index:9999; display:block;">
    <script type="text/javascript">
        atOptions = { 'key' : '9b61f7351b78d433de0ffc16189bc341', 'format' : 'iframe', 'height' : 600, 'width' : 160, 'params' : {} };
    </script>
    <script src="https://www.highperformanceformat.com/9b61f7351b78d433de0ffc16189bc341/invoke.js"></script>
</div>
<div style="position:fixed; right:0; top:50%; transform:translateY(-50%); z-index:9999; display:block;">
    <script type="text/javascript">
        atOptions = { 'key' : '9b61f7351b78d433de0ffc16189bc341', 'format' : 'iframe', 'height' : 600, 'width' : 160, 'params' : {} };
    </script>
    <script src="https://www.highperformanceformat.com/9b61f7351b78d433de0ffc16189bc341/invoke.js"></script>
</div>
"""

def update_index_files(base_path):
    for root, dirs, files in os.walk(base_path):
        if "index.html" in files:
            file_path = os.path.join(root, "index.html")
            
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()

            modified = False

            # 1. Injection Clarity (si absent)
            if "whddotnjjk" not in content:
                content = content.replace("</head>", f"{CLARITY_CODE}\n</head>")
                modified = True
            
            # 2. Injection Analytics (si absent)
            if "G-CGX0C765PG" not in content:
                content = content.replace("</head>", f"{ANALYTICS_CODE}\n</head>")
                modified = True

            # 3. Injection Bannières (si absentes)
            if "9b61f7351b78d433de0ffc16189bc341" not in content:
                # On injecte juste après l'ouverture de <body>
                content = content.replace("<body>", f"<body>\n{BANNERS_CODE}")
                modified = True

            if modified:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(content)
                print(f"✅ Mis à jour : {file_path}")
            else:
                print(f"ℹ️ Déjà à jour : {file_path}")

# Lancer le script dans le dossier games
if __name__ == "__main__":
    update_index_files("games")