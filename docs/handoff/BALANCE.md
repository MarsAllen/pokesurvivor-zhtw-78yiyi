# 數值總表（BALANCE）

> 由 `node tools/make_balance_doc.js` 從遊戲原始碼產生，**不要手改**；改了數值就重新產生。
> 名稱格式：西文原名（繁中）。時間單位為秒，除非另外註明。

## 1. 玩家成長

升級所需經驗：`Player.xpFor(level) = floor((8 + 6·level + 1.6·level^1.75) × 4)`（js/entities/player.js）

| 等級 | 升到下一級需要 | 累計 |
|---|---|---|
| 1 | 62 | 62 |
| 2 | 101 | 163 |
| 3 | 147 | 310 |
| 4 | 200 | 510 |
| 5 | 258 | 768 |
| 6 | 323 | 1091 |
| 7 | 392 | 1483 |
| 8 | 467 | 1950 |
| 9 | 547 | 2497 |
| 10 | 631 | 3128 |
| 15 | 1123 | 7716 |
| 20 | 1722 | 15087 |
| 25 | 2420 | 25753 |
| 30 | 3213 | 40195 |
| 35 | 4095 | 58869 |
| 40 | 5063 | 82215 |

### 升級卡片（局內強化，js/systems/levelup.js）

權重：新招式 10、招式強化 8、進化 40（有就必出）、能力卡 4（招式欄未滿）／7（已滿）／14（可解鎖進化）。三張卡依權重抽、不重複。

| id | 名稱 | 效果 | 本局上限 |
|---|---|---|---|
| hp | Vigor（活力） | 最大 HP +20（並回復等量 HP）。 | 無 |
| atk | Potencia（威力） | 所有招式傷害 +10%。 | 40 |
| spd | Carrera（衝刺） | 移動速度 +7%。 | 8 |
| cd | Reflejos（反射神經） | 所有招式冷卻 -8%。 | 10 |
| def | Coraza（護甲） | 傷害減免 +6%。 | 12 |
| rgn | Síntesis（光合作用） | 每秒回復 0.9 HP。 | 無 |
| mag | Imán（磁鐵） | 經驗值拾取範圍 +30%。 | 6 |
| xp | Aprendizaje（學習） | 獲得經驗值 +12%。 | 8 |
| heal | Baya Zidra（文柚果） | 立即回復 45% 的 HP。 | 無 |

## 2. 永久強化（每隻寶可夢各自購買，js/data/upgrades.js）

價格：`round(base × grow^目前等級 / 10) × 10` 寶可金幣。

| id | 名稱 | 每級效果 | 上限 | 第 1 級 | 最後一級 | 全部買完 |
|---|---|---|---|---|---|---|
| hp | Vitalidad（體力） | HP +8 | 10 | 60 | 890 | 3270 |
| atk | Fuerza（力量） | 傷害 +4% | 10 | 80 | 1450 | 5050 |
| spd | Zancada（步伐） | 速度 +3% | 8 | 70 | 740 | 2420 |
| cd | Reflejos（反射神經） | 冷卻 -3% | 8 | 90 | 1050 | 3340 |
| def | Coraza（護甲） | 防禦 +2% | 8 | 80 | 840 | 2750 |
| regen | Síntesis（光合作用） | HP 回復 +0.2/秒 | 5 | 120 | 610 | 1590 |
| magnet | Imán（磁鐵） | 拾取範圍 +12% | 6 | 50 | 270 | 820 |
| xp | Sabiduría（智慧） | 經驗值 +5% | 8 | 100 | 1160 | 3700 |
| coins | Fortuna（財運） | 寶可金幣 +8% | 8 | 120 | 1620 | 4950 |
| moves | Repertorio（招式庫） | 開局就有 2 個招式 | 1 | 1500 | 1500 | 1500 |
| crit | Golpe Crítico（會心一擊） | 會心機率 +3%（傷害 ×1.5） | 10 | 90 | 1860 | 6300 |
| reroll | Cambio de cartas（重抽卡片） | 每局升級卡片重抽次數 +1 | 5 | 150 | 980 | 2360 |
| ban | Veto（禁用） | 禁用 1 個招式：它永遠不會出現在你的卡片中 | 3 | 300 | 1080 | 1950 |

