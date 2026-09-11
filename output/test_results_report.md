# Information Retrieval Assignment-1 (CSD358) - Comprehensive Test Report

**Corpus Size**: 100 Documents (D001 - D100)
**Weighting Scheme**: Vector Space Model `lnc.ltc` with Cosine Normalization
**Positional Indexing**: Exact Phrase (`k=1`) & Ordered Proximity (`WITHIN/k`)

---

## 1. Free-Text Queries (VSM `lnc.ltc`)

### Query 1: `breathable cotton t-shirt`

| Rank | Doc ID | Category | Product Title | Cosine Score |
|:---:|:---:|:---:|:---|:---:|
| 1 | **D001** | T-Shirt | Men's Cotton Crew Neck T-Shirt - Black | `0.344806` |
| 2 | **D041** | T-Shirt | Men's Cotton Crew Neck T-Shirt - Maroon | `0.344806` |
| 3 | **D061** | T-Shirt | Men's Cotton Crew Neck T-Shirt - White | `0.344806` |
| 4 | **D081** | T-Shirt | Men's Cotton Crew Neck T-Shirt - Mustard | `0.341561` |
| 5 | **D011** | T-Shirt | Men's Oversized Graphic T-Shirt - Mustard | `0.337700` |
| 6 | **D071** | T-Shirt | Men's Oversized Graphic T-Shirt - Black | `0.337700` |
| 7 | **D021** | T-Shirt | Men's Cotton Crew Neck T-Shirt - Sky Blue | `0.334786` |
| 8 | **D031** | T-Shirt | Men's Oversized Graphic T-Shirt - Olive Green | `0.330725` |
| 9 | **D091** | T-Shirt | Men's Oversized Graphic T-Shirt - Sky Blue | `0.330725` |
| 10 | **D051** | T-Shirt | Men's Oversized Graphic T-Shirt - Navy Blue | `0.327670` |

### Query 2: `black slim fit casual shirt`

| Rank | Doc ID | Category | Product Title | Cosine Score |
|:---:|:---:|:---:|:---|:---:|
| 1 | **D072** | Shirt | Women's Striped Casual Shirt - Black | `0.347243` |
| 2 | **D002** | Shirt | Men's Checked Cotton Shirt - Black | `0.342012` |
| 3 | **D052** | Shirt | Women's Striped Casual Shirt - Beige | `0.235542` |
| 4 | **D022** | Shirt | Men's Checked Cotton Shirt - White | `0.234309` |
| 5 | **D082** | Shirt | Men's Checked Cotton Shirt - Blue | `0.234309` |
| 6 | **D012** | Shirt | Women's Striped Casual Shirt - Blue | `0.234060` |
| 7 | **D042** | Shirt | Men's Checked Cotton Shirt - Maroon | `0.232850` |
| 8 | **D092** | Shirt | Women's Striped Casual Shirt - White | `0.231708` |
| 9 | **D062** | Shirt | Men's Checked Cotton Shirt - Olive | `0.230534` |
| 10 | **D032** | Shirt | Women's Striped Casual Shirt - Light Pink | `0.226813` |

### Query 3: `stretch denim jeans grey`

| Rank | Doc ID | Category | Product Title | Cosine Score |
|:---:|:---:|:---:|:---|:---:|
| 1 | **D013** | Jeans | Men's Slim Fit Stretch Jeans - Grey | `0.383230` |
| 2 | **D073** | Jeans | Men's Slim Fit Stretch Jeans - Grey | `0.383230` |
| 3 | **D043** | Jeans | Men's Regular Fit Denim Jeans - Grey | `0.382853` |
| 4 | **D033** | Jeans | Men's Slim Fit Stretch Jeans - Grey | `0.376988` |
| 5 | **D093** | Jeans | Men's Slim Fit Stretch Jeans - Grey | `0.376988` |
| 6 | **D003** | Jeans | Men's Regular Fit Denim Jeans - Grey | `0.376556` |
| 7 | **D063** | Jeans | Men's Regular Fit Denim Jeans - Grey | `0.376556` |
| 8 | **D053** | Jeans | Men's Slim Fit Stretch Jeans - Grey | `0.371454` |
| 9 | **D023** | Jeans | Men's Regular Fit Denim Jeans - Grey | `0.315404` |
| 10 | **D083** | Jeans | Men's Regular Fit Denim Jeans - Grey | `0.315404` |

