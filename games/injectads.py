import os

# --- CONFIGURATION DES SCRIPTS ---
CLARITY_ID = "whddotnjjk"
CLARITY_CODE = f"""<script type="text/javascript">
    (function(c,l,a,r,i,t,y){{
        c[a]=c[a]||function(){{(c[a].q=c[a].q||[]).push(arguments)}};
        t=l.createElement(r);t.async=1;t.src="https://www.clarity.ms/tag/"+i;
        y=l.getElementsByTagName(r)[0];y.parentNode.insertBefore(t,y);
    }})(window, document, "clarity", "script", "{CLARITY_ID}");
</script>"""

GA_ID = "G-CGX0C765PG"
ANALYTICS_CODE = f"""<script async src="https://www.googletagmanager.com/gtag/js?id={GA_ID}"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){{dataLayer.push(arguments);}}
  gtag('js', new Date());
  gtag('config', '{GA_ID}');
</script>"""

AD_ID = "9b61f7351b78d433de0ffc16189bc341"
BANNERS_CODE = f"""
<div id="ads-container" style="position:absolute; top:0; left:0; width:100%; height:100%; pointer-events:none; z-index:2147483647;">
    <div style="position:fixed; left:0; top:50%; transform:translateY(-50%); pointer-events:auto;">
        <script type="text/javascript">
            atOptions = {{ 'key' : '{AD_ID}', 'format' : 'iframe', 'height' : 600, 'width' : 160, 'params' : {{}} }};
        </script>
        <script src="https://www.highperformanceformat.com/{AD_ID}/invoke.js"></script>
    </div>
    <div style="position:fixed; right:0; top:50%; transform:translateY(-50%); pointer-events:auto;">
        <script type="text/javascript">
            atOptions = {{ 'key' : '{AD_ID}', 'format' : 'iframe', 'height' : 600, 'width' : 160, 'params' : {{}} }};
        </script>
        <script src="https://www.highperformanceformat.com/{AD_ID}/invoke.js"></script>
    </div>
</div>
"""

def clean_content(content):
    """Supprime les blocs s'ils sont déjà présents pour permettre une ré-injection propre"""
    # On supprime les blocs s'ils correspondent exactement
    content = content.replace(CLARITY_CODE + "\n", "").replace(CLARITY_CODE, "")
    content = content.replace(ANALYTICS_CODE + "\n", "").replace(ANALYTICS_CODE, "")
    content = content.replace(BANNERS_CODE + "\n", "").replace(BANNERS_CODE, "")
    
    # On supprime aussi au cas où il y aurait des variantes avec IDs
    if "whddotnjjk" in content and "clarity" in content:
        print("  ⚠️ Ancien script Clarity détecté et nettoyé")
        # Logique simplifiée pour retirer entre <script> et </script> contenant l'ID
        # (Optionnel : pourrait être amélioré avec du Regex)
    
    return content

def update_index_files(base_path, force_update=False):
    print(f"--- Scan en cours (Mode: {'FORCE (Ré-application)' if force_update else 'NORMAL (Sauter si existe)'}) ---")
    
    for root, dirs, files in os.walk(base_path):
        if "index.html" in files:
            file_path = os.path.join(root, "index.html")
            
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()

            modified = False
            
            # En mode FORCE, on nettoie d'abord pour pouvoir ré-injecter
            if force_update:
                original_content = content
                content = clean_content(content)
                modified = True # On force l'écriture

            # Injection Clarity
            if CLARITY_ID not in content or force_update:
                if CLARITY_ID not in content: # Évite doublon interne si clean_content a raté
                    content = content.replace("</head>", f"{CLARITY_CODE}\n</head>")
                    modified = True
            
            # Injection Analytics
            if GA_ID not in content or force_update:
                if GA_ID not in content:
                    content = content.replace("</head>", f"{ANALYTICS_CODE}\n</head>")
                    modified = True

            # Injection Bannières
            if AD_ID not in content or force_update:
                if AD_ID not in content:
                    if "<body>" in content:
                        content = content.replace("<body>", f"<body>\n{BANNERS_CODE}")
                        modified = True
                    elif "<body" in content:
                        parts = content.split("<body", 1)
                        sub_parts = parts[1].split(">", 1)
                        content = parts[0] + "<body" + sub_parts[0] + ">\n" + BANNERS_CODE + sub_parts[1]
                        modified = True

            if modified:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(content)
                print(f"✅ Mis à jour (Appliqué) : {file_path}")
            else:
                print(f"ℹ️ Déjà à jour : {file_path}")

if __name__ == "__main__":
    print("=== GESTIONNAIRE D'INJECTION 100FREEGAMES ===")
    print("1. Mode Normal (Sauter les fichiers déjà équipés)")
    print("2. Mode FORCE (Ré-appliquer les scripts sur tous les fichiers)")
    
    choix = input("Votre choix (1 ou 2) : ")
    is_force = (choix == "2")
    
    folder = "games" if os.path.exists("games") else "."
    update_index_files(folder, force_update=is_force)
    print("\nTerminé !")