## 3. 屬性相剋（js/data/types.js）

原作把正作的倍率柔化：×2 → ×1.6、×0.5 → ×0.6、×0（無效）→ ×0.3；雙屬性相乘，夾在 [×0.3, ×2.4]。雙向適用（你打敵人、敵人打你）。

傷害公式：`招式 dmg × 玩家 atk（種族攻擊 × 強化 × 增益）× 屬性倍率 × 天氣倍率 × 會心 1.5`（js/systems/combat.js `hit()`）。

| 攻\守 | 一般 | 火 | 水 | 草 | 電 | 冰 | 格鬥 | 毒 | 地面 | 飛行 | 超能力 | 蟲 | 岩石 | 幽靈 | 龍 | 惡 | 鋼 | 妖精 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 一般 | · | · | · | · | · | · | · | · | · | · | · | · | 0.6 | 0.3 | · | · | 0.6 | · |
| 火 | · | 0.6 | 0.6 | 1.6 | · | 1.6 | · | · | · | · | · | 1.6 | 0.6 | · | 0.6 | · | 1.6 | · |
| 水 | · | 1.6 | 0.6 | 0.6 | · | · | · | · | 1.6 | · | · | · | 1.6 | · | 0.6 | · | · | · |
| 草 | · | 0.6 | 1.6 | 0.6 | · | · | · | 0.6 | 1.6 | 0.6 | · | 0.6 | 1.6 | · | 0.6 | · | 0.6 | · |
| 電 | · | · | 1.6 | 0.6 | 0.6 | · | · | · | 0.3 | 1.6 | · | · | · | · | 0.6 | · | · | · |
| 冰 | · | 0.6 | 0.6 | 1.6 | · | 0.6 | · | · | 1.6 | 1.6 | · | · | · | · | 1.6 | · | 0.6 | · |
| 格鬥 | 1.6 | · | · | · | · | 1.6 | · | 0.6 | · | 0.6 | 0.6 | 0.6 | 1.6 | 0.3 | · | 1.6 | 1.6 | 0.6 |
| 毒 | · | · | · | 1.6 | · | · | · | 0.6 | 0.6 | · | · | · | 0.6 | 0.6 | · | · | 0.3 | 1.6 |
| 地面 | · | 1.6 | · | 0.6 | 1.6 | · | · | 1.6 | · | 0.3 | · | 0.6 | 1.6 | · | · | · | 1.6 | · |
| 飛行 | · | · | · | 1.6 | 0.6 | · | 1.6 | · | · | · | · | 1.6 | 0.6 | · | · | · | 0.6 | · |
| 超能力 | · | · | · | · | · | · | 1.6 | 1.6 | · | · | 0.6 | · | · | · | · | 0.3 | 0.6 | · |
| 蟲 | · | 0.6 | · | 1.6 | · | · | 0.6 | 0.6 | · | 0.6 | 1.6 | · | · | 0.6 | · | 1.6 | 0.6 | 0.6 |
| 岩石 | · | 1.6 | · | · | · | 1.6 | 0.6 | · | 0.6 | 1.6 | · | 1.6 | · | · | · | · | 0.6 | · |
| 幽靈 | 0.3 | · | · | · | · | · | · | · | · | · | 1.6 | · | · | 1.6 | · | 0.6 | · | · |
| 龍 | · | · | · | · | · | · | · | · | · | · | · | · | · | · | 1.6 | · | 0.6 | 0.3 |
| 惡 | · | · | · | · | · | · | 0.6 | · | · | · | 1.6 | · | · | 1.6 | · | 0.6 | · | 0.6 |
| 鋼 | · | 0.6 | 0.6 | · | 0.6 | 1.6 | · | · | · | · | · | · | 1.6 | · | · | · | 0.6 | 1.6 |
| 妖精 | · | 0.6 | · | · | · | · | 1.6 | 0.6 | · | · | · | · | · | · | 1.6 | 1.6 | 0.6 | · |

## 4. 招式（64 個，js/data/moves.js）

同一隻寶可夢能學的招式＝自己的屬性＋一般屬性。只有「啟用中」的招式會發動（1–4 / Q / E 切換）。

