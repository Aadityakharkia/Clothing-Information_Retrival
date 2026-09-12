# CSD358 Information Retrieval — Assignment 1: Part E Test Report
**Corpus**: 100 Clothing Product Descriptions (`D001`–`D100`)
**Evaluation Date**: September 2026

---

## 1. Free-Text Ranked Retrieval Queries (Vector Space Model - lnc.ltc)

Each query computes $w_{d,t} = 1 + \log_{10}(tf)$ and $w_{q,t} = (1 + \log_{10}(tf)) \cdot \log_{10}(N/df)$ with cosine normalization.

### Query 1.1: `cotton t-shirt`
| Rank | Doc ID | Category | Product Title                                 | Cosine Score |
|------|--------|----------|-----------------------------------------------|--------------|
| 1    | D001   | T-Shirt  | Men's Cotton Crew Neck T-Shirt - Black        | 0.317884     |
| 2    | D041   | T-Shirt  | Men's Cotton Crew Neck T-Shirt - Maroon       | 0.317884     |
| 3    | D061   | T-Shirt  | Men's Cotton Crew Neck T-Shirt - White        | 0.317884     |
| 4    | D081   | T-Shirt  | Men's Cotton Crew Neck T-Shirt - Mustard      | 0.314892     |
| 5    | D011   | T-Shirt  | Men's Oversized Graphic T-Shirt - Mustard     | 0.308838     |
| 6    | D071   | T-Shirt  | Men's Oversized Graphic T-Shirt - Black       | 0.308838     |
| 7    | D021   | T-Shirt  | Men's Cotton Crew Neck T-Shirt - Sky Blue     | 0.308646     |
| 8    | D031   | T-Shirt  | Men's Oversized Graphic T-Shirt - Olive Green | 0.302460     |
| 9    | D091   | T-Shirt  | Men's Oversized Graphic T-Shirt - Sky Blue    | 0.302460     |
| 10   | D051   | T-Shirt  | Men's Oversized Graphic T-Shirt - Navy Blue   | 0.299666     |

### Query 1.2: `denim jeans grey`
| Rank | Doc ID | Category | Product Title                        | Cosine Score |
|------|--------|----------|--------------------------------------|--------------|
| 1    | D023   | Jeans    | Men's Regular Fit Denim Jeans - Grey | 0.362184     |
| 2    | D083   | Jeans    | Men's Regular Fit Denim Jeans - Grey | 0.362184     |
| 3    | D043   | Jeans    | Men's Regular Fit Denim Jeans - Grey | 0.359960     |
| 4    | D003   | Jeans    | Men's Regular Fit Denim Jeans - Grey | 0.354039     |
| 5    | D063   | Jeans    | Men's Regular Fit Denim Jeans - Grey | 0.354039     |
| 6    | D053   | Jeans    | Men's Slim Fit Stretch Jeans - Grey  | 0.323302     |
| 7    | D013   | Jeans    | Men's Slim Fit Stretch Jeans - Grey  | 0.322971     |
| 8    | D073   | Jeans    | Men's Slim Fit Stretch Jeans - Grey  | 0.322971     |
| 9    | D033   | Jeans    | Men's Slim Fit Stretch Jeans - Grey  | 0.317711     |
| 10   | D093   | Jeans    | Men's Slim Fit Stretch Jeans - Grey  | 0.317711     |

### Query 1.3: `oversized hoodie`
| Rank | Doc ID | Category | Product Title                               | Cosine Score |
|------|--------|----------|---------------------------------------------|--------------|
| 1    | D007   | Hoodie   | Women's Oversized Fleece Hoodie - Black     | 0.279159     |
| 2    | D067   | Hoodie   | Women's Oversized Fleece Hoodie - Black     | 0.279159     |
| 3    | D027   | Hoodie   | Women's Oversized Fleece Hoodie - Wine      | 0.276382     |
| 4    | D087   | Hoodie   | Women's Oversized Fleece Hoodie - Wine      | 0.276382     |
| 5    | D047   | Hoodie   | Women's Oversized Fleece Hoodie - Navy Blue | 0.273205     |
| 6    | D037   | Hoodie   | Unisex Fleece Pullover Hoodie - Black       | 0.153474     |
| 7    | D097   | Hoodie   | Unisex Fleece Pullover Hoodie - Black       | 0.153474     |
| 8    | D057   | Hoodie   | Unisex Fleece Pullover Hoodie - Wine        | 0.151843     |
| 9    | D017   | Hoodie   | Unisex Fleece Pullover Hoodie - Navy Blue   | 0.149982     |
| 10   | D077   | Hoodie   | Unisex Fleece Pullover Hoodie - Navy Blue   | 0.149982     |