### Query 4: `festive wear saree printed border`

| Rank | Doc ID | Category | Product Title | Cosine Score |
|:---:|:---:|:---:|:---|:---:|
| 1 | **D005** | Saree | Women's Printed Daily Wear Saree - Blue | `0.320222` |
| 2 | **D025** | Saree | Women's Printed Daily Wear Saree - Maroon | `0.320222` |
| 3 | **D065** | Saree | Women's Printed Daily Wear Saree - Green | `0.320222` |
| 4 | **D085** | Saree | Women's Printed Daily Wear Saree - Red | `0.320222` |
| 5 | **D045** | Saree | Women's Printed Daily Wear Saree - Purple | `0.316955` |
| 6 | **D035** | Saree | Women's Cotton Handloom Saree - Yellow | `0.290889` |
| 7 | **D055** | Saree | Women's Cotton Handloom Saree - Pink | `0.290889` |
| 8 | **D095** | Saree | Women's Cotton Handloom Saree - Maroon | `0.290889` |
| 9 | **D015** | Saree | Women's Cotton Handloom Saree - Red | `0.287900` |
| 10 | **D075** | Saree | Women's Cotton Handloom Saree - Blue | `0.287900` |

### Query 5: `women winter warm fleece hoodie`

| Rank | Doc ID | Category | Product Title | Cosine Score |
|:---:|:---:|:---:|:---|:---:|
| 1 | **D007** | Hoodie | Women's Oversized Fleece Hoodie - Black | `0.305567` |
| 2 | **D067** | Hoodie | Women's Oversized Fleece Hoodie - Black | `0.305567` |
| 3 | **D037** | Hoodie | Unisex Fleece Pullover Hoodie - Black | `0.303133` |
| 4 | **D097** | Hoodie | Unisex Fleece Pullover Hoodie - Black | `0.303133` |
| 5 | **D027** | Hoodie | Women's Oversized Fleece Hoodie - Wine | `0.302528` |
| 6 | **D087** | Hoodie | Women's Oversized Fleece Hoodie - Wine | `0.302528` |
| 7 | **D057** | Hoodie | Unisex Fleece Pullover Hoodie - Wine | `0.299913` |
| 8 | **D047** | Hoodie | Women's Oversized Fleece Hoodie - Navy Blue | `0.299050` |
| 9 | **D017** | Hoodie | Unisex Fleece Pullover Hoodie - Navy Blue | `0.296236` |
| 10 | **D077** | Hoodie | Unisex Fleece Pullover Hoodie - Navy Blue | `0.296236` |

### Query 6: `comfortable kurta everyday Indian wear`

| Rank | Doc ID | Category | Product Title | Cosine Score |
|:---:|:---:|:---:|:---|:---:|
| 1 | **D004** | Kurta | Men's Regular Fit Kurta - Pink | `0.214611` |
| 2 | **D064** | Kurta | Men's Regular Fit Kurta - White | `0.214611` |
| 3 | **D024** | Kurta | Men's Regular Fit Kurta - Teal | `0.212781` |
| 4 | **D084** | Kurta | Men's Regular Fit Kurta - Beige | `0.212781` |
| 5 | **D034** | Kurta | Women's Printed Straight Kurta - Maroon | `0.212334` |
| 6 | **D094** | Kurta | Women's Printed Straight Kurta - Teal | `0.212334` |
| 7 | **D054** | Kurta | Women's Printed Straight Kurta - Mustard | `0.210561` |
| 8 | **D014** | Kurta | Women's Printed Straight Kurta - Beige | `0.209095` |
| 9 | **D074** | Kurta | Women's Printed Straight Kurta - Pink | `0.209095` |
| 10 | **D044** | Kurta | Men's Regular Fit Kurta - Navy Blue | `0.206706` |

### Query 7: `quilted puffer jacket lightweight`