| id | 名稱 | 屬性 | kind | cd | dmg | count | pierce | radius | 進化（條件） |
|---|---|---|---|---|---|---|---|---|---|
| tackle | Placaje（撞擊） | 一般 | melee | 0.5 | 16 |  |  | 60 | Derribo（猛撞）（Vigor（活力）） |
| quick-attack | Ataque Rápido（電光一閃） | 一般 | dash | 0.75 | 20 |  |  | 110 | Velocidad Extrema（神速）（Carrera（衝刺）） |
| swords-dance | Danza Espada（劍舞） | 一般 | buff | 0.85 |  |  |  |  | — |
| agility | Agilidad（高速移動） | 一般 | buff | 0.85 |  |  |  |  | — |
| harden | Fortaleza（變硬） | 一般 | buff | 0.85 |  |  |  |  | — |
| ember | Ascuas（火花） | 火 | projectile | 0.52 | 18 | 1 | 0 |  | Llamarada（大字爆炎）（Potencia（威力）） |
| flamethrower | Lanzallamas（噴射火焰） | 火 | cone | 0.7 | 7 | 7 | 1 |  | Sofoco（過熱）（Reflejos（反射神經）） |
| fire-spin | Giro Fuego（火焰旋渦） | 火 | orbit | 0.3 | 14 | 3 |  | 62 | Fuego Sagrado（神聖之火）（Síntesis（光合作用）） |
| heat-wave | Onda Ígnea（熱風） | 火 | nova | 1.25 | 13 | 10 | 1 |  | Erupción（噴火）（Vigor（活力）） |
| water-gun | Pistola Agua（水槍） | 水 | projectile | 0.44 | 14 | 1 | 1 |  | Escaldar（熱水）（Potencia（威力）） |
| bubble | Burbuja（泡沫） | 水 | nova | 1 | 9 | 8 | 0 |  | Surf（衝浪）（Carrera（衝刺）） |
| hydro-pump | Hidrobomba（水炮） | 水 | beam | 1.5 | 29 |  |  | 250 | Hidrocañón（加農水炮）（Potencia（威力）） |
| aqua-ring | Acua Aro（水流環） | 水 | buff | 0.9 |  |  |  |  | — |
| vine-whip | Látigo Cepa（藤鞭） | 草 | melee | 0.62 | 19 |  |  | 85 | Latigazo（強力鞭打）（Potencia（威力）） |
| razor-leaf | Hoja Afilada（飛葉快刀） | 草 | boomerang | 0.9 | 10 | 2 |  | 210 | Lluevehojas（飛葉風暴）（Reflejos（反射神經）） |
| leaf-storm | Tormenta Floral（落英繽紛） | 草 | orbit | 0.26 | 14 | 4 |  | 74 | Danza Pétalo（花瓣舞）（Síntesis（光合作用）） |
| giga-drain | Hierba Lazo（打草結） | 草 | aura | 0.55 | 9 |  |  | 76 | Planta Feroz（瘋狂植物）（Vigor（活力）） |
| thunder-shock | Impactrueno（電擊） | 電 | projectile | 0.4 | 13 | 1 | 2 |  | Trueno（打雷）（Potencia（威力）） |
| discharge | Chispazo（放電） | 電 | aura | 0.45 | 8 |  |  | 70 | Campo Eléctrico（電氣場地）（Coraza（護甲）） |
| thunderbolt | Rayo（十萬伏特） | 電 | chain | 0.95 | 21 | 4 |  | 140 | Electrocañón（電磁炮）（Reflejos（反射神經）） |
| confusion | Confusión（念力） | 超能力 | projectile | 0.58 | 13 | 1 | 0 |  | Psicocarga（精神衝擊）（Reflejos（反射神經）） |
| psybeam | Psicorrayo（幻象光線） | 超能力 | beam | 1.15 | 17 |  |  | 215 | Premonición（預知未來）（Potencia（威力）） |
| psychic | Psíquico（超能力） | 超能力 | nova | 1.35 | 10 | 12 | 1 |  | Vasta Fuerza（廣域戰力）（Imán（磁鐵）） |
| sludge | Residuos（污泥攻擊） | 毒 | projectile | 0.6 | 17 | 1 | 0 |  | Bomba Lodo（污泥炸彈）（Potencia（威力）） |
| mud-shot | Disparo Lodo（泥巴射擊） | 地面 | nova | 1.1 | 11 | 7 | 0 |  | Tierra Viva（大地之力）（Potencia（威力）） |
| gust | Tornado（起風） | 飛行 | orbit | 0.26 | 13 | 3 |  | 72 | Vendaval（暴風）（Carrera（衝刺）） |
| wing-attack | Ataque Ala（翅膀攻擊） | 飛行 | melee | 0.55 | 17 |  |  | 73 | Pájaro Osado（勇鳥猛攻）（Potencia（威力）） |
| body-slam | Golpe Cuerpo（泰山壓頂） | 一般 | melee | 0.95 | 36 |  |  | 58 | Gigaimpacto（終極衝擊）（Potencia（威力）） |
| hyper-voice | Vozarrón（巨聲） | 一般 | nova | 1.15 | 12 | 9 | 1 |  | Alboroto（吵鬧）（Reflejos（反射神經）） |
| poison-sting | Picotazo Veneno（毒針） | 毒 | projectile | 0.34 | 8 | 1 | 0 |  | Puya Nociva（毒擊）（Carrera（衝刺）） |
| toxic | Tóxico（劇毒） | 毒 | trail | 0.3 | 6 |  |  | 26 | Gas Venenoso（毒瓦斯）（Síntesis（光合作用）） |
| bulldoze | Terratemblor（重踏） | 地面 | aura | 0.7 | 11 |  |  | 80 | Terremoto（地震）（Potencia（威力）） |
| bug-bite | Picadura（蟲咬） | 蟲 | melee | 0.42 | 13 |  |  | 55 | Tijera X（十字剪）（Potencia（威力）） |
| string-shot | Disparo Demora（吐絲） | 蟲 | mine | 1.1 | 14 | 2 |  | 56 | Red Viscosa（黏黏網）（Reflejos（反射神經）） |
| bug-buzz | Zumbido（蟲鳴） | 蟲 | aura | 0.45 | 8 |  |  | 66 | Enjambre（蟲群）（Síntesis（光合作用）） |
| rock-throw | Lanzarrocas（落石） | 岩石 | projectile | 0.7 | 24 | 1 | 0 |  | Roca Afilada（尖石攻擊）（Potencia（威力）） |
| rock-slide | Avalancha（岩崩） | 岩石 | meteor | 1.3 | 21 | 3 |  | 46 | Trampa Rocas（隱形岩）（Reflejos（反射神經）） |
| ice-beam | Rayo Hielo（冰凍光束） | 冰 | beam | 1.1 | 20 |  |  | 220 | Ventisca（暴風雪）（Potencia（威力）） |
| powder-snow | Nieve Polvo（細雪） | 冰 | aura | 0.55 | 8 |  |  | 76 | Viento Hielo（冰凍之風）（Carrera（衝刺）） |
| karate-chop | Golpe Kárate（空手劈） | 格鬥 | melee | 0.5 | 22 |  |  | 63 | A Bocajarro（近身戰）（Potencia（威力）） |
| aura-sphere | Esfera Aural（波導彈） | 格鬥 | projectile | 0.62 | 17 | 1 | 0 |  | Onda Certera（真氣彈）（Reflejos（反射神經）） |
| lick | Lengüetazo（舌舔） | 幽靈 | melee | 0.48 | 14 |  |  | 60 | Puño Sombra（暗影拳）（Potencia（威力）） |
| shadow-ball | Bola Sombra（暗影球） | 幽靈 | projectile | 0.66 | 19 | 1 | 2 |  | Golpe Fantasma（潛靈奇襲）（Reflejos（反射神經）） |
| dragon-rage | Furia Dragón（龍之怒） | 龍 | beam | 1 | 24 |  |  | 230 | Cometa Draco（流星群）（Potencia（威力）） |
| dragon-dance | Danza Dragón（龍之舞） | 龍 | buff | 0.7 |  |  |  |  | — |
| fairy-wind | Viento Feérico（妖精之風） | 妖精 | nova | 1 | 11 | 10 | 0 |  | Fuerza Lunar（月亮之力）（Potencia（威力）） |
| dazzling-gleam | Brillo Mágico（魔法閃耀） | 妖精 | aura | 0.5 | 9 |  |  | 72 | Campo de Niebla（薄霧場地）（Síntesis（光合作用）） |
| metal-claw | Garra Metal（金屬爪） | 鋼 | melee | 0.5 | 18 |  |  | 63 | Cabeza de Hierro（鐵頭）（Potencia（威力）） |
| flash-cannon | Foco Resplandor（加農光炮） | 鋼 | beam | 1.05 | 23 |  |  | 220 | Rayo Metálico（鐵蹄光線）（Coraza（護甲）） |
| bite | Mordisco（咬住） | 惡 | melee | 0.45 | 17 |  |  | 58 | Triturar（咬碎）（Potencia（威力）） |
| dark-pulse | Pulso Umbrío（惡之波動） | 惡 | nova | 1.15 | 14 | 10 | 1 |  | Alarido（大聲咆哮）（Carrera（衝刺）） |
| night-shade | Tinieblas（黑夜魔影） | 惡 | aura | 0.5 | 9 |  |  | 72 | Pesadilla（惡夢）（Síntesis（光合作用）） |
| bonemerang | Huesomerang（骨頭回力鏢） | 地面 | boomerang | 0.95 | 16 | 1 |  | 230 | Ataque Óseo（骨棒亂打）（Potencia（威力）） |
| psycho-cut | Psicocorte（精神利刃） | 超能力 | boomerang | 0.8 | 9 | 2 |  | 200 | Psicocolmillo（精神之牙）（Reflejos（反射神經）） |
| spikes | Púas（撒菱） | 地面 | mine | 1.2 | 18 | 2 |  | 60 | Fisura（地裂）（Potencia（威力）） |
| toxic-spikes | Púas Tóxicas（毒菱） | 毒 | mine | 1.1 | 11 | 2 |  | 56 | Lanza Mugre（垃圾射擊）（Síntesis（光合作用）） |
| hail | Granizo（冰雹） | 冰 | meteor | 1.2 | 18 | 4 |  | 40 | Alud（雪崩）（Reflejos（反射神經）） |
| meteor-mash | Puño Meteoro（彗星拳） | 鋼 | meteor | 1.4 | 34 | 2 |  | 54 | Bomba Imán（磁鐵炸彈）（Potencia（威力）） |
| will-o-wisp | Fuego Fatuo（鬼火） | 火 | turret | 3.5 | 15 | 1 |  |  | Infierno（煉獄）（Reflejos（反射神經）） |
| substitute | Sustituto（替身） | 一般 | turret | 4 | 14 | 1 |  |  | Doble Equipo（影子分身）（Coraza（護甲）） |
| aerial-ace | Golpe Aéreo（燕返） | 飛行 | dash | 0.75 | 18 |  |  | 120 | Acróbata（雜技）（Carrera（衝刺）） |
| flame-wheel | Rueda Fuego（火焰輪） | 火 | trail | 0.28 | 10 |  |  | 28 | Envite Ígneo（閃焰衝鋒）（Carrera（衝刺）） |
| bubble-beam | Rayo Burbuja（泡沫光線） | 水 | cone | 0.65 | 6 | 7 |  |  | Acua Cola（水流尾）（Potencia（威力）） |
| hex | Infortunio（禍不單行） | 幽靈 | chain | 0.9 | 17 | 4 |  | 150 | Poltergeist（靈騷）（Imán（磁鐵）） |