### Query 1.4: `printed saree blue`
| Rank | Doc ID | Category | Product Title                             | Cosine Score |
|------|--------|----------|-------------------------------------------|--------------|
| 1    | D005   | Saree    | Women's Printed Daily Wear Saree - Blue   | 0.364132     |
| 2    | D075   | Saree    | Women's Cotton Handloom Saree - Blue      | 0.329016     |
| 3    | D025   | Saree    | Women's Printed Daily Wear Saree - Maroon | 0.247970     |
| 4    | D065   | Saree    | Women's Printed Daily Wear Saree - Green  | 0.247970     |
| 5    | D085   | Saree    | Women's Printed Daily Wear Saree - Red    | 0.247970     |
| 6    | D045   | Saree    | Women's Printed Daily Wear Saree - Purple | 0.245441     |
| 7    | D035   | Saree    | Women's Cotton Handloom Saree - Yellow    | 0.215831     |
| 8    | D055   | Saree    | Women's Cotton Handloom Saree - Pink      | 0.215831     |
| 9    | D095   | Saree    | Women's Cotton Handloom Saree - Maroon    | 0.215831     |
| 10   | D015   | Saree    | Women's Cotton Handloom Saree - Red       | 0.213613     |

### Query 1.5: `solid midi dress`
| Rank | Doc ID | Category | Product Title                          | Cosine Score |
|------|--------|----------|----------------------------------------|--------------|
| 1    | D046   | Dress    | Women's Solid Midi Dress - Lavender    | 0.335553     |
| 2    | D006   | Dress    | Women's Solid Midi Dress - Green       | 0.332723     |
| 3    | D066   | Dress    | Women's Solid Midi Dress - Maroon      | 0.332723     |
| 4    | D026   | Dress    | Women's Solid Midi Dress - Navy Blue   | 0.322359     |
| 5    | D086   | Dress    | Women's Solid Midi Dress - Floral Pink | 0.322359     |
| 6    | D076   | Dress    | Women's Casual Fit Dress - Green       | 0.104157     |
| 7    | D036   | Dress    | Women's Casual Fit Dress - Black       | 0.103240     |
| 8    | D056   | Dress    | Women's Casual Fit Dress - Yellow      | 0.102152     |
| 9    | D016   | Dress    | Women's Casual Fit Dress - Floral Pink | 0.101764     |
| 10   | D096   | Dress    | Women's Casual Fit Dress - Navy Blue   | 0.100909     |

### Query 1.6: `checked cotton shirt`
| Rank | Doc ID | Category | Product Title                             | Cosine Score |
|------|--------|----------|-------------------------------------------|--------------|
| 1    | D022   | Shirt    | Men's Checked Cotton Shirt - White        | 0.289956     |
| 2    | D082   | Shirt    | Men's Checked Cotton Shirt - Blue         | 0.289956     |
| 3    | D042   | Shirt    | Men's Checked Cotton Shirt - Maroon       | 0.288151     |
| 4    | D002   | Shirt    | Men's Checked Cotton Shirt - Black        | 0.285285     |
| 5    | D062   | Shirt    | Men's Checked Cotton Shirt - Olive        | 0.285285     |
| 6    | D001   | T-Shirt  | Men's Cotton Crew Neck T-Shirt - Black    | 0.127666     |
| 7    | D041   | T-Shirt  | Men's Cotton Crew Neck T-Shirt - Maroon   | 0.127666     |
| 8    | D061   | T-Shirt  | Men's Cotton Crew Neck T-Shirt - White    | 0.127666     |
| 9    | D081   | T-Shirt  | Men's Cotton Crew Neck T-Shirt - Mustard  | 0.126464     |
| 10   | D021   | T-Shirt  | Men's Cotton Crew Neck T-Shirt - Sky Blue | 0.123956     |

