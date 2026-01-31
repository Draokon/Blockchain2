# Supaprastintas Blockchain k8rimas

## Projekto tikslas
Sukurti supaprastintą blockchain sistemą, imituojančią:
- vartotojų kūrimą,
- transakcijų generavimą,
- blokų formavimą,
- Proof-of-Work kasimą,
- Merkle Tree naudojimą,
- decentralizuotą kasimo procesą.

---

##  Versija v0.1
✔️ Savadarbė hash funkcija  
✔️ User klasė (vardas, public_key, balansas)  
✔️ Transaction klasė (siuntėjas, gavėjas, suma, tx_id)  
✔️ Block klasė (transakcijos, previous_hash, block_hash)  
✔️ Paprastas blokų kūrimas  

---

## Versija v0.2 
✔️ Merkle Tree ir tikras Merkle Root  
✔️ Proof-of-Work (nonce, difficulty, hash prasideda 000...)  
✔️ Bloko antraštė (header):  
- version  
- timestamp  
- previous_hash  
- merkle_root  
- nonce  
- difficulty  

✔️ Transakcijų verifikacija:
- balanso tikrinimas,
- tx_id tikrinimas.

✔️ Decentralizuotas kasimas:
- generuojami 5 kandidatų blokai,
- bandoma juos kasti ribotą laiką / bandymų skaičių,
- jei nepavyksta – didinamos ribos ir kartojama.

---

##  Kaip paleisti

```bash
python main.py