### 每種 kind 的升級階梯（Lv1 → Lv5）

- **melee**：Lv2 傷害 +40%；Lv3 範圍 +25%；Lv4 冷卻 -25%；Lv5 360° 攻擊、傷害 +50%
- **dash**：Lv2 傷害 +40%；Lv3 距離 +30%；Lv4 冷卻 -25%；Lv5 傷害 +60%，範圍更寬
- **buff**：Lv2 最大層數 +1；Lv3 威力 +40%；Lv4 持續時間 +50%；Lv5 層數 +1、威力 +40%
- **projectile**：Lv2 投射物 +1；Lv3 傷害 +45%；Lv4 冷卻 -25%；Lv5 投射物 +1、貫穿 +1
- **cone**：Lv2 射擊次數 +3；Lv3 傷害 +40%；Lv4 範圍 +30%；Lv5 射擊次數 +3、貫穿 +1
- **orbit**：Lv2 光球 +1；Lv3 傷害 +55%；Lv4 半徑 +25%，旋轉更快；Lv5 光球 +1、傷害 +55%
- **nova**：Lv2 投射物 +4；Lv3 傷害 +40%；Lv4 冷卻 -25%；Lv5 投射物 +4、貫穿 +1
- **beam**：Lv2 傷害 +45%；Lv3 範圍與寬度 +30%；Lv4 冷卻 -25%；Lv5 傷害 +50%
- **boomerang**：Lv2 迴力鏢 +1；Lv3 傷害 +45%；Lv4 範圍 +30%；Lv5 迴力鏢 +1、傷害 +40%
- **aura**：Lv2 半徑 +30%；Lv3 傷害 +45%；Lv4 攻擊頻率提高 40%；Lv5 半徑 +30%、傷害 +50%
- **chain**：Lv2 跳躍次數 +2；Lv3 傷害 +45%；Lv4 冷卻 -25%；Lv5 跳躍次數 +2、傷害 +40%
- **trail**：Lv2 傷害 +40%；Lv3 持續時間 +40%；Lv4 毒池加大 30%；Lv5 傷害 +50%、半徑 +30%
- **mine**：Lv2 地雷 +1；Lv3 傷害 +50%；Lv4 爆炸半徑 +30%；Lv5 地雷 +1、冷卻 -25%
- **meteor**：Lv2 流星 +1；Lv3 傷害 +45%；Lv4 半徑 +30%；Lv5 流星 +2、冷卻 -20%
- **turret**：Lv2 傷害 +50%；Lv3 射擊速度提高 35%；Lv4 同時存在數量 +1；Lv5 持續時間 +50%、傷害 +40%