| Rank | Doc ID | Category | Product Title | Cosine Score |
|:---:|:---:|:---:|:---|:---:|
| 1 | **D028** | Jacket | Women's Casual Puffer Jacket - Black | `0.347786` |
| 2 | **D088** | Jacket | Women's Casual Puffer Jacket - Black | `0.347786` |
| 3 | **D048** | Jacket | Women's Casual Puffer Jacket - Beige | `0.345538` |
| 4 | **D008** | Jacket | Women's Casual Puffer Jacket - Olive | `0.341972` |
| 5 | **D068** | Jacket | Women's Casual Puffer Jacket - Olive | `0.341972` |
| 6 | **D058** | Jacket | Women's Quilted Winter Jacket - Black | `0.256909` |
| 7 | **D018** | Jacket | Women's Quilted Winter Jacket - Beige | `0.255213` |
| 8 | **D078** | Jacket | Women's Quilted Winter Jacket - Beige | `0.255213` |
| 9 | **D038** | Jacket | Women's Quilted Winter Jacket - Olive | `0.252524` |
| 10 | **D098** | Jacket | Women's Quilted Winter Jacket - Olive | `0.252524` |

### Query 8: `high waist stretch leggings olive`

| Rank | Doc ID | Category | Product Title | Cosine Score |
|:---:|:---:|:---:|:---|:---:|
| 1 | **D009** | Leggings | Women's High Waist Stretch Leggings - Olive Green | `0.455117` |
| 2 | **D069** | Leggings | Women's High Waist Stretch Leggings - Olive Green | `0.455117` |
| 3 | **D029** | Leggings | Women's High Waist Stretch Leggings - Grey | `0.373453` |
| 4 | **D049** | Leggings | Women's High Waist Stretch Leggings - Black | `0.373453` |
| 5 | **D089** | Leggings | Women's High Waist Stretch Leggings - Grey | `0.373453` |
| 6 | **D039** | Leggings | Women's Printed Active Leggings - Olive Green | `0.312888` |
| 7 | **D099** | Leggings | Women's Printed Active Leggings - Olive Green | `0.312888` |
| 8 | **D019** | Leggings | Women's Printed Active Leggings - Black | `0.226588` |
| 9 | **D059** | Leggings | Women's Printed Active Leggings - Grey | `0.226588` |
| 10 | **D079** | Leggings | Women's Printed Active Leggings - Black | `0.226588` |

### Query 9: `casual fit dress minimal shrinkage`

| Rank | Doc ID | Category | Product Title | Cosine Score |
|:---:|:---:|:---:|:---|:---:|
| 1 | **D036** | Dress | Women's Casual Fit Dress - Black | `0.339248` |
| 2 | **D096** | Dress | Women's Casual Fit Dress - Navy Blue | `0.331587` |
| 3 | **D006** | Dress | Women's Solid Midi Dress - Green | `0.316787` |
| 4 | **D066** | Dress | Women's Solid Midi Dress - Maroon | `0.316787` |
| 5 | **D024** | Kurta | Men's Regular Fit Kurta - Teal | `0.196168` |
| 6 | **D084** | Kurta | Men's Regular Fit Kurta - Beige | `0.196168` |
| 7 | **D076** | Dress | Women's Casual Fit Dress - Green | `0.190131` |
| 8 | **D060** | Sweatshirt | Men's Regular Fit Sweatshirt - Maroon | `0.189473` |
| 9 | **D056** | Dress | Women's Casual Fit Dress - Yellow | `0.186470` |
| 10 | **D016** | Dress | Women's Casual Fit Dress - Floral Pink | `0.185763` |

### Query 10: `waterproof cyberpunk rainwear`

> **Out-of-Vocabulary (OOV) Test Case**: Notice that words like 'cyberpunk' and 'rainwear' do not appear in the corpus. The system safely returns empty results or zero scores without throwing exceptions.

| Rank | Doc ID | Category | Product Title | Cosine Score |
|:---:|:---:|:---:|:---|:---:|
| - | *No matching documents* | - | Query terms Out-Of-Vocabulary | 0.0000 |

## 2. Exact Phrase Queries (Positional Index)

### Phrase Query 1: `"cotton shirt"` (Total Matches: 5)