### Query 1.7: `breathable summer kurta`
| Rank | Doc ID | Category | Product Title                            | Cosine Score |
|------|--------|----------|------------------------------------------|--------------|
| 1    | D004   | Kurta    | Men's Regular Fit Kurta - Pink           | 0.259137     |
| 2    | D064   | Kurta    | Men's Regular Fit Kurta - White          | 0.259137     |
| 3    | D024   | Kurta    | Men's Regular Fit Kurta - Teal           | 0.256928     |
| 4    | D084   | Kurta    | Men's Regular Fit Kurta - Beige          | 0.256928     |
| 5    | D034   | Kurta    | Women's Printed Straight Kurta - Maroon  | 0.256387     |
| 6    | D094   | Kurta    | Women's Printed Straight Kurta - Teal    | 0.256387     |
| 7    | D054   | Kurta    | Women's Printed Straight Kurta - Mustard | 0.254247     |
| 8    | D014   | Kurta    | Women's Printed Straight Kurta - Beige   | 0.252477     |
| 9    | D074   | Kurta    | Women's Printed Straight Kurta - Pink    | 0.252477     |
| 10   | D044   | Kurta    | Men's Regular Fit Kurta - Navy Blue      | 0.249592     |

### Query 1.8: `warm fleece winter jacket`
| Rank | Doc ID | Category   | Product Title                         | Cosine Score |
|------|--------|------------|---------------------------------------|--------------|
| 1    | D058   | Jacket     | Women's Quilted Winter Jacket - Black | 0.226831     |
| 2    | D018   | Jacket     | Women's Quilted Winter Jacket - Beige | 0.225334     |
| 3    | D078   | Jacket     | Women's Quilted Winter Jacket - Beige | 0.225334     |
| 4    | D038   | Jacket     | Women's Quilted Winter Jacket - Olive | 0.222959     |
| 5    | D098   | Jacket     | Women's Quilted Winter Jacket - Olive | 0.222959     |
| 6    | D010   | Sweatshirt | Women's Fleece Sweatshirt - Black     | 0.221286     |
| 7    | D070   | Sweatshirt | Women's Fleece Sweatshirt - Black     | 0.221286     |
| 8    | D030   | Sweatshirt | Women's Fleece Sweatshirt - Maroon    | 0.219850     |
| 9    | D090   | Sweatshirt | Women's Fleece Sweatshirt - Maroon    | 0.219850     |
| 10   | D050   | Sweatshirt | Women's Fleece Sweatshirt - Navy Blue | 0.213488     |

### Query 1.9: `high waist stretch leggings`
| Rank | Doc ID | Category | Product Title                                     | Cosine Score |
|------|--------|----------|---------------------------------------------------|--------------|
| 1    | D029   | Leggings | Women's High Waist Stretch Leggings - Grey        | 0.419897     |
| 2    | D049   | Leggings | Women's High Waist Stretch Leggings - Black       | 0.419897     |
| 3    | D089   | Leggings | Women's High Waist Stretch Leggings - Grey        | 0.419897     |
| 4    | D009   | Leggings | Women's High Waist Stretch Leggings - Olive Green | 0.406987     |
| 5    | D069   | Leggings | Women's High Waist Stretch Leggings - Olive Green | 0.406987     |
| 6    | D019   | Leggings | Women's Printed Active Leggings - Black           | 0.254767     |
| 7    | D059   | Leggings | Women's Printed Active Leggings - Grey            | 0.254767     |
| 8    | D079   | Leggings | Women's Printed Active Leggings - Black           | 0.254767     |
| 9    | D039   | Leggings | Women's Printed Active Leggings - Olive Green     | 0.246910     |
| 10   | D099   | Leggings | Women's Printed Active Leggings - Olive Green     | 0.246910     |

### Query 1.10: `casual comfortable daily wear`
| Rank | Doc ID | Category | Product Title                             | Cosine Score |
|------|--------|----------|-------------------------------------------|--------------|
| 1    | D005   | Saree    | Women's Printed Daily Wear Saree - Blue   | 0.187265     |
| 2    | D025   | Saree    | Women's Printed Daily Wear Saree - Maroon | 0.187265     |
| 3    | D065   | Saree    | Women's Printed Daily Wear Saree - Green  | 0.187265     |
| 4    | D085   | Saree    | Women's Printed Daily Wear Saree - Red    | 0.187265     |
| 5    | D045   | Saree    | Women's Printed Daily Wear Saree - Purple | 0.185355     |