## 5. 敵人與生怪（js/data/enemies.js、js/systems/spawner.js）

每局開始時，每個階層從 BST 範圍內隨機選 7 隻當「本局陣容」（至少 1 隻支援型；第 2 階層起至少 1 隻預警攻擊型；最快的一隻變成 runner）。

| 階層 | 開始時間 | BST 範圍 | hp | spd | dmg | xp |
|---|---|---|---|---|---|---|
| 1 | 0 | 180–330 | 17 | 56 | 6 | 3.5 |
| 2 | 70 | 300–405 | 32 | 62 | 8.5 | 5 |
| 3 | 160 | 385–465 | 52 | 60 | 11 | 8 |
| 4 | 260 | 445–515 | 88 | 70 | 14 | 13 |
| 5 | 380 | 495–560 | 150 | 66 | 22 | 24 |
| 6 | 500 | 530–620 | 250 | 72 | 28 | 38 |

首領（非傳說，依 BST 抽選；實際數值為 hp × 1.35、dmg × 1.2）：

| 出現時間 | hp | dmg | xp | BST 範圍 |
|---|---|---|---|---|
| 180 | 1400 | 34 | 220 | 490–545 |
| 360 | 3200 | 42 | 420 | 520–580 |
| 540 | 5600 | 48 | 680 | 540–600 |
| 720 | 9000 | 56 | 1000 | 580–700 |
| 900 | 16000 | 68 | 1800 | 600–700 |