| Doc ID | Category | Product Title | Matches | Matched Positions `[p1, p2, ...]` |
|:---:|:---:|:---|:---:|:---|
| **D002** | Shirt | Men's Checked Cotton Shirt - Black | 2 | `[[3, 4], [9, 10]]` |
| **D022** | Shirt | Men's Checked Cotton Shirt - White | 2 | `[[3, 4], [9, 10]]` |
| **D042** | Shirt | Men's Checked Cotton Shirt - Maroon | 2 | `[[3, 4], [9, 10]]` |
| **D062** | Shirt | Men's Checked Cotton Shirt - Olive | 2 | `[[3, 4], [9, 10]]` |
| **D082** | Shirt | Men's Checked Cotton Shirt - Blue | 2 | `[[3, 4], [9, 10]]` |

### Phrase Query 2: `"stretch denim"` (Total Matches: 7)

| Doc ID | Category | Product Title | Matches | Matched Positions `[p1, p2, ...]` |
|:---:|:---:|:---|:---:|:---|
| **D003** | Jeans | Men's Regular Fit Denim Jeans - Grey | 1 | `[[16, 17]]` |
| **D013** | Jeans | Men's Slim Fit Stretch Jeans - Grey | 1 | `[[15, 16]]` |
| **D033** | Jeans | Men's Slim Fit Stretch Jeans - Grey | 1 | `[[16, 17]]` |
| **D043** | Jeans | Men's Regular Fit Denim Jeans - Grey | 1 | `[[15, 16]]` |
| **D063** | Jeans | Men's Regular Fit Denim Jeans - Grey | 1 | `[[16, 17]]` |
| **D073** | Jeans | Men's Slim Fit Stretch Jeans - Grey | 1 | `[[15, 16]]` |
| **D093** | Jeans | Men's Slim Fit Stretch Jeans - Grey | 1 | `[[16, 17]]` |

### Phrase Query 3: `"festive wear"` (Total Matches: 10)

| Doc ID | Category | Product Title | Matches | Matched Positions `[p1, p2, ...]` |
|:---:|:---:|:---|:---:|:---|
| **D005** | Saree | Women's Printed Daily Wear Saree - Blue | 1 | `[[22, 23]]` |
| **D015** | Saree | Women's Cotton Handloom Saree - Red | 1 | `[[20, 21]]` |
| **D025** | Saree | Women's Printed Daily Wear Saree - Maroon | 1 | `[[22, 23]]` |
| **D035** | Saree | Women's Cotton Handloom Saree - Yellow | 1 | `[[20, 21]]` |
| **D045** | Saree | Women's Printed Daily Wear Saree - Purple | 1 | `[[22, 23]]` |
| **D055** | Saree | Women's Cotton Handloom Saree - Pink | 1 | `[[20, 21]]` |
| **D065** | Saree | Women's Printed Daily Wear Saree - Green | 1 | `[[22, 23]]` |
| **D075** | Saree | Women's Cotton Handloom Saree - Blue | 1 | `[[20, 21]]` |
| **D085** | Saree | Women's Printed Daily Wear Saree - Red | 1 | `[[22, 23]]` |
| **D095** | Saree | Women's Cotton Handloom Saree - Maroon | 1 | `[[20, 21]]` |

### Phrase Query 4: `"winter wear"` (Total Matches: 20)

| Doc ID | Category | Product Title | Matches | Matched Positions `[p1, p2, ...]` |
|:---:|:---:|:---|:---:|:---|
| **D008** | Jacket | Women's Casual Puffer Jacket - Olive | 1 | `[[22, 23]]` |
| **D010** | Sweatshirt | Women's Fleece Sweatshirt - Black | 1 | `[[19, 20]]` |
| **D018** | Jacket | Women's Quilted Winter Jacket - Beige | 1 | `[[21, 22]]` |
| **D020** | Sweatshirt | Men's Regular Fit Sweatshirt - Navy Blue | 1 | `[[23, 24]]` |
| **D028** | Jacket | Women's Casual Puffer Jacket - Black | 1 | `[[22, 23]]` |
| **D030** | Sweatshirt | Women's Fleece Sweatshirt - Maroon | 1 | `[[19, 20]]` |
| **D038** | Jacket | Women's Quilted Winter Jacket - Olive | 1 | `[[21, 22]]` |
| **D040** | Sweatshirt | Men's Regular Fit Sweatshirt - Black | 1 | `[[21, 22]]` |
| **D048** | Jacket | Women's Casual Puffer Jacket - Beige | 1 | `[[22, 23]]` |
| **D050** | Sweatshirt | Women's Fleece Sweatshirt - Navy Blue | 1 | `[[21, 22]]` |