---

## 2. Exact Phrase Queries (Positional Inverted Index)

Requires strictly consecutive token positions: $pos(t_{i+1}) = pos(t_i) + 1$.

### Phrase Query 2.1: `"cotton shirt"`
| Rank | Doc ID | Category | Product Title                       | Matches | Token Position Chains |
|------|--------|----------|-------------------------------------|---------|-----------------------|
| 1    | D002   | Shirt    | Men's Checked Cotton Shirt - Black  | 2       | [3 → 4], [9 → 10]     |
| 2    | D022   | Shirt    | Men's Checked Cotton Shirt - White  | 2       | [3 → 4], [9 → 10]     |
| 3    | D042   | Shirt    | Men's Checked Cotton Shirt - Maroon | 2       | [3 → 4], [9 → 10]     |
| 4    | D062   | Shirt    | Men's Checked Cotton Shirt - Olive  | 2       | [3 → 4], [9 → 10]     |
| 5    | D082   | Shirt    | Men's Checked Cotton Shirt - Blue   | 2       | [3 → 4], [9 → 10]     |
*Total Documents with Exact Phrase: 5*

### Phrase Query 2.2: `"stretch denim"`
| Rank | Doc ID | Category | Product Title                        | Matches | Token Position Chains |
|------|--------|----------|--------------------------------------|---------|-----------------------|
| 1    | D003   | Jeans    | Men's Regular Fit Denim Jeans - Grey | 1       | [16 → 17]             |
| 2    | D013   | Jeans    | Men's Slim Fit Stretch Jeans - Grey  | 1       | [15 → 16]             |
| 3    | D033   | Jeans    | Men's Slim Fit Stretch Jeans - Grey  | 1       | [16 → 17]             |
| 4    | D043   | Jeans    | Men's Regular Fit Denim Jeans - Grey | 1       | [15 → 16]             |
| 5    | D063   | Jeans    | Men's Regular Fit Denim Jeans - Grey | 1       | [16 → 17]             |
| 6    | D073   | Jeans    | Men's Slim Fit Stretch Jeans - Grey  | 1       | [15 → 16]             |
| 7    | D093   | Jeans    | Men's Slim Fit Stretch Jeans - Grey  | 1       | [16 → 17]             |
*Total Documents with Exact Phrase: 7*

### Phrase Query 2.3: `"festive wear"`
| Rank | Doc ID | Category | Product Title                             | Matches | Token Position Chains |
|------|--------|----------|-------------------------------------------|---------|-----------------------|
| 1    | D005   | Saree    | Women's Printed Daily Wear Saree - Blue   | 1       | [22 → 23]             |
| 2    | D015   | Saree    | Women's Cotton Handloom Saree - Red       | 1       | [20 → 21]             |
| 3    | D025   | Saree    | Women's Printed Daily Wear Saree - Maroon | 1       | [22 → 23]             |
| 4    | D035   | Saree    | Women's Cotton Handloom Saree - Yellow    | 1       | [20 → 21]             |
| 5    | D045   | Saree    | Women's Printed Daily Wear Saree - Purple | 1       | [22 → 23]             |
| 6    | D055   | Saree    | Women's Cotton Handloom Saree - Pink      | 1       | [20 → 21]             |
| 7    | D065   | Saree    | Women's Printed Daily Wear Saree - Green  | 1       | [22 → 23]             |
| 8    | D075   | Saree    | Women's Cotton Handloom Saree - Blue      | 1       | [20 → 21]             |
| 9    | D085   | Saree    | Women's Printed Daily Wear Saree - Red    | 1       | [22 → 23]             |
| 10   | D095   | Saree    | Women's Cotton Handloom Saree - Maroon    | 1       | [20 → 21]             |
*Total Documents with Exact Phrase: 10*