生怪常數：
- 同時在場上限：`const CAP = 64, ELITE_FROM = 0.85;`（js/systems/spawner.js:17）（達 85% 後新出的敵人是菁英：hp ×1.6、dmg ×1.25、xp ×1.6）
- 密度與倍率：`const DENSITY = 0.24, DMG_K = 2.4, XP_K = 5.6;`（js/systems/spawner.js:20）
- 額外血量：`const hpK = t => 3.3 + Math.min(1.7, t / 210);`（js/systems/spawner.js:23）
- 異色率：`const SHINY_RATE = 1 / 4096;`（js/systems/spawner.js:24）
- 隨時間成長：`return { hp: 1 + t / 95, dmg: 1 + t / 420, spd: 1 + Math.min(0.35, t / 1400) };`（js/data/enemies.js:177）
- 怪物潮：每 38–56 秒一次（首領戰期間暫停），數量 `(14 + floor(t/22)) × 0.4`。

| 分鐘 | 每秒生成數 rate(t) | hp 倍率（scale×hpK） | dmg 倍率（scale×2.4） |
|---|---|---|---|
| 0 | 0.384 | 3.3 | 2.4 |
| 1 | 0.907 | 5.85 | 2.743 |
| 2 | 1.554 | 8.762 | 3.086 |
| 3 | 2.29 | 12.034 | 3.429 |
| 5 | 3.976 | 19.661 | 4.114 |
| 7 | 5.906 | 27.105 | 4.8 |
| 10 | 9.193 | 36.579 | 5.829 |
| 15 | 15.572 | 52.368 | 7.543 |
| 20 | 22.93 | 68.158 | 9.257 |
| 25 | 31.16 | 83.947 | 10.971 |
| 30 | 40.186 | 99.737 | 12.686 |