### Phrase Query 5: `"regular fit"` (Total Matches: 15)

| Doc ID | Category | Product Title | Matches | Matched Positions `[p1, p2, ...]` |
|:---:|:---:|:---|:---:|:---|
| **D003** | Jeans | Men's Regular Fit Denim Jeans - Grey | 2 | `[[2, 3], [9, 10]]` |
| **D004** | Kurta | Men's Regular Fit Kurta - Pink | 2 | `[[2, 3], [8, 9]]` |
| **D020** | Sweatshirt | Men's Regular Fit Sweatshirt - Navy Blue | 2 | `[[2, 3], [9, 10]]` |
| **D023** | Jeans | Men's Regular Fit Denim Jeans - Grey | 2 | `[[2, 3], [9, 10]]` |
| **D024** | Kurta | Men's Regular Fit Kurta - Teal | 2 | `[[2, 3], [8, 9]]` |
| **D040** | Sweatshirt | Men's Regular Fit Sweatshirt - Black | 2 | `[[2, 3], [8, 9]]` |
| **D043** | Jeans | Men's Regular Fit Denim Jeans - Grey | 2 | `[[2, 3], [9, 10]]` |
| **D044** | Kurta | Men's Regular Fit Kurta - Navy Blue | 2 | `[[2, 3], [9, 10]]` |
| **D060** | Sweatshirt | Men's Regular Fit Sweatshirt - Maroon | 2 | `[[2, 3], [8, 9]]` |
| **D063** | Jeans | Men's Regular Fit Denim Jeans - Grey | 2 | `[[2, 3], [9, 10]]` |

## 3. Ordered Proximity Queries (`term1 WITHIN/k term2`)

### Proximity Query 1: `cotton WITHIN/3 shirt` (k=3, Total Matches: 15)

| Doc ID | Category | Product Title | Matches | Position Pairs `(pos1, pos2, dist)` |
|:---:|:---:|:---|:---:|:---|
| **D001** | T-Shirt | Men's Cotton Crew Neck T-Shirt - Black | 1 | `(18, 20, d=2)` |
| **D002** | Shirt | Men's Checked Cotton Shirt - Black | 2 | `(3, 4, d=1), (9, 10, d=1)` |
| **D011** | T-Shirt | Men's Oversized Graphic T-Shirt - Mustard | 1 | `(15, 18, d=3)` |
| **D021** | T-Shirt | Men's Cotton Crew Neck T-Shirt - Sky Blue | 1 | `(20, 22, d=2)` |
| **D022** | Shirt | Men's Checked Cotton Shirt - White | 2 | `(3, 4, d=1), (9, 10, d=1)` |
| **D031** | T-Shirt | Men's Oversized Graphic T-Shirt - Olive Green | 1 | `(17, 20, d=3)` |
| **D041** | T-Shirt | Men's Cotton Crew Neck T-Shirt - Maroon | 1 | `(18, 20, d=2)` |
| **D042** | Shirt | Men's Checked Cotton Shirt - Maroon | 2 | `(3, 4, d=1), (9, 10, d=1)` |

### Proximity Query 2: `stretch WITHIN/4 denim` (k=4, Total Matches: 7)

| Doc ID | Category | Product Title | Matches | Position Pairs `(pos1, pos2, dist)` |
|:---:|:---:|:---|:---:|:---|
| **D003** | Jeans | Men's Regular Fit Denim Jeans - Grey | 1 | `(16, 17, d=1)` |
| **D013** | Jeans | Men's Slim Fit Stretch Jeans - Grey | 1 | `(15, 16, d=1)` |
| **D033** | Jeans | Men's Slim Fit Stretch Jeans - Grey | 1 | `(16, 17, d=1)` |
| **D043** | Jeans | Men's Regular Fit Denim Jeans - Grey | 1 | `(15, 16, d=1)` |
| **D063** | Jeans | Men's Regular Fit Denim Jeans - Grey | 1 | `(16, 17, d=1)` |
| **D073** | Jeans | Men's Slim Fit Stretch Jeans - Grey | 1 | `(15, 16, d=1)` |
| **D093** | Jeans | Men's Slim Fit Stretch Jeans - Grey | 1 | `(16, 17, d=1)` |