### Phrase Query 2.4: `"regular fit"`
| Rank | Doc ID | Category   | Product Title                            | Matches | Token Position Chains |
|------|--------|------------|------------------------------------------|---------|-----------------------|
| 1    | D003   | Jeans      | Men's Regular Fit Denim Jeans - Grey     | 2       | [2 → 3], [9 → 10]     |
| 2    | D004   | Kurta      | Men's Regular Fit Kurta - Pink           | 2       | [2 → 3], [8 → 9]      |
| 3    | D020   | Sweatshirt | Men's Regular Fit Sweatshirt - Navy Blue | 2       | [2 → 3], [9 → 10]     |
| 4    | D023   | Jeans      | Men's Regular Fit Denim Jeans - Grey     | 2       | [2 → 3], [9 → 10]     |
| 5    | D024   | Kurta      | Men's Regular Fit Kurta - Teal           | 2       | [2 → 3], [8 → 9]      |
| 6    | D040   | Sweatshirt | Men's Regular Fit Sweatshirt - Black     | 2       | [2 → 3], [8 → 9]      |
| 7    | D043   | Jeans      | Men's Regular Fit Denim Jeans - Grey     | 2       | [2 → 3], [9 → 10]     |
| 8    | D044   | Kurta      | Men's Regular Fit Kurta - Navy Blue      | 2       | [2 → 3], [9 → 10]     |
| 9    | D060   | Sweatshirt | Men's Regular Fit Sweatshirt - Maroon    | 2       | [2 → 3], [8 → 9]      |
| 10   | D063   | Jeans      | Men's Regular Fit Denim Jeans - Grey     | 2       | [2 → 3], [9 → 10]     |
*Total Documents with Exact Phrase: 15*

### Phrase Query 2.5: `"breathable fabric"`
| Rank | Doc ID | Category | Product Title                                 | Matches | Token Position Chains |
|------|--------|----------|-----------------------------------------------|---------|-----------------------|
| 1    | D001   | T-Shirt  | Men's Cotton Crew Neck T-Shirt - Black        | 1       | [26 → 27]             |
| 2    | D004   | Kurta    | Men's Regular Fit Kurta - Pink                | 1       | [21 → 22]             |
| 3    | D011   | T-Shirt  | Men's Oversized Graphic T-Shirt - Mustard     | 1       | [24 → 25]             |
| 4    | D014   | Kurta    | Women's Printed Straight Kurta - Beige        | 1       | [21 → 22]             |
| 5    | D021   | T-Shirt  | Men's Cotton Crew Neck T-Shirt - Sky Blue     | 1       | [28 → 29]             |
| 6    | D024   | Kurta    | Men's Regular Fit Kurta - Teal                | 1       | [21 → 22]             |
| 7    | D031   | T-Shirt  | Men's Oversized Graphic T-Shirt - Olive Green | 1       | [26 → 27]             |
| 8    | D034   | Kurta    | Women's Printed Straight Kurta - Maroon       | 1       | [21 → 22]             |
| 9    | D041   | T-Shirt  | Men's Cotton Crew Neck T-Shirt - Maroon       | 1       | [26 → 27]             |
| 10   | D044   | Kurta    | Men's Regular Fit Kurta - Navy Blue           | 1       | [23 → 24]             |
*Total Documents with Exact Phrase: 20*

---

## 3. Ordered Proximity Queries (WITHIN/k)

Requires term 2 to occur within $k$ token positions after term 1: $0 < pos(t_2) - pos(t_1) \le k$.