## 6. 扭蛋（js/systems/gacha.js）

- 機率：1★ 45% · 2★ 30% · 3★ 17% · 4★ 6.5% · 5★ 1.5%
- 保底：`const PITY_5 = 70;`（js/systems/gacha.js:25）（每個卡池各自計算）；×10 連抽保證至少一隻 4★
- 異色：`const SHINY_RATE = 1 / 100;`（js/systems/gacha.js:26）
- 重複退款：`const REFUND = { 1: 15, 2: 30, 3: 60, 4: 120, 5: 300 };`（js/systems/gacha.js:27）（異色重複 ×3）
- 費用：×1 用 1 張獎券；×10 用 10 張獎券或 1 張 ×10 獎券。

## 7. 攜帶道具（每局一個，js/data/items.js）

| id | 名稱 | 效果 |
|---|---|---|
| leftovers | Restos（吃剩的東西） | 每秒回復 1.5% 的 HP。 |
| choiceband | Cinta Elección（講究頭帶） | 傷害 +40%，但無法切換招式。 |
| quickclaw | Garra Rápida（先制之爪） | 所有招式冷卻 -20%。 |
| focussash | Banda Focus（氣勢披帶） | 受到致命一擊時保留 1 HP（每 60 秒一次）。 |
| shellbell | Cascabel Concha（貝殼之鈴） | 造成傷害時回復 HP。 |
| amuletcoin | Moneda Amuleto（護符金幣） | 一局結束時寶可金幣 +50%。 |
| luckyegg | Huevo Suerte（幸運蛋） | 經驗值 +30%。 |
| lifeorb | Vidasfera（生命寶珠） | 傷害 +30%，但每次攻擊會消耗少量 HP。 |
| choicescarf | Pañuelo Elección（講究圍巾） | 速度 +35%。 |
| rockyhelmet | Casco Dentado（凸凸頭盔） | 近身攻擊你的敵人會受到傷害。 |
| assaultvest | Chaleco Asalto（突擊背心） | 傷害減免 +20%。 |

## 8. 一局的節奏

- 生態區每 240 秒切換：`const b = Math.floor(time / 240);`（js/game.js:637）
- 裂縫：`const CHECK = 30, CHANCE = 0.2, TTL = 45;`（js/systems/rift.js:25）；`const ARENA_R = 11, ARENA_TIME = 120, FROM = 75;`（js/systems/rift.js:26）
- 局中事件（怪物潮屬性、黃金時刻、迷路寶可夢）：`const EVERY = [240, 300], DUR = 30, LOST_TIME = 120;`（js/systems/events.js:22）
- 寶藏精靈：`const THIEF_FIRST = [120, 240], THIEF_NEXT = [240, 360], THIEF_LIFE = 15;`（js/systems/events.js:23）
- 天氣：`const FROM = 120, CHECK = 60, CHANCE = 0.18;`（js/systems/weather.js:37）
- 阿爾宙斯的審判：`const AT = 30 * 60;`（js/systems/judgment.js:32）；`const BOSS_EVERY = 5;               // sin tope: siguen saliendo mientras aguantes`（js/systems/judgment.js:34）
- 主迴圈：可變時間步長，每格上限 1/30 秒（`const dt = Math.min(1 / 30, real) * speedK;`（js/game.js:591））
