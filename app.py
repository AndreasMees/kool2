from flask import Flask, render_template, request, redirect, url_for
import json
import os

app = Flask(__name__)
HINNANGU_FAIL = 'hinnangud.json'

def loe_hinnangud():
    if not os.path.exists(HINNANGU_FAIL):
        with open(HINNANGU_FAIL, 'w', encoding='utf-8') as f:
            f.write('[]')
        return []

    try:
        with open(HINNANGU_FAIL, 'r', encoding='utf-8') as f:
            sisu = f.read().strip()
            if not sisu:
                return []
            return json.loads(sisu)
    except json.JSONDecodeError:
        with open(HINNANGU_FAIL, 'w', encoding='utf-8') as f:
            f.write('[]')
        return []

def salvesta_hinnangud(hinnangud):
    with open(HINNANGU_FAIL, 'w', encoding='utf-8') as f:
        json.dump(hinnangud, f, ensure_ascii=False, indent=2)

@app.route('/', methods=['GET', 'POST'])
def index():
    hinnangud = loe_hinnangud()
    if request.method == 'POST':
        aine = request.form.get('aine')
        nimi = request.form.get('nimi')
        hinne = request.form.get('hinne')
        kommentaar = request.form.get('kommentaar')

        if aine and nimi and hinne:
            uus_hinnang = {
                'aine': aine,
                'nimi': nimi,
                'hinne': int(hinne),
                'kommentaar': kommentaar or ''
            }
            hinnangud.append(uus_hinnang)
            salvesta_hinnangud(hinnangud)
        return redirect(url_for('index'))

    return render_template('index.html', hinnangud=hinnangud)

@app.route('/kustuta/<int:hinnang_id>', methods=['POST'])
def kustuta_hinnang(hinnang_id):
    hinnangud = loe_hinnangud()
    if 0 <= hinnang_id < len(hinnangud):
        hinnangud.pop(hinnang_id)
        salvesta_hinnangud(hinnangud)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