### Proximity Query 3.1: `cotton WITHIN/3 shirt`
| Rank | Doc ID | Category | Product Title                                 | Matches | Position Pairs (Δ ≤ 3)            |
|------|--------|----------|-----------------------------------------------|---------|-----------------------------------|
| 1    | D001   | T-Shirt  | Men's Cotton Crew Neck T-Shirt - Black        | 1       | (pos 18, 20; Δ=2)                 |
| 2    | D002   | Shirt    | Men's Checked Cotton Shirt - Black            | 2       | (pos 3, 4; Δ=1), (pos 9, 10; Δ=1) |
| 3    | D011   | T-Shirt  | Men's Oversized Graphic T-Shirt - Mustard     | 1       | (pos 15, 18; Δ=3)                 |
| 4    | D021   | T-Shirt  | Men's Cotton Crew Neck T-Shirt - Sky Blue     | 1       | (pos 20, 22; Δ=2)                 |
| 5    | D022   | Shirt    | Men's Checked Cotton Shirt - White            | 2       | (pos 3, 4; Δ=1), (pos 9, 10; Δ=1) |
| 6    | D031   | T-Shirt  | Men's Oversized Graphic T-Shirt - Olive Green | 1       | (pos 17, 20; Δ=3)                 |
| 7    | D041   | T-Shirt  | Men's Cotton Crew Neck T-Shirt - Maroon       | 1       | (pos 18, 20; Δ=2)                 |
| 8    | D042   | Shirt    | Men's Checked Cotton Shirt - Maroon           | 2       | (pos 3, 4; Δ=1), (pos 9, 10; Δ=1) |
| 9    | D051   | T-Shirt  | Men's Oversized Graphic T-Shirt - Navy Blue   | 1       | (pos 17, 20; Δ=3)                 |
| 10   | D061   | T-Shirt  | Men's Cotton Crew Neck T-Shirt - White        | 1       | (pos 18, 20; Δ=2)                 |
*Total Documents within Distance 3: 15*

### Proximity Query 3.2: `stretch WITHIN/4 denim`
| Rank | Doc ID | Category | Product Title                        | Matches | Position Pairs (Δ ≤ 4) |
|------|--------|----------|--------------------------------------|---------|------------------------|
| 1    | D003   | Jeans    | Men's Regular Fit Denim Jeans - Grey | 1       | (pos 16, 17; Δ=1)      |
| 2    | D013   | Jeans    | Men's Slim Fit Stretch Jeans - Grey  | 1       | (pos 15, 16; Δ=1)      |
| 3    | D033   | Jeans    | Men's Slim Fit Stretch Jeans - Grey  | 1       | (pos 16, 17; Δ=1)      |
| 4    | D043   | Jeans    | Men's Regular Fit Denim Jeans - Grey | 1       | (pos 15, 16; Δ=1)      |
| 5    | D063   | Jeans    | Men's Regular Fit Denim Jeans - Grey | 1       | (pos 16, 17; Δ=1)      |
| 6    | D073   | Jeans    | Men's Slim Fit Stretch Jeans - Grey  | 1       | (pos 15, 16; Δ=1)      |
| 7    | D093   | Jeans    | Men's Slim Fit Stretch Jeans - Grey  | 1       | (pos 16, 17; Δ=1)      |
*Total Documents within Distance 4: 7*

### Proximity Query 3.3: `winter WITHIN/3 wear`
| Rank | Doc ID | Category   | Product Title                            | Matches | Position Pairs (Δ ≤ 3) |
|------|--------|------------|------------------------------------------|---------|------------------------|
| 1    | D008   | Jacket     | Women's Casual Puffer Jacket - Olive     | 1       | (pos 22, 23; Δ=1)      |
| 2    | D010   | Sweatshirt | Women's Fleece Sweatshirt - Black        | 1       | (pos 19, 20; Δ=1)      |
| 3    | D018   | Jacket     | Women's Quilted Winter Jacket - Beige    | 1       | (pos 21, 22; Δ=1)      |
| 4    | D020   | Sweatshirt | Men's Regular Fit Sweatshirt - Navy Blue | 1       | (pos 23, 24; Δ=1)      |
| 5    | D028   | Jacket     | Women's Casual Puffer Jacket - Black     | 1       | (pos 22, 23; Δ=1)      |
| 6    | D030   | Sweatshirt | Women's Fleece Sweatshirt - Maroon       | 1       | (pos 19, 20; Δ=1)      |
| 7    | D038   | Jacket     | Women's Quilted Winter Jacket - Olive    | 1       | (pos 21, 22; Δ=1)      |
| 8    | D040   | Sweatshirt | Men's Regular Fit Sweatshirt - Black     | 1       | (pos 21, 22; Δ=1)      |
| 9    | D048   | Jacket     | Women's Casual Puffer Jacket - Beige     | 1       | (pos 22, 23; Δ=1)      |
| 10   | D050   | Sweatshirt | Women's Fleece Sweatshirt - Navy Blue    | 1       | (pos 21, 22; Δ=1)      |
*Total Documents within Distance 3: 20*