### Proximity Query 3: `winter WITHIN/3 wear` (k=3, Total Matches: 20)

| Doc ID | Category | Product Title | Matches | Position Pairs `(pos1, pos2, dist)` |
|:---:|:---:|:---|:---:|:---|
| **D008** | Jacket | Women's Casual Puffer Jacket - Olive | 1 | `(22, 23, d=1)` |
| **D010** | Sweatshirt | Women's Fleece Sweatshirt - Black | 1 | `(19, 20, d=1)` |
| **D018** | Jacket | Women's Quilted Winter Jacket - Beige | 1 | `(21, 22, d=1)` |
| **D020** | Sweatshirt | Men's Regular Fit Sweatshirt - Navy Blue | 1 | `(23, 24, d=1)` |
| **D028** | Jacket | Women's Casual Puffer Jacket - Black | 1 | `(22, 23, d=1)` |
| **D030** | Sweatshirt | Women's Fleece Sweatshirt - Maroon | 1 | `(19, 20, d=1)` |
| **D038** | Jacket | Women's Quilted Winter Jacket - Olive | 1 | `(21, 22, d=1)` |
| **D040** | Sweatshirt | Men's Regular Fit Sweatshirt - Black | 1 | `(21, 22, d=1)` |

### Proximity Query 4: `festive WITHIN/4 kurta` (k=4, Total Matches: 0)

| Doc ID | Category | Product Title | Matches | Position Pairs `(pos1, pos2, dist)` |
|:---:|:---:|:---|:---:|:---|

## 4. In-Depth Comparative Analysis (Positional vs VSM)

### Case 1: Pure VSM vs Exact Phrase (`"cotton shirt"`)

In pure VSM retrieval for 'cotton shirt', documents containing 'cotton' and 'shirt' at distant positions (for instance, D001, D011 where 'cotton' describes fabric and 'shirt' appears in t-shirt) receive high cosine scores due to bag-of-words term frequency. In contrast, Positional Exact Phrase retrieval strictly enforces pos(shirt) == pos(cotton) + 1, filtering out documents where the two terms do not occur as an uninterrupted phrase. For example, D002, D022, D042, D062, D082 ('Men's Checked Cotton Shirt') match the exact phrase, whereas documents mentioning both words in separate contexts are properly excluded.

- **VSM Top 5 DocIDs**: `['D022', 'D082', 'D001', 'D041', 'D061']`
- **Exact Phrase DocIDs**: `['D002', 'D022', 'D042', 'D062', 'D082']`

### Case 2: Broad Co-occurrence vs Proximity (`winter WITHIN/3 wear`)

In VSM retrieval for 'winter wear', every document mentioning either 'winter' or 'wear' is retrieved. Because 'wear' is ubiquitous in the clothing corpus ('everyday Indian wear', 'daily wear', etc.), numerous documents (e.g. Sarees, Kurtas) obtain non-zero cosine similarity even if they have no winter association. Positional proximity search with k=3 requires 'wear' to appear within 3 tokens after 'winter', isolating genuine winter apparel mentions ('winter wear' in Jackets, Hoodies, Sweatshirts) and discarding false-positive co-occurrences.

- **VSM Top 5 DocIDs**: `['D058', 'D018', 'D078', 'D038', 'D098']`
- **Proximity DocIDs**: `['D008', 'D010', 'D018', 'D020', 'D028', 'D030', 'D038', 'D040', 'D048', 'D050']`

### Case 3: Positional Hybrid Proximity Re-Ranking (Special Idea 1)

When applying our Positional Hybrid Proximity Boost (Special Idea 1), documents having terms in an immediate 2-token span receive an elevated boost over documents where terms are separated by filler words, demonstrating ranked re-ordering driven directly by positional token distance.

| Doc ID | Base VSM Score | Shortest Span (tokens) | Hybrid Proximity Score |
|:---:|:---:|:---:|:---:|
| **D013** | `0.247551` | `2` | `0.371327` |
| **D073** | `0.247551` | `2` | `0.371327` |
| **D043** | `0.245348` | `2` | `0.368022` |
| **D033** | `0.243519` | `2` | `0.365279` |
| **D093** | `0.243519` | `2` | `0.365279` |