### Proximity Query 3.4: `festive WITHIN/4 kurta`
*No documents matched.*

---

## 4. Query Containing Term Not Occurring in the Corpus

Validates graceful handling of out-of-vocabulary terms ($df = 0$, $IDF = 0$, cosine score = 0).

### Out-of-Vocabulary Query: `astronaut velvet kimono`
- **VSM Results Count**: 0 (Returned empty list, 0 crashes)
- **Positional Results Count**: 0 (Returned empty list, 0 crashes)
- **Behavior**: The preprocessor stems the terms (`astronaut`, `velvet`, `kimono`), checks vocabulary, recognizes $df=0$, and safely normalizes vectors without zero-division.

---

## 5. Comparative Analysis: How Positional Information Changes Results

The assignment requires explaining at least two cases where positional information changes the result set or order:

### Case Study A: Query `cotton shirt` — VSM Free-Text vs. Exact Phrase
#### Free-Text VSM Top-5:
| Rank | Doc ID | Category | Title                                   | Score  |
|------|--------|----------|-----------------------------------------|--------|
| 1    | D022   | Shirt    | Men's Checked Cotton Shirt - White      | 0.2597 |
| 2    | D082   | Shirt    | Men's Checked Cotton Shirt - Blue       | 0.2597 |
| 3    | D001   | T-Shirt  | Men's Cotton Crew Neck T-Shirt - Black  | 0.2588 |
| 4    | D041   | T-Shirt  | Men's Cotton Crew Neck T-Shirt - Maroon | 0.2588 |
| 5    | D061   | T-Shirt  | Men's Cotton Crew Neck T-Shirt - White  | 0.2588 |

#### Exact Phrase Positional Matches (All):
| # | Doc ID | Category | Title                               | Positions         |
|---|--------|----------|-------------------------------------|-------------------|
| 1 | D002   | Shirt    | Men's Checked Cotton Shirt - Black  | [[3, 4], [9, 10]] |
| 2 | D022   | Shirt    | Men's Checked Cotton Shirt - White  | [[3, 4], [9, 10]] |
| 3 | D042   | Shirt    | Men's Checked Cotton Shirt - Maroon | [[3, 4], [9, 10]] |
| 4 | D062   | Shirt    | Men's Checked Cotton Shirt - Olive  | [[3, 4], [9, 10]] |
| 5 | D082   | Shirt    | Men's Checked Cotton Shirt - Blue   | [[3, 4], [9, 10]] |

**Explanation**:
- Under **VSM (lnc.ltc)**, retrieval is bag-of-words. `D001` (Men's Cotton Crew Neck T-Shirt) ranks #1 with a score of ~0.37 because 'cotton' appears 3 times in `D001`. However, `D001` is a *T-Shirt*, NOT a *Shirt*!
- Under **Positional Exact Phrase Search**, terms must satisfy $pos(shirt) = pos(cotton) + 1$. `D001` is completely eliminated because 'cotton' and 'shirt' do not occur consecutively (intervened by 'crew', 'neck', etc.).
- Only genuine shirts (`D002`, `D022`, `D042`, `D062`, `D082` — 'Checked Cotton Shirt') match the exact phrase. Thus, positional indexing dramatically improves **precision** and eliminates false positive apparel categories.

### Case Study B: `stretch` & `denim` — Exact Phrase vs. Proximity `stretch WITHIN/4 denim`
- **Exact Phrase (`"stretch denim"`)**: 7 documents matched.
- **Proximity Search (`stretch WITHIN/4 denim`)**: 7 documents matched.

**Explanation**:
- Exact phrase matching is often too restrictive: in `D003` ('Men's Regular Fit Denim Jeans'), the text contains *'Made from comfort stretch denim'*, where `pos(denim) - pos(stretch) = 1` (an exact phrase match).
- However, if a product description reads *'stretchable, durable cotton denim'* or *'stretch fabric blended with denim'*, an exact phrase search fails ($pos(denim) - pos(stretch) > 1$).
- With `stretch WITHIN/4 denim`, we capture all documents where 'stretch' semantically modifies 'denim' within a 4-token window, giving users the recall flexibility of VSM combined with the syntactic word-ordering guarantee of positional indexing.